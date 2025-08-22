# Use plawright image as base
FROM mcr.microsoft.com/playwright/python:v1.54.0-noble

# Set working directory in the container
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ .
# Copy the .env file
COPY .env .
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
