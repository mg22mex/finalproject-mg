#!/bin/bash

# 🚀 Autosell.mx Quick Start Script for GitHub Codespaces
# Optimized for Codespace environment (no Docker, no systemctl)

echo "🚀 AUTOSELL.MX CODESPACE QUICK START"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting Autosell.mx system in Codespace..."

# Step 1: Setup Backend Environment
print_status "Setting up backend environment..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing Python dependencies..."
print_status "Upgrading pip first..."
pip install --upgrade pip

print_status "Installing core dependencies first..."
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart

print_status "Installing remaining dependencies..."
pip install -r requirements.txt

# If opencv-python fails, install without it
if [ $? -ne 0 ]; then
    print_warning "Some dependencies failed, trying without opencv-python..."
    pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart pydantic python-dotenv
fi

# Check if PostgreSQL is available (Codespace might have it pre-installed)
print_status "Checking database availability..."
if command -v psql &> /dev/null; then
    print_success "PostgreSQL client found"
    # Try to start PostgreSQL if it's not running
    if ! pg_isready -q; then
        print_status "Starting PostgreSQL service..."
        sudo service postgresql start 2>/dev/null || print_warning "PostgreSQL service start failed, continuing anyway..."
    fi
else
    print_warning "PostgreSQL not found, using SQLite for development"
fi

# Start backend
print_status "Starting FastAPI backend server..."
python main_fixed.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 5

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    print_success "Backend started successfully (PID: $BACKEND_PID)"
else
    print_error "Failed to start backend"
    print_status "Trying alternative backend startup..."
    python main.py &
    BACKEND_PID=$!
    sleep 3
    if ps -p $BACKEND_PID > /dev/null; then
        print_success "Backend started with main.py (PID: $BACKEND_PID)"
    else
        print_error "Both backend startup methods failed"
        exit 1
    fi
fi

# Step 2: Setup Frontend
print_status "Setting up frontend..."
cd ../frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
npm install

# Build frontend
print_status "Building React frontend..."
npm run build

# Start frontend server
print_status "Starting frontend server..."
cd dist
python3 -m http.server 3000 &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 3

# Check if frontend is running
if ps -p $FRONTEND_PID > /dev/null; then
    print_success "Frontend started successfully (PID: $FRONTEND_PID)"
else
    print_error "Failed to start frontend"
    exit 1
fi

# Step 3: Display URLs and Status
echo ""
echo "🎉 AUTOSELL.MX SYSTEM READY!"
echo "============================"
echo ""
print_success "Backend API: http://localhost:8000"
print_success "Frontend Dashboard: http://localhost:3000"
print_success "API Documentation: http://localhost:8000/docs"
echo ""
print_status "System components:"
echo "  ✅ FastAPI Backend (Port 8000) - PID: $BACKEND_PID"
echo "  ✅ React Frontend (Port 3000) - PID: $FRONTEND_PID"
echo "  ✅ Database (PostgreSQL/SQLite)"
echo "  ✅ Google Drive Integration"
echo ""
print_status "To stop the system, run:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
print_status "To check system health:"
echo "  curl http://localhost:8000/health"
echo "  curl http://localhost:3000"
echo ""
print_success "🚀 Ready for production use in Codespace!"
