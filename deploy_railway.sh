#!/bin/bash
# Railway deployment script for Autosell.mx

echo "🚀 Deploying Autosell.mx to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Create new project
echo "📦 Creating Railway project..."
railway project new autosell-mx

# Deploy backend
echo "🔧 Deploying backend..."
cd backend
railway service create autosell-backend
railway deploy

# Deploy frontend
echo "🎨 Deploying frontend..."
cd ../frontend
railway service create autosell-frontend
railway deploy

# Deploy n8n
echo "🤖 Deploying n8n..."
cd ..
railway service create autosell-n8n
railway deploy

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
railway service create autosell-db --template postgresql

echo "✅ Deployment complete!"
echo "🌐 Check your Railway dashboard for service URLs"
