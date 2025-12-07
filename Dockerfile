###########################
#   BUILDER
###########################
FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies to a fixed folder `/install`
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt --no-cache-dir

COPY preload_insightface.py preload_insightface.py
COPY preload_easyocr.py preload_easyocr.py

ENV PYTHONPATH=/install/lib/python3.10/site-packages

RUN python preload_insightface.py
RUN python preload_easyocr.py


###########################
#   RUNTIME
###########################
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    INSIGHTFACE_HOME=/root/.insightface/models \
    PYTHONPATH="/install/lib/python3.10/site-packages" \
    PATH="/install/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /install

# Copy models
COPY --from=builder /root/.insightface /root/.insightface
COPY --from=builder /root/.EasyOCR /root/.EasyOCR

# Copy app
COPY app ./app
COPY requirements.txt preload_insightface.py preload_easyocr.py ./


EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
