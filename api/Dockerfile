# Use an official CUDA runtime as a parent image
FROM nvidia/cuda:12.2.2-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && apt-get clean

# Upgrade pip
RUN pip3 install --upgrade pip

# Install PyTorch and torchvision
RUN pip3 install --timeout 500 torch torchvision torchaudio

# Set a working directory
WORKDIR /api

COPY . ./api
RUN pip install --no-cache-dir -r ./api/requirements.txt


CMD [ "python", ".api/src/api_server.py" ]

# Copy your Python scripts or project files to the container
# COPY your_script.py /app/

# Command to run your Python script (replace with your script name)
# CMD ["python3", "your_script.py"]
