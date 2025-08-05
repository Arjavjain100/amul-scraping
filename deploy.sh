#!/bin/bash

# Amul Scraper Deployment Script

set -e  # Exit on any error

echo "🐳 Building and deploying Amul Scraper..."

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t amul-scraper .

# Stop and remove existing container if it exists
echo "🛑 Stopping existing container (if any)..."
docker stop amul-scraper 2>/dev/null || true
docker rm amul-scraper 2>/dev/null || true

# Run the container
echo "🚀 Starting new container..."
docker run -d \
  --name amul-scraper \
  --restart unless-stopped \
  -v "$(pwd)/data:/app/data" \
  amul-scraper

echo "✅ Deployment complete!"
echo ""
echo "📊 Container status:"
docker ps --filter name=amul-scraper

echo ""
echo "📝 To view logs:"
echo "   docker logs -f amul-scraper"
echo ""
echo "🛑 To stop:"
echo "   docker stop amul-scraper"
echo ""
echo "🔄 To restart:"
echo "   docker restart amul-scraper"
