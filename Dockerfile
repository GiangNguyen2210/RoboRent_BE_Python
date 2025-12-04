# 1. Base image: Python 3.10 on Debian (manylinux wheels work well here)
FROM python:3.10-slim

# 2. Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    INSIGHTFACE_HOME=/models/insightface

# 3. System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 4. Workdir
WORKDIR /app

# 5. Install Python deps into a venv
COPY requirements.txt .

RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"

# 6. Pre-download InsightFace model
RUN python3 - << 'PY'
FROM insightface.app import FaceAnalysis
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))
PY

# 7. Pre-download EasyOCR models
RUN python3 - << 'PY'
import easyocr
easyocr.Reader(['vi', 'en'], gpu=False)
PY

# 8. Copy source code
COPY . .

# 9. Expose port
EXPOSE 8000

# 10. Start with Gunicorn + Uvicorn worker
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
