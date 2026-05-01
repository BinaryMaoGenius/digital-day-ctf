FROM python:3.11-alpine

WORKDIR /app

RUN pip install flask pyjwt

COPY premium_css.py .
COPY app.py .

EXPOSE 8002

CMD ["python", "app.py"]
