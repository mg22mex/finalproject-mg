# 🚗 Autosell.mx - Quick Setup Guide
## Get Your Development Environment Running in 5 Minutes

---

## 🚀 **Quick Start (5 minutes)**

### **1. Prerequisites Check**
```bash
# Check if you have the required tools
node --version    # Should be 18+
npm --version     # Should be 9+
python --version  # Should be 3.9+
docker --version  # Should be installed
docker-compose --version  # Should be installed
```

### **2. Clone & Setup**
```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd autosell-mx

# Install all dependencies
npm run install:all

# Copy environment template
cp env.example .env

# Edit .env with your API keys
nano .env
```

### **3. Start Development Environment**
```bash
# Start all services (PostgreSQL, Redis, n8n)
npm run start

# In a new terminal, start development servers
npm run dev:all
```

### **4. Access Your Services**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **n8n:** http://localhost:5678 (admin/autosell123)
- **Database:** localhost:5432
- **Redis:** localhost:6379

---

## 🔧 **Manual Setup (Step by Step)**

### **Step 1: Environment Configuration**
```bash
# Copy environment template
cp env.example .env

# Edit with your actual values
nano .env
```

**Required Environment Variables:**
- `GOOGLE_SHEET_ID` - Your Google Sheets ID
- `GOOGLE_DRIVE_FOLDER_ID` - Your Google Drive folder ID
- `FACEBOOK_ACCESS_TOKEN` - Your Facebook API token
- `JWT_SECRET_KEY` - Random secret for JWT tokens

### **Step 2: Database Setup**
```bash
# Start PostgreSQL
npm run db:setup

# Run database migrations
npm run db:migrate

# Seed with sample data
npm run db:seed
```

### **Step 3: Google API Setup**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API and Google Drive API
4. Create service account credentials
5. Download `google-credentials.json`
6. Place in `credentials/` folder

### **Step 4: Social Media API Setup**
1. **Facebook:** Create app in Meta Developers
2. **Instagram:** Set up Basic Display API
3. **Twitter:** Create app in Twitter Developer Portal
4. Add all tokens to `.env` file

---

## 🐳 **Docker Services**

### **Service Overview:**
- **PostgreSQL:** Main database (port 5432)
- **Redis:** Caching and sessions (port 6379)
- **n8n:** Workflow automation (port 5678)
- **Backend:** FastAPI server (port 8000)
- **Frontend:** React app (port 3000)
- **Prometheus:** Metrics (port 9090)
- **Grafana:** Dashboards (port 3001)

### **Useful Docker Commands:**
```bash
# View all services
docker-compose ps

# View logs
npm run logs

# Restart specific service
docker-compose restart postgres

# Stop all services
npm run stop

# Clean up (removes volumes)
npm run clean
```

---

## 📱 **Frontend Development**

### **Start Frontend Only:**
```bash
cd frontend
npm run dev
```

### **Frontend Features:**
- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- React Hook Form for forms
- Zustand for state management

### **Available Scripts:**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run test         # Run tests
npm run lint         # Lint code
npm run format       # Format code
```

---

## 🐍 **Backend Development**

### **Start Backend Only:**
```bash
cd backend
npm run dev
```

### **Backend Features:**
- FastAPI with Python 3.9+
- PostgreSQL with SQLAlchemy
- Redis for caching
- JWT authentication
- Comprehensive API documentation

### **Available Scripts:**
```bash
npm run dev          # Start with auto-reload
npm run test         # Run tests
npm run lint         # Lint code
npm run format       # Format code
npm run db:migrate   # Run database migrations
npm run db:seed      # Seed database
```

---

## 🤖 **n8n Workflow Automation**

### **Access n8n:**
- **URL:** http://localhost:5678
- **Username:** admin
- **Password:** autosell123

### **Pre-built Workflows:**
1. **Daily Vehicle Sync** - Syncs Google Sheets data
2. **Facebook Marketplace Repost** - Daily reposting
3. **Social Media Posting** - Multi-platform posting
4. **Status Change Handler** - Automatic status updates

### **Workflow Location:**
- **Workflows:** `./workflows/`
- **Templates:** `./workflows/templates/`

---

## 🧪 **Testing**

### **Run All Tests:**
```bash
npm run test
```

### **Test Coverage:**
```bash
npm run test:coverage
```

### **Frontend Tests:**
```bash
cd frontend
npm run test
npm run test:coverage
```

### **Backend Tests:**
```bash
cd backend
npm run test
npm run test:coverage
```

---

## 📊 **Monitoring & Analytics**

### **Prometheus Metrics:**
- **URL:** http://localhost:9090
- **Metrics:** API performance, database queries, automation workflows

### **Grafana Dashboards:**
- **URL:** http://localhost:3001
- **Username:** admin
- **Password:** admin123
- **Dashboards:** System performance, business metrics

---

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **Database Connection Failed:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Reset database
npm run db:reset
```

#### **Port Already in Use:**
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### **Dependencies Installation Failed:**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
rm -rf node_modules package-lock.json
npm install
```

#### **Python Virtual Environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install requirements
pip install -r backend/requirements.txt
```

---

## 📚 **Next Steps**

### **After Setup:**
1. **Configure APIs** - Add your actual API keys
2. **Test Endpoints** - Visit http://localhost:8000/docs
3. **Create Workflows** - Set up n8n automation
4. **Add Vehicles** - Test the complete system
5. **Customize** - Modify for your specific needs

### **Development Workflow:**
1. **Make Changes** - Edit code in frontend/ or backend/
2. **Auto-reload** - Changes appear automatically
3. **Test** - Run tests to ensure quality
4. **Commit** - Save your progress

---

## 🆘 **Need Help?**

### **Documentation:**
- [Technical README](README.md)
- [Business Overview](BUSINESS_OVERVIEW.md)
- [User Stories](USER_STORIES.md)
- [Work Tickets](WORK_TICKETS.md)

### **Support:**
- Check logs: `npm run logs`
- View health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

---

**🎉 You're all set! Your Autosell.mx development environment is ready to go!**

**Start building amazing vehicle management automation!** 🚗✨
