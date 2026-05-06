FROM python:3.11-alpine

# Hardening: Non-root user
RUN addgroup -S ctf && adduser -S ctf -G ctf

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hardening: Ownership
RUN chown -R ctf:ctf /app

USER ctf

EXPOSE 8007

CMD ["python", "app.py"]
