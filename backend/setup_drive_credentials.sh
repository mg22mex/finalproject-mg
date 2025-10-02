#!/bin/bash

echo "🔧 Google Drive OAuth2 Setup for Autosell.mx"
echo "============================================="

# Check if we're in the right directory
if [ ! -f "main_fixed.py" ]; then
    echo "❌ Please run this script from the backend directory"
    exit 1
fi

echo "📋 Setting up Google Drive OAuth2 credentials..."
echo ""

# Check if credentials file exists
if [ -f "drive_credentials.json" ]; then
    echo "✅ Found drive_credentials.json"
else
    echo "❌ drive_credentials.json not found"
    echo ""
    echo "📋 To get your OAuth2 credentials:"
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Select your project (the same one you use for n8n)"
    echo "3. Go to 'APIs & Services' > 'Credentials'"
    echo "4. Find your existing OAuth 2.0 Client ID (the one you use for n8n)"
    echo "5. Click on it and download the JSON file"
    echo "6. Save it as 'drive_credentials.json' in this directory"
    echo "7. Run this script again"
    echo ""
    echo "💡 If you need to create new credentials:"
    echo "   - Click 'Create Credentials' > 'OAuth 2.0 Client IDs'"
    echo "   - Choose 'Desktop application'"
    echo "   - Download the JSON file"
    exit 1
fi

# Check if token file exists
if [ -f "drive_token.json" ]; then
    echo "✅ Found drive_token.json (already authenticated)"
    echo "🎉 OAuth2 setup is complete!"
else
    echo "🔐 First-time authentication required"
    echo "This will open a browser window for Google authentication..."
    echo ""
    read -p "Press Enter to continue with authentication..."
    
    # Run the authentication
    echo "🔄 Starting OAuth2 authentication..."
    python configure_drive_oauth.py
fi

echo ""
echo "✅ Google Drive OAuth2 setup complete!"
echo "🚀 You can now use the Drive integration features"
