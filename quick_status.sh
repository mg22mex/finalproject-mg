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
