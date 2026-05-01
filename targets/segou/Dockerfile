FROM python:3.11-alpine

WORKDIR /app

RUN pip install flask

COPY premium_css.py .
COPY app.py .

EXPOSE 8001

CMD ["python", "app.py"]
