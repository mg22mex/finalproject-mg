# 🚀 n8n Setup Guide for Autosell.mx

## 📋 **Quick Access**
- **n8n Dashboard**: https://autosell-n8n.onrender.com
- **Username**: `admin`
- **Password**: `AutosellN8n2025!`

## 🎯 **Step-by-Step Setup**

### **Step 1: Access n8n Dashboard**
1. Go to: https://autosell-n8n.onrender.com
2. Login with credentials above
3. You'll see the n8n workflow editor

### **Step 2: Import Workflows**

#### **2.1 Facebook Automation Workflow**
1. Click **"Import from File"**
2. Upload: `n8n_workflows/facebook_automation.json`
3. **Configure Credentials**:
   - Go to **Settings** → **Credentials**
   - Add **Facebook App** credentials
   - Test connection

#### **2.2 Google Sheets Sync Workflow**
1. Click **"Import from File"**
2. Upload: `n8n_workflows/google_sheets_sync.json`
3. **Configure Credentials**:
   - Go to **Settings** → **Credentials**
   - Add **Google Sheets** OAuth2 credentials
   - Test connection

#### **2.3 Google Drive Photos Workflow**
1. Click **"Import from File"**
2. Upload: `n8n_workflows/google_drive_photos.json`
3. **Configure Credentials**:
   - Go to **Settings** → **Credentials**
   - Add **Google Drive** OAuth2 credentials
   - Test connection

#### **2.4 Vehicle Processing Pipeline**
1. Click **"Import from File"**
2. Upload: `n8n_workflows/vehicle_processing.json`
3. **No additional credentials needed** (uses webhooks)

### **Step 3: Configure Webhooks**

#### **3.1 Get Webhook URLs**
After importing workflows, n8n will provide webhook URLs:

- **Facebook Posting**: `https://autosell-n8n.onrender.com/webhook/facebook-post`
- **Google Sheets Sync**: `https://autosell-n8n.onrender.com/webhook/sync-sheets`
- **Google Drive Upload**: `https://autosell-n8n.onrender.com/webhook/upload-photos`
- **Vehicle Processing**: `https://autosell-n8n.onrender.com/webhook/process-vehicle`

#### **3.2 Update Backend Configuration**
Add these webhook URLs to your backend environment variables:

```bash
# In Render backend service environment variables:
WEBHOOK_FACEBOOK_POST=https://autosell-n8n.onrender.com/webhook/facebook-post
WEBHOOK_SHEETS_SYNC=https://autosell-n8n.onrender.com/webhook/sync-sheets
WEBHOOK_DRIVE_UPLOAD=https://autosell-n8n.onrender.com/webhook/upload-photos
WEBHOOK_VEHICLE_PROCESS=https://autosell-n8n.onrender.com/webhook/process-vehicle
```

### **Step 4: Test Workflows**

#### **4.1 Test Facebook Posting**
```bash
curl -X POST https://autosell-n8n.onrender.com/webhook/facebook-post \
  -H "Content-Type: application/json" \
  -d '{
    "account_type": "auto",
    "message": "🚗 Test post from Autosell.mx automation!",
    "access_token": "YOUR_FACEBOOK_ACCESS_TOKEN"
  }'
```

#### **4.2 Test Google Sheets Sync**
```bash
curl -X POST https://autosell-n8n.onrender.com/webhook/sync-sheets \
  -H "Content-Type: application/json" \
  -d '{
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
    "vehicle_id": "123"
  }'
```

#### **4.3 Test Vehicle Processing**
```bash
curl -X POST https://autosell-n8n.onrender.com/webhook/process-vehicle \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": "123"
  }'
```

## 🔧 **Workflow Descriptions**

### **🤖 Facebook Automation Workflow**
- **Trigger**: Webhook call
- **Process**: 
  1. Receives vehicle data
  2. Checks account type (auto/manual)
  3. Gets Facebook account credentials
  4. Posts to Facebook
  5. Logs activity
- **Use Case**: Automatic Facebook posting when new vehicles are added

### **📊 Google Sheets Sync Workflow**
- **Trigger**: Webhook call
- **Process**:
  1. Gets vehicle data from backend
  2. Updates Google Sheets with vehicle info
  3. Updates sync status in backend
- **Use Case**: Keep inventory synchronized with Google Sheets

### **📸 Google Drive Photos Workflow**
- **Trigger**: Webhook call
- **Process**:
  1. Receives photo upload request
  2. Uploads to Google Drive
  3. Updates vehicle photo records
  4. Processes photos (resize, optimize)
- **Use Case**: Automatic photo management and optimization

### **🚗 Vehicle Processing Pipeline**
- **Trigger**: Webhook call
- **Process**:
  1. Gets vehicle details
  2. Checks if vehicle is active
  3. Syncs to Google Sheets
  4. Posts to Facebook
  5. Marks processing complete
- **Use Case**: Complete vehicle processing automation

## 🔐 **Required Credentials**

### **Facebook App Credentials**
- **App ID**: From Facebook Developer Console
- **App Secret**: From Facebook Developer Console
- **Access Token**: From OAuth flow

### **Google Services Credentials**
- **Google Sheets API**: OAuth2 credentials
- **Google Drive API**: OAuth2 credentials
- **Service Account**: For backend integration

## 📱 **Integration Points**

### **Backend Integration**
Your FastAPI backend can trigger n8n workflows by calling webhooks:

```python
# Example: Trigger Facebook posting
import requests

def trigger_facebook_post(vehicle_data):
    webhook_url = "https://autosell-n8n.onrender.com/webhook/facebook-post"
    response = requests.post(webhook_url, json=vehicle_data)
    return response.json()
```

### **Frontend Integration**
Your React frontend can trigger workflows through the backend API:

```typescript
// Example: Process new vehicle
const processVehicle = async (vehicleId: string) => {
  const response = await fetch('/api/vehicles/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ vehicle_id: vehicleId })
  });
  return response.json();
};
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Webhook Not Responding**
   - Check n8n service status
   - Verify webhook URL is correct
   - Check n8n logs in Render dashboard

2. **Authentication Errors**
   - Verify OAuth2 credentials are configured
   - Check token expiration
   - Re-authenticate if needed

3. **Workflow Execution Failed**
   - Check n8n execution logs
   - Verify all required fields are provided
   - Test individual nodes

### **Monitoring**
- **n8n Dashboard**: Monitor workflow executions
- **Render Logs**: Check service logs
- **Backend Logs**: Monitor API calls

## 🎉 **Success Indicators**

✅ **All workflows imported successfully**
✅ **All credentials configured and tested**
✅ **Webhook URLs accessible**
✅ **Test executions successful**
✅ **Backend integration working**

## 📞 **Support**

If you encounter issues:
1. Check n8n execution logs
2. Verify webhook URLs
3. Test individual workflow nodes
4. Check Render service status

**Your n8n automation system is now ready to power Autosell.mx!** 🚀
