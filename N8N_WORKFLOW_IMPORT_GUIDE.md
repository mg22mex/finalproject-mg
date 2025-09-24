# 🤖 n8n Workflow Import Guide

## 🎯 **How to Import Your Workflows**

### **Step 1: Access n8n Dashboard**
1. Open your browser
2. Go to: http://localhost:5678
3. Login with: admin / AutosellN8n2025!

### **Step 2: Import Workflows**

#### **2.1 Import Facebook Automation**
1. Click **"Import from File"**
2. Select: `n8n_workflows/facebook_automation.json`
3. Click **"Import"**

#### **2.2 Import Google Sheets Sync**
1. Click **"Import from File"**
2. Select: `n8n_workflows/google_sheets_sync.json`
3. Click **"Import"**

#### **2.3 Import Vehicle Processing**
1. Click **"Import from File"**
2. Select: `n8n_workflows/vehicle_processing.json`
3. Click **"Import"**

### **Step 3: Configure Credentials**

#### **3.1 Google Sheets Credentials**
1. Go to **Settings** → **Credentials**
2. Click **"Add Credential"**
3. Select **"Google Sheets OAuth2 API"**
4. Follow the OAuth setup process

#### **3.2 Facebook App Credentials**
1. Go to **Settings** → **Credentials**
2. Click **"Add Credential"**
3. Select **"Facebook Graph API"**
4. Enter your App ID and App Secret

### **Step 4: Test Workflows**

#### **4.1 Test Facebook Posting**
```bash
curl -X POST http://localhost:5678/webhook/facebook-post \
  -H "Content-Type: application/json" \
  -d '{"account_type": "auto", "message": "Test post from Autosell.mx!"}'
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

## 🎉 **Your Workflows Are Ready!**

### **What Each Workflow Does:**

1. **Facebook Automation**: Auto-posts to Facebook when triggered
2. **Google Sheets Sync**: Syncs vehicle data to Google Sheets
3. **Vehicle Processing**: Complete vehicle processing pipeline

### **Webhook URLs:**
- **Facebook Posting**: http://localhost:5678/webhook/facebook-post
- **Google Sheets Sync**: http://localhost:5678/webhook/sync-sheets
- **Vehicle Processing**: http://localhost:5678/webhook/process-vehicle

## 🚀 **Next Steps:**

1. **Import all workflows** into n8n
2. **Configure credentials** for Google and Facebook
3. **Test each workflow** with the curl commands
4. **Connect to your backend** for full automation

**Your n8n automation system is ready to power Autosell.mx!** 🎉
