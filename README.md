# Amul Product Scraper

A Python application that monitors Amul product availability by scraping their API and tracking stock changes in a SQLite database. The application sends notifications when products become available again.

## Features

- 🔄 Continuous monitoring of Amul product availability
- 📦 SQLite database for persistent storage
- 🔔 Email notifications when products come back in stock
- 🐳 Docker containerization for easy deployment
- ⚡ Configurable check intervals
- 📍 Location-based monitoring with pincode support

## 🚀 Quick Start Guide (For Beginners)

This guide will help you set up and run the Amul product scraper on your computer, even if you're not a technical person.

### Prerequisites

**You'll need to install these first:**
1. **Docker Desktop** - Download from [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. **Git** - Download from [https://git-scm.com/downloads](https://git-scm.com/downloads)
3. **A Gmail account** (for notifications)

### Step 1: Download the Project

1. Open Terminal (Mac/Linux) or Command Prompt/PowerShell (Windows)
2. Run this command to download the project:
   ```bash
   git clone https://github.com/your-username/amul-scraping.git
   cd amul-scraping
   ```

### Step 2: Configure Your Settings

#### A. Set Your Location (Pincode)
1. Open the file `src/config.py` in any text editor
2. Find the line: `PINCODE = "248001"`
3. Change `"248001"` to your pincode (keep the quotes)
4. Save the file

#### B. Set Up Email Notifications
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file in a text editor
3. Fill in your email details:
   ```
   EMAIL_FROM=your-email@gmail.com
   EMAIL_PASSWORD=your-app-password
   EMAIL_TO=recipient1@email.com,recipient2@email.com
   ```

**⚠️ Important for Gmail users:**
- Don't use your regular Gmail password
- You need to create an "App Password"
- Follow this guide: [How to create Gmail App Password](https://support.google.com/accounts/answer/185833?hl=en)

#### C. Adjust Check Frequency (Optional)
1. In `src/config.py`, find: `CHECK_INTERVAL_SECONDS = 600`
2. Change `600` to your preferred interval in seconds:
   - `300` = 5 minutes
   - `600` = 10 minutes (default)
   - `1800` = 30 minutes
   - `3600` = 1 hour

### Step 3: Launch the Application

#### Option 1: One-Click Setup (Easiest)

**For Windows users:**
```powershell
.\deploy.ps1
```

**For Mac/Linux users:**
```bash
./deploy.sh
```

#### Option 2: Using Docker Compose
```bash
docker-compose up -d
```

#### Option 3: Manual Docker Commands
```bash
# Build and run
docker build -t amul-scraper .
docker run -d --name amul-scraper --restart unless-stopped -v "$(pwd)/data:/app/data" amul-scraper
```

### Step 4: Verify It's Working

1. Check if the container is running:
   ```bash
   docker ps
   ```
   You should see `amul-scraper` in the list

2. View the logs to see what's happening:
   ```bash
   docker logs -f amul-scraper
   ```
   Press `Ctrl+C` to stop viewing logs

### Step 5: Understanding What Happens Next

- The application will check Amul's website every 10 minutes (or your configured interval)
- It tracks product availability in a local database (`./data/data.db`)
- When a product becomes available, you'll get an email notification
- The application runs continuously in the background

### Managing Your Scraper

#### View Live Activity
```bash
docker logs -f amul-scraper
```

#### Stop the Scraper
```bash
docker stop amul-scraper
```

#### Start the Scraper Again
```bash
docker start amul-scraper
```

#### Restart After Configuration Changes
```bash
docker-compose restart
```

#### Remove Everything (Clean Uninstall)
```bash
docker stop amul-scraper
docker rm amul-scraper
docker rmi amul-scraper
```

### Troubleshooting Common Issues

#### "Docker command not found"
- Make sure Docker Desktop is installed and running
- Restart your terminal after installation

#### "No email notifications"
- Check your `.env` file has correct email credentials
- Make sure you're using Gmail App Password, not regular password
- Check spam folder for notifications

#### "Container keeps stopping"
- Check logs: `docker logs amul-scraper`
- Common issue: incorrect pincode format or email configuration

#### "Permission denied" (Mac/Linux)
- Make deployment script executable: `chmod +x deploy.sh`

### Files You Can Safely Modify
- `src/config.py` - Change pincode and check intervals
- `.env` - Update email settings

### Files You Should NOT Modify
- `Dockerfile`
- `docker-compose.yml` 
- `src/` folder (except config.py)

---

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
- [ ] Product filtering and alerts
