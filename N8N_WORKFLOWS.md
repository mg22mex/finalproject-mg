# 🤖 n8n Workflows Documentation

## 🎯 **Overview**

n8n workflows provide the automation backbone for Autosell.mx, handling Google Sheets integration, Facebook posting, and complete vehicle processing pipelines.

## 📁 **Essential Workflows (5 Total)**

### **0. Enhanced Google Sheets to Backend Sync with Drive Integration**
**File**: `enhanced_google_sheets_to_backend_sync.json`

**Purpose**: Enhanced version with Google Drive folder creation for new vehicles.

**Trigger**: Webhook (`/webhook/sync-from-sheets`)

**Flow**:
```
Webhook Trigger → Read Google Sheets → Process Data → Sync to Backend → Check New Vehicle → Create Drive Folder → Update Vehicle Drive Info
                                                                     → Check Sold Status → Remove from Autosell/Facebook
```

**New Features**:
- **Google Drive Integration**: Automatically creates Drive folders for new vehicles
- **Folder Naming**: `Marca_Modelo_Año_Precio_Date` format
- **Drive Folder Updates**: Updates vehicle records with Drive folder information
- **Enhanced Data Processing**: Includes Drive folder creation flags

**Configuration**:
- **Google Drive**: Configure OAuth2 credentials for Drive API
- **Parent Folder**: Set `YOUR_GOOGLE_DRIVE_PARENT_FOLDER_ID`
- **Folder Permissions**: Automatically set to public read access

**Benefits**:
- **Automatic Organization**: Each vehicle gets its own Drive folder
- **Professional Structure**: Consistent folder naming convention
- **Photo Management**: Ready for photo uploads to organized folders
- **Scalable Storage**: Unlimited Drive storage vs database limitations

### **1. Google Sheets to Backend Sync**
**File**: `google_sheets_to_backend_sync.json`

**Purpose**: Syncs vehicle data from Google Sheets to the backend database and handles status-based actions.

**Trigger**: Webhook (`/webhook/sync-from-sheets`)

**Flow**:
```
Webhook Trigger → Read Google Sheets → Process Data → Sync to Backend → Check Status → Remove from Autosell/Facebook
```

**Configuration**:
- **Google Sheets**: Configure OAuth2 credentials
- **Sheet ID**: Update with your Google Sheet ID
- **Range**: `A2:I1000` (adjust as needed)

**Data Mapping**:
| Google Sheets | Backend Field | Notes |
|---------------|---------------|-------|
| `Marca` | `marca` | Brand |
| `Modelo` | `modelo` | Model |
| `Año` | `año` | Year |
| `Color` | `color` | Color |
| `Precio` | `precio` | Price (removes $ and commas) |
| `km` | `kilometraje` | Mileage |
| `Estatus` | `estatus` | Status |
| `Ubicacion` | `ubicacion` | Location |

**Status Handling**:
- **"Disponible"** → `is_available = true`, `is_sold = false`
- **"Vendido"** → Triggers removal from Autosell.mx and Facebook

### **2. Frontend to Google Sheets Sync**
**File**: `frontend_to_sheets_sync.json`

**Purpose**: Syncs new vehicles from the frontend to Google Sheets.

**Trigger**: Webhook (`/webhook/sync-single-vehicle`)

**Flow**:
```
Webhook Trigger → Process Vehicle Data → Append to Google Sheets
```

**Configuration**:
- **Google Sheets**: Configure OAuth2 credentials
- **Sheet ID**: Update with your Google Sheet ID
- **Sheet Name**: `Inventario a web`

**Data Processing**:
- Converts frontend data to Google Sheets format
- Adds current date to "Ingreso" column
- Formats price with currency symbol
- Maps all vehicle fields

### **3. Scheduled Google Sheets Sync**
**File**: `scheduled_sheets_sync.json`

**Purpose**: Automatically syncs Google Sheets data every 30 minutes and handles status changes.

