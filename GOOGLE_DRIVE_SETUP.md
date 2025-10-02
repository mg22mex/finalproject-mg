# Google Drive Integration Setup Guide

## Overview
This guide explains how to set up Google Drive integration for the Autosell.mx system, allowing seamless photo management through Drive folders.

## Features Implemented

### ✅ Backend API Endpoints
- `POST /drive/create-folder/{vehicle_id}` - Create Drive folder for vehicle
- `GET /drive/folder/{folder_id}/files` - List files in Drive folder
- `POST /drive/sync-photos/{vehicle_id}` - Sync photos from Drive to system
- `GET /drive/vehicle/{vehicle_id}/folder-info` - Get vehicle folder info
- `POST /drive/test-connection` - Test Drive API connection

### ✅ Database Schema
- Added `drive_folder_id` and `drive_folder_url` to vehicles table
- Added `drive_file_id` and `drive_url` to photos table
- Created `drive_files` tracking table
- Added proper indexes for performance

### ✅ Frontend Components
- `DriveFolderManager` component for folder management
- Enhanced `VehicleDetail` page with Drive integration
- Real-time folder creation and photo syncing

## Setup Instructions

### 1. Google Cloud Console Setup

1. **Create a Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Note your project ID

2. **Enable Google Drive API**
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Download the JSON file

4. **Configure OAuth Consent Screen**
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in required information
   - Add your email to test users

### 2. Backend Configuration

1. **Copy Credentials File**
   ```bash
   cp /path/to/your/credentials.json backend/drive_credentials.json
   ```

2. **Set Environment Variables**
   ```bash
   export GOOGLE_DRIVE_PARENT_FOLDER_ID="your-parent-folder-id"
   export DATABASE_URL="postgresql://postgres:password@localhost:5434/autosell_db"
   ```

3. **Create Parent Folder (Optional)**
   - Create a folder in Google Drive for all vehicle folders
   - Copy the folder ID from the URL
   - Set as `GOOGLE_DRIVE_PARENT_FOLDER_ID`

### 3. First-Time Authentication

1. **Start Backend Server**
   ```bash
   cd backend
   DATABASE_URL="postgresql://postgres:password@localhost:5434/autosell_db" python main_fixed.py
   ```

2. **Test Connection**
   ```bash
   curl -X POST http://localhost:8000/drive/test-connection
   ```

3. **Complete OAuth Flow**
   - The first API call will open a browser window
   - Sign in with your Google account
   - Grant permissions to the application
   - A `drive_token.json` file will be created

### 4. Frontend Integration

The frontend is already configured with Drive integration components:

- **VehicleDetail Page**: Shows Drive folder management
- **DriveFolderManager Component**: Handles folder creation and photo syncing
- **Real-time Updates**: Folder status updates automatically

## Usage Workflow

### Option 1: Frontend Workflow
1. Navigate to a vehicle detail page
2. Click "Create Drive Folder" 
3. Upload photos to the generated Drive folder
4. Click "Sync Photos" to import to system
5. Photos appear in the vehicle's photo gallery

### Option 2: Spreadsheet Workflow
1. Add vehicle to Google Sheets
2. n8n workflow creates Drive folder automatically
3. Upload photos to Drive folder
4. n8n syncs photos to system
5. Vehicle appears in frontend with photos

## n8n Workflow Enhancement

### Drive Photo Sync Workflow
```json
{
  "nodes": [
    {
      "name": "Monitor Drive Changes",
      "type": "n8n-nodes-base.googleDrive",
      "parameters": {
        "operation": "watch",
        "folderId": "{{$json.drive_folder_id}}"
      }
    },
    {
      "name": "Download New Photos",
      "type": "n8n-nodes-base.googleDrive",
      "parameters": {
        "operation": "download",
        "fileId": "{{$json.id}}"
      }
    },
    {
      "name": "Upload to Backend",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "method": "POST",
        "url": "http://localhost:8000/photos/upload/{{$json.vehicle_id}}",
        "body": "{{$json.file_data}}"
      }
    }
  ]
}
```

## API Endpoints Reference

### Create Drive Folder
```bash
POST /drive/create-folder/{vehicle_id}
```
**Response:**
```json
{
  "success": true,
  "vehicle_id": 123,
  "folder_id": "1ABC123DEF456",
  "folder_name": "Vehicle-123-Honda-Civic",
  "folder_url": "https://drive.google.com/drive/folders/1ABC123DEF456"
}
```

### Sync Photos
```bash
POST /drive/sync-photos/{vehicle_id}
```
**Response:**
```json
{
  "success": true,
  "vehicle_id": 123,
  "synced_photos": 5,
  "photos": [...]
}
```

### Get Folder Info
```bash
GET /drive/vehicle/{vehicle_id}/folder-info
```
**Response:**
```json
{
  "success": true,
  "vehicle_id": 123,
  "has_folder": true,
  "folder_id": "1ABC123DEF456",
  "folder_url": "https://drive.google.com/drive/folders/1ABC123DEF456",
  "files": [...],
  "file_count": 5
}
```

## Troubleshooting

### Common Issues

1. **"Google Drive API connection failed"**
   - Check if `drive_credentials.json` exists
   - Verify OAuth consent screen is configured
   - Complete first-time authentication flow

2. **"Failed to create Drive folder"**
   - Check if parent folder ID is correct
   - Verify Google Drive API is enabled
   - Check OAuth permissions

3. **"Photos not syncing"**
   - Verify folder has photos
   - Check file permissions in Drive
   - Ensure photos are image files

### Debug Commands

```bash
# Test Drive connection
curl -X POST http://localhost:8000/drive/test-connection

# Check vehicle folder info
curl http://localhost:8000/drive/vehicle/1/folder-info

# List folder files
curl http://localhost:8000/drive/folder/FOLDER_ID/files
```

## Security Considerations

1. **Credentials Security**
   - Never commit `drive_credentials.json` to version control
   - Use environment variables for sensitive data
   - Rotate credentials regularly

2. **Folder Permissions**
   - Folders are created with "anyone with link" access
   - Consider using more restrictive permissions for production
   - Monitor folder access logs

3. **Data Privacy**
   - Photos are stored in your Google Drive
   - Ensure compliance with data protection regulations
   - Consider encryption for sensitive data

## Next Steps

1. **Complete Google Cloud Setup** - Follow the setup instructions above
2. **Test Drive Integration** - Create a test vehicle and folder
3. **Configure n8n Workflows** - Set up automated photo syncing
4. **Production Deployment** - Deploy with proper security measures

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Google Drive API documentation
- Test with the provided debug commands
