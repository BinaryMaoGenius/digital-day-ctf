####################################
#
#  Digital Day CTF — Dockerfile
#  Multi-stage build (optimized image size)
#

# ── Stage 1 : Builder ───────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    zlib1g-dev \
    rustc \
    libcurl4-openssl-dev \
    libssl-dev \
    python3-pycurl \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY setup/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt --prefix=/install

# ── Stage 2 : Runtime ───────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Runtime-only system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libcurl4 \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-installed Python packages from builder
COPY --from=builder /install/bin /usr/local/bin
COPY --from=builder /install/lib /usr/local/lib

# Application code
WORKDIR /opt/ctf
COPY . .

# Persist game data (DB, uploads, config) outside the container
VOLUME ["/opt/ctf/files"]

# Tornado listens on 8888 by default
EXPOSE 8888

ENV SQL_DIALECT=sqlite \
    PYTHONUNBUFFERED=1

# HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
#     CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8888/')" || exit 1

ENTRYPOINT ["python3", "/opt/ctf/rootthebox.py", "--start"]