**Trigger**: Schedule (every 30 minutes)

**Flow**:
```
Schedule Trigger → Read Google Sheets → Process Data → Sync to Backend → Check Status → Remove from Autosell/Facebook
```

**Configuration**:
- **Schedule**: Every 30 minutes
- **Google Sheets**: Configure OAuth2 credentials
- **Sheet ID**: Update with your Google Sheet ID
- **Range**: `A2:I1000`

**Features**:
- **Automatic Sync**: Runs every 30 minutes
- **Status Monitoring**: Detects "Vendido" status changes
- **Automatic Actions**: Removes vehicles from Autosell.mx and Facebook

### **4. Facebook Automation**
**File**: `facebook_automation.json`

**Purpose**: Posts vehicles to Facebook Marketplace.

**Trigger**: Webhook (`/webhook/facebook-post`)

**Flow**:
```
Webhook Trigger → Get Facebook Credentials → Post to Facebook → Log Activity
```

**Configuration**:
- **Facebook**: Configure Graph API credentials
- **Account Type**: Auto or Manual
- **Post Format**: Customizable message format

**Features**:
- **Multi-Account Support**: Handles multiple Facebook accounts
- **Custom Messages**: Configurable post content
- **Activity Logging**: Tracks posting activity

## 🔧 **Setup Instructions**

### **Step 1: Access n8n Dashboard**
1. **URL**: http://localhost:5678
2. **Username**: `admin`
3. **Password**: `AutosellN8n2025!`

### **Step 2: Import Workflows**
1. **Click "Import from File"**
2. **Select each workflow file**:
   - `google_sheets_to_backend_sync.json`
   - `frontend_to_sheets_sync.json`
   - `scheduled_sheets_sync.json`
   - `facebook_automation.json`
3. **Click "Import"** for each
4. **Click "Save"** to activate

### **Step 3: Configure Credentials**

#### **Google Sheets OAuth2**
1. **Go to Settings → Credentials**
2. **Click "Add Credential"**
3. **Select "Google Sheets OAuth2 API"**
4. **Follow OAuth setup**:
   - Authorize with Google
   - Grant permissions to your Google Sheet
   - Save credentials

#### **Facebook Graph API**
1. **Go to Settings → Credentials**
2. **Click "Add Credential"**
3. **Select "Facebook Graph API"**
4. **Enter credentials**:
   - App ID: Your Facebook App ID
   - App Secret: Your Facebook App Secret
   - Save credentials

### **Step 4: Update Configuration**

#### **Update Sheet IDs**
1. **Open each workflow**
2. **Find "Read Google Sheets" or "Append to Google Sheets" nodes**
3. **Replace `YOUR_GOOGLE_SHEET_ID`** with your actual sheet ID
4. **Save all workflows**

#### **Update Webhook URLs**
1. **Verify webhook URLs** in each workflow
2. **Ensure they match your backend URLs**:
   - `http://127.0.0.1:8000/vehicles/sync-from-sheets`
   - `http://127.0.0.1:8000/vehicles/{id}/remove-from-autosell`
   - `http://127.0.0.1:8000/vehicles/{id}/remove-from-facebook`

## 🧪 **Testing Workflows**

### **Test Google Sheets Sync**
```bash
# Test manual sync
curl -X POST http://localhost:5678/webhook/sync-from-sheets \
  -H "Content-Type: application/json" \
  -d '{"spreadsheet_id": "YOUR_GOOGLE_SHEET_ID"}'
```

### **Test Frontend Sync**
```bash
# Test frontend to sheets sync
curl -X POST http://localhost:5678/webhook/sync-single-vehicle \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Toyota",
    "modelo": "Camry",
    "año": 2020,
    "color": "Blanco",
    "precio": 250000,
    "kilometraje": "45,000 km",
    "estatus": "DISPONIBLE",
    "ubicacion": "CDMX"
  }'
```

