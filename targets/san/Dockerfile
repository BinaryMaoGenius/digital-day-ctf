FROM python:3.11-alpine

WORKDIR /app

RUN pip install flask

COPY app.py .

EXPOSE 8005

CMD ["python", "app.py"]
