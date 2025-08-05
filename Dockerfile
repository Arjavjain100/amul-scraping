# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ .
# Create a directory for the database
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Expose port (optional, not needed for this script but good practice)
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
