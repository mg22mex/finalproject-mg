#!/bin/bash

echo "🚀 Autosell.mx Local Environment Setup"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install package if not exists
install_if_missing() {
    local package=$1
    local install_command=$2
    
    if ! command_exists "$package"; then
        echo -e "${YELLOW}📦 Installing $package...${NC}"
        eval "$install_command"
    else
        echo -e "${GREEN}✅ $package is already installed${NC}"
    fi
}

echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check Node.js
if ! command_exists node; then
    echo -e "${RED}❌ Node.js is required but not installed${NC}"
    echo -e "${YELLOW}Please install Node.js from: https://nodejs.org/${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Node.js is installed${NC}"
fi

# Check Python
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Python 3 is installed${NC}"
fi

# Check PostgreSQL
if ! command_exists psql; then
    echo -e "${YELLOW}⚠️  PostgreSQL is not installed${NC}"
    echo -e "${BLUE}Installing PostgreSQL...${NC}"
    
    # Try different package managers
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y postgresql postgresql-contrib
    elif command_exists yum; then
        sudo yum install -y postgresql postgresql-server
    elif command_exists brew; then
        brew install postgresql
    else
        echo -e "${RED}❌ Cannot install PostgreSQL automatically${NC}"
        echo -e "${YELLOW}Please install PostgreSQL manually${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ PostgreSQL is installed${NC}"
fi

# Check Docker (optional)
if command_exists docker; then
    echo -e "${GREEN}✅ Docker is available${NC}"
else
    echo -e "${YELLOW}⚠️  Docker is not installed (optional for PostgreSQL)${NC}"
fi

echo -e "\n${BLUE}📦 Installing global dependencies...${NC}"

# Install global npm packages
install_if_missing "n8n" "npm install -g n8n"
install_if_missing "vite" "npm install -g vite"

echo -e "\n${BLUE}🔧 Setting up backend...${NC}"

# Backend setup
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating Python virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

cd ..

echo -e "\n${BLUE}🎨 Setting up frontend...${NC}"

# Frontend setup
cd frontend

# Install npm dependencies
echo -e "${BLUE}📦 Installing frontend dependencies...${NC}"
npm install

cd ..

echo -e "\n${BLUE}🗄️ Setting up database...${NC}"

# Start PostgreSQL
if command_exists systemctl; then
    echo -e "${BLUE}🚀 Starting PostgreSQL service...${NC}"
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
elif command_exists brew; then
    echo -e "${BLUE}🚀 Starting PostgreSQL service...${NC}"
    brew services start postgresql
fi

# Wait for PostgreSQL to start
sleep 3

# Create database
echo -e "${BLUE}🗄️ Creating database...${NC}"
sudo -u postgres createdb autosell 2>/dev/null || echo "Database may already exist"

echo -e "\n${GREEN}🎉 Environment setup completed!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}Next steps:${NC}"
echo -e "${YELLOW}1. Run: ./fix_all_issues.sh${NC}"
echo -e "${YELLOW}2. Run: ./start_local.sh${NC}"
echo -e "${YELLOW}3. Open: http://localhost:5173${NC}"
echo -e "${BLUE}==========================================${NC}"
