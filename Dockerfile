###########################
#   BUILDER
###########################
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# -------------------------------
#  FIX #1 — Create virtualenv
# -------------------------------
# This guarantees gunicorn, uvicorn, torch, insightface all end up in /venv
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r requirements.txt --no-cache-dir

# Preload models using virtualenv Python
COPY preload_insightface.py preload_insightface.py
COPY preload_easyocr.py preload_easyocr.py

ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH="/venv/lib/python3.10/site-packages"

RUN python preload_insightface.py
RUN python preload_easyocr.py


###########################
#   RUNTIME
###########################
FROM python:3.10-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    INSIGHTFACE_HOME=/root/.insightface/models \
    PATH="/venv/bin:$PATH" \
    PYTHONPATH="/venv/lib/python3.10/site-packages"

# Install runtime system libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy Python virtual environment
COPY --from=builder /venv /venv

# Copy model folders
COPY --from=builder /root/.insightface /root/.insightface
COPY --from=builder /root/.EasyOCR /root/.EasyOCR

# Copy application code
COPY app ./app
COPY requirements.txt preload_insightface.py preload_easyocr.py ./


EXPOSE 8000

# -------------------------------
# RUN GUNICORN USING VENV
# -------------------------------
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
