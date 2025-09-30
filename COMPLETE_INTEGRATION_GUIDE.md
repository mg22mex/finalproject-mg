# 🔄 Complete Integration Guide

## 🎯 **System Overview**

Autosell.mx features a complete integration system that automates vehicle management across multiple platforms:

- **Frontend** → **Database** → **Google Sheets** → **Facebook**
- **Google Sheets** → **Database** → **Autosell.mx** → **Facebook**
- **Scheduled Sync** → **Status Monitoring** → **Automatic Actions**

## 🏗️ **Architecture Diagram**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   n8n          │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (Automation)  │
│                 │    │                 │    │                 │
│ Add Vehicle     │    │ Store Data      │    │ Process Data    │
│ Edit Vehicle    │    │ API Endpoints  │    │ Sync Sheets     │
│ Delete Vehicle  │    │ Database       │    │ Post Facebook   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User          │    │   PostgreSQL    │    │   Google Sheets │
│   Interface     │    │   Database      │    │   + Facebook    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 **Integration Flows**

### **Flow 1: Add Vehicle (Frontend → All Systems)**

```mermaid
graph TD
    A[User Adds Vehicle] --> B[Frontend Form]
    B --> C[Backend API]
    C --> D[Database Storage]
    C --> E[n8n Webhook]
    E --> F[Google Sheets Update]
    E --> G[Facebook Post]
    F --> H[Inventory Updated]
    G --> I[Marketplace Post]
```

**Steps**:
1. **User** adds vehicle in frontend
2. **Frontend** sends data to backend API
3. **Backend** stores vehicle in database
4. **Backend** triggers n8n webhook
5. **n8n** updates Google Sheets
6. **n8n** posts to Facebook Marketplace

### **Flow 2: Status Change (Google Sheets → Actions)**

```mermaid
graph TD
    A[User Changes Status] --> B[Google Sheets]
    B --> C[Scheduled Sync]
    C --> D[n8n Workflow]
    D --> E[Backend API]
    E --> F[Database Update]
    D --> G{Status = Vendido?}
    G -->|Yes| H[Remove from Autosell]
    G -->|Yes| I[Remove from Facebook]
    G -->|No| J[No Action]
```

**Steps**:
1. **User** changes vehicle status to "Vendido" in Google Sheets
2. **Scheduled sync** (every 30 minutes) detects change
3. **n8n** updates backend database
4. **n8n** checks if status = "Vendido"
5. **n8n** removes vehicle from Autosell.mx
6. **n8n** removes vehicle from Facebook

### **Flow 3: Complete Processing Pipeline**

```mermaid
graph TD
    A[Vehicle Data] --> B[Frontend Processing]
    B --> C[Backend Storage]
    C --> D[Google Sheets Sync]
    C --> E[Facebook Posting]
    D --> F[Inventory Management]
    E --> G[Marketplace Listing]
    F --> H[Status Monitoring]
    H --> I[Automatic Actions]
```

## 🛠️ **Technical Implementation**

### **Frontend Integration**

#### **Add Vehicle with Full Automation**
```typescript
// Frontend service
const addVehicle = async (vehicleData: VehicleData) => {
  // Step 1: Save to database
  const response = await fetch('/api/vehicles', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(vehicleData)
  });
  
  // Step 2: Trigger complete processing
  const processingResponse = await fetch('/api/frontend/complete-vehicle-processing', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(vehicleData)
  });
  
  return processingResponse.json();
};
```

