#!/bin/bash

# TBM Advance Rate Calculator Startup Script
# This script provides easy startup options for different environments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  🚇 TBM Advance Rate Calculator - Production Startup"
    echo "═══════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to start with Docker Compose
start_docker() {
    print_status "Starting with Docker Compose..."
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose not found. Please install Docker Compose."
        exit 1
    fi
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example"
        cp .env.example .env
        print_warning "Please edit .env file with your configuration"
    fi
    
    # Build and start services
    docker-compose up --build -d
    
    print_status "Services started successfully!"
    print_status "Application: http://localhost"
    print_status "API Docs: http://localhost/docs"
    print_status "Health Check: http://localhost/api/v1/health"
    
    # Show logs
    echo ""
    print_status "Showing logs (Ctrl+C to exit log view):"
    docker-compose logs -f
}

# Function to start with Python directly
start_python() {
    print_status "Starting with Python directly..."
    
    if ! command_exists python3; then
        print_error "Python 3 not found. Please install Python 3.8+"
        exit 1
    fi
    
    # Check if virtual environment exists
    if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
        print_warning "Virtual environment not found. Creating one..."
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        if [ -d "venv" ]; then
            source venv/bin/activate
        else
            source .venv/bin/activate
        fi
    fi
    
    # Install dependencies if needed
    pip install -r requirements.txt
    
    # Start the application
    print_status "Starting TBM Calculator..."
    python3 run.py
}

# Function to start development mode
start_dev() {
    print_status "Starting in development mode..."
    export DEBUG=true
    export LOG_LEVEL=debug
    export WORKERS=1
    start_python
}

# Function to run tests
run_tests() {
    print_status "Running tests..."
    
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    
    # Install test dependencies
    pip install pytest pytest-asyncio httpx pytest-cov
    
    # Run tests
    pytest tests/ -v --cov=app
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  docker    Start with Docker Compose (recommended for production)"
    echo "  python    Start with Python directly"
    echo "  dev       Start in development mode"
    echo "  test      Run tests"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 docker    # Start with Docker"
    echo "  $0 dev       # Start in development mode"
    echo "  $0 test      # Run tests"
}

# Main execution
print_header

case "${1:-docker}" in
    docker)
        start_docker
        ;;
    python)
        start_python
        ;;
    dev)
        start_dev
        ;;
    test)
        run_tests
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown option: $1"
        show_help
        exit 1
        ;;
esac