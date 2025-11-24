

import boto3
import os
import json
from datetime import datetime, timezone
from ai_helper import explain_findings


def run_scan_and_write_report():
    s3 = boto3.client('s3')
    
    report_bucket = os.getenv('REPORTS_BUCKET')
    if not report_bucket: 
        raise RuntimeError("REPORTS_BUCKET environment variable is not set. Please set it before running.")
    
    # 1. Get all bucket names
    buckets_response = s3.list_buckets()
    bucket_names = []
    for bucket in buckets_response.get('Buckets', []):
        bucket_names.append(bucket['Name'])
    
    # 2. Check each bucket for compliance and build findings for each bucket    
    results = []
    for bucket in bucket_names:
        try:
            policy_status = s3.get_bucket_policy_status(Bucket=bucket)
            is_public = policy_status.get('PolicyStatus', {}).get('IsPublic', False)
        except Exception:
            is_public = False
            
        try:
            s3.get_bucket_encryption(Bucket=bucket)
            encryption_enabled = True
        except Exception:
            encryption_enabled = False
            
        try:
            versioning = s3.get_bucket_versioning(Bucket=bucket)
            versioning_enabled = versioning.get('Status') == 'Enabled'
        except Exception:
            versioning_enabled = False
            
        results.append(
            {
                'name': bucket,
                'public_access': is_public,
                'encryption': encryption_enabled,
                'versioning': versioning_enabled
                }
        )
    
    # 3. Count non-compliant buckets    
    non_compliant = [
        r for r in results
        if (r['public_access'] == True or
            r['encryption'] == False or
            r['versioning'] == False)
    ]
    
    # 4. Build AI summary input from results
    ai_input = []
    for r in results:
        bucket_info = {
            "bucket": r["name"],
            "public": r["public_access"],
            "encryption": r["encryption"],
            "versioning": r["versioning"],
        }
        ai_input.append(bucket_info)
    
    # 5. Get AI summary notes & split into lines for clean JSON storage 
    ai_notes = explain_findings(ai_input)
    ai_summary_lines = ai_notes.split("\n")


    # 6. Build final payload JSON and write to S3
    payload = {
        'timestamp': datetime.now(timezone.utc).isoformat(),  # Use timezone-aware datetime
        'total_buckets': len(bucket_names),
        'non_compliant_buckets': len(non_compliant),
        'findings': results,
        'ai_summary': ai_summary_lines,
    }
    
    # 7. Write report to S3
    key = f"reports/s3_compliance_report_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"
    s3.put_object(
        Bucket=report_bucket,
        Key=key,
        Body=json.dumps(payload, indent=4).encode('utf-8'),
        ContentType='application/json'
    )
    
    # 8. Return a small summary for the lambda invoke output
    return{
        'message': 'Scan complete',
        'report_bucket': report_bucket,
        'report_key': key,
        'total_buckets': len(bucket_names),
        'non_compliant_buckets': len(non_compliant)
    }


def handler(event=None, context= None):
    return run_scan_and_write_report() 

# Uncomment below to enable handling findings from event input to test only the lambda function in the aws console only
# def handler(event=None, context=None):
    # if event and "findings" in event:
        # return explain_findings(event["findings"])
    
    # return run_scan_and_write_report()


if __name__ == "__main__": 
    result = run_scan_and_write_report()
    print(json.dumps(result, indent=2))