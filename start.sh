#!/bin/bash

# 🚀 Autosell.mx Lightweight Startup Script
# Optimized for GitHub Codespaces - minimal resource usage

echo "🚀 AUTOSELL.MX LIGHTWEIGHT STARTUP"
echo "==================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run from project root directory"
    exit 1
fi

# Step 1: Light cleanup (only essential processes)
print_status "🧹 Light cleanup..."
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "http.server" 2>/dev/null || true
sleep 1

# Step 2: Backend Setup (minimal)
print_status "🔧 Setting up backend..."
cd backend

# Use existing venv if available
if [ -d "venv" ]; then
    source venv/bin/activate
    print_status "Using existing virtual environment"
else
    print_status "Creating minimal virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --quiet fastapi uvicorn sqlalchemy python-dotenv
fi

# Use SQLite for simplicity (no PostgreSQL setup)
print_status "Using SQLite database (lightweight)"

# Start backend on fixed port 8000
print_status "Starting backend on port 8000..."
python start_backend.py &
BACKEND_PID=$!
sleep 3

# Quick health check
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    print_success "Backend is running (PID: $BACKEND_PID)"
else
    print_warning "Backend may need more time to start"
fi

# Step 3: Frontend Setup (minimal)
print_status "🎨 Setting up frontend..."
cd ../frontend

# Check if dist exists, if not build quickly
if [ ! -d "dist" ]; then
    print_status "Building frontend..."
    npm install --silent
    npm run build --silent
fi

# Start frontend on fixed port 3000
print_status "Starting frontend on port 3000..."
cd dist
python3 -m http.server 3000 &
FRONTEND_PID=$!
sleep 2

# Quick check
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend is running (PID: $FRONTEND_PID)"
else
    print_warning "Frontend may need more time to start"
fi

# Step 4: Display Results (minimal)
echo ""
echo "🎉 SYSTEM READY!"
echo "================"
echo ""
print_success "🚀 Backend: http://localhost:8000"
print_success "🎨 Frontend: http://localhost:3000"
print_success "📚 API Docs: http://localhost:8000/docs"
echo ""
print_status "Process IDs: Backend=$BACKEND_PID, Frontend=$FRONTEND_PID"
echo ""
print_status "💡 Lightweight mode - optimized for Codespaces"