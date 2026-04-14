# Use Python 3.10 bullseye (full Debian - more compatible)
FROM python:3.10-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for Docker layer caching)
COPY requirements_web.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir cmake
RUN pip install --no-cache-dir dlib
RUN pip install --no-cache-dir face-recognition
RUN pip install git+https://github.com/ageitgey/face_recognition_models
RUN pip install --no-cache-dir -r requirements_web.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p Pics attendance_records static/images

# Expose port 8000
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]
