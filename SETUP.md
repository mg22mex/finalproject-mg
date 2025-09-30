# 🚀 Autosell.mx Setup Guide

## 📋 **Prerequisites**

- **Node.js 18+** for frontend development
- **Python 3.13+** for backend development
- **Git** for version control
- **Google Account** for Google Sheets integration
- **Facebook Developer Account** for Facebook integration

## 🏗️ **Complete Setup Process**

### **Step 1: Clone and Prepare**

```bash
# Clone repository
git clone <your-repository-url>
cd finalproject-mg

# Verify structure
ls -la
# Should show: backend/, frontend/, n8n_workflows/, README.md
```

### **Step 2: Backend Setup**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python main_fixed.py
```

**Expected Output:**
```
✅ API routers loaded successfully
🚗 Starting Autosell.mx API v1.0.0
✅ Database connection established
✅ Database tables initialized
INFO: Uvicorn running on http://0.0.0.0:8000
```

### **Step 3: Frontend Setup**

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected Output:**
```
VITE v5.x.x ready in xxx ms
➜ Local: http://localhost:3000/
```

### **Step 4: n8n Automation Setup**

```bash
# Open new terminal
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

**Expected Output:**
```
n8n ready on ::, port 5678
Editor is now accessible via:
http://localhost:5678
```

### **Step 5: Access Applications**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **n8n Dashboard**: http://localhost:5678

## 🔧 **Configuration Steps**

### **Step 6: Configure n8n Workflows**

1. **Access n8n Dashboard**
   - Go to: http://localhost:5678
   - Username: `admin`
   - Password: `AutosellN8n2025!`

2. **Import Workflows**
   - Click "Import from File"
   - Import each workflow from `n8n_workflows/`:
     - `google_sheets_to_backend_sync.json`
     - `frontend_to_sheets_sync.json`
     - `scheduled_sheets_sync.json`
     - `facebook_automation.json`

3. **Configure Google Sheets Credentials**
   - Go to Settings → Credentials
   - Add "Google Sheets OAuth2 API"
   - Authorize with your Google account
   - Grant access to your Google Sheets

4. **Configure Facebook Credentials**
   - Go to Settings → Credentials
   - Add "Facebook Graph API"
   - Enter your Facebook App ID and Secret

5. **Update Sheet IDs**
   - Open each workflow
   - Replace `YOUR_GOOGLE_SHEET_ID` with your actual sheet ID
   - Save all workflows

### **Step 7: Test Complete System**

```bash
# Run integration tests
python test_complete_integration.py
```

**Expected Output:**
```
🧪 Testing Complete Integration System
✅ Backend is running
✅ n8n is running
✅ Frontend Endpoints working
✅ Complete Processing working
✅ Sheets Sync Trigger working
✅ Vehicle Removal working
🎉 All tests passed!
```

## 🎯 **Google Sheets Setup**

### **Step 8: Create Google Sheet**

1. **Create New Google Sheet**
   - Name: "Inventario a web"
   - Columns: Ingreso, Modelo, Marca, Año, Color, Precio, km, Estatus, Ubicacion

2. **Share Sheet**
   - Share with your Google account
   - Grant edit permissions

3. **Get Sheet ID**
   - Copy the ID from the URL
   - Format: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### **Step 9: Facebook App Setup**

1. **Create Facebook App**
   - Go to: https://developers.facebook.com/
   - Create new app
   - Choose "Consumer App" (no business verification needed)

2. **Configure App**
   - Add Facebook Login product
   - Set redirect URI: `http://localhost:5678/oauth/callback`
   - Get App ID and App Secret

3. **Test App**
   - Add yourself as test user
   - Generate access token

## 🧪 **Testing Workflows**

### **Step 10: Test Google Sheets Sync**

```bash
# Test manual sync
curl -X POST http://localhost:8000/frontend/trigger-sheets-sync
```

### **Step 11: Test Facebook Posting**

```bash
# Test Facebook posting
curl -X POST http://localhost:8000/frontend/post-to-facebook \
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

### **Step 12: Test Complete Processing**

```bash
# Test complete automation
curl -X POST http://localhost:8000/frontend/complete-vehicle-processing \
  -H "Content-Type: application/json" \
  -d '{
    "marca": "Honda",
    "modelo": "Civic",
    "año": 2019,
    "color": "Negro",
    "precio": 220000,
    "kilometraje": "52,000 km",
    "estatus": "DISPONIBLE",
    "ubicacion": "CDMX"
  }'
```

## 🚀 **Production Deployment**

### **Step 13: Deploy Frontend to Vercel**

1. **Connect to Vercel**
   - Go to: https://vercel.com/
   - Connect GitHub repository
   - Set build command: `npm run build`
   - Set output directory: `dist`

2. **Configure Environment Variables**
   - `VITE_API_URL`: Your backend URL
   - `VITE_N8N_URL`: Your n8n URL

### **Step 14: Deploy Backend to GitHub Codespaces**

1. **Create Codespace**
   - Go to your GitHub repository
   - Click "Code" → "Codespaces" → "Create codespace"

2. **Configure Codespace**
   - Install dependencies
   - Set environment variables
   - Start services

3. **Configure Ports**
   - Backend: Port 8000
   - n8n: Port 5678
   - Make ports public

## 🔍 **Verification Checklist**

### **✅ System Health**
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] n8n running on port 5678
- [ ] Database connected
- [ ] All API endpoints responding

### **✅ n8n Configuration**
- [ ] All workflows imported
- [ ] Google Sheets credentials configured
- [ ] Facebook credentials configured
- [ ] Sheet IDs updated in workflows
- [ ] Workflows active and running

### **✅ Integration Testing**
- [ ] Google Sheets sync working
- [ ] Facebook posting working
- [ ] Vehicle removal working
- [ ] Complete processing pipeline working
- [ ] Scheduled sync working

### **✅ Production Readiness**
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Codespaces
- [ ] n8n deployed to Codespaces
- [ ] All services accessible
- [ ] Monitoring in place

## 🐛 **Troubleshooting**

### **Common Issues**

1. **"Port already in use"**
   ```bash
   # Find process using port
   lsof -i :8000
   # Kill process
   kill -9 <PID>
   ```

2. **"Module not found"**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt
   npm install
   ```

3. **"Database connection failed"**
   ```bash
   # Check database URL
   echo $DATABASE_URL
   # Test connection
   python -c "from app.database import check_db_connection; print(check_db_connection())"
   ```

4. **"n8n workflow failed"**
   - Check n8n execution logs
   - Verify credentials
   - Test individual nodes
   - Check webhook URLs

### **Debug Commands**

```bash
# Check running processes
ps aux | grep -E "(python|node|n8n)"

# Check port usage
netstat -tlnp | grep -E "(3000|5678|8000)"

# Check logs
tail -f backend/logs/app.log

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:5678/
```

## 🎉 **Success Indicators**

When everything is working correctly, you should see:

- ✅ **Backend**: "Autosell.mx API v1.0.0" running
- ✅ **Frontend**: React app loading at localhost:3000
- ✅ **n8n**: Dashboard accessible at localhost:5678
- ✅ **Database**: Connection established
- ✅ **Workflows**: All imported and active
- ✅ **Integration**: Complete automation pipeline working

## 📞 **Support**

If you encounter issues:

1. **Check logs** for error messages
2. **Verify configuration** in n8n
3. **Test individual components**
4. **Check network connectivity**
5. **Review this guide** for missed steps

---

**Your Autosell.mx system is now ready for production!** 🚀
