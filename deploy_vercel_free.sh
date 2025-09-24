#!/bin/bash
# Vercel Free Deployment Script for Autosell.mx

echo "🚀 Deploying Autosell.mx to Vercel (FREE FOREVER)..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Login to Vercel
echo "🔐 Logging into Vercel..."
vercel login

# Deploy frontend
echo "🎨 Deploying frontend..."
cd frontend
vercel --prod

# Deploy backend
echo "🔧 Deploying backend..."
cd ../backend
vercel --prod

echo "✅ Deployment complete!"
echo "🌐 Check your Vercel dashboard for service URLs"
echo "💰 Total cost: $0/month FOREVER!"
