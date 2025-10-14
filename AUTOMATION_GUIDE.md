# Autosell.mx Automation Guide
## Complete Setup and Usage Guide

### 🚀 Quick Start

1. **Start the system:**
   ```bash
   ./manage_automation.sh start
   ```

2. **Test the system:**
   ```bash
   ./test_system.sh
   ```

3. **Check status:**
   ```bash
   ./manage_automation.sh status
   ```

4. **Access interfaces:**
   - Frontend: http://localhost:3002
   - Backend: http://localhost:8001
   - n8n: http://localhost:5678

### 🔧 n8n Workflow Setup

#### Step 1: Create Google Sheets Workflow

1. **Go to http://localhost:5678**
2. **Click "Create Workflow"**
3. **Add Google Sheets node:**
   - Authentication: Your Google account
   - Spreadsheet: Your Google Sheet ID
   - Range: A101:J231 (for 131 vehicles)
   - Operation: Read

4. **Add Data Processing node:**
   ```javascript
   // Clean and validate data
   const items = $input.all();
   const processedItems = [];
   
   for (const item of items) {
     const data = item.json;
     const vehicleData = {
       marca: data.A || 'Unknown',
       modelo: data.B || 'Unknown',
       año: parseInt(data.C) || new Date().getFullYear(),
       precio: parseInt(data.D) || 0,
       estatus: data.E || 'DISPONIBLE',
       color: data.F || 'Unknown',
       kilometraje: data.G || '',
       ubicacion: data.H || 'PERIFERICO',
       descripcion: data.I || ''
     };
     processedItems.push({ json: vehicleData });
   }
   
   return processedItems;
   ```

5. **Add Backend API node:**
   - Method: POST
   - URL: http://localhost:8001/vehicles/
   - Headers: Content-Type: application/json
   - Body: {{ $json }}

6. **Set to MANUAL execution only**

#### Step 2: Test the Workflow

1. **Test with small batch first:**
   - Change range to A101:A105 (5 vehicles)
   - Execute workflow
   - Check results

2. **If successful, increase batch size:**
   - Change range to A101:A110 (10 vehicles)
   - Execute workflow
   - Check results

3. **Run full import:**
   - Change range to A101:J231 (131 vehicles)
   - Execute workflow
   - Monitor execution

### 🚨 Important Safety Measures

#### Before Running Any Workflow:

1. **Check current vehicle count:**
   ```bash
   curl -s http://localhost:8001/dashboard/stats | grep total_vehicles
   ```

2. **If count > 200, reset system:**
   ```bash
   ./manage_automation.sh reset
   ```

3. **Always test with small batches first**
4. **Monitor execution closely**
5. **Stop immediately if errors occur**

### 📊 Monitoring and Troubleshooting

#### Check System Status:
```bash
./manage_automation.sh status
```

#### View Logs:
```bash
./manage_automation.sh logs
```

#### Reset System:
```bash
./manage_automation.sh reset
```

#### Test System:
```bash
./test_system.sh
```

### 🔄 Workflow Execution Process

1. **Prepare:**
   - Ensure system is running
   - Check current vehicle count
   - Reset if necessary

2. **Configure:**
   - Set up Google Sheets workflow
   - Configure with your credentials
   - Set to manual execution

3. **Test:**
   - Start with 5 vehicles
   - Check results
   - Increase batch size gradually

4. **Execute:**
   - Run full import (131 vehicles)
   - Monitor execution
   - Check final results

5. **Verify:**
   - Check frontend at http://localhost:3002
   - Verify vehicle count
   - Test functionality

### 🎯 Expected Results

After successful import:
- **Total Vehicles: 131**
- **Available Vehicles: 131**
- **Total Value: ~$25,000,000**
- **All vehicles visible in frontend**
- **All functionality working**

### 🛠️ Troubleshooting

#### Common Issues:

1. **High vehicle count (>200):**
   - Run: `./manage_automation.sh reset`
   - Start fresh

2. **n8n connection errors:**
   - Check if n8n is running
   - Restart: `./manage_automation.sh stop && ./manage_automation.sh start`

3. **Backend API errors:**
   - Check backend logs
   - Restart backend

4. **Frontend not loading:**
   - Check if frontend is running
   - Check port 3002

#### Getting Help:

1. **Check status:** `./manage_automation.sh status`
2. **View logs:** `./manage_automation.sh logs`
3. **Test system:** `./test_system.sh`
4. **Reset if needed:** `./manage_automation.sh reset`

This guide provides everything you need to set up and run the automation system successfully!
