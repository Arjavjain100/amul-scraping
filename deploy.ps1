# Amul Product Scraper - Windows Deployment Script
# This script automates the setup and deployment of the Amul scraper

param(
    [switch]$Help,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Logs,
    [switch]$Status,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

# Script configuration
$CONTAINER_NAME = "amul-scraper"
$IMAGE_NAME = "amul-scraper"
$PROJECT_NAME = "amul-scraping"

# Colors for output
$RED = "Red"
$GREEN = "Green"
$YELLOW = "Yellow"
$BLUE = "Cyan"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-ColorOutput "🚀 Amul Product Scraper - Windows Deployment Script" $BLUE
    Write-ColorOutput ""
    Write-ColorOutput "USAGE:" $YELLOW
    Write-ColorOutput "  .\deploy.ps1                 # Deploy/start the scraper"
    Write-ColorOutput "  .\deploy.ps1 -Stop          # Stop the scraper"
    Write-ColorOutput "  .\deploy.ps1 -Restart       # Restart the scraper"
    Write-ColorOutput "  .\deploy.ps1 -Logs          # View live logs"
    Write-ColorOutput "  .\deploy.ps1 -Status        # Check status"
    Write-ColorOutput "  .\deploy.ps1 -Clean         # Remove everything"
    Write-ColorOutput "  .\deploy.ps1 -Help          # Show this help"
    Write-ColorOutput ""
    Write-ColorOutput "EXAMPLES:" $YELLOW
    Write-ColorOutput "  # First time setup"
    Write-ColorOutput "  .\deploy.ps1"
    Write-ColorOutput ""
    Write-ColorOutput "  # Check if it's working"
    Write-ColorOutput "  .\deploy.ps1 -Status"
    Write-ColorOutput "  .\deploy.ps1 -Logs"
    Write-ColorOutput ""
    exit 0
}

function Test-Prerequisites {
    Write-ColorOutput "🔍 Checking prerequisites..." $BLUE
    
    # Check if Docker is installed and running
    try {
        $dockerVersion = docker --version 2>$null
        if ($dockerVersion) {
            Write-ColorOutput "✅ Docker found: $dockerVersion" $GREEN
        } else {
            throw "Docker not found"
        }
    } catch {
        Write-ColorOutput "❌ Docker is not installed or not running" $RED
        Write-ColorOutput "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/" $YELLOW
        Write-ColorOutput "Make sure Docker Desktop is running before continuing." $YELLOW
        exit 1
    }
    
    # Check if docker daemon is running
    try {
        docker info | Out-Null
    } catch {
        Write-ColorOutput "❌ Docker daemon is not running" $RED
        Write-ColorOutput "Please start Docker Desktop and try again." $YELLOW
        exit 1
    }
    
    Write-ColorOutput "✅ All prerequisites met!" $GREEN
}

function Test-Configuration {
    Write-ColorOutput "🔧 Checking configuration..." $BLUE
    
    # Check if .env file exists
    if (Test-Path ".env") {
        Write-ColorOutput "✅ .env file found" $GREEN
    } else {
        Write-ColorOutput "⚠️  .env file not found" $YELLOW
        if (Test-Path ".env.example") {
            Write-ColorOutput "📋 Creating .env file from example..." $BLUE
            Copy-Item ".env.example" ".env"
            Write-ColorOutput "✅ .env file created" $GREEN
            Write-ColorOutput "🔧 Please edit .env file with your email credentials:" $YELLOW
            Write-ColorOutput "   - EMAIL_FROM=your-email@gmail.com" $YELLOW
            Write-ColorOutput "   - EMAIL_PASSWORD=your-app-password" $YELLOW
            Write-ColorOutput "   - EMAIL_TO=recipient@email.com" $YELLOW
            Write-ColorOutput ""
            Write-ColorOutput "⚠️  Don't forget to use Gmail App Password, not your regular password!" $YELLOW
            Write-ColorOutput "📖 Guide: https://support.google.com/accounts/answer/185833" $BLUE
        } else {
            Write-ColorOutput "❌ .env.example not found. Please check your project files." $RED
            exit 1
        }
    }
    
    # Check if config file exists
    if (Test-Path "src/config.py") {
        Write-ColorOutput "✅ Configuration file found" $GREEN
        
        # Read pincode from config
        $configContent = Get-Content "src/config.py" -Raw
        if ($configContent -match 'PINCODE\s*=\s*["\']([^"\']+)["\']') {
            $pincode = $matches[1]
            Write-ColorOutput "📍 Current pincode: $pincode" $BLUE
        }
    } else {
        Write-ColorOutput "❌ src/config.py not found" $RED
        exit 1
    }
}

function Get-ContainerStatus {
    try {
        $status = docker ps -a --filter "name=$CONTAINER_NAME" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>$null
        return $status
    } catch {
        return $null
    }
}

