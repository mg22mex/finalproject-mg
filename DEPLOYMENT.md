# 🚀 Autosell.mx - Production Deployment Guide
## Complete Deployment Documentation for Render Cloud Platform

---

## 📋 **DEPLOYMENT OVERVIEW**

This document provides complete instructions for deploying the Autosell.mx system to Render cloud platform. The system consists of four main services:

1. **Backend API** - FastAPI application with PostgreSQL database
2. **Frontend** - React static site
3. **n8n Automation** - Docker container with workflow automation
4. **Database** - PostgreSQL instance

---

## 🌐 **LIVE PRODUCTION URLS**

### **Deployed Services:**
- **Frontend Dashboard**: [https://autosell-frontend.onrender.com](https://autosell-frontend.onrender.com)
- **Backend API**: [https://autosell-backend.onrender.com](https://autosell-backend.onrender.com)
- **n8n Automation**: [https://autosell-n8n.onrender.com](https://autosell-n8n.onrender.com)
- **API Documentation**: [https://autosell-backend.onrender.com/docs](https://autosell-backend.onrender.com)

---

## 🛠️ **DEPLOYMENT ARCHITECTURE**

### **Service Configuration:**

#### **Backend Service (autosell-backend)**
- **Type**: Web Service
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python main_fixed.py`
- **Health Check**: `/health`
- **Plan**: Free

#### **Frontend Service (autosell-frontend)**
- **Type**: Static Site
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- **Plan**: Free

#### **n8n Service (autosell-n8n)**
- **Type**: Web Service
- **Runtime**: Docker
- **Dockerfile**: `./Dockerfile.n8n`
- **Plan**: Free

#### **Database (autosell-db)**
- **Type**: PostgreSQL
- **Plan**: Free
- **Database Name**: `autosell`
- **User**: `autosell_user`

---

## 🔧 **ENVIRONMENT VARIABLES**

### **Backend Service Environment Variables:**
```bash
DATABASE_URL=postgresql://autosell_user:[password]@[host]:[port]/autosell
PYTHON_VERSION=3.11.0
PORT=10000
CORS_ORIGINS=http://localhost:3000,https://autosell-frontend.onrender.com
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,finalproject-mg.onrender.com,*.onrender.com
```

### **Frontend Service Environment Variables:**
```bash
VITE_API_URL=https://autosell-backend.onrender.com
```

### **n8n Service Environment Variables:**
```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=[secure_password]
WEBHOOK_URL=https://autosell-n8n.onrender.com
GENERIC_TIMEZONE=America/Mexico_City
```

---

## 📁 **DEPLOYMENT FILES**

### **render.yaml**
```yaml
services:
  - type: web
    name: autosell-backend
    env: python
    plan: free
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && python main_fixed.py
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: autosell-db
          property: connectionString
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: PORT
        value: 10000
      - key: CORS_ORIGINS
        value: "http://localhost:3000,https://autosell-frontend.onrender.com"
      - key: ALLOWED_HOSTS
        value: "localhost,127.0.0.1,0.0.0.0,finalproject-mg.onrender.com,*.onrender.com"
    healthCheckPath: /health

  - type: static
    name: autosell-frontend
    plan: free
    buildCommand: cd frontend && npm install && npm run build
    publishPath: frontend/dist
    envVars:
      - key: VITE_API_URL
        value: https://autosell-backend.onrender.com

  - type: web
    name: autosell-n8n
    env: docker
    plan: free
    dockerfilePath: ./Dockerfile.n8n
    envVars:
      - key: N8N_BASIC_AUTH_ACTIVE
        value: "true"
      - key: N8N_BASIC_AUTH_USER
        value: "admin"
      - key: N8N_BASIC_AUTH_PASSWORD
        generateValue: true
      - key: WEBHOOK_URL
        value: "https://autosell-n8n.onrender.com"
      - key: GENERIC_TIMEZONE
        value: "America/Mexico_City"

databases:
  - name: autosell-db
    plan: free
    databaseName: autosell
    user: autosell_user
```

### **Dockerfile.n8n**
```dockerfile
# Dockerfile.n8n
FROM n8nio/n8n:latest

# Set environment variables for n8n
ENV N8N_HOST=0.0.0.0
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=http
ENV N8N_PATH=/
ENV N8N_EDITOR_BASE_URL=http://localhost:5678/
ENV N8N_BASIC_AUTH_ACTIVE=true
ENV N8N_BASIC_AUTH_USER=admin
# This should be overridden by Render env var
ENV N8N_BASIC_AUTH_PASSWORD=AutosellN8n2025!

# Expose the port n8n runs on
EXPOSE 5678

# Use the default entrypoint from the base image
# The n8nio/n8n image already has the correct entrypoint configured
```

---

## 🚀 **DEPLOYMENT STEPS**

### **Step 1: Render Account Setup**
1. Create account at [render.com](https://render.com)
2. Connect GitHub repository: `mg22mex/finalproject-mg`
3. Ensure repository is public or connected via GitHub integration

### **Step 2: Database Deployment**
1. Create new PostgreSQL database
2. Name: `autosell-db`
3. Plan: Free
4. Note the connection string for backend configuration

### **Step 3: Backend Service Deployment**
1. Create new Web Service
2. Connect to GitHub repository
3. Configure as Python service
4. Set build and start commands
5. Add environment variables
6. Deploy and test

### **Step 4: Frontend Service Deployment**
1. Create new Static Site
2. Connect to GitHub repository
3. Configure build settings
4. Add environment variables
5. Deploy and test

### **Step 5: n8n Service Deployment**
1. Create new Web Service
2. Configure as Docker service
3. Set Dockerfile path
4. Add environment variables
5. Deploy and test

### **Step 6: Service Integration Testing**
1. Test backend API endpoints
2. Test frontend-backend communication
3. Test n8n automation platform
4. Verify database connectivity
5. Test all integrations

---

## 🔍 **TROUBLESHOOTING**

### **Common Issues and Solutions:**

#### **Frontend Build Failures**
- **Issue**: npm workspace conflicts
- **Solution**: Remove backend from workspaces in package.json
- **Fix**: Update build command to `cd frontend && npm install && npm run build`

#### **Backend Host Header Errors**
- **Issue**: "Invalid host header" error
- **Solution**: Configure ALLOWED_HOSTS environment variable
- **Fix**: Add Render domain to allowed hosts list

#### **n8n Command Not Found**
- **Issue**: "Command n8n not found" error
- **Solution**: Use default entrypoint from n8nio/n8n image
- **Fix**: Remove custom CMD from Dockerfile

#### **Database Connection Issues**
- **Issue**: Database connection failures
- **Solution**: Verify DATABASE_URL environment variable
- **Fix**: Ensure connection string is properly formatted

---

## 📊 **MONITORING AND MAINTENANCE**

### **Health Checks:**
- **Backend**: `https://autosell-backend.onrender.com/health`
- **Frontend**: `https://autosell-frontend.onrender.com`
- **n8n**: `https://autosell-n8n.onrender.com`

### **Logs Access:**
- Access logs through Render dashboard
- Monitor deployment status
- Check error logs for troubleshooting

### **Performance Monitoring:**
- Monitor service uptime
- Check response times
- Monitor database performance
- Track automation workflow execution

---

## 🔐 **SECURITY CONSIDERATIONS**

### **Environment Variables:**
- All sensitive data stored in environment variables
- Database credentials secured
- API keys properly managed
- CORS origins restricted to production domains

### **Authentication:**
- n8n basic authentication enabled
- Facebook OAuth properly configured
- Google API credentials secured
- Database access restricted

### **HTTPS/SSL:**
- All services use HTTPS
- SSL certificates automatically managed by Render
- Secure communication between services

---

## 📈 **SCALING CONSIDERATIONS**

### **Free Tier Limitations:**
- Services may spin down after inactivity
- Limited CPU and memory resources
- Database connection limits
- File storage limitations

### **Upgrade Options:**
- Upgrade to paid plans for better performance
- Add more resources as needed
- Implement caching strategies
- Optimize database queries

---

## 🎯 **SUCCESS METRICS**

### **Deployment Success Indicators:**
- ✅ All services deployed and accessible
- ✅ Database connectivity established
- ✅ Frontend-backend communication working
- ✅ n8n automation platform operational
- ✅ Facebook integration active
- ✅ Google services connected
- ✅ SSL certificates enabled
- ✅ Environment variables configured

---

## 📞 **SUPPORT AND MAINTENANCE**

### **Render Platform Support:**
- Documentation: [render.com/docs](https://render.com/docs)
- Community: [community.render.com](https://community.render.com)
- Status: [status.render.com](https://status.render.com)

### **Application Support:**
- GitHub Repository: [github.com/mg22mex/finalproject-mg](https://github.com/mg22mex/finalproject-mg)
- Documentation: See README.md and other project documentation
- Issues: Report via GitHub Issues

---

*This deployment guide ensures the Autosell.mx system is properly deployed and maintained on the Render cloud platform.*
