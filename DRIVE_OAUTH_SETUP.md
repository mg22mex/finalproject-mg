# Google Drive OAuth2 Setup Guide

## Using Your Existing OAuth2 Credentials

Since you already have OAuth2 credentials set up for n8n, we can use the same credentials for Google Drive integration.

## Quick Setup

### Option 1: Use Existing Credentials (Recommended)

1. **Copy your existing OAuth2 credentials:**
   ```bash
   # If you have the credentials file from n8n setup
   cp /path/to/your/n8n/credentials.json backend/drive_credentials.json
   ```

2. **Run the setup script:**
   ```bash
   cd backend
   ./setup_drive_credentials.sh
   ```

### Option 2: Download from Google Cloud Console

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Select your existing project (the same one you use for n8n)

2. **Navigate to Credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Find your existing OAuth 2.0 Client ID (the one you use for n8n)

3. **Download Credentials:**
   - Click on your existing OAuth 2.0 Client ID
   - Click "Download JSON"
   - Save as `backend/drive_credentials.json`

4. **Enable Google Drive API:**
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

5. **Run the setup:**
   ```bash
   cd backend
   ./setup_drive_credentials.sh
   ```

## First-Time Authentication

When you run the setup script for the first time, it will:

1. **Open a browser window** for Google authentication
2. **Ask you to sign in** with your Google account
3. **Request permissions** for Google Drive access
4. **Save the token** to `drive_token.json`

## Testing the Integration

After setup, test the Drive integration:

```bash
# Test the connection
curl -X POST http://localhost:8000/drive/test-connection

# Expected response:
# {"success": true, "message": "Google Drive API connection successful"}
```

## Using the Drive Integration

### Frontend Workflow
1. Navigate to a vehicle detail page
2. Click "Create Drive Folder"
3. Upload photos to the generated Drive folder
4. Click "Sync Photos" to import to system

### API Endpoints
- `POST /drive/create-folder/{vehicle_id}` - Create Drive folder
- `POST /drive/sync-photos/{vehicle_id}` - Sync photos from Drive
- `GET /drive/vehicle/{vehicle_id}/folder-info` - Get folder information

## Troubleshooting

### Common Issues

1. **"Google Drive API connection failed"**
   - Check if `drive_credentials.json` exists
   - Verify Google Drive API is enabled in Google Cloud Console
   - Run the setup script again

2. **"Failed to create Drive folder"**
   - Check OAuth permissions
   - Verify the credentials file is valid
   - Check Google Cloud Console for API quotas

3. **"Photos not syncing"**
   - Verify folder has photos
   - Check file permissions in Drive
   - Ensure photos are image files

### Debug Commands

```bash
# Check if credentials exist
ls -la backend/drive_credentials.json
ls -la backend/drive_token.json

# Test authentication
cd backend
python configure_drive_oauth.py

# Check API endpoints
curl http://localhost:8000/drive/test-connection -X POST
```

## Security Notes

- **Never commit** `drive_credentials.json` or `drive_token.json` to version control
- **Use environment variables** for production deployment
- **Rotate credentials** regularly for security
- **Monitor API usage** in Google Cloud Console

## Next Steps

1. **Complete OAuth2 setup** using the guide above
2. **Test Drive integration** with a sample vehicle
3. **Configure n8n workflows** for automated photo syncing
4. **Deploy to production** with proper security measures

## Support

If you encounter issues:
- Check the troubleshooting section above
- Verify your Google Cloud Console settings
- Test with the provided debug commands
- Review the Google Drive API documentation
