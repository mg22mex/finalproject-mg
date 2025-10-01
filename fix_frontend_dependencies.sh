#!/bin/bash

echo "🔧 Fixing Frontend Dependencies..."

# Navigate to frontend directory
cd frontend

echo "📦 Removing old dependencies..."
rm -rf node_modules
rm -f package-lock.json
rm -f yarn.lock

echo "📦 Installing fresh dependencies..."
npm install

echo "🔍 Verifying Vite installation..."
if [ -f "node_modules/.bin/vite" ]; then
    echo "✅ Vite is available locally"
    ./node_modules/.bin/vite --version
else
    echo "❌ Vite not found in node_modules"
    exit 1
fi

echo "🧪 Testing Vite configuration..."
./node_modules/.bin/vite --version

echo "✅ Frontend dependencies fixed!"
echo "🚀 You can now run: npm run dev"
