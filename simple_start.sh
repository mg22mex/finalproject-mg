#!/bin/bash

# 🚀 Simple Autosell.mx Startup for Codespaces
# Minimal dependencies, maximum compatibility

echo "🚀 SIMPLE AUTOSELL.MX STARTUP"
echo "============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run from project root"
    exit 1
fi

# Step 1: Backend Setup
print_status "Setting up backend..."
cd backend

# Create venv if needed
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install minimal deps
source venv/bin/activate
print_status "Installing essential dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart pydantic python-dotenv

# Start backend
print_status "Starting backend..."
python main_fixed.py &
BACKEND_PID=$!
sleep 3

if ps -p $BACKEND_PID > /dev/null; then
    print_success "Backend started (PID: $BACKEND_PID)"
else
    print_error "Backend failed to start"
    exit 1
fi

# Step 2: Frontend Setup
print_status "Setting up frontend..."
cd ../frontend

# Install and build
npm install
npm run build

# Start frontend
cd dist
python3 -m http.server 3000 &
FRONTEND_PID=$!
sleep 2

if ps -p $FRONTEND_PID > /dev/null; then
    print_success "Frontend started (PID: $FRONTEND_PID)"
else
    print_error "Frontend failed to start"
    exit 1
fi

# Display results
echo ""
echo "🎉 SYSTEM READY!"
echo "================"
print_success "Backend: http://localhost:8000"
print_success "Frontend: http://localhost:3000"
echo ""
echo "To stop: kill $BACKEND_PID $FRONTEND_PID"