### **Test Facebook Posting**
```bash
# Test Facebook posting
curl -X POST http://localhost:5678/webhook/facebook-post \
  -H "Content-Type: application/json" \
  -d '{
    "account_type": "auto",
    "vehicle_data": {
      "marca": "Toyota",
      "modelo": "Camry",
      "año": 2020,
      "color": "Blanco",
      "precio": 250000,
      "kilometraje": "45,000 km",
      "estatus": "DISPONIBLE",
      "ubicacion": "CDMX"
    },
    "message": "🚗 Toyota Camry 2020 - $250,000"
  }'
```

## 🔍 **Monitoring and Debugging**

### **Execution Logs**
1. **Go to n8n Dashboard**
2. **Click "Executions"** in the sidebar
3. **View execution history** for each workflow
4. **Click on individual executions** to see detailed logs

### **Node Debugging**
1. **Open workflow**
2. **Click on individual nodes**
3. **View input/output data**
4. **Check for errors** in red nodes

### **Common Issues**

#### **"Authentication failed"**
- **Check credentials** in Settings → Credentials
- **Re-authenticate** if tokens expired
- **Verify permissions** for Google Sheets and Facebook

#### **"Webhook not responding"**
- **Check backend is running** on port 8000
- **Verify webhook URLs** are correct
- **Check network connectivity**

#### **"Google Sheets access denied"**
- **Re-authorize Google Sheets** credentials
- **Check sheet permissions**
- **Verify sheet ID** is correct

#### **"Facebook posting failed"**
- **Check Facebook credentials**
- **Verify app permissions**
- **Check access token** validity

## 📊 **Workflow Status**

### **Active Workflows**
- ✅ **Google Sheets to Backend Sync**: Active
- ✅ **Frontend to Sheets Sync**: Active
- ✅ **Scheduled Sheets Sync**: Active (every 30 minutes)
- ✅ **Facebook Automation**: Active

### **Webhook Endpoints**
- **Sync from Sheets**: `http://localhost:5678/webhook/sync-from-sheets`
- **Frontend Sync**: `http://localhost:5678/webhook/sync-single-vehicle`
- **Facebook Post**: `http://localhost:5678/webhook/facebook-post`

## 🔄 **Automation Flows**

### **Flow 1: Add Vehicle (Frontend → All Systems)**
```
Frontend Add → Backend Database → n8n Webhook → Google Sheets + Facebook
```

### **Flow 2: Status Change (Google Sheets → Actions)**
```
Google Sheets Change → Scheduled Sync → Backend Update → Remove from Autosell/Facebook
```

### **Flow 3: Manual Sync (Triggered)**
```
Manual Trigger → n8n Workflow → Google Sheets → Backend → Status Check → Actions
```

## 🎯 **Best Practices**

### **Workflow Management**
- **Keep workflows simple** and focused
- **Use descriptive node names**
- **Add error handling** for critical nodes
- **Test workflows** before activating

### **Credential Management**
- **Use environment variables** for sensitive data
- **Rotate credentials** regularly
- **Monitor credential usage**
- **Backup credential configurations**

### **Monitoring**
- **Check execution logs** regularly
- **Monitor error rates**
- **Set up alerts** for failed executions
- **Review performance** metrics

## 🚀 **Production Deployment**

### **Environment Variables**
```env
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=AutosellN8n2025!
N8N_ENCRYPTION_KEY=your-encryption-key
N8N_USER_MANAGEMENT_DISABLED=true
```

### **Database Configuration**
```env
DB_TYPE=postgresql
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n
DB_POSTGRESDB_PASSWORD=your-password
```

### **Security Considerations**
- **Use HTTPS** for production
- **Implement proper authentication**
- **Restrict webhook access**
- **Monitor for suspicious activity**

---

**Your n8n automation system is ready to power Autosell.mx!** 🤖
