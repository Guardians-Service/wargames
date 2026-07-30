FROM python:3.11-slim

WORKDIR /app

COPY app.py flag.txt /app/
COPY keys/ /app/keys/

RUN pip install --no-cache-dir flask pyjwt

EXPOSE 8000

CMD ["python", "app.py"]
