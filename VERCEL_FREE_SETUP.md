# 🆓 Vercel Free Setup for Autosell.mx

## 🎯 **Why Vercel is Perfect for You**

- **✅ Completely FREE FOREVER**
- **✅ No time limits**
- **✅ No credit card required**
- **✅ No payment surprises**
- **✅ Perfect for React + FastAPI**
- **✅ Automatic deployments**
- **✅ Custom domains included**

## 🚀 **Step-by-Step Setup**

### **Step 1: Create Vercel Account**
1. Go to: https://vercel.com
2. Click **"Sign up"**
3. **Sign up with GitHub** (recommended)
4. **No credit card required!**

### **Step 2: Deploy Frontend (React)**

#### **2.1 Connect Repository**
1. **Click "New Project"**
2. **Import Git Repository**
3. **Select `finalproject-mg`**
4. **Choose "frontend" folder**
5. **Vercel will auto-detect React**

#### **2.2 Configure Build Settings**
```bash
# Build Command
npm run build

# Output Directory
dist

# Install Command
npm install
```

#### **2.3 Environment Variables**
```bash
VITE_API_URL=https://autosell-backend.vercel.app
```

### **Step 3: Deploy Backend (FastAPI)**

#### **3.1 Convert to Vercel Functions**
Create `api/index.py`:
```python
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Vercel handler
handler = Mangum(app)
```

#### **3.2 Create `vercel.json`**
```json
{
  "functions": {
    "api/index.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

#### **3.3 Deploy Backend**
1. **Click "New Project"**
2. **Import Git Repository**
3. **Select `finalproject-mg`**
4. **Choose "backend" folder**
5. **Vercel will auto-detect Python**

### **Step 4: Setup Supabase Database (Free)**

#### **4.1 Create Supabase Account**
1. Go to: https://supabase.com
2. **Sign up with GitHub**
3. **No credit card required!**

#### **4.2 Create New Project**
1. **Click "New Project"**
2. **Choose organization**
3. **Enter project name**: `autosell-mx`
4. **Choose region**: `US East`
5. **Click "Create new project"**

#### **4.3 Get Database URL**
1. **Go to Settings → Database**
2. **Copy "Connection string"**
3. **Update backend environment variables**

### **Step 5: Self-Host n8n (Free)**

#### **5.1 Install n8n on Your Computer**
```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start

# Access at http://localhost:5678
# Username: admin
# Password: AutosellN8n2025!
```

#### **5.2 Configure n8n Webhooks**
Update webhook URLs in n8n workflows:
```bash
# Update webhook URLs to point to Vercel
https://autosell-backend.vercel.app/api/facebook/post
https://autosell-backend.vercel.app/api/sheets/sync
https://autosell-backend.vercel.app/api/drive/upload
```

### **Step 6: Test Everything**

#### **6.1 Test Frontend**
Visit your Vercel frontend URL

#### **6.2 Test Backend**
```bash
curl https://autosell-backend.vercel.app/health
```

#### **6.3 Test Database**
Check Supabase dashboard for data

#### **6.4 Test n8n**
Visit http://localhost:5678

## 🔧 **Environment Variables Setup**

### **Frontend (Vercel)**
```bash
VITE_API_URL=https://autosell-backend.vercel.app
```

### **Backend (Vercel)**
```bash
DATABASE_URL=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
CORS_ORIGINS=https://autosell-frontend.vercel.app,http://localhost:3000
ALLOWED_HOSTS=autosell-backend.vercel.app,localhost,127.0.0.1
```

### **n8n (Local)**
```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=AutosellN8n2025!
WEBHOOK_URL=http://localhost:5678
```

## 📱 **Expected URLs**

After deployment, you'll get:
- **Frontend**: `https://autosell-frontend.vercel.app`
- **Backend**: `https://autosell-backend.vercel.app`
- **n8n**: `http://localhost:5678` (when running)

## 🎯 **Benefits of This Setup**

✅ **Completely free** - No costs ever
✅ **No time limits** - Run forever
✅ **No credit card** - No payment required
✅ **Automatic deployments** - Deploy on every push
✅ **Custom domains** - Available on free tier
✅ **SSL certificates** - Included automatically
✅ **Global CDN** - Fast worldwide
✅ **Serverless scaling** - Auto-scales with usage

## 🚨 **Important Notes**

1. **n8n runs locally** - Start when needed
2. **Database limits** - 500MB free (usually enough)
3. **Bandwidth limits** - 100GB free (generous)
4. **Function limits** - 100GB-hours free (plenty)
5. **Custom domains** - Available on free tier

## 🎉 **Quick Start Commands**

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy frontend
cd frontend
vercel

# 3. Deploy backend
cd ../backend
vercel

# 4. Install n8n
npm install -g n8n

# 5. Start n8n
n8n start
```

## 💰 **Cost Breakdown**

| Service | Cost | Limits |
|---------|------|--------|
| **Vercel Frontend** | FREE | 100GB bandwidth |
| **Vercel Backend** | FREE | 100GB-hours functions |
| **Supabase Database** | FREE | 500MB storage |
| **n8n (Local)** | FREE | No limits |
| **Total** | **$0/month** | **Forever** |

**This setup will cost you $0 forever!** 🎉

Would you like me to help you set up any of these free services?
