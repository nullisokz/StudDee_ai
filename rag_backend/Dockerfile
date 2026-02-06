FROM python:3.11-slim

WORKDIR /app

# Installera nödvändiga systembibliotek för ChromaDB
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Fixa timeout-problem och installera CPU-versionen av Torch (sparar ca 2GB plats!)
ENV PIP_DEFAULT_TIMEOUT=100
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "server.py"]