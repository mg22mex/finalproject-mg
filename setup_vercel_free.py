#!/usr/bin/env python3
"""
Setup script for Vercel free deployment
Configures the project for Vercel's free tier
"""

import os
import json
import yaml
from datetime import datetime

def create_vercel_config():
    """Create Vercel configuration files"""
    print("🔄 Creating Vercel configuration...")
    
    # Create vercel.json for backend
    vercel_config = {
        "functions": {
            "api/index.py": {
                "runtime": "python3.9"
            }
        },
        "routes": [
            {
                "src": "/(.*)",
                "dest": "api/index.py"
            }
        ],
        "env": {
            "DATABASE_URL": "@database_url",
            "CORS_ORIGINS": "@cors_origins",
            "ALLOWED_HOSTS": "@allowed_hosts"
        }
    }
    
    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Created vercel.json")

def create_api_index():
    """Create API index file for Vercel"""
    print("🔄 Creating API index file...")
    
    api_content = '''from fastapi import FastAPI
from mangum import Mangum
import os
from app.database import get_db
from app.models import *
from app.api.endpoints import *

app = FastAPI()

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Autosell.mx API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "{{ $now }}"}

# Vercel handler
handler = Mangum(app)
'''
    
    os.makedirs('api', exist_ok=True)
    with open('api/index.py', 'w') as f:
        f.write(api_content)
    
    print("✅ Created api/index.py")

def create_frontend_vercel_config():
    """Create Vercel configuration for frontend"""
    print("🔄 Creating frontend Vercel configuration...")
    
    frontend_config = {
        "buildCommand": "npm run build",
        "outputDirectory": "dist",
        "installCommand": "npm install",
        "framework": "vite",
        "env": {
            "VITE_API_URL": "@vite_api_url"
        }
    }
    
    with open('frontend/vercel.json', 'w') as f:
        json.dump(frontend_config, f, indent=2)
    
    print("✅ Created frontend/vercel.json")

def create_supabase_setup():
    """Create Supabase setup instructions"""
    print("🔄 Creating Supabase setup instructions...")
    
    supabase_setup = '''# 🗄️ Supabase Database Setup

## Step 1: Create Supabase Account
1. Go to: https://supabase.com
2. Sign up with GitHub
3. No credit card required!

## Step 2: Create New Project
1. Click "New Project"
2. Choose organization
3. Enter project name: autosell-mx
4. Choose region: US East
5. Click "Create new project"

## Step 3: Get Database URL
1. Go to Settings → Database
2. Copy "Connection string"
3. Update backend environment variables

## Step 4: Run Database Migrations
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize project
supabase init

# Push database schema
supabase db push
```

## Step 5: Test Database Connection
```bash
# Test connection
supabase db ping
```
'''
    
    with open('SUPABASE_SETUP.md', 'w') as f:
        f.write(supabase_setup)
    
    print("✅ Created Supabase setup instructions")

def create_n8n_local_setup():
    """Create n8n local setup instructions"""
    print("🔄 Creating n8n local setup instructions...")
    
    n8n_setup = '''# 🤖 n8n Local Setup (Free)

## Step 1: Install n8n
```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

## Step 2: Access n8n Dashboard
- URL: http://localhost:5678
- Username: admin
- Password: AutosellN8n2025!

## Step 3: Configure Webhooks
Update webhook URLs in n8n workflows:
- Facebook: https://autosell-backend.vercel.app/api/facebook/post
- Sheets: https://autosell-backend.vercel.app/api/sheets/sync
- Drive: https://autosell-backend.vercel.app/api/drive/upload

## Step 4: Import Workflows
1. Go to n8n dashboard
2. Click "Import from File"
3. Upload JSON files from n8n_workflows/ folder

## Step 5: Test Workflows
```bash
# Test webhook connectivity
curl -X POST http://localhost:5678/webhook/facebook-post \\
  -H "Content-Type: application/json" \\
  -d '{"message": "Test post"}'
```
'''
    
    with open('N8N_LOCAL_SETUP.md', 'w') as f:
        f.write(n8n_setup)
    
    print("✅ Created n8n local setup instructions")

def create_deployment_script():
    """Create deployment script for Vercel"""
    print("🔄 Creating Vercel deployment script...")
    
    deployment_script = '''#!/bin/bash
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
'''
    
    with open('deploy_vercel_free.sh', 'w') as f:
        f.write(deployment_script)
    
    # Make script executable
    os.chmod('deploy_vercel_free.sh', 0o755)
    
    print("✅ Created Vercel deployment script")

def generate_setup_summary():
    """Generate setup summary"""
    print("📋 Generating setup summary...")
    
    summary = f"""
# 🆓 Vercel Free Setup Summary

## Setup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ✅ Files Created:
- `vercel.json` - Backend Vercel configuration
- `api/index.py` - Vercel API handler
- `frontend/vercel.json` - Frontend Vercel configuration
- `SUPABASE_SETUP.md` - Database setup instructions
- `N8N_LOCAL_SETUP.md` - n8n local setup instructions
- `deploy_vercel_free.sh` - Deployment script

## 🚀 Next Steps:
1. Install Vercel CLI: `npm install -g vercel`
2. Run deployment script: `./deploy_vercel_free.sh`
3. Setup Supabase database (free)
4. Install n8n locally: `npm install -g n8n`
5. Test all services

## 🌐 Expected URLs:
- Frontend: `https://autosell-frontend.vercel.app`
- Backend: `https://autosell-backend.vercel.app`
- n8n: `http://localhost:5678` (local)

## 💰 Cost Breakdown:
- Vercel Frontend: FREE
- Vercel Backend: FREE
- Supabase Database: FREE
- n8n (Local): FREE
- Total: $0/month FOREVER

## 🎯 Benefits:
✅ No time limits
✅ No credit card required
✅ No payment surprises
✅ Automatic deployments
✅ Custom domains included
✅ SSL certificates included
✅ Global CDN
✅ Serverless scaling
"""
    
    with open('VERCEL_FREE_SUMMARY.md', 'w') as f:
        f.write(summary)
    
    print("✅ Generated setup summary")

def main():
    """Main setup function"""
    print("🆓 Autosell.mx Vercel Free Setup")
    print("=" * 50)
    print(f"⏰ Setup started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create configuration files
    create_vercel_config()
    create_api_index()
    create_frontend_vercel_config()
    create_supabase_setup()
    create_n8n_local_setup()
    create_deployment_script()
    generate_setup_summary()
    
    print()
    print("🎉 Vercel Free Setup Complete!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Install Vercel CLI: npm install -g vercel")
    print("2. Run: ./deploy_vercel_free.sh")
    print("3. Setup Supabase database (free)")
    print("4. Install n8n locally: npm install -g n8n")
    print("5. Test all services")
    print()
    print("💰 Total Cost: $0/month FOREVER!")
    print("✅ No time limits, no credit card required!")

if __name__ == "__main__":
    main()
