#!/bin/bash
echo "🚀 Setting up Autosell.mx in GitHub Codespaces..."

# Install system dependencies
sudo apt-get update
sudo apt-get install -y postgresql-client

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
npm run build

# Setup database
cd ../backend
python init_database.py

echo "✅ Setup complete! Your system is ready."
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:8000"
