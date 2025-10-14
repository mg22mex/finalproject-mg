#!/bin/bash

# Kill any existing processes on ports 3000 and 8000
echo "🔄 Stopping existing servers..."
pkill -f "python.*http.server" 2>/dev/null || true
pkill -f "python.*start_backend" 2>/dev/null || true
sleep 2

# Start backend
echo "🚀 Starting backend server..."
cd /home/mg/Yandex.Disk/L1der/Finalproject-mg/backend
source venv/bin/activate
python start_backend.py &
BACKEND_PID=$!
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "🌐 Starting frontend server..."
cd /home/mg/Yandex.Disk/L1der/Finalproject-mg/frontend-clean
python3 -m http.server 3000 &
FRONTEND_PID=$!
sleep 2

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running on http://localhost:3000"
    echo ""
    echo "🎯 Your application is ready!"
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend: http://localhost:8000"
    echo "📊 API Docs: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop both servers"
else
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Wait for user to stop
wait
