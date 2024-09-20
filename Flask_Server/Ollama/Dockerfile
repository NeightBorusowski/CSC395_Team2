# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5001 for Ollama service
EXPOSE 5001

# Start the Ollama service
CMD ["python", "ollama.py"]
