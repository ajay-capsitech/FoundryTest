# Use slim Python image
FROM python:3.10-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Create work directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements first (to use Docker cache effectively)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Azure's required container port
EXPOSE 80

# Run with Gunicorn + Uvicorn workers on port 80
# IMPORTANT: replace `main:app` with the correct import path
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "main:app"]
