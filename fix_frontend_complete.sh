#!/bin/bash

echo "🔧 Complete Frontend Fix Script"
echo "=============================="

cd frontend

echo "🔍 Current state analysis..."
echo "Node version: $(node --version)"
echo "NPM version: $(npm --version)"
echo "Working directory: $(pwd)"

echo "📦 Checking Vite installation..."
if [ -f "node_modules/.bin/vite" ]; then
    echo "✅ Vite found in node_modules/.bin/"
    VITE_VERSION=$(./node_modules/.bin/vite --version)
    echo "Vite version: $VITE_VERSION"
else
    echo "❌ Vite not found, installing..."
    npm install vite
fi

echo "🔧 Testing different ways to start Vite..."

echo "1. Testing direct execution..."
if ./node_modules/.bin/vite --version > /dev/null 2>&1; then
    echo "✅ Direct execution works"
else
    echo "❌ Direct execution failed"
fi

echo "2. Testing npx..."
if npx vite --version > /dev/null 2>&1; then
    echo "✅ npx works"
else
    echo "❌ npx failed"
fi

echo "3. Testing npm script..."
echo "Current dev script in package.json:"
grep -A 1 '"dev"' package.json

echo "🔧 Creating alternative start script..."
cat > start_frontend.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Starting frontend with direct Vite execution..."
./node_modules/.bin/vite --host 0.0.0.0 --port 5173
EOF

chmod +x start_frontend.sh

echo "✅ Created start_frontend.sh script"

echo "🧪 Testing the new script..."
timeout 5s ./start_frontend.sh &
FRONTEND_PID=$!

sleep 3

if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "✅ Frontend started successfully with direct script"
    kill $FRONTEND_PID
    wait $FRONTEND_PID 2>/dev/null
else
    echo "❌ Frontend script failed"
fi

echo "🔧 Updating package.json dev script..."
# Backup original
cp package.json package.json.backup

# Update dev script to use direct path
sed -i 's/"dev": "vite"/"dev": ".\/node_modules\/.bin\/vite"/' package.json

echo "✅ Updated package.json dev script"

echo "🧪 Testing updated npm script..."
timeout 5s npm run dev &
NPM_PID=$!

sleep 3

if kill -0 $NPM_PID 2>/dev/null; then
    echo "✅ npm run dev now works!"
    kill $NPM_PID
    wait $NPM_PID 2>/dev/null
else
    echo "❌ npm run dev still fails, restoring backup..."
    mv package.json.backup package.json
fi

echo "✅ Frontend fix completed!"
echo "🚀 You can now use:"
echo "   - npm run dev"
echo "   - ./start_frontend.sh"
echo "   - ./node_modules/.bin/vite --host 0.0.0.0 --port 5173"
