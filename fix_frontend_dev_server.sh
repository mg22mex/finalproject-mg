#!/bin/bash

echo "🔧 Fixing Frontend Dev Server Issue"
echo "=================================="

cd frontend

echo "🔍 Checking current state..."
echo "Node version: $(node --version)"
echo "NPM version: $(npm --version)"

echo "📦 Checking Vite installation..."
if [ -f "node_modules/.bin/vite" ]; then
    echo "✅ Vite found in node_modules/.bin/"
    ./node_modules/.bin/vite --version
else
    echo "❌ Vite not found, reinstalling..."
    npm install vite
fi

echo "🔧 Testing direct Vite execution..."
if ./node_modules/.bin/vite --version > /dev/null 2>&1; then
    echo "✅ Vite works directly"
else
    echo "❌ Vite direct execution failed"
    exit 1
fi

echo "🔧 Testing npm script..."
echo "Current package.json dev script:"
grep -A 1 '"dev"' package.json

echo "🧪 Testing npm run dev with timeout..."
timeout 10s npm run dev &
DEV_PID=$!

sleep 3

if kill -0 $DEV_PID 2>/dev/null; then
    echo "✅ npm run dev started successfully"
    kill $DEV_PID
    wait $DEV_PID 2>/dev/null
else
    echo "❌ npm run dev failed to start"
fi

echo "🔧 Alternative: Using npx..."
echo "Testing npx vite..."
npx vite --version

echo "✅ Frontend dev server fix completed!"
echo "🚀 Try running: npm run dev"
echo "🚀 Or: npx vite"
echo "🚀 Or: ./node_modules/.bin/vite"
