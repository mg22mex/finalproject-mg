# 🧪 Autosell.mx Testing Guide
## Complete System Testing for Optimized Architecture

## 🎯 **Testing Overview**

This guide covers testing the complete Autosell.mx system with the new optimized Google Drive + Database architecture.

## 📊 **Current System Status**

### **✅ Running Services:**
- **Backend API**: ✅ Running on port 8000
- **Frontend**: ✅ Running on port 5173  
- **n8n**: ✅ Running (process 43121)

### **🔍 Test URLs:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **n8n Interface**: http://localhost:5678

## 🧪 **Testing Phases**

### **Phase 1: Basic System Health Tests**

#### **1.1 Backend API Health Check**
```bash
# Test backend health
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "2024-10-02T12:00:00Z"}
```

#### **1.2 Frontend Accessibility**
```bash
# Test frontend
curl http://localhost:5173

# Expected: HTML content with React app
```

#### **1.3 Database Connection**
```bash
# Test database connection
curl http://localhost:8000/vehicles/

# Expected: JSON array of vehicles or empty array
```

### **Phase 2: Google Drive Integration Tests**

#### **2.1 Drive Authentication Test**
```bash
# Test Drive connection
curl -X POST http://localhost:8000/drive/test-connection

# Expected: Success message or authentication prompt
```

#### **2.2 Photo Upload Test**
```bash
# Test photo upload (requires a test image file)
curl -X POST http://localhost:8000/photos/upload/1 \
  -F "file=@test_image.jpg" \
  -F "description=Test photo"

# Expected: Photo metadata with Drive file ID
```

#### **2.3 Drive Folder Creation Test**
```bash
# Test Drive folder creation for vehicle
curl -X POST http://localhost:8000/drive/create-folder/1

# Expected: Folder information with Drive folder ID and URL
```

### **Phase 3: Frontend Integration Tests**

#### **3.1 Dashboard Test**
- **URL**: http://localhost:5173
- **Expected**: Dashboard with vehicle statistics
- **Check**: Total vehicles count, available vehicles, etc.

#### **3.2 Vehicles Page Test**
- **URL**: http://localhost:5173/vehicles
- **Expected**: List of vehicles with photos
- **Check**: Vehicle cards, photo thumbnails, search functionality

#### **3.3 Photos Page Test**
- **URL**: http://localhost:5173/photos
- **Expected**: Photo management interface
- **Check**: Vehicle selection, photo upload, Drive integration

#### **3.4 Vehicle Details Test**
- **URL**: http://localhost:5173/vehicles/{id}
- **Expected**: Professional vehicle details page
- **Check**: High-quality photos, specifications, pricing

### **Phase 4: n8n Workflow Tests**

#### **4.1 n8n Interface Test**
- **URL**: http://localhost:5678
- **Expected**: n8n workflow interface
- **Check**: Workflows are loaded and configured

#### **4.2 Google Sheets Sync Test**
```bash
# Test Google Sheets sync webhook
curl -X POST http://localhost:5678/webhook/sync-from-sheets

# Expected: Workflow execution and vehicle sync
```

#### **4.3 Enhanced Workflow Test**
- **File**: `enhanced_google_sheets_to_backend_sync.json`
- **Expected**: Drive folder creation for new vehicles
- **Check**: Folders created in Google Drive

### **Phase 5: End-to-End Integration Tests**

#### **5.1 Complete Vehicle Flow**
1. **Add vehicle** via Google Sheets
2. **n8n creates** Drive folder automatically
3. **Upload photos** via frontend
4. **Photos stored** in Drive folder
5. **Frontend displays** photos from Drive URLs

#### **5.2 Photo Management Flow**
1. **Select vehicle** in Photos page
2. **Upload multiple photos** via frontend
3. **Photos uploaded** to Drive folder
4. **Database stores** metadata only
5. **Frontend displays** Drive thumbnails

#### **5.3 Status Management Flow**
1. **Change status** to "Vendido" in Google Sheets
2. **n8n workflow** triggers removal
3. **Vehicle removed** from Autosell.mx
4. **Facebook post** removed (if applicable)

## 🔧 **Testing Commands**

### **Quick Health Check**
```bash
# Check all services
echo "🔍 Checking services..."
curl -s http://localhost:8000/health && echo "✅ Backend OK" || echo "❌ Backend Failed"
curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend OK" || echo "❌ Frontend Failed"
curl -s http://localhost:5678 > /dev/null && echo "✅ n8n OK" || echo "❌ n8n Failed"
```

### **Database Test**
```bash
# Test database connection and data
curl -s http://localhost:8000/vehicles/ | jq '.[0:3]'  # First 3 vehicles
curl -s http://localhost:8000/dashboard/stats | jq '.'  # Dashboard stats
```

### **Photo System Test**
```bash
# Test photo endpoints
curl -s http://localhost:8000/photos/ | jq '.[0:3]'  # First 3 photos
curl -s http://localhost:8000/photos/vehicle/1 | jq '.'  # Vehicle photos
```

### **Drive Integration Test**
```bash
# Test Drive connection
curl -X POST http://localhost:8000/drive/test-connection
curl -X POST http://localhost:8000/drive/create-folder/1
```

## 🎯 **Expected Results**

### **✅ Successful Tests Should Show:**
- **Backend**: FastAPI docs accessible, health endpoint working
- **Frontend**: React app loading, navigation working
- **Database**: Vehicle data accessible, photo metadata stored
- **Drive**: Photos uploaded to organized folders
- **n8n**: Workflows executing, automation working
- **Integration**: Complete end-to-end flow functional

### **📊 Performance Metrics:**
- **Database size**: Should be under 1GB (metadata only)
- **Photo loading**: Fast thumbnail display from Drive
- **API response**: Under 200ms for most endpoints
- **Frontend**: Smooth navigation and photo display

## 🚨 **Troubleshooting**

### **Common Issues:**
1. **Port conflicts**: Check if ports 8000, 5173, 5678 are free
2. **Database connection**: Ensure PostgreSQL is running
3. **Drive authentication**: Check OAuth2 credentials
4. **Frontend build**: Ensure React app is built properly

### **Debug Commands:**
```bash
# Check running processes
ps aux | grep -E "(python|node|n8n)" | grep -v grep

# Check port usage
netstat -tlnp | grep -E "(8000|5173|5678)"

# Check logs
tail -f backend.log  # Backend logs
tail -f n8n.log     # n8n logs
```

## 🎉 **Success Criteria**

### **System is working when:**
- ✅ **All services** running without errors
- ✅ **Frontend** displays vehicles and photos
- ✅ **Backend** responds to all API calls
- ✅ **Database** stores metadata efficiently
- ✅ **Drive** stores photos in organized folders
- ✅ **n8n** executes workflows successfully
- ✅ **Complete integration** working end-to-end

## 📈 **Next Steps After Testing**

1. **Fix any issues** found during testing
2. **Optimize performance** if needed
3. **Deploy to GitHub Codespaces** for production
4. **Configure production** environment variables
5. **Set up monitoring** and health checks

This testing guide ensures your optimized Autosell.mx system is working perfectly with the new Google Drive + Database architecture! 🚀
