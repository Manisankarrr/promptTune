# Use a Python base image, ideal for Flask applications
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --default-timeout=1000 --retries=5

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
