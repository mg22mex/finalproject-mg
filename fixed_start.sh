#!/bin/bash

# 🚀 Fixed Autosell.mx Startup for Codespaces
# Handles port conflicts and database issues

echo "🚀 FIXED AUTOSELL.MX STARTUP"
echo "============================"
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
    print_error "Please run from project root"
    exit 1
fi

# Step 1: Clean up existing processes
print_status "Cleaning up existing processes..."
pkill -f "python.*main" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "http.server.*3000" 2>/dev/null || true
sleep 2

# Step 2: Backend Setup
print_status "Setting up backend..."
cd backend

# Create venv if needed
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install deps
source venv/bin/activate
print_status "Installing essential dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart pydantic python-dotenv

# Try to start PostgreSQL, fallback to SQLite
print_status "Setting up database..."
if command -v psql &> /dev/null; then
    print_status "PostgreSQL found, trying to start..."
    sudo service postgresql start 2>/dev/null || print_warning "PostgreSQL start failed, using SQLite"
else
    print_warning "PostgreSQL not found, using SQLite"
fi

# Start backend on different port if 8000 is busy
print_status "Starting backend..."
if lsof -ti:8000 >/dev/null 2>&1; then
    print_warning "Port 8000 is busy, using port 8001"
    PORT=8001
else
    PORT=8000
fi

python main_fixed.py --port $PORT &
BACKEND_PID=$!
sleep 5

if ps -p $BACKEND_PID > /dev/null; then
    print_success "Backend started on port $PORT (PID: $BACKEND_PID)"
else
    print_error "Backend failed to start"
    exit 1
fi

# Step 3: Frontend Setup
print_status "Setting up frontend..."
cd ../frontend

# Install and build
npm install
npm run build

# Start frontend
cd dist
python3 -m http.server 3000 &
FRONTEND_PID=$!
sleep 3

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
print_success "Backend: http://localhost:$PORT"
print_success "Frontend: http://localhost:3000"
print_success "API Docs: http://localhost:$PORT/docs"
echo ""
print_status "Process IDs:"
echo "  Backend: $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
print_status "To stop: kill $BACKEND_PID $FRONTEND_PID"
print_status "To test: curl http://localhost:$PORT/health"