function Show-Status {
    Write-ColorOutput "📊 Container Status:" $BLUE
    
    $status = Get-ContainerStatus
    if ($status) {
        $statusLines = $status -split "`n"
        if ($statusLines.Length -gt 1) {
            Write-ColorOutput $statusLines[0] $YELLOW  # Header
            for ($i = 1; $i -lt $statusLines.Length; $i++) {
                if ($statusLines[$i] -match "Up") {
                    Write-ColorOutput $statusLines[$i] $GREEN
                } else {
                    Write-ColorOutput $statusLines[$i] $RED
                }
            }
        } else {
            Write-ColorOutput "No containers found with name: $CONTAINER_NAME" $YELLOW
        }
    } else {
        Write-ColorOutput "No containers found" $YELLOW
    }
}

function Stop-Container {
    Write-ColorOutput "🛑 Stopping container..." $BLUE
    
    try {
        docker stop $CONTAINER_NAME 2>$null
        Write-ColorOutput "✅ Container stopped successfully" $GREEN
    } catch {
        Write-ColorOutput "⚠️  Container was not running or doesn't exist" $YELLOW
    }
}

function Remove-Container {
    Write-ColorOutput "🗑️  Removing container..." $BLUE
    
    try {
        docker rm $CONTAINER_NAME 2>$null
        Write-ColorOutput "✅ Container removed successfully" $GREEN
    } catch {
        Write-ColorOutput "⚠️  Container doesn't exist or already removed" $YELLOW
    }
}

function Clean-All {
    Write-ColorOutput "🧹 Cleaning up everything..." $BLUE
    
    # Stop container
    Stop-Container
    
    # Remove container
    Remove-Container
    
    # Remove image
    try {
        docker rmi $IMAGE_NAME 2>$null
        Write-ColorOutput "✅ Image removed successfully" $GREEN
    } catch {
        Write-ColorOutput "⚠️  Image doesn't exist or already removed" $YELLOW
    }
    
    Write-ColorOutput "✅ Cleanup completed!" $GREEN
}

function Build-Image {
    Write-ColorOutput "🏗️  Building Docker image..." $BLUE
    
    try {
        docker build -t $IMAGE_NAME . --no-cache
        Write-ColorOutput "✅ Image built successfully" $GREEN
    } catch {
        Write-ColorOutput "❌ Failed to build image" $RED
        exit 1
    }
}

function Start-Container {
    Write-ColorOutput "🚀 Starting container..." $BLUE
    
    # Create data directory if it doesn't exist
    if (!(Test-Path "data")) {
        New-Item -ItemType Directory -Name "data" | Out-Null
        Write-ColorOutput "📁 Created data directory" $BLUE
    }
    
    try {
        $currentPath = (Get-Location).Path
        docker run -d `
            --name $CONTAINER_NAME `
            --restart unless-stopped `
            -v "${currentPath}/data:/app/data" `
            -e PYTHONUNBUFFERED=1 `
            $IMAGE_NAME
        
        Write-ColorOutput "✅ Container started successfully" $GREEN
        Write-ColorOutput "📋 Container name: $CONTAINER_NAME" $BLUE
    } catch {
        Write-ColorOutput "❌ Failed to start container" $RED
        exit 1
    }
}

function Show-Logs {
    Write-ColorOutput "📜 Showing live logs (Press Ctrl+C to exit)..." $BLUE
    try {
        docker logs -f $CONTAINER_NAME
    } catch {
        Write-ColorOutput "❌ Failed to show logs. Container might not be running." $RED
    }
}

function Restart-Container {
    Write-ColorOutput "🔄 Restarting container..." $BLUE
    
    Stop-Container
    Start-Container
    
    Write-ColorOutput "✅ Container restarted successfully" $GREEN
}

function Deploy-Application {
    Write-ColorOutput "🚀 Deploying Amul Product Scraper..." $BLUE
    Write-ColorOutput ""
    
    Test-Prerequisites
    Test-Configuration
    
    # Stop existing container if running
    $status = Get-ContainerStatus
    if ($status -match "Up") {
        Write-ColorOutput "🔄 Stopping existing container..." $BLUE
        Stop-Container
        Remove-Container
    }
    
    Build-Image
    Start-Container
    
    Write-ColorOutput ""
    Write-ColorOutput "🎉 Deployment completed successfully!" $GREEN
    Write-ColorOutput ""
    Write-ColorOutput "📋 Next Steps:" $YELLOW
    Write-ColorOutput "  1. Check status: .\deploy.ps1 -Status" $BLUE
    Write-ColorOutput "  2. View logs:    .\deploy.ps1 -Logs" $BLUE
    Write-ColorOutput "  3. Stop scraper: .\deploy.ps1 -Stop" $BLUE
    Write-ColorOutput ""
    Write-ColorOutput "📊 Current Status:" $YELLOW
    Show-Status
}

# Main script logic
if ($Help) {
    Show-Help
} elseif ($Status) {
    Show-Status
} elseif ($Stop) {
    Stop-Container
} elseif ($Restart) {
    Restart-Container
} elseif ($Logs) {
    Show-Logs
} elseif ($Clean) {
    Clean-All
} else {
    # Default action: deploy
    Deploy-Application
}
