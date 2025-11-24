import os
import json
from typing import List, Dict, Any

import boto3


def explain_findings(findings: List[Dict[str, Any]]) -> str:
    if not _is_ai_enabled():
        return "AI summary disabled (set ENABLE_AI=true to enable)."

    try:
        api_key = _get_api_key_from_secrets_manager()
    except Exception as error:
        return f"AI summary skipped (secret error: {error})"

    if not api_key:
        return "AI summary skipped (no API key found in secret)."

    try:
        summary = _generate_ai_summary(findings, api_key)
        return summary
    except Exception as error:
        return f"AI summary error (non-fatal): {error}"


def _is_ai_enabled() -> bool:
    ai_flag = os.getenv("ENABLE_AI", "false").lower()
    return ai_flag in {"1", "true", "yes"}


def _get_api_key_from_secrets_manager() -> str:
    secret_name = os.getenv("AI_SECRET_NAME")
    if not secret_name:
        raise RuntimeError("AI_SECRET_NAME environment variable is not set.")

    client = boto3.client("secretsmanager")

    response = client.get_secret_value(SecretId=secret_name)

    secret_string = response.get("SecretString")
    if not secret_string:
        raise RuntimeError("Secret does not contain a SecretString value.")

    data = json.loads(secret_string)
    api_key = data.get("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not found in secret payload.")

    return api_key


def _generate_ai_summary(findings: List[Dict[str, Any]], api_key: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    prompt = _create_prompt(findings)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def _create_prompt(findings: List[Dict[str, Any]]) -> str:
    MAX_FINDINGS = 50
    limited_findings = findings[:MAX_FINDINGS]

    bullet_points = []
    for finding in limited_findings:
        bucket_name = finding.get("bucket", "unknown-bucket")
        issues = _extract_issues(finding)

        issue_summary = ", ".join(issues) if issues else "No critical issues"
        bullet_points.append(f"- {bucket_name}: {issue_summary}")

    prompt = (
        "You are a cloud security assistant. In 6–10 bullet points, "
        "prioritize the S3 risks and give direct, actionable fixes. "
        "Buckets and issues:\n" + "\n".join(bullet_points)
    )

    return prompt


def _extract_issues(finding: Dict[str, Any]) -> List[str]:
    issues = []

    if finding.get("public"):
        issues.append("Public")

    if not finding.get("encryption"):
        issues.append("No encryption")

    if not finding.get("versioning"):
        issues.append("No versioning")

    return issues
