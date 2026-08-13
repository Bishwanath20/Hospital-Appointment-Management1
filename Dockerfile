FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /workspace

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Force Python stdout/stderr streams to be unbuffered (immediate log visibility)
ENV PYTHONUNBUFFERED=1

# Install system compilation dependencies required for certain Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker's caching layer
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire project code into the container workspace
COPY . .

# Expose FastAPI's standard communication port
EXPOSE 8000

# Execute Uvicorn, pointing explicitly to main.py inside your /app directory package structure
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
