FROM python:3.11-alpine

# Install build tools for C
RUN apk add --no-cache gcc musl-dev

# Hardening: Non-root user
RUN addgroup -S ctf && adduser -S ctf -G ctf

WORKDIR /app

# Copy and compile the C binary
COPY kidal_sentinel.c .
# Compile with no protections for the challenge (classic BoF)
RUN gcc -o kidal_sentinel kidal_sentinel.c -fno-stack-protector -z execstack

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Hardening: Ownership
RUN chown -R ctf:ctf /app

USER ctf

EXPOSE 8008

CMD ["python", "app.py"]
