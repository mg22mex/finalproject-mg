# 🤖 Complete n8n Setup Guide for Autosell.mx

## 🎯 **Your n8n Workflows Are Ready!**

### **✅ What We've Created:**

1. **🤖 Facebook Automation Workflow**
   - Auto-posts to Facebook when triggered
   - Handles multiple Facebook accounts
   - Logs activity to backend

2. **📊 Google Sheets Sync Workflow**
   - Syncs vehicle data to Google Sheets
   - Updates inventory automatically
   - Tracks sync status

3. **🚗 Vehicle Processing Workflow**
   - Complete vehicle processing pipeline
   - Syncs to Google Sheets
   - Posts to Facebook
   - Marks processing complete

## 🚀 **Step-by-Step Setup:**

### **Step 1: Access n8n Dashboard**
1. **Open your browser**
2. **Go to**: http://localhost:5678
3. **Login with**:
   - **Username**: `admin`
   - **Password**: `AutosellN8n2025!`

### **Step 2: Import Workflows**

#### **2.1 Import Facebook Automation**
1. Click **"Import from File"** (or drag & drop)
2. Select: `n8n_workflows/facebook_automation.json`
3. Click **"Import"**
4. Click **"Save"** to activate

#### **2.2 Import Google Sheets Sync**
1. Click **"Import from File"**
2. Select: `n8n_workflows/google_sheets_sync.json`
3. Click **"Import"**
4. Click **"Save"** to activate

#### **2.3 Import Vehicle Processing**
1. Click **"Import from File"**
2. Select: `n8n_workflows/vehicle_processing.json`
3. Click **"Import"**
4. Click **"Save"** to activate

### **Step 3: Configure Credentials**

#### **3.1 Google Sheets Credentials**
1. Go to **Settings** → **Credentials**
2. Click **"Add Credential"**
3. Select **"Google Sheets OAuth2 API"**
4. Follow the OAuth setup process:
   - Authorize with Google
   - Grant permissions
   - Save credentials

#### **3.2 Facebook App Credentials**
1. Go to **Settings** → **Credentials**
2. Click **"Add Credential"**
3. Select **"Facebook Graph API"**
4. Enter your credentials:
   - **App ID**: From Facebook Developer Console
   - **App Secret**: From Facebook Developer Console

### **Step 4: Test Your Workflows**

#### **4.1 Test Facebook Posting**
```bash
curl -X POST http://localhost:5678/webhook/facebook-post \
  -H "Content-Type: application/json" \
  -d '{"account_type": "auto", "message": "🚗 Test post from Autosell.mx!"}'
```

#### **4.2 Test Google Sheets Sync**
```bash
curl -X POST http://localhost:5678/webhook/sync-sheets \
  -H "Content-Type: application/json" \
  -d '{"spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"}'
```

#### **4.3 Test Vehicle Processing**
```bash
curl -X POST http://localhost:5678/webhook/process-vehicle \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "123"}'
```

## 🎯 **What Each Workflow Does:**

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

### **🚗 Vehicle Processing Pipeline**
- **Trigger**: Webhook call
- **Process**:
  1. Gets vehicle details
  2. Checks if vehicle is active
  3. Syncs to Google Sheets
  4. Posts to Facebook
  5. Marks processing complete
- **Use Case**: Complete vehicle processing automation

## 🔧 **Webhook URLs:**

After importing workflows, you'll have these webhook URLs:

- **Facebook Posting**: http://localhost:5678/webhook/facebook-post
- **Google Sheets Sync**: http://localhost:5678/webhook/sync-sheets
- **Vehicle Processing**: http://localhost:5678/webhook/process-vehicle

## 🎉 **Integration with Your Backend:**

### **Backend Integration Points:**
Your FastAPI backend can trigger n8n workflows by calling webhooks:

```python
# Example: Trigger Facebook posting
import requests

def trigger_facebook_post(vehicle_data):
    webhook_url = "http://localhost:5678/webhook/facebook-post"
    response = requests.post(webhook_url, json=vehicle_data)
    return response.json()
```

### **Frontend Integration:**
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

## 🚨 **Troubleshooting:**

### **Common Issues:**

1. **Webhook Not Responding**
   - Check n8n service status
   - Verify webhook URL is correct
   - Check n8n logs

2. **Authentication Errors**
   - Verify OAuth2 credentials are configured
   - Check token expiration
   - Re-authenticate if needed

3. **Workflow Execution Failed**
   - Check n8n execution logs
   - Verify all required fields are provided
   - Test individual nodes

### **Monitoring:**
- **n8n Dashboard**: Monitor workflow executions
- **Execution Logs**: Check individual node results
- **Backend Logs**: Monitor API calls

## 🎯 **Success Indicators:**

✅ **All workflows imported successfully**
✅ **All credentials configured and tested**
✅ **Webhook URLs accessible**
✅ **Test executions successful**
✅ **Backend integration working**

## 🚀 **Your Automation System is Ready!**

**Your n8n automation system is now ready to power Autosell.mx!** 🎉

### **What You Can Do Now:**
- ✅ **Automated Facebook posting** when vehicles are added
- ✅ **Google Sheets synchronization** for inventory management
- ✅ **Complete vehicle processing** pipeline
- ✅ **Multi-account Facebook** integration
- ✅ **Real-time automation** workflows

**Your free hosting setup with n8n automation is complete and ready to use!** 🚀
