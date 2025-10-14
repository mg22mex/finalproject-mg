# 🤖 n8n Workflows Documentation

## 🎯 **Overview**

n8n workflows provide the automation backbone for Autosell.mx, handling Google Sheets integration, Facebook posting, and complete vehicle processing pipelines. Currently operational with Google Sheets sync workflow successfully importing 133 vehicles.

## 📁 **Essential Workflows (2 Active)**

### **0. Google Sheets to Backend Sync (ACTIVE)**
**File**: `google_sheets_sync.json`
**Purpose**: Import vehicles from Google Sheets to backend
**Status**: ✅ **ACTIVE - Successfully importing 133 vehicles**
**Trigger**: Manual execution
**Features**:
- Manual trigger execution
- Google Sheets data extraction
- AI-powered data validation and cleaning
- Backend API integration
- Error handling and retry logic
- Comprehensive logging

### **1. Facebook Automation (DEACTIVATED)**
**File**: `facebook_automation_fixed.json`
**Purpose**: Facebook posting automation
**Status**: ⚠️ **DEACTIVATED - Facebook posting node disabled**
**Features**:
- Facebook posting capabilities
- Currently deactivated due to Marketplace posting complexity
- Ready for future activation when needed

## 🚀 **Current System Status**

### **Active Workflows**
- **Google Sheets Sync**: ✅ Operational, importing 133 vehicles
- **Backend API**: ✅ Connected to backend on port 8001
- **Data Processing**: ✅ AI-powered validation working
- **Error Handling**: ✅ Comprehensive logging active

### **Deactivated Components**
- **Facebook Posting**: ⚠️ Deactivated due to Marketplace posting complexity
- **Automatic Triggers**: ⚠️ Disabled to prevent duplicate imports

### **Configuration Requirements**
- **Google Sheets**: OAuth2 credentials configured
- **Sheet ID**: Connected to working Google Sheet
- **Range**: `A2:I1000` (adjust as needed)
- **Backend API**: Connected to backend on port 8001

## 📊 **Workflow Performance**

### **Google Sheets Sync Results**
- **Total Vehicles Imported**: 133
- **Success Rate**: 100%
- **Data Validation**: AI-powered cleaning active
- **Error Handling**: Comprehensive logging
- **Backend Integration**: Seamless API connection

### **System Monitoring**
- **n8n Status**: ✅ Running on port 5678
- **Backend Status**: ✅ Running on port 8001
- **Frontend Status**: ✅ Running on port 3002
- **Database Status**: ✅ 133 vehicles stored

## 🔧 **Troubleshooting Guide**

### **Common Issues**
1. **Connection Refused**: Ensure backend is running on port 8001
2. **JSON Expression Greyed Out**: Check AI Data Processor configuration
3. **Facebook Posting Fails**: Node is deactivated, can be reactivated when needed
4. **Duplicate Imports**: Manual execution prevents automatic duplicates

### **Manual Execution**
- **Trigger**: Manual execution only
- **Frequency**: As needed
- **Data Source**: Google Sheets
- **Destination**: Backend API

## 📋 **Workflow Management**

### **Active Workflows**
- **google_sheets_sync.json**: ✅ Importing 133 vehicles
- **facebook_automation_fixed.json**: ⚠️ Facebook posting deactivated

### **Workflow Status**
- **Google Sheets Sync**: ✅ Operational
- **Backend API**: ✅ Connected
- **Data Processing**: ✅ AI validation active
- **Error Handling**: ✅ Comprehensive logging

## 🔧 **Setup Instructions**

### **Step 1: Access n8n Dashboard**
1. **URL**: http://localhost:5678
2. **Username**: `admin`
3. **Password**: `AutosellN8n2025!`

### **Step 2: Import Workflows**
1. **Google Sheets Sync**: Import `google_sheets_sync.json`
2. **Facebook Automation**: Import `facebook_automation_fixed.json`
3. **Configure Credentials**: Set up Google Sheets and Facebook credentials

