# 🚀 GitHub Codespaces Deployment Guide
## Optimized Autosell.mx Production Deployment

## 🎯 **Overview**

This guide covers deploying the complete Autosell.mx system on GitHub Codespaces with optimized storage usage (~300MB vs 15GB limit) and unlimited photo storage via Google Drive.

## 📊 **Space Analysis**

### **GitHub Codespaces Free Tier:**
- **Compute**: 120 core-hours/month (60 hours with 2-core machine)
- **Storage**: 15 GB-month per month
- **Auto-stop**: 30 minutes of inactivity

### **Optimized Usage:**
- **Database**: ~20MB (metadata only)
- **Application Code**: ~50MB
- **Dependencies**: ~200MB
- **Total**: ~300MB (well within 15GB limit!)

### **Google Drive (External):**
- **Photos**: Unlimited storage
- **Organization**: Automatic vehicle folders
- **Backup**: Built-in Google Drive backup

## 🏗️ **Architecture Benefits**

### **Database (GitHub Codespaces):**
- ✅ **Vehicle metadata** (marca, modelo, precio, estatus)
- ✅ **Drive folder references** (folder_id, folder_url)
- ✅ **Photo metadata** (drive_file_id, filename, file_size)
- ✅ **No actual photo files** stored

### **Google Drive (External):**
- ✅ **All actual photos** stored in organized folders
- ✅ **Professional sharing URLs** for frontend display
- ✅ **Automatic folder creation** via n8n workflows
- ✅ **Unlimited storage** (Google Drive quota)

## 🚀 **Deployment Steps**

### **1. Create GitHub Codespace**
```bash
# From your GitHub repository
# Click "Code" → "Codespaces" → "Create codespace on main"
```

### **2. Install Dependencies**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install

# Install n8n globally
npm install -g n8n
```

### **3. Database Setup**
```bash
# Start PostgreSQL (pre-installed in Codespaces)
sudo service postgresql start

# Create database
sudo -u postgres createdb autosell_db

# Initialize database schema
python init_database.py
```

### **4. Environment Configuration**
```bash
# Set environment variables
export DATABASE_URL="postgresql://postgres:password@localhost:5432/autosell_db"
export GOOGLE_DRIVE_PARENT_FOLDER_ID="your_drive_folder_id"
export VITE_API_URL="http://localhost:8000"
```

### **5. Start Services**
```bash
# Terminal 1: Backend API
python main.py

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: n8n Automation
n8n start
```

## 🌐 **Access URLs**

### **GitHub Codespaces:**
- **Frontend**: `https://your-codespace.region.app.github.dev:5173`
- **Backend**: `https://your-codespace.region.app.github.dev:8000`
- **n8n**: `https://your-codespace.region.app.github.dev:5678`
- **API Docs**: `https://your-codespace.region.app.github.dev:8000/docs`

### **Local Development:**
- **Frontend**: `http://localhost:5173`
- **Backend**: `http://localhost:8000`
- **n8n**: `http://localhost:5678`

## 🔧 **Google Drive Integration**

### **1. OAuth2 Setup**
```bash
# Download credentials from Google Cloud Console
# Save as: drive_credentials_n8n.json
# Set redirect URI: http://localhost:8081/
```

### **2. Folder Structure**
```
Google Drive/
├── Autosell.mx/
│   ├── Vehicle-1-Toyota-Corolla-2023/
│   ├── Vehicle-2-Honda-Civic-2022/
│   └── Vehicle-3-Ford-F150-2024/
```

### **3. n8n Workflow Configuration**
- **Enhanced Workflow**: `enhanced_google_sheets_to_backend_sync.json`
- **Google Drive Node**: Configure OAuth2 credentials
- **Parent Folder**: Set your main Drive folder ID
- **Auto Permissions**: Public read access for photos

## 📱 **Frontend Features**

### **Professional Vehicle Details Page**
- ✅ **High-quality photo display** from Google Drive
- ✅ **Thumbnail optimization** for fast loading
- ✅ **Professional layout** matching Autosell.mx branding
- ✅ **Responsive design** for all devices

### **Photo Management**
- ✅ **Upload to Google Drive** with automatic organization
- ✅ **Thumbnail generation** for fast display
- ✅ **Professional URLs** for sharing
- ✅ **Unlimited storage** via Google Drive

## 🔄 **Automation Workflows**

### **1. Google Sheets Sync**
- **Trigger**: Webhook `/webhook/sync-from-sheets`
- **Process**: Read Sheets → Process Data → Sync Backend → Create Drive Folder
- **Result**: Vehicle created with organized Drive folder

### **2. Photo Management**
- **Upload**: Frontend → Backend → Google Drive → Database metadata
- **Display**: Database metadata → Drive thumbnail URLs → Frontend
- **Sync**: n8n workflows handle Drive ↔ Database synchronization

### **3. Status Management**
- **"Vendido"**: Remove from Autosell.mx and Facebook
- **"Disponible"**: Post to Facebook Marketplace
- **"Apartado"**: Mark as reserved

## 💾 **Storage Optimization**

### **Database (Minimal Usage):**
```sql
-- Vehicle metadata only
vehicles: id, marca, modelo, año, precio, estatus, drive_folder_id, drive_folder_url

-- Photo metadata only
photos: id, vehicle_id, drive_file_id, filename, file_size, mime_type, drive_url
```

### **Google Drive (Unlimited):**
- **Actual photos** stored in organized vehicle folders
- **Professional sharing URLs** for frontend display
- **Automatic backup** via Google Drive
- **Version control** for photo management

## 🎯 **Production Benefits**

### **Cost Efficiency:**
- ✅ **Free GitHub Codespaces** (120 hours/month)
- ✅ **Free Google Drive** (unlimited photos)
- ✅ **No database storage costs** for photos
- ✅ **Professional URLs** without CDN costs

### **Scalability:**
- ✅ **Unlimited photo storage** via Google Drive
- ✅ **Fast database queries** (metadata only)
- ✅ **Professional photo URLs** for sharing
- ✅ **Automatic organization** via n8n

### **Performance:**
- ✅ **Fast loading** with Drive thumbnails
- ✅ **Optimized database** (metadata only)
- ✅ **Professional URLs** for photo sharing
- ✅ **Automatic backups** via Google Drive

## 🔧 **Troubleshooting**

### **Common Issues:**
1. **Port conflicts**: Use different ports for each service
2. **OAuth redirect**: Ensure `http://localhost:8081/` is configured
3. **Drive permissions**: Check folder sharing settings
4. **Database connection**: Verify PostgreSQL is running

### **Health Checks:**
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:5173

# Check n8n
curl http://localhost:5678
```

## 📈 **Monitoring**

### **Usage Tracking:**
- **GitHub Codespaces**: Monitor compute hours and storage
- **Google Drive**: Track photo storage and organization
- **Database**: Monitor metadata storage and performance
- **n8n**: Track workflow executions and automation

### **Performance Metrics:**
- **Database size**: Should stay under 1GB
- **Drive organization**: Automatic folder creation
- **Photo loading**: Optimized thumbnail URLs
- **System health**: Comprehensive monitoring endpoints

## 🎉 **Success Criteria**

### **Deployment Complete When:**
- ✅ **All services running** on GitHub Codespaces
- ✅ **Google Drive integration** working
- ✅ **Photo upload/display** functional
- ✅ **n8n workflows** executing
- ✅ **Database storage** under 1GB
- ✅ **Frontend displaying** photos from Drive
- ✅ **Complete automation** working end-to-end

This optimized architecture provides unlimited photo storage while keeping GitHub Codespaces usage minimal and cost-effective!
