FROM python:3.11-slim

WORKDIR /app

RUN pip install flask

COPY app.py .
COPY flag.txt .

EXPOSE 8000

CMD ["python", "app.py"]
