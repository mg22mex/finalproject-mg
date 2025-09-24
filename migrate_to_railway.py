#!/usr/bin/env python3
"""
Migration script to help transition from Render to Railway
Updates configuration files and provides migration guidance
"""

import os
import json
import yaml
from datetime import datetime

def update_render_yaml_for_railway():
    """Update render.yaml to work with Railway deployment"""
    print("🔄 Updating render.yaml for Railway compatibility...")
    
    # Read current render.yaml
    with open('render.yaml', 'r') as f:
        render_config = yaml.safe_load(f)
    
    # Create Railway-compatible configuration
    railway_config = {
        'services': [
            {
                'name': 'autosell-backend',
                'source': './backend',
                'build': {'builder': 'nixpacks'},
                'variables': [
                    'PYTHON_VERSION=3.11.0',
                    'PORT=8000',
                    'DATABASE_URL=${{Postgres.DATABASE_URL}}',
                    'CORS_ORIGINS=https://autosell-frontend.railway.app,http://localhost:3000',
                    'ALLOWED_HOSTS=autosell-backend.railway.app,localhost,127.0.0.1'
                ],
                'healthcheck': {
                    'path': '/health',
                    'timeout': '30s',
                    'interval': '30s'
                }
            },
            {
                'name': 'autosell-frontend',
                'source': './frontend',
                'build': {'builder': 'nixpacks'},
                'variables': [
                    'VITE_API_URL=https://autosell-backend.railway.app'
                ],
                'deploy': {
                    'startCommand': 'npm run preview',
                    'healthcheckPath': '/'
                }
            },
            {
                'name': 'autosell-n8n',
                'source': './Dockerfile.n8n',
                'build': {'builder': 'dockerfile'},
                'variables': [
                    'N8N_BASIC_AUTH_ACTIVE=true',
                    'N8N_BASIC_AUTH_USER=admin',
                    'N8N_BASIC_AUTH_PASSWORD=AutosellN8n2025!',
                    'WEBHOOK_URL=https://autosell-n8n.railway.app',
                    'GENERIC_TIMEZONE=America/Mexico_City'
                ],
                'deploy': {
                    'healthcheckPath': '/healthz'
                }
            }
        ],
        'databases': [
            {
                'name': 'autosell-db',
                'type': 'postgresql',
                'version': '15'
            }
        ]
    }
    
    # Write Railway configuration
    with open('railway.yaml', 'w') as f:
        yaml.dump(railway_config, f, default_flow_style=False)
    
    print("✅ Created railway.yaml configuration")

def update_frontend_env():
    """Update frontend environment configuration for Railway"""
    print("🔄 Updating frontend environment for Railway...")
    
    # Update Vite configuration
    vite_config = """
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3000
  },
  preview: {
    host: '0.0.0.0',
    port: 3000
  }
})
"""
    
    with open('frontend/vite.config.ts', 'w') as f:
        f.write(vite_config)
    
    print("✅ Updated frontend Vite configuration")

def update_backend_cors():
    """Update backend CORS configuration for Railway"""
    print("🔄 Updating backend CORS for Railway...")
    
    # Read current main_fixed.py
    with open('backend/main_fixed.py', 'r') as f:
        content = f.read()
    
    # Update CORS origins for Railway
    updated_content = content.replace(
        'allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,https://finalproject-mg.onrender.com").split(",")',
        'allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,https://autosell-frontend.railway.app").split(",")'
    )
    
    with open('backend/main_fixed.py', 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated backend CORS configuration")

def create_railway_deployment_script():
    """Create deployment script for Railway"""
    print("🔄 Creating Railway deployment script...")
    
    deployment_script = """#!/bin/bash
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
"""
    
    with open('deploy_railway.sh', 'w') as f:
        f.write(deployment_script)
    
    # Make script executable
    os.chmod('deploy_railway.sh', 0o755)
    
    print("✅ Created Railway deployment script")

def generate_migration_summary():
    """Generate migration summary"""
    print("📋 Generating migration summary...")
    
    summary = f"""
# 🚀 Autosell.mx Railway Migration Summary

## Migration Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ✅ Files Updated:
- `railway.yaml` - Railway deployment configuration
- `frontend/vite.config.ts` - Updated for Railway hosting
- `backend/main_fixed.py` - Updated CORS for Railway domains
- `deploy_railway.sh` - Railway deployment script

## 🔧 Next Steps:
1. Install Railway CLI: `npm install -g @railway/cli`
2. Run deployment script: `./deploy_railway.sh`
3. Configure environment variables in Railway dashboard
4. Test all services
5. Update domain references

## 🌐 Expected Railway URLs:
- Backend: `https://autosell-backend-production.up.railway.app`
- Frontend: `https://autosell-frontend-production.up.railway.app`
- n8n: `https://autosell-n8n-production.up.railway.app`

## 💰 Cost Benefits:
- Railway: $5 credit monthly (no time limits)
- Render: 30 days free, then $7/month
- Savings: $7/month + no expiration

## 🎯 Migration Benefits:
✅ No time limits on free tier
✅ Better performance than Render
✅ Easier deployment process
✅ Same features as Render
✅ PostgreSQL included
✅ Custom domains supported
"""
    
    with open('RAILWAY_MIGRATION_SUMMARY.md', 'w') as f:
        f.write(summary)
    
    print("✅ Generated migration summary")

def main():
    """Main migration function"""
    print("🚀 Autosell.mx Railway Migration Script")
    print("=" * 50)
    print(f"⏰ Migration started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Update configuration files
    update_render_yaml_for_railway()
    update_frontend_env()
    update_backend_cors()
    create_railway_deployment_script()
    generate_migration_summary()
    
    print()
    print("🎉 Railway Migration Preparation Complete!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Install Railway CLI: npm install -g @railway/cli")
    print("2. Run: ./deploy_railway.sh")
    print("3. Configure environment variables in Railway dashboard")
    print("4. Test all services")
    print("5. Update domain references")
    print()
    print("💰 Cost Benefits:")
    print("- Railway: $5 credit monthly (no time limits)")
    print("- Render: 30 days free, then $7/month")
    print("- Savings: $7/month + no expiration")

if __name__ == "__main__":
    main()
