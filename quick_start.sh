#!/bin/bash

# 🚗 Autosell.mx - Quick Start Script
# This script will get your development environment running in minutes!

set -e

echo "🚗 Autosell.mx - Quick Start Script"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Current directory: $(pwd)"
    echo "   Expected files: package.json, docker-compose.yml"
    exit 1
fi

echo "✅ Project directory confirmed"
echo ""

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version too old. Please install Node.js 18+ (current: $(node --version))"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm 9+ first."
    exit 1
fi
echo "✅ npm $(npm --version)"

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi
echo "✅ Docker $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi
echo "✅ Docker Compose $(docker-compose --version)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi
echo "✅ Python $(python3 --version)"

echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ .env file created from template"
        echo "⚠️  IMPORTANT: Please edit .env file with your actual API keys before continuing"
        echo "   You can do this later, but some features won't work without proper configuration"
        echo ""
        read -p "Press Enter to continue or Ctrl+C to edit .env first..."
    else
        echo "❌ env.example not found. Please create .env file manually."
        exit 1
    fi
else
    echo "✅ .env file found"
fi

echo ""

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "✅ Node.js dependencies already installed"
fi

# Check Python virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Python virtual environment created"
fi

# Activate virtual environment and install Python dependencies
echo "🐍 Installing Python dependencies..."
source venv/bin/activate
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ backend/requirements.txt not found"
    exit 1
fi

pip install -r backend/requirements.txt
echo "✅ Python dependencies installed"

echo ""

# Start services
echo "🚀 Starting development environment..."
echo ""

# Start Docker services in background
echo "🐳 Starting Docker services (PostgreSQL, Redis, n8n)..."
npm run start

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if docker-compose ps | grep -q "Up"; then
    echo "✅ Docker services are running"
else
    echo "❌ Docker services failed to start. Check logs with: npm run logs"
    exit 1
fi

echo ""

# Run database setup
echo "🗄️  Setting up database..."
npm run db:setup

echo ""

# Show status
echo "🎉 Development environment is ready!"
echo ""
echo "📱 Services running:"
echo "   Frontend:     http://localhost:3000"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   n8n:         http://localhost:5678 (admin/autosell123)"
echo "   Database:     localhost:5432"
echo "   Redis:        localhost:6379"
echo "   Prometheus:   http://localhost:9090"
echo "   Grafana:      http://localhost:3001 (admin/admin123)"
echo ""

echo "🚀 To start development servers, run:"
echo "   npm run dev:all"
echo ""

echo "📚 For more information, see:"
echo "   SETUP.md - Detailed setup guide"
echo "   PROGRESS_SUMMARY.md - Project status and next steps"
echo ""

echo "🎯 Next steps:"
echo "   1. Edit .env file with your API keys"
echo "   2. Start development servers: npm run dev:all"
echo "   3. Open http://localhost:3000 in your browser"
echo "   4. Start building features!"
echo ""

echo "🚗 Happy coding! Your Autosell.mx system is ready to go! 🎉"
