FROM python:3.11-slim

WORKDIR /app

COPY app.py flag.txt /app/

RUN pip install flask pyjwt

EXPOSE 8000

CMD ["python", "app.py"]
