#!/bin/bash
# Simple Automation Setup for Autosell.mx
# This creates a robust automation system without complex MCP dependencies

set -e

echo "🚀 Setting up Simple Automation for Autosell.mx"
echo "==============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

print_status "Creating automation management system..."

# Create the main automation script
cat > manage_automation.sh << 'EOF'
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
EOF

chmod +x manage_automation.sh

print_success "Automation management script created"

print_status "Creating log directory..."
mkdir -p logs

print_success "Log directory created"

print_status "Creating n8n workflow configuration..."

# Create a simple n8n workflow configuration
cat > n8n_workflow_config.md << 'EOF'
# n8n Workflow Configuration for Autosell.mx

## 🎯 Recommended Workflow Setup

### 1. Google Sheets to Backend Sync

**CRITICAL SETTINGS:**
- ✅ **Manual execution ONLY** (no automatic triggers)
- ✅ **Batch size: 10 vehicles** (to avoid overwhelming the backend)
- ✅ **Error handling: Continue on failure**
- ✅ **Retry logic: 3 attempts with 1-second delay**

**Workflow Steps:**
1. **Manual Trigger** (Webhook or Manual)
2. **Google Sheets Read** (Range: A101:J231 for 131 vehicles)
3. **Data Validation** (AI-powered cleaning)
4. **Batch Processing** (10 vehicles at a time)
5. **Backend API Call** (POST to /vehicles/)
6. **Success/Error Handling**
7. **Facebook Posting** (optional, for new vehicles)
8. **Response/Notification**

### 2. Facebook Automation

**Settings:**
- ✅ **Trigger: New vehicle created**
- ✅ **Page ID: Your Facebook Page ID**
- ✅ **Access Token: Your Facebook Access Token**
- ✅ **Auto-post: Only for new vehicles**

### 3. Status Synchronization

**Settings:**
- ✅ **Trigger: Status change**
- ✅ **Sync: Backend ↔ Facebook ↔ Google Sheets**
- ✅ **Remove from Facebook when status = "VENDIDO"**

## 🚨 IMPORTANT: Preventing Duplicate Imports

### Before Running Any Workflow:

1. **Check current vehicle count:**
   ```bash
   curl -s http://localhost:8001/dashboard/stats | grep total_vehicles
   ```

2. **If count is > 200, reset the system:**
   ```bash
   ./manage_automation.sh reset
   ```

3. **Only run workflows MANUALLY**
4. **Test with small batches first**
5. **Monitor the execution closely**

### Safe Workflow Execution:

1. **Start with 5 vehicles** (range: A101:A105)
2. **Check results**
3. **If successful, increase to 10 vehicles**
4. **Continue until all 131 vehicles are imported**

## 🔧 Configuration Steps:

1. **Go to http://localhost:5678**
2. **Create new workflow**
3. **Add Google Sheets node**
4. **Configure with your credentials**
5. **Set range to A101:J231**
6. **Add data processing node**
7. **Add backend API node**
8. **Set to MANUAL execution only**
9. **Test with small batch**
10. **Run full import when ready**

This configuration ensures reliable, controlled data synchronization without the duplicate import issues.
EOF

print_success "n8n workflow configuration created"

print_status "Creating test and validation scripts..."

# Create a comprehensive test script
cat > test_system.sh << 'EOF'
#!/bin/bash
# Comprehensive system test for Autosell.mx

echo "🧪 Testing Autosell.mx System..."
echo "================================="

