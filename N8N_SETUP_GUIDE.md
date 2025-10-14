# n8n Workflow Setup Guide
## Safe Google Sheets to Backend Sync

### 🚨 CRITICAL: Before You Start

**Current Status:**
- ✅ Backend: Running with **0 vehicles** (clean state)
- ✅ n8n: Running **WITHOUT automatic workflows**
- ✅ Frontend: Accessible at http://localhost:3002
- ✅ All APIs: Working perfectly

### 📋 Step-by-Step Setup

#### **Step 1: Access n8n Interface**
1. **Go to**: http://localhost:5678
2. **Login** with your n8n credentials
3. **You should see**: Clean interface with no active workflows

#### **Step 2: Create New Workflow**

1. **Click "Create Workflow"**
2. **Name it**: " "
3. **Make sure it's set to MANUAL execution**

#### **Step 3: Add Google Sheets Node**

1. **Drag "Google Sheets" node** to the canvas
2. **Configure**:
   - **Authentication**: Your Google account
   - **Operation**: Read
   - **Spreadsheet ID**: Your Google Sheet ID
   - **Range**: `A101:J231` (for 131 vehicles)
   - **Options**: 
     - Value Render Option: `UNFORMATTED_VALUE`
     - Date Time Render Option: `SERIAL_NUMBER`

#### **Step 4: Add Data Processing Node**

1. **Drag "Code" node** to the canvas
2. **Connect** it to Google Sheets node
3. **Add this code**:

```javascript
// AI-powered data validation and transformation
const items = $input.all();
const processedItems = [];

for (const item of items) {
  const data = item.json;
  
  // Extract and clean data
  const vehicleData = {
    marca: (data.A || data.Marca || 'Unknown').toString().toUpperCase().trim(),
    modelo: (data.B || data.Modelo || 'Unknown').toString().toUpperCase().trim(),
    año: parseInt(data.C || data.Año) || new Date().getFullYear(),
    precio: parseInt(data.D || data.Precio) || 0,
    estatus: (data.E || data.Estatus || 'DISPONIBLE').toString().toUpperCase().trim(),
    color: (data.F || data.Color || 'Unknown').toString().toUpperCase().trim(),
    kilometraje: (data.G || data.Kilometraje || '').toString().trim(),
    ubicacion: (data.H || data.Ubicacion || 'PERIFERICO').toString().toUpperCase().trim(),
    descripcion: (data.I || data.Descripcion || '').toString().trim(),
    external_id: `GS_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  };
  
  // AI validation and cleaning
  if (vehicleData.año < 1990 || vehicleData.año > new Date().getFullYear() + 1) {
    vehicleData.año = new Date().getFullYear();
  }
  
  if (vehicleData.precio <= 0) {
    vehicleData.precio = 100000; // Default price
  }
  
  // Only add if it has valid data
  if (vehicleData.marca !== 'Unknown' && vehicleData.modelo !== 'Unknown') {
    processedItems.push({ json: vehicleData });
  }
}

return processedItems;
```

#### **Step 5: Add Batch Processing**

1. **Drag "Split in Batches" node** to the canvas
2. **Connect** it to Code node
3. **Configure**:
   - **Batch Size**: `10` (process 10 vehicles at a time)
   - **Options**: 
     - Continue on Fail: `true`

#### **Step 6: Add Backend API Node**

1. **Drag "HTTP Request" node** to the canvas
2. **Connect** it to Split in Batches node
3. **Configure**:
   - **Method**: `POST`
   - **URL**: `http://localhost:8001/vehicles/`
   - **Headers**:
     - `Content-Type`: `application/json`
   - **Body**: `{{ $json }}`
   - **Options**:
     - Timeout: `30000`
     - Retry: `3 attempts with 1 second delay`

#### **Step 7: Add Success/Error Handling**

1. **Drag "IF" node** to the canvas
2. **Connect** it to HTTP Request node
3. **Configure**:
   - **Condition**: `{{ $json.status === 'success' }}`

4. **Add "Respond to Webhook" node** for success
5. **Add "Respond to Webhook" node** for error

#### **Step 8: Configure Workflow Settings**

1. **Click "Settings"** (gear icon)
2. **Set**:
   - **Execution Order**: `v1`
   - **Save Execution Progress**: `All`
   - **Save Data on Error**: `All`
   - **Save Data on Success**: `All`

#### **Step 9: Test the Workflow**

1. **Click "Execute Workflow"**
2. **Monitor** the execution
3. **Check** the results
4. **Verify** in the frontend: http://localhost:3002

### 🚨 Safety Checklist

**Before Running:**
- [ ] Workflow is set to **MANUAL execution only**
- [ ] No automatic triggers (Schedule, Webhook, etc.)
- [ ] Batch size is set to **10 or less**
- [ ] Error handling is configured
- [ ] Backend has **0 vehicles** (clean state)

**During Execution:**
- [ ] Monitor execution closely
- [ ] Check for errors
- [ ] Stop immediately if issues occur
- [ ] Verify results in frontend

**After Execution:**
- [ ] Check vehicle count in frontend
- [ ] Verify all vehicles are displayed
- [ ] Test functionality (add, edit, delete)
- [ ] Check for duplicates

### 🔧 Troubleshooting

#### **If You Get Errors:**

1. **Stop the workflow immediately**
2. **Check the error messages**
3. **Fix the configuration**
4. **Test with smaller batch size**
5. **Try again**

#### **If Vehicle Count is Wrong:**

1. **Reset the system**:
   ```bash
   ./manage_automation.sh reset
   ```
2. **Start fresh**
3. **Configure workflow again**
4. **Test with small batch first**

#### **If n8n Won't Start:**

1. **Check if it's running**:
   ```bash
   ./manage_automation.sh status
   ```
2. **Restart if needed**:
   ```bash
   ./manage_automation.sh stop
   ./manage_automation.sh start
   ```

### 📊 Expected Results

**After Successful Import:**
- **Total Vehicles**: 131
- **Available Vehicles**: 131
- **Total Value**: ~$25,000,000
- **All vehicles visible** in frontend
- **All functionality working**

### 🎯 Success Criteria

- [ ] **131 vehicles imported** successfully
- [ ] **No duplicate vehicles**
- [ ] **All data validated** and cleaned
- [ ] **Frontend displays** all vehicles
- [ ] **All CRUD operations** working
- [ ] **No system errors** or crashes

### 📞 Need Help?

1. **Check system status**: `./manage_automation.sh status`
2. **View logs**: `./manage_automation.sh logs`
3. **Test system**: `./test_system.sh`
4. **Reset if needed**: `./manage_automation.sh reset`

**Remember**: Always test with small batches first, and never run automatic workflows!
