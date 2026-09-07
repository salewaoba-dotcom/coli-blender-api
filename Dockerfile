FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget \
    xz-utils \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libxi6 \
    libxfixes3 \
    libsm6 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://download.blender.org/release/Blender4.3/blender-4.3.3-linux-x64.tar.xz \
    && tar -xf blender-4.3.3-linux-x64.tar.xz \
    && mv blender-4.3.3-linux-x64 /opt/blender \
    && rm blender-4.3.3-linux-x64.tar.xz

ENV PATH="/opt/blender:$PATH"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "server:app"]
