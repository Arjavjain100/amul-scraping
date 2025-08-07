# Amul Product Scraper

A Python application that monitors Amul product availability by scraping their API and tracking stock changes in a SQLite database. The application sends notifications when products become available again.

## Features

- 🔄 Continuous monitoring of Amul product availability
- 📦 SQLite database for persistent storage
- 🔔 Notifications when products come back in stock
- 🐳 Docker containerization for easy deployment
- ⚡ Configurable check intervals

## Quick Start with Docker

### Prerequisites
- Docker installed on your system
- Docker Compose (optional, but recommended)

### Option 1: Using the Deployment Script (Recommended)
```bash
./deploy.sh
```

### Option 2: Using Docker Compose 
```bash
docker-compose up -d
```

### Option 3: Manual Docker Commands
```bash
# Build the image
docker build -t amul-scraper .

# Run the container
docker run -d --name amul-scraper --restart unless-stopped -v "$(pwd)/data:/app/data" amul-scraper
```

## Management Commands

### View Logs
```bash
docker logs -f amul-scraper
```

### Stop the Application
```bash
docker stop amul-scraper
# or
docker-compose down
```

### Restart the Application
```bash
docker restart amul-scraper
# or
docker-compose restart
```

### Remove Container
```bash
docker rm amul-scraper
```

## Configuration

The application can be configured by modifying `config.py`:

- `DB_PATH`: Database file location
- `CHECK_INTERVAL_SECONDS`: Time between API checks (default: 600 seconds/10 minutes)
- `API_URL`: Amul API endpoint
- `API_HEADERS` and `API_COOKIES`: Required for API authentication

## Data Persistence

The SQLite database is stored in the `./data/` directory on your host machine, ensuring data persists across container restarts.

## Local Development

If you prefer to run without Docker:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Update `DB_PATH` in `config.py`

3. Run the application:
   ```bash
   python main.py
   ```

## Database Schema

The application creates an `items` table with the following structure:
- `id` (TEXT PRIMARY KEY): Product ID
- `name` (TEXT): Product name
- `quantity` (INTEGER): Available quantity
- `available` (INTEGER): Availability status (0/1)

## Notifications

Notifications are send using email more details in `EMAIL_SETUP.md`

## Troubleshooting

### Check Container Status
```bash
docker ps --filter name=amul-scraper
```

### View Real-time Logs
```bash
docker logs -f amul-scraper
```

### Access Container Shell
```bash
docker exec -it amul-scraper /bin/bash
```

### Check Database
The database file is located at `./data/data.db` on your host machine.

## Future Enhancements

- [ ] Web dashboard for monitoring
- [ ] Multiple store location support
- [ ] Pincode-based substore ID detection
- [ ] Product filtering and alerts
