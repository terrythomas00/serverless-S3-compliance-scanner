FROM python:3.11-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app
ENV REPORTS_BUCKET=tt-secure-reports-19570
CMD ["python", "main.py"]
