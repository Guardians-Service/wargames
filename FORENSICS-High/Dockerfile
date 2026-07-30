FROM python:3.11-slim

RUN pip install flask

WORKDIR /app

COPY app.py .
COPY evidence.bin .

EXPOSE 8000

CMD ["python", "app.py"]