#### **Update Vehicle Status**
```typescript
// Frontend service
const updateVehicleStatus = async (vehicleId: string, status: string) => {
  const response = await fetch(`/api/vehicles/${vehicleId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ estatus: status })
  });
  
  // If status is "VENDIDO", trigger removal
  if (status === 'VENDIDO') {
    await fetch(`/api/vehicles/${vehicleId}/remove-from-autosell`, {
      method: 'POST'
    });
    await fetch(`/api/vehicles/${vehicleId}/remove-from-facebook`, {
      method: 'POST'
    });
  }
  
  return response.json();
};
```

### **Backend API Integration**

#### **Complete Vehicle Processing Endpoint**
```python
@router.post("/frontend/complete-vehicle-processing")
async def complete_vehicle_processing(
    vehicle_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Complete vehicle processing: Database → Google Sheets → Facebook
    """
    try:
        # Step 1: Save to database (already done by frontend)
        # Step 2: Sync to Google Sheets
        sheets_response = await sync_vehicle_to_sheets(vehicle_data, db)
        
        # Step 3: Post to Facebook
        facebook_response = await post_vehicle_to_facebook(vehicle_data, db)
        
        return {
            "message": "Vehicle processing completed successfully",
            "google_sheets": sheets_response,
            "facebook": facebook_response,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in complete processing: {str(e)}"
        )
```

#### **Google Sheets Sync Endpoint**
```python
@router.post("/vehicles/sync-from-sheets")
async def sync_vehicles_from_sheets(
    vehicles: List[dict],
    db: Session = Depends(get_db)
):
    """
    Sync vehicles from Google Sheets to backend database
    """
    try:
        # Clear existing Google Sheets vehicles
        existing_gs_vehicles = db.query(Vehicle).filter(
            Vehicle.external_id.like('GS_%')
        ).all()
        
        for vehicle in existing_gs_vehicles:
            db.delete(vehicle)
        
        # Add new vehicles from Google Sheets
        synced_count = 0
        for vehicle_data in vehicles:
            vehicle = Vehicle(
                external_id=vehicle_data.get('external_id'),
                marca=vehicle_data.get('marca', ''),
                modelo=vehicle_data.get('modelo', ''),
                año=vehicle_data.get('año'),
                color=vehicle_data.get('color', ''),
                precio=vehicle_data.get('precio', 0),
                kilometraje=vehicle_data.get('kilometraje', ''),
                estatus=VehicleStatus(vehicle_data.get('estatus', 'DISPONIBLE')),
                ubicacion=vehicle_data.get('ubicacion', ''),
                descripcion=vehicle_data.get('descripcion', '')
            )
            
            db.add(vehicle)
            synced_count += 1
        
        db.commit()
        
        return {
            "message": f"Successfully synced {synced_count} vehicles from Google Sheets",
            "synced_count": synced_count,
            "total_vehicles": len(vehicles)
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error syncing vehicles: {str(e)}"
        )
```

### **n8n Workflow Integration**

#### **Google Sheets to Backend Sync Workflow**
```json
{
  "name": "Google Sheets to Backend Sync",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "sync-from-sheets"
      },
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook"
    },
    {
      "parameters": {
        "authentication": "oAuth2",
        "resource": "spreadsheet",
        "operation": "read",
        "documentId": "YOUR_GOOGLE_SHEET_ID",
        "sheetName": "Inventario a web"
      },
      "name": "Read Google Sheets",
      "type": "n8n-nodes-base.googleSheets"
    },
    {
      "parameters": {
        "url": "http://127.0.0.1:8000/vehicles/sync-from-sheets",
        "requestMethod": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            {
              "name": "vehicles",
              "value": "={{ $json }}"
            }
          ]
        }
      },
      "name": "Sync to Backend",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

#### **Scheduled Sync Workflow**
```json
{
  "name": "Scheduled Google Sheets Sync",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "minutes",
              "minutesInterval": 30
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger"
    },
    {
      "parameters": {
        "authentication": "oAuth2",
        "resource": "spreadsheet",
        "operation": "read",
        "documentId": "YOUR_GOOGLE_SHEET_ID",
        "sheetName": "Inventario a web"
      },
      "name": "Read Google Sheets",
      "type": "n8n-nodes-base.googleSheets"
    },
    {
      "parameters": {
        "conditions": {
          "conditions": [
            {
              "leftValue": "={{ $json.estatus }}",
              "rightValue": "Vendido",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ]
        }
      },
      "name": "Check Sold Status",
      "type": "n8n-nodes-base.if"
    },
    {
      "parameters": {
        "url": "http://127.0.0.1:8000/vehicles/{{ $json.external_id }}/remove-from-autosell",
        "requestMethod": "POST"
      },
      "name": "Remove from Autosell",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "parameters": {
        "url": "http://127.0.0.1:8000/vehicles/{{ $json.external_id }}/remove-from-facebook",
        "requestMethod": "POST"
      },
      "name": "Remove from Facebook",
      "type": "n8n-nodes-base.httpRequest"
    }
  ]
}
```

## 🧪 **Testing Integration**

### **Test Complete Flow**
```bash
# Test complete vehicle processing
curl -X POST http://localhost:8000/frontend/complete-vehicle-processing \
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

### **Test Google Sheets Sync**
```bash
# Test manual sync
curl -X POST http://localhost:8000/frontend/trigger-sheets-sync
```

### **Test Status Change**
```bash
# Test vehicle removal
curl -X POST http://localhost:8000/vehicles/1/remove-from-autosell
curl -X POST http://localhost:8000/vehicles/1/remove-from-facebook
```

## 📊 **Data Flow Mapping**

### **Frontend → Backend → Google Sheets**
| Frontend Field | Backend Field | Google Sheets Column |
|----------------|---------------|---------------------|
| `marca` | `marca` | `Marca` |
| `modelo` | `modelo` | `Modelo` |
| `año` | `año` | `Año` |
| `color` | `color` | `Color` |
| `precio` | `precio` | `Precio` |
| `kilometraje` | `kilometraje` | `km` |
| `estatus` | `estatus` | `Estatus` |
| `ubicacion` | `ubicacion` | `Ubicacion` |

### **Google Sheets → Backend → Actions**
| Google Sheets Status | Backend Status | Action |
|---------------------|----------------|--------|
| `Disponible` | `DISPONIBLE` | No action |
| `Vendido` | `VENDIDO` | Remove from Autosell + Facebook |
| `Apartado` | `APARTADO` | No action |
| `Ausente` | `AUSENTE` | No action |

## 🔍 **Monitoring and Debugging**

### **Integration Health Checks**
```bash
# Check backend health
curl http://localhost:8000/health

# Check n8n health
curl http://localhost:5678/

# Check frontend health
curl http://localhost:3000/
```

### **Workflow Execution Monitoring**
1. **n8n Dashboard**: http://localhost:5678
2. **Executions Tab**: View workflow execution history
3. **Individual Executions**: Click to see detailed logs
4. **Error Handling**: Red nodes indicate errors

### **Database Monitoring**
```sql
-- Check vehicle counts
SELECT estatus, COUNT(*) FROM vehicles GROUP BY estatus;

-- Check recent vehicles
SELECT * FROM vehicles ORDER BY created_at DESC LIMIT 10;

-- Check external IDs
SELECT external_id, COUNT(*) FROM vehicles WHERE external_id LIKE 'GS_%' GROUP BY external_id;
```

## 🚀 **Production Deployment**

### **Environment Configuration**
```env
# Backend
DATABASE_URL=postgresql://user:password@localhost/autosell
SECRET_KEY=your-secret-key

# Frontend
VITE_API_URL=https://your-backend-url.com
VITE_N8N_URL=https://your-n8n-url.com

# n8n
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your-secure-password
N8N_ENCRYPTION_KEY=your-encryption-key
```

### **Security Considerations**
- **HTTPS**: Use HTTPS for all production URLs
- **Authentication**: Implement proper authentication
- **Rate Limiting**: Add rate limiting to prevent abuse
- **Monitoring**: Set up monitoring and alerting

## 🎯 **Success Indicators**

### **✅ Complete Integration Working**
- [ ] Frontend can add vehicles
- [ ] Backend stores vehicles in database
- [ ] Google Sheets syncs automatically
- [ ] Facebook posts automatically
- [ ] Status changes trigger actions
- [ ] Scheduled sync runs every 30 minutes
- [ ] All workflows execute successfully

### **✅ Data Consistency**
- [ ] Frontend data matches database
- [ ] Database data matches Google Sheets
- [ ] Status changes are reflected everywhere
- [ ] No data loss during sync

### **✅ Automation Working**
- [ ] New vehicles appear in Google Sheets
- [ ] New vehicles are posted to Facebook
- [ ] Status changes trigger removals
- [ ] Scheduled sync updates database

---

**Your complete integration system is ready for production!** 🚀
