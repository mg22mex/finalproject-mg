#!/bin/bash
# Automation Management Script for Autosell.mx

case "$1" in
    start)
        echo "🚀 Starting Autosell.mx System..."
        
        # Stop any existing processes
        pkill -f "start_backend.py" 2>/dev/null || true
        pkill -f "n8n start" 2>/dev/null || true
        pkill -f "python3 -m http.server 3002" 2>/dev/null || true
        
        # Start backend
        cd backend && source venv/bin/activate && nohup python start_backend.py > ../logs/backend.log 2>&1 &
        echo $! > ../.backend.pid
        echo "✅ Backend started (PID: $(cat ../.backend.pid))"
        
        # Wait for backend to start
        sleep 5
        
        # Start n8n (without automatic workflows)
        N8N_DISABLE_PRODUCTION_MAIN_PROCESS=true nohup n8n start > logs/n8n.log 2>&1 &
        echo $! > .n8n.pid
        echo "✅ n8n started (PID: $(cat .n8n.pid))"
        
        # Wait for n8n to start
        sleep 10
        
        # Start frontend
        cd frontend-clean && nohup python3 -m http.server 3002 > ../logs/frontend.log 2>&1 &
        echo $! > ../.frontend.pid
        echo "✅ Frontend started (PID: $(cat ../.frontend.pid))"
        
        echo ""
        echo "🎉 All services started successfully!"
        echo "🌐 Frontend: http://localhost:3002"
        echo "🔧 Backend: http://localhost:8001"
        echo "🤖 n8n: http://localhost:5678"
        echo ""
        echo "📋 Next steps:"
        echo "1. Go to http://localhost:5678"
        echo "2. Configure your Google Sheets workflow"
        echo "3. Set it to MANUAL execution only"
        echo "4. Test with a small batch first"
        ;;
        
    stop)
        echo "🛑 Stopping Autosell.mx System..."
        
        # Stop all services
        for pid_file in .backend.pid .n8n.pid .frontend.pid; do
            if [ -f "$pid_file" ]; then
                PID=$(cat "$pid_file")
                if kill -0 "$PID" 2>/dev/null; then
                    kill "$PID"
                    echo "✅ Stopped service (PID: $PID)"
                fi
                rm "$pid_file"
            fi
        done
        
        # Force kill any remaining processes
        pkill -f "start_backend.py" 2>/dev/null || true
        pkill -f "n8n start" 2>/dev/null || true
        pkill -f "python3 -m http.server 3002" 2>/dev/null || true
        
        echo "✅ All services stopped"
        ;;
        
    status)
        echo "📊 Autosell.mx System Status:"
        echo "=============================="
        
        # Check backend
        if [ -f ".backend.pid" ] && kill -0 "$(cat .backend.pid)" 2>/dev/null; then
            echo "✅ Backend: Running (PID: $(cat .backend.pid))"
        else
            echo "❌ Backend: Not running"
        fi
        
        # Check n8n
        if [ -f ".n8n.pid" ] && kill -0 "$(cat .n8n.pid)" 2>/dev/null; then
            echo "✅ n8n: Running (PID: $(cat .n8n.pid))"
        else
            echo "❌ n8n: Not running"
        fi
        
        # Check frontend
        if [ -f ".frontend.pid" ] && kill -0 "$(cat .frontend.pid)" 2>/dev/null; then
            echo "✅ Frontend: Running (PID: $(cat .frontend.pid))"
        else
            echo "❌ Frontend: Not running"
        fi
        
        # Check API connectivity
        echo ""
        echo "🔗 API Connectivity:"
        if curl -s http://localhost:8001/health > /dev/null 2>&1; then
            echo "✅ Backend API: Accessible"
        else
            echo "❌ Backend API: Not accessible"
        fi
        
        if curl -s http://localhost:3002 > /dev/null 2>&1; then
            echo "✅ Frontend: Accessible"
        else
            echo "❌ Frontend: Not accessible"
        fi
        
        if curl -s http://localhost:5678 > /dev/null 2>&1; then
            echo "✅ n8n: Accessible"
        else
            echo "❌ n8n: Not accessible"
        fi
        
        # Check vehicle count
        echo ""
        echo "📊 Current Data:"
        VEHICLE_COUNT=$(curl -s http://localhost:8001/dashboard/stats 2>/dev/null | grep -o '"total_vehicles":[0-9]*' | cut -d: -f2 || echo "N/A")
        echo "🚗 Total Vehicles: $VEHICLE_COUNT"
        ;;
        
    reset)
        echo "🔄 Resetting system (clearing all data)..."
        
        # Stop all services
        ./manage_automation.sh stop
        
        # Clear backend data (restart backend)
        echo "Clearing backend data..."
        sleep 2
        
        # Start fresh
        ./manage_automation.sh start
        
        echo "✅ System reset completed"
        ;;
        
    sync)
        echo "🔄 Manual sync instructions:"
        echo "1. Go to http://localhost:5678"
        echo "2. Find your Google Sheets workflow"
        echo "3. Click 'Execute Workflow'"
        echo "4. Monitor the execution"
        echo "5. Check results at http://localhost:3002"
        ;;
        
    logs)
        echo "📋 Recent logs:"
        echo "==============="
        echo ""
        echo "Backend logs:"
        tail -20 logs/backend.log 2>/dev/null || echo "No backend logs found"
        echo ""
        echo "n8n logs:"
        tail -20 logs/n8n.log 2>/dev/null || echo "No n8n logs found"
        echo ""
        echo "Frontend logs:"
        tail -20 logs/frontend.log 2>/dev/null || echo "No frontend logs found"
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|reset|sync|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start all services"
        echo "  stop    - Stop all services"
        echo "  status  - Check status of all services"
        echo "  reset   - Reset system (clear data and restart)"
        echo "  sync    - Instructions for manual sync"
        echo "  logs    - Show recent logs"
        exit 1
        ;;
esac