# Test backend API
echo "Testing Backend API..."
if curl -s http://localhost:8001/health > /dev/null; then
    echo "✅ Backend API: OK"
    
    # Get vehicle count
    VEHICLE_COUNT=$(curl -s http://localhost:8001/dashboard/stats | grep -o '"total_vehicles":[0-9]*' | cut -d: -f2)
    echo "📊 Current vehicles: $VEHICLE_COUNT"
    
    if [ "$VEHICLE_COUNT" -gt 200 ]; then
        echo "⚠️  WARNING: High vehicle count detected ($VEHICLE_COUNT)"
        echo "   Consider running: ./manage_automation.sh reset"
    fi
else
    echo "❌ Backend API: Failed"
fi

# Test frontend
echo "Testing Frontend..."
if curl -s http://localhost:3002 > /dev/null; then
    echo "✅ Frontend: OK"
else
    echo "❌ Frontend: Failed"
fi

# Test n8n
echo "Testing n8n..."
if curl -s http://localhost:5678 > /dev/null; then
    echo "✅ n8n: OK"
else
    echo "❌ n8n: Failed"
fi

# Test API endpoints
echo "Testing API Endpoints..."
if curl -s http://localhost:8001/vehicles > /dev/null; then
    echo "✅ Vehicles API: OK"
else
    echo "❌ Vehicles API: Failed"
fi

if curl -s http://localhost:8001/dashboard/stats > /dev/null; then
    echo "✅ Dashboard API: OK"
else
    echo "❌ Dashboard API: Failed"
fi

echo ""
echo "🎉 System test completed!"
echo ""
echo "📋 Next steps:"
echo "1. If all tests pass, go to http://localhost:5678"
echo "2. Configure your Google Sheets workflow"
echo "3. Set it to MANUAL execution only"
echo "4. Test with a small batch first"
echo "5. Run full import when ready"
EOF

chmod +x test_system.sh

print_success "Test script created"

print_status "Creating documentation..."

# Create comprehensive documentation
cat > AUTOMATION_GUIDE.md << 'EOF'
# Autosell.mx Automation Guide
## Complete Setup and Usage Guide

### 🚀 Quick Start

1. **Start the system:**
   ```bash
   ./manage_automation.sh start
   ```

2. **Test the system:**
   ```bash
   ./test_system.sh
   ```

3. **Check status:**
   ```bash
   ./manage_automation.sh status
   ```

4. **Access interfaces:**
   - Frontend: http://localhost:3002
   - Backend: http://localhost:8001
   - n8n: http://localhost:5678

### 🔧 n8n Workflow Setup

#### Step 1: Create Google Sheets Workflow

1. **Go to http://localhost:5678**
2. **Click "Create Workflow"**
3. **Add Google Sheets node:**
   - Authentication: Your Google account
   - Spreadsheet: Your Google Sheet ID
   - Range: A101:J231 (for 131 vehicles)
   - Operation: Read

4. **Add Data Processing node:**
   ```javascript
   // Clean and validate data
   const items = $input.all();
   const processedItems = [];
   
   for (const item of items) {
     const data = item.json;
     const vehicleData = {
       marca: data.A || 'Unknown',
       modelo: data.B || 'Unknown',
       año: parseInt(data.C) || new Date().getFullYear(),
       precio: parseInt(data.D) || 0,
       estatus: data.E || 'DISPONIBLE',
       color: data.F || 'Unknown',
       kilometraje: data.G || '',
       ubicacion: data.H || 'PERIFERICO',
       descripcion: data.I || ''
     };
     processedItems.push({ json: vehicleData });
   }
   
   return processedItems;
   ```

5. **Add Backend API node:**
   - Method: POST
   - URL: http://localhost:8001/vehicles/
   - Headers: Content-Type: application/json
   - Body: {{ $json }}

6. **Set to MANUAL execution only**

#### Step 2: Test the Workflow

1. **Test with small batch first:**
   - Change range to A101:A105 (5 vehicles)
   - Execute workflow
   - Check results

2. **If successful, increase batch size:**
   - Change range to A101:A110 (10 vehicles)
   - Execute workflow
   - Check results

3. **Run full import:**
   - Change range to A101:J231 (131 vehicles)
   - Execute workflow
   - Monitor execution

### 🚨 Important Safety Measures

#### Before Running Any Workflow:

1. **Check current vehicle count:**
   ```bash
   curl -s http://localhost:8001/dashboard/stats | grep total_vehicles
   ```

2. **If count > 200, reset system:**
   ```bash
   ./manage_automation.sh reset
   ```

3. **Always test with small batches first**
4. **Monitor execution closely**
5. **Stop immediately if errors occur**

### 📊 Monitoring and Troubleshooting

#### Check System Status:
```bash
./manage_automation.sh status
```

#### View Logs:
```bash
./manage_automation.sh logs
```

#### Reset System:
```bash
./manage_automation.sh reset
```

#### Test System:
```bash
./test_system.sh
```

### 🔄 Workflow Execution Process

1. **Prepare:**
   - Ensure system is running
   - Check current vehicle count
   - Reset if necessary

2. **Configure:**
   - Set up Google Sheets workflow
   - Configure with your credentials
   - Set to manual execution

3. **Test:**
   - Start with 5 vehicles
   - Check results
   - Increase batch size gradually

4. **Execute:**
   - Run full import (131 vehicles)
   - Monitor execution
   - Check final results

5. **Verify:**
   - Check frontend at http://localhost:3002
   - Verify vehicle count
   - Test functionality

### 🎯 Expected Results

After successful import:
- **Total Vehicles: 131**
- **Available Vehicles: 131**
- **Total Value: ~$25,000,000**
- **All vehicles visible in frontend**
- **All functionality working**

### 🛠️ Troubleshooting

#### Common Issues:

1. **High vehicle count (>200):**
   - Run: `./manage_automation.sh reset`
   - Start fresh

2. **n8n connection errors:**
   - Check if n8n is running
   - Restart: `./manage_automation.sh stop && ./manage_automation.sh start`

3. **Backend API errors:**
   - Check backend logs
   - Restart backend

4. **Frontend not loading:**
   - Check if frontend is running
   - Check port 3002

#### Getting Help:

1. **Check status:** `./manage_automation.sh status`
2. **View logs:** `./manage_automation.sh logs`
3. **Test system:** `./test_system.sh`
4. **Reset if needed:** `./manage_automation.sh reset`

This guide provides everything you need to set up and run the automation system successfully!
EOF

print_success "Documentation created"

print_status "Finalizing setup..."

# Create a simple status check script
cat > quick_status.sh << 'EOF'
#!/bin/bash
# Quick status check for Autosell.mx

echo "📊 Autosell.mx Quick Status"
echo "=========================="

# Check if services are running
if [ -f ".backend.pid" ] && kill -0 "$(cat .backend.pid)" 2>/dev/null; then
    echo "✅ Backend: Running"
else
    echo "❌ Backend: Not running"
fi

if [ -f ".n8n.pid" ] && kill -0 "$(cat .n8n.pid)" 2>/dev/null; then
    echo "✅ n8n: Running"
else
    echo "❌ n8n: Not running"
fi

if [ -f ".frontend.pid" ] && kill -0 "$(cat .frontend.pid)" 2>/dev/null; then
    echo "✅ Frontend: Running"
else
    echo "❌ Frontend: Not running"
fi

# Get vehicle count
VEHICLE_COUNT=$(curl -s http://localhost:8001/dashboard/stats 2>/dev/null | grep -o '"total_vehicles":[0-9]*' | cut -d: -f2 || echo "N/A")
echo "🚗 Total Vehicles: $VEHICLE_COUNT"

if [ "$VEHICLE_COUNT" != "N/A" ] && [ "$VEHICLE_COUNT" -gt 200 ]; then
    echo "⚠️  WARNING: High vehicle count detected!"
    echo "   Consider running: ./manage_automation.sh reset"
fi

echo ""
echo "🌐 Access Points:"
echo "   Frontend: http://localhost:3002"
echo "   Backend: http://localhost:8001"
echo "   n8n: http://localhost:5678"
EOF

chmod +x quick_status.sh

print_success "Quick status script created"

print_status "Setup completed successfully! 🎉"
echo ""
echo "📋 Next Steps:"
echo "1. Run: ./manage_automation.sh start"
echo "2. Run: ./test_system.sh"
echo "3. Go to http://localhost:5678"
echo "4. Configure your Google Sheets workflow"
echo "5. Set it to MANUAL execution only"
echo "6. Test with small batches first"
echo ""
echo "📚 Documentation:"
echo "   - AUTOMATION_GUIDE.md (complete guide)"
echo "   - n8n_workflow_config.md (workflow setup)"
echo ""
echo "🔧 Management:"
echo "   - ./manage_automation.sh (main control)"
echo "   - ./quick_status.sh (quick check)"
echo "   - ./test_system.sh (system test)"
echo ""
print_success "Autosell.mx Automation System is ready! 🚀"
