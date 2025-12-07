###########################
#   BUILDER (CPU ONLY)
###########################
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install deps WITHOUT CUDA / GPU runtimes
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY preload_insightface.py preload_insightface.py
COPY preload_easyocr.py preload_easyocr.py

RUN python preload_insightface.py
RUN python preload_easyocr.py


############################
#     RUNTIME IMAGE
############################
FROM python:3.10-slim

ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    INSIGHTFACE_HOME=/root/.insightface/models

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy ONLY installed Python packages
COPY --from=builder /usr/local/lib/python3.10/site-packages \
                   /usr/local/lib/python3.10/site-packages

# Copy InsightFace & OCR model caches
COPY --from=builder /root/.insightface /root/.insightface
COPY --from=builder /root/.EasyOCR /root/.EasyOCR

# Copy actual application
COPY app ./app
COPY requirements.txt preload_insightface.py preload_easyocr.py ./

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
