#!/bin/bash

echo "🔧 Final Frontend Fix Script"
echo "============================"

cd frontend

echo "🔍 Current state analysis..."
echo "Node version: $(node --version)"
echo "NPM version: $(npm --version)"
echo "Working directory: $(pwd)"

echo "📦 Checking Vite installation..."
if [ -f "node_modules/.bin/vite" ]; then
    echo "✅ Vite found in node_modules/.bin/"
    ./node_modules/.bin/vite --version
else
    echo "❌ Vite not found, installing..."
    npm install vite@latest --save-dev
fi

echo "🔧 Testing npx approach..."
if npx vite --version > /dev/null 2>&1; then
    echo "✅ npx vite works"
    echo "🚀 Starting frontend with npx..."
    npx vite --host 0.0.0.0 --port 5173
else
    echo "❌ npx vite failed"
    echo "🔧 Trying alternative approach..."
    
    # Create a simple start script
    cat > start_frontend_npx.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Starting frontend with npx vite..."
npx vite --host 0.0.0.0 --port 5173
EOF
    
    chmod +x start_frontend_npx.sh
    echo "✅ Created start_frontend_npx.sh script"
    echo "🚀 You can now use: ./start_frontend_npx.sh"
fi
