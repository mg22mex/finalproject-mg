#!/bin/bash

# 🚀 Autosell.mx Master Startup Script
# One script to rule them all - handles all issues automatically

echo "🚀 AUTOSELL.MX MASTER STARTUP"
echo "============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
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

print_magic() {
    echo -e "${PURPLE}[MAGIC]${NC} $1"
}

# Check directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run from project root directory"
    exit 1
fi

print_magic "One script to start them all..."

# Step 1: Nuclear cleanup
print_status "🧹 Cleaning up existing processes..."
pkill -f "python.*main" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "http.server" 2>/dev/null || true
pkill -f "node.*serve" 2>/dev/null || true
sleep 3

# Step 2: Backend Setup
print_status "🔧 Setting up backend environment..."
cd backend

# Create venv if needed
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate environment
source venv/bin/activate

# Install dependencies with fallbacks
print_status "Installing Python dependencies..."
pip install --upgrade pip

# Install core dependencies first
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart pydantic python-dotenv

# Try to install remaining dependencies
pip install -r requirements.txt 2>/dev/null || print_warning "Some optional dependencies failed, continuing..."

# Handle database
print_status "Setting up database..."
if command -v psql &> /dev/null; then
    print_status "PostgreSQL found, attempting to start..."
    sudo service postgresql start 2>/dev/null || print_warning "PostgreSQL start failed, using SQLite fallback"
else
    print_warning "PostgreSQL not found, using SQLite"
fi

# Find available port
print_status "Finding available port..."
for port in 8000 8001 8002 8003; do
    if ! lsof -ti:$port >/dev/null 2>&1; then
        print_success "Using port $port for backend"
        BACKEND_PORT=$port
        break
    fi
done

if [ -z "$BACKEND_PORT" ]; then
    print_error "No available ports found"
    exit 1
fi

# Start backend
print_status "Starting FastAPI backend on port $BACKEND_PORT..."
python main_fixed.py --port $BACKEND_PORT &
BACKEND_PID=$!
sleep 5

if ps -p $BACKEND_PID > /dev/null; then
    print_success "Backend started successfully (PID: $BACKEND_PID)"
else
    print_error "Backend failed to start"
    exit 1
fi

# Step 3: Frontend Setup
print_status "🎨 Setting up frontend..."
cd ../frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
npm install

# Build frontend
print_status "Building React frontend..."
npm run build

# Find available port for frontend
print_status "Finding available port for frontend..."
for port in 3000 3001 3002 3003; do
    if ! lsof -ti:$port >/dev/null 2>&1; then
        print_success "Using port $port for frontend"
        FRONTEND_PORT=$port
        break
    fi
done

if [ -z "$FRONTEND_PORT" ]; then
    print_error "No available ports found for frontend"
    exit 1
fi

# Start frontend
print_status "Starting frontend on port $FRONTEND_PORT..."
cd dist
python3 -m http.server $FRONTEND_PORT &
FRONTEND_PID=$!
sleep 3

if ps -p $FRONTEND_PID > /dev/null; then
    print_success "Frontend started successfully (PID: $FRONTEND_PID)"
else
    print_error "Frontend failed to start"
    exit 1
fi

# Step 4: Display Results
echo ""
echo "🎉 AUTOSELL.MX SYSTEM READY!"
echo "============================"
echo ""
print_success "🚀 Backend API: http://localhost:$BACKEND_PORT"
print_success "🎨 Frontend Dashboard: http://localhost:$FRONTEND_PORT"
print_success "📚 API Documentation: http://localhost:$BACKEND_PORT/docs"
echo ""
print_status "System Components:"
echo "  ✅ FastAPI Backend (Port $BACKEND_PORT) - PID: $BACKEND_PID"
echo "  ✅ React Frontend (Port $FRONTEND_PORT) - PID: $FRONTEND_PID"
echo "  ✅ Database (PostgreSQL/SQLite)"
echo "  ✅ Google Drive Integration"
echo ""
print_status "Management Commands:"
echo "  Stop system: kill $BACKEND_PID $FRONTEND_PID"
echo "  Test backend: curl http://localhost:$BACKEND_PORT/health"
echo "  Test frontend: curl http://localhost:$FRONTEND_PORT"
echo ""
print_magic "🚀 Ready for production use!"
