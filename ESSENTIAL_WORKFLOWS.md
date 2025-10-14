# Essential n8n Workflows for Autosell.mx
## Only 2 Workflows You Need

### 🎯 **Workflow 1: Google Sheets Sync**
**File**: `google_sheets_sync.json`
**Purpose**: Import your 131 vehicles from Google Sheets to the backend

**Configuration:**
- **Trigger**: Manual execution only
- **Source**: Google Sheets (rows 101-231)
- **Target**: Backend API (http://localhost:8001/vehicles/)
- **Batch Size**: 10 vehicles at a time
- **Error Handling**: Continue on failure, retry 3 times

**Steps:**
1. Import the workflow into n8n
2. Configure Google Sheets authentication
3. Set the correct sheet ID and range (A101:J231)
4. Test with 5 vehicles first
5. Run full import when ready

### 🎯 **Workflow 2: Facebook Automation**
**File**: `facebook_automation_fixed.json`
**Purpose**: Automatically post vehicles to Facebook Marketplace

**Configuration:**
- **Trigger**: When new vehicle is added
- **Target**: Facebook Page
- **Features**: Auto-post, photo upload, status sync

**Steps:**
1. Import the workflow into n8n
2. Configure Facebook authentication
3. Set your Page ID and Access Token
4. Test with one vehicle first
5. Enable for all new vehicles

### 🚨 **Important Safety Rules**

#### **Before Using Any Workflow:**
1. **Check current vehicle count**:
   ```bash
   curl -s http://localhost:8001/dashboard/stats | grep total_vehicles
   ```

2. **If count > 200, reset system**:
   ```bash
   ./manage_automation.sh reset
   ```

3. **Always test with small batches first**
4. **Set workflows to MANUAL execution only**
5. **Monitor execution closely**

#### **Safe Execution Process:**
1. **Start with 5 vehicles** (range: A101:A105)
2. **Check results** in frontend
3. **If successful, increase to 10 vehicles**
4. **Continue until all 131 vehicles are imported**
5. **Never run automatic workflows**

### 📊 **Expected Results**

**After Successful Import:**
- **Total Vehicles**: 131
- **Available Vehicles**: 131
- **Total Value**: ~$25,000,000
- **All vehicles visible** in frontend
- **Facebook integration** working

### 🔧 **Management Commands**

```bash
# Check system status
./manage_automation.sh status

# Reset if needed
./manage_automation.sh reset

# Test system
./test_system.sh

# Quick status
./quick_status.sh
```

### 🎯 **Next Steps**

1. **Go to n8n**: http://localhost:5678
2. **Import the 2 essential workflows**
3. **Configure Google Sheets authentication**
4. **Set to MANUAL execution only**
5. **Test with 5 vehicles first**
6. **Run full import when ready**

### 📚 **Documentation**

- `N8N_SETUP_GUIDE.md` - Detailed setup instructions
- `AUTOMATION_GUIDE.md` - Complete system guide
- `manage_automation.sh` - System control

**You now have a clean, focused automation system with only the essential workflows you need!** 🎉
