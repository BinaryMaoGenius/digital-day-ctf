FROM python:3.11-alpine

WORKDIR /app

RUN pip install flask requests

COPY app.py .

EXPOSE 8003

CMD ["python", "app.py"]
