FROM python:3.9-slim
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    g++ \
    python3-dev \
    libffi-dev \
    libjpeg-dev \
    zlib1g-dev \
    bash \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*  
WORKDIR /src/backend/
ADD . /src/backend/
RUN chmod -R 777 /src/backend/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir Pillow

RUN pip install --no-cache-dir -r requirements
