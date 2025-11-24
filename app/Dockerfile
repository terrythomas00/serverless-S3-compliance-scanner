# Use AWS Lambda Python base image so this runs as a Lambda container
FROM public.ecr.aws/lambda/python:3.14

# Upgrade setuptools to fix CVEs
RUN pip install --upgrade setuptools==78.1.1
RUN dnf update -y && dnf clean all

# Copy code and install deps
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY app/ ${LAMBDA_TASK_ROOT}

# Lambda will call "handler" in main.py by default if we set CMD accordingly
CMD [ "main.handler" ]
