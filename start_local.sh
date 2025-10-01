#!/bin/bash

echo "🚀 Starting Autosell.mx Local Deployment"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}❌ Port $1 is already in use${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Port $1 is available${NC}"
        return 0
    fi
}

# Function to start service in background
start_service() {
    local name=$1
    local command=$2
    local port=$3
    
    echo -e "${BLUE}🔧 Starting $name...${NC}"
    
    if ! check_port $port; then
        echo -e "${YELLOW}⚠️  $name might already be running on port $port${NC}"
        return 1
    fi
    
    # Start service in background
    eval "$command" &
    local pid=$!
    echo "$name:$pid" >> .service_pids
    
    # Wait a moment and check if process is still running
    sleep 2
    if kill -0 $pid 2>/dev/null; then
        echo -e "${GREEN}✅ $name started successfully (PID: $pid)${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to start $name${NC}"
        return 1
    fi
}

# Clean up function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down all services...${NC}"
    
    if [ -f .service_pids ]; then
        while IFS=':' read -r service pid; do
            if kill -0 $pid 2>/dev/null; then
                echo -e "${BLUE}🛑 Stopping $service (PID: $pid)${NC}"
                kill $pid
            fi
        done < .service_pids
        rm -f .service_pids
    fi
    
    echo -e "${GREEN}✅ All services stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Remove old PID file
rm -f .service_pids

echo -e "${BLUE}📊 Checking system requirements...${NC}"

# Check if PostgreSQL is running
if ! pg_isready -q; then
    echo -e "${YELLOW}⚠️  PostgreSQL is not running. Starting with Docker...${NC}"
    if command -v docker &> /dev/null; then
        docker-compose up -d postgres
        sleep 5
    else
        echo -e "${RED}❌ PostgreSQL is not running and Docker is not available${NC}"
        echo -e "${YELLOW}Please start PostgreSQL manually: sudo systemctl start postgresql${NC}"
        exit 1
    fi
fi

# Check if n8n is available
if ! command -v n8n &> /dev/null; then
    echo -e "${YELLOW}⚠️  n8n is not installed. Installing...${NC}"
    npm install -g n8n
fi

echo -e "${GREEN}✅ System requirements checked${NC}"

# Start Backend
echo -e "\n${BLUE}🔧 Starting Backend...${NC}"
cd backend

# Clean database first
echo -e "${YELLOW}🧹 Cleaning database...${NC}"
source venv/bin/activate
python clean_database.py

# Start backend
start_service "Backend" "uvicorn main_fixed:app --host 0.0.0.0 --port 8000 --reload" 8000
cd ..

# Start n8n
echo -e "\n${BLUE}🤖 Starting n8n...${NC}"
start_service "n8n" "n8n start" 5678

# Start Frontend
echo -e "\n${BLUE}🎨 Starting Frontend...${NC}"
cd frontend

# Fix dependencies if needed
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing frontend dependencies...${NC}"
    npm install
fi

start_service "Frontend" "npm run dev" 5173
cd ..

# Wait a moment for all services to start
sleep 3

echo -e "\n${GREEN}🎉 All services started successfully!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}📊 Frontend: http://localhost:5173${NC}"
echo -e "${GREEN}🔧 Backend:  http://localhost:8000${NC}"
echo -e "${GREEN}🤖 n8n:      http://localhost:5678${NC}"
echo -e "${GREEN}📚 API Docs: http://localhost:8000/docs${NC}"
echo -e "${BLUE}==========================================${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"

# Keep script running and wait for interrupt
while true; do
    sleep 1
done
