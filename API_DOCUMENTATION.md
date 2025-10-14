# 📚 Autosell.mx API Documentation

## 🎯 **Overview**

The Autosell.mx API provides comprehensive vehicle management and automation capabilities through RESTful endpoints. The API is built with FastAPI and provides automatic documentation at `/docs`.

## 🔗 **Base URLs**

- **Development**: `http://localhost:8001`
- **Production**: `https://your-backend-url.com`
- **API Documentation**: `http://localhost:8001/docs`
- **Current Status**: Backend running on port 8001 with 133 vehicles imported

## 🔐 **Authentication**

Currently, the API does not require authentication for development. In production, implement proper authentication mechanisms.

## 📊 **Core Endpoints**

### **Vehicle Management**

#### **Get All Vehicles**
```http
GET /vehicles/
```

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Number of records to return (default: 100, max: 1000)
- `marca` (string, optional): Filter by brand
- `modelo` (string, optional): Filter by model
- `año` (int, optional): Filter by year
- `estatus` (string, optional): Filter by status
- `precio_min` (float, optional): Minimum price
- `precio_max` (float, optional): Maximum price
- `search` (string, optional): Search in marca, modelo, descripcion

**Response:**
```json
{
  "vehicles": [
    {
      "id": 1,
      "external_id": "GS_TOYOTA_2020_abc123",
      "marca": "Toyota",
      "modelo": "Camry",
      "año": 2020,
      "color": "Blanco",
      "precio": 250000.0,
      "kilometraje": "45,000 km",
      "estatus": "DISPONIBLE",
      "ubicacion": "CDMX",
      "descripcion": "Toyota Camry 2020",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "is_available": true,
      "is_sold": false
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### **Get Vehicle by ID**
```http
GET /vehicles/{vehicle_id}
```

**Response:**
```json
{
  "id": 1,
  "external_id": "GS_TOYOTA_2020_abc123",
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 250000.0,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX",
  "descripcion": "Toyota Camry 2020",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_available": true,
  "is_sold": false
}
```

#### **Create Vehicle**
```http
POST /vehicles/
```

**Request Body:**
```json
{
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 250000.0,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX",
  "descripcion": "Toyota Camry 2020"
}
```

**Response:**
```json
{
  "id": 1,
  "external_id": null,
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 250000.0,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX",
  "descripcion": "Toyota Camry 2020",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "is_available": true,
  "is_sold": false
}
```

#### **Update Vehicle**
```http
PUT /vehicles/{vehicle_id}
```

**Request Body:**
```json
{
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 240000.0,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX",
  "descripcion": "Toyota Camry 2020 - Price Reduced"
}
```

#### **Delete Vehicle**
```http
DELETE /vehicles/{vehicle_id}
```

**Response:**
```json
{
  "message": "Vehicle deleted successfully",
  "vehicle_id": 1
}
```

## 🔄 **Google Sheets Integration**

### **Sync from Google Sheets**
```http
POST /vehicles/sync-from-sheets
```

**Request Body:**
```json
[
  {
    "external_id": "GS_TOYOTA_2020_abc123",
    "marca": "Toyota",
    "modelo": "Camry",
    "año": 2020,
    "color": "Blanco",
    "precio": 250000,
    "kilometraje": "45,000 km",
    "estatus": "DISPONIBLE",
    "ubicacion": "CDMX",
    "descripcion": "Toyota Camry 2020"
  }
]
```

**Response:**
```json
{
  "message": "Successfully synced 1 vehicles from Google Sheets",
  "synced_count": 1,
  "total_vehicles": 1
}
```

## 🤖 **Frontend Integration**

### **Sync Vehicle to Google Sheets**
```http
POST /frontend/sync-to-sheets
```

**Request Body:**
```json
{
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 250000,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX"
}
```

**Response:**
```json
{
  "message": "Vehicle synced to Google Sheets successfully",
  "status": "success"
}
```

### **Post Vehicle to Facebook**
```http
POST /frontend/post-to-facebook
```

**Request Body:**
```json
{
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 250000,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX"
}
```

**Response:**
```json
{
  "message": "Vehicle posted to Facebook successfully",
  "status": "success"
}
```

### **Complete Vehicle Processing**
```http
POST /frontend/complete-vehicle-processing
```

**Request Body:**
```json
{
  "marca": "Toyota",
  "modelo": "Camry",
  "año": 2020,
  "color": "Blanco",
  "precio": 250000,
  "kilometraje": "45,000 km",
  "estatus": "DISPONIBLE",
  "ubicacion": "CDMX"
}
```

**Response:**
```json
{
  "message": "Vehicle processing completed successfully",
  "google_sheets": {
    "message": "Vehicle synced to Google Sheets successfully",
    "status": "success"
  },
  "facebook": {
    "message": "Vehicle posted to Facebook successfully",
    "status": "success"
  },
  "status": "success"
}
```

### **Trigger Google Sheets Sync**
```http
POST /frontend/trigger-sheets-sync
```

**Request Body:**
```json
{
  "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
}
```

**Response:**
```json
{
  "message": "Google Sheets sync triggered successfully",
  "status": "success"
}
```

## 🗑️ **Vehicle Removal**

### **Remove from Autosell.mx**
```http
POST /vehicles/{vehicle_identifier}/remove-from-autosell
```

**Parameters:**
- `vehicle_identifier`: Vehicle ID or external_id

**Response:**
```json
{
  "message": "Vehicle 1 removed from Autosell.mx",
  "vehicle_id": 1,
  "status": "removed"
}
```

### **Remove from Facebook**
```http
POST /vehicles/{vehicle_identifier}/remove-from-facebook
```

**Parameters:**
- `vehicle_identifier`: Vehicle ID or external_id

**Response:**
```json
{
  "message": "Vehicle 1 marked for Facebook deletion",
  "vehicle_id": 1,
  "status": "marked_for_deletion"
}
```

## 📊 **Health and Status**

### **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Autosell.mx API",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### **API Information**
```http
GET /
```

**Response:**
```json
{
  "message": "Welcome to Autosell.mx API",
  "version": "1.0.0",
  "description": "Complete Vehicle Management & Automation System",
  "docs": "/docs",
  "health": "/health",
  "api_endpoints": {
    "vehicles": "/vehicles",
    "health": "/health",
    "openapi": "/openapi.json"
  }
}
```

## 🔍 **Search and Filtering**

### **Search Vehicles**
```http
GET /vehicles/?search=toyota
```

### **Filter by Brand**
```http
GET /vehicles/?marca=Toyota
```

### **Filter by Price Range**
```http
GET /vehicles/?precio_min=200000&precio_max=300000
```

### **Filter by Status**
```http
GET /vehicles/?estatus=DISPONIBLE
```

### **Combined Filters**
```http
GET /vehicles/?marca=Toyota&año=2020&precio_min=200000&search=camry
```

## 📝 **Data Models**

### **Vehicle Object**
```json
{
  "id": "integer",
  "external_id": "string (nullable)",
  "marca": "string",
  "modelo": "string",
  "año": "integer",
  "color": "string",
  "precio": "number",
  "kilometraje": "string",
  "estatus": "enum (DISPONIBLE, FOTOS, AUSENTE, APARTADO, VENDIDO)",
  "ubicacion": "string",
  "descripcion": "string",
  "caracteristicas": "object (nullable)",
  "created_at": "datetime",
  "updated_at": "datetime",
  "created_by": "string (nullable)",
  "updated_by": "string (nullable)",
  "photo_count": "integer",
  "is_available": "boolean",
  "is_sold": "boolean",
  "is_reserved": "boolean",
  "is_temporarily_unavailable": "boolean"
}
```

### **Vehicle Status Enum**
```json
{
  "DISPONIBLE": "Available for sale",
  "FOTOS": "Photos being taken",
  "AUSENTE": "Temporarily unavailable",
  "APARTADO": "Reserved",
  "VENDIDO": "Sold"
}
```

## 🚨 **Error Handling**

### **Common Error Responses**

#### **400 Bad Request**
```json
{
  "detail": "Validation error: Invalid input data"
}
```

#### **404 Not Found**
```json
{
  "detail": "Vehicle with id 999 not found"
}
```

#### **500 Internal Server Error**
```json
{
  "detail": "Internal server error while processing request"
}
```

### **Error Codes**
- `400`: Bad Request - Invalid input data
- `404`: Not Found - Resource not found
- `422`: Unprocessable Entity - Validation error
- `500`: Internal Server Error - Server error

## 🧪 **Testing**

### **Test Endpoints**
```bash
# Health check
curl http://localhost:8001/health

# Get all vehicles (133 vehicles available)
curl http://localhost:8001/vehicles/

# Create vehicle
curl -X POST http://localhost:8001/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{"marca": "Toyota", "modelo": "Camry", "año": 2020}'

# Test Google Sheets sync
curl -X POST http://localhost:8001/frontend/trigger-sheets-sync

# Get dashboard stats
curl http://localhost:8001/dashboard/stats
```

### **Integration Tests**
```bash
# Run complete integration tests
python test_complete_integration.py
```

## 📚 **Additional Resources**

- **Interactive API Docs**: http://localhost:8001/docs
- **OpenAPI Schema**: http://localhost:8001/openapi.json
- **ReDoc Documentation**: http://localhost:8001/redoc
- **Current Status**: API fully operational with 133 vehicles imported

## 🔄 **Rate Limiting**

Currently, no rate limiting is implemented. For production, consider implementing rate limiting to prevent abuse.

## 🛡️ **Security Considerations**

- **Input Validation**: All inputs are validated using Pydantic schemas
- **SQL Injection**: Protected by SQLAlchemy ORM
- **CORS**: Configured for cross-origin requests
- **HTTPS**: Recommended for production deployment

---

**For more information, visit the interactive API documentation at `/docs`** 📚
