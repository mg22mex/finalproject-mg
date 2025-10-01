#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 Starting frontend with direct Vite execution..."
./node_modules/.bin/vite --host 0.0.0.0 --port 5173