### **Step 3: Execute Workflows**
1. **Manual Execution**: Click "Execute Workflow" for Google Sheets sync
2. **Monitor Results**: Check execution logs and results
3. **Verify Backend**: Confirm vehicles imported to backend

## 🧪 **Testing Workflows**

### **Test Google Sheets Sync**
1. **Execute Workflow**: Click "Execute Workflow" on Google Sheets sync
2. **Check Results**: Verify vehicles imported to backend
3. **Monitor Logs**: Check execution logs for errors
4. **Verify Frontend**: Confirm vehicles appear in frontend

### **Test Facebook Automation**
1. **Execute Workflow**: Click "Execute Workflow" on Facebook automation
2. **Check Results**: Verify Facebook posts created
3. **Monitor Logs**: Check execution logs for errors
4. **Verify Facebook**: Confirm posts appear on Facebook

## 🔍 **Monitoring and Debugging**

### **Check Workflow Status**
1. **n8n Dashboard**: http://localhost:5678
2. **Execution History**: Check workflow execution logs
3. **Error Logs**: Review any error messages
4. **Backend Status**: Verify backend API responses

### **Common Issues**
1. **Connection Refused**: Ensure backend is running on port 8001
2. **JSON Expression Greyed Out**: Check AI Data Processor configuration
3. **Facebook Posting Fails**: Node is deactivated, can be reactivated when needed
4. **Duplicate Imports**: Manual execution prevents automatic duplicates

## 📊 **Current System Status**

### **Active Workflows**
- ✅ **Google Sheets Sync**: Operational, importing 133 vehicles
- ⚠️ **Facebook Automation**: Deactivated (Facebook posting node disabled)

### **System Components**
- **n8n**: ✅ Running on port 5678
- **Backend**: ✅ Running on port 8001
- **Frontend**: ✅ Running on port 3002
- **Database**: ✅ 133 vehicles stored

### **Workflow Performance**
- **Total Vehicles Imported**: 133
- **Success Rate**: 100%
- **Data Validation**: AI-powered cleaning active
- **Error Handling**: Comprehensive logging
- **Backend Integration**: Seamless API connection

## 🔄 **Current Automation Flow**

### **Google Sheets to Backend Sync (ACTIVE)**
```
Manual Trigger → Google Sheets → AI Data Processor → Backend API → Database → Frontend Display
```

### **Facebook Automation (DEACTIVATED)**
```
Facebook Posting Node → DEACTIVATED (Marketplace posting complexity)
```

### **System Integration**
```
Google Sheets → n8n → Backend → Database → Frontend
```

## 🎯 **Best Practices**

### **Workflow Management**
- **Manual execution only** to prevent duplicates
- **Use descriptive node names**
- **Add error handling** for critical nodes
- **Test workflows** before activating

### **Credential Management**
- **Google Sheets OAuth2** configured
- **Facebook credentials** ready for future use
- **Backend API** connection stable
- **Monitor credential usage**

### **Monitoring**
- **Check execution logs** regularly
- **Monitor error rates**
- **Set up alerts** for failed executions
- **Review performance** metrics

## 🚀 **Production Deployment**

### **Current Status**
- **n8n**: ✅ Running on port 5678
- **Backend**: ✅ Running on port 8001
- **Frontend**: ✅ Running on port 3002
- **Database**: ✅ 133 vehicles stored

### **System Configuration**
- **n8n**: Manual execution only
- **Backend**: In-memory storage (133 vehicles)
- **Frontend**: React-based interface
- **Database**: PostgreSQL ready for production

### **Security Considerations**
- **Use HTTPS** for production
- **Implement proper authentication**
- **Restrict webhook access**
- **Monitor for suspicious activity**

---

**Your n8n automation system is ready to power Autosell.mx!** 🤖

## 📈 **Success Metrics**

- **Total Vehicles**: 133 successfully imported
- **Success Rate**: 100% data consistency
- **System Uptime**: All components operational
- **Integration Status**: Google Sheets → n8n → Backend → Frontend
