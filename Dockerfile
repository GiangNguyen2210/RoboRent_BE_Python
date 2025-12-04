FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    INSIGHTFACE_HOME=/models/insightface

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"


# ----------------------------
# Pre-download InsightFace model
# ----------------------------
COPY preload_insightface.py /tmp/preload_insightface.py
RUN python /tmp/preload_insightface.py


# ----------------------------
# Pre-download EasyOCR model
# ----------------------------
COPY preload_easyocr.py /tmp/preload_easyocr.py
RUN python /tmp/preload_easyocr.py


# Copy full source
COPY . .

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
