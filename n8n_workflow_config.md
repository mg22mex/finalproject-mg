# n8n Workflow Configuration for Autosell.mx

## 🎯 Recommended Workflow Setup

### 1. Google Sheets to Backend Sync

**CRITICAL SETTINGS:**
- ✅ **Manual execution ONLY** (no automatic triggers)
- ✅ **Batch size: 10 vehicles** (to avoid overwhelming the backend)
- ✅ **Error handling: Continue on failure**
- ✅ **Retry logic: 3 attempts with 1-second delay**

**Workflow Steps:**
1. **Manual Trigger** (Webhook or Manual)
2. **Google Sheets Read** (Range: A101:J231 for 131 vehicles)
3. **Data Validation** (AI-powered cleaning)
4. **Batch Processing** (10 vehicles at a time)
5. **Backend API Call** (POST to /vehicles/)
6. **Success/Error Handling**
7. **Facebook Posting** (optional, for new vehicles)
8. **Response/Notification**

### 2. Facebook Automation

**Settings:**
- ✅ **Trigger: New vehicle created**
- ✅ **Page ID: Your Facebook Page ID**
- ✅ **Access Token: Your Facebook Access Token**
- ✅ **Auto-post: Only for new vehicles**

### 3. Status Synchronization

**Settings:**
- ✅ **Trigger: Status change**
- ✅ **Sync: Backend ↔ Facebook ↔ Google Sheets**
- ✅ **Remove from Facebook when status = "VENDIDO"**

## 🚨 IMPORTANT: Preventing Duplicate Imports

### Before Running Any Workflow:

1. **Check current vehicle count:**
   ```bash
   curl -s http://localhost:8001/dashboard/stats | grep total_vehicles
   ```

2. **If count is > 200, reset the system:**
   ```bash
   ./manage_automation.sh reset
   ```

3. **Only run workflows MANUALLY**
4. **Test with small batches first**
5. **Monitor the execution closely**

### Safe Workflow Execution:

1. **Start with 5 vehicles** (range: A101:A105)
2. **Check results**
3. **If successful, increase to 10 vehicles**
4. **Continue until all 131 vehicles are imported**

## 🔧 Configuration Steps:

1. **Go to http://localhost:5678**
2. **Create new workflow**
3. **Add Google Sheets node**
4. **Configure with your credentials**
5. **Set range to A101:J231**
6. **Add data processing node**
7. **Add backend API node**
8. **Set to MANUAL execution only**
9. **Test with small batch**
10. **Run full import when ready**

This configuration ensures reliable, controlled data synchronization without the duplicate import issues.
