# 🚀 Railway Migration Guide for Autosell.mx

## 🎯 **Why Railway?**
- **$5 free credit monthly** (no time limits!)
- **PostgreSQL included** in free tier
- **Easy GitHub deployment**
- **Similar to Render** but better free tier
- **No 30-day expiration**

## 📋 **Migration Steps**

### **Step 1: Create Railway Account**
1. Go to: https://railway.app
2. Sign up with GitHub
3. Connect your `finalproject-mg` repository

### **Step 2: Deploy Services**

#### **2.1 Deploy Backend**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `finalproject-mg` repository
4. Select **"backend"** folder
5. Railway will auto-detect Python and deploy

#### **2.2 Deploy Frontend**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `finalproject-mg` repository
4. Select **"frontend"** folder
5. Railway will auto-detect Node.js and deploy

#### **2.3 Deploy n8n**
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `finalproject-mg` repository
4. Select **"Dockerfile.n8n"**
5. Railway will use Docker to deploy

#### **2.4 Add PostgreSQL Database**
1. Click **"New Project"**
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Railway will create the database

### **Step 3: Configure Environment Variables**

#### **Backend Environment Variables:**
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
CORS_ORIGINS=https://autosell-frontend.railway.app,http://localhost:3000
ALLOWED_HOSTS=autosell-backend.railway.app,localhost,127.0.0.1
PYTHON_VERSION=3.11.0
PORT=8000
```

#### **Frontend Environment Variables:**
```bash
VITE_API_URL=https://autosell-backend.railway.app
```

#### **n8n Environment Variables:**
```bash
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=AutosellN8n2025!
WEBHOOK_URL=https://autosell-n8n.railway.app
GENERIC_TIMEZONE=America/Mexico_City
```

### **Step 4: Connect Services**

#### **4.1 Connect Backend to Database**
1. In Railway dashboard, go to backend service
2. Click **"Variables"**
3. Add `DATABASE_URL` variable
4. Set value to your PostgreSQL connection string

#### **4.2 Connect Frontend to Backend**
1. In Railway dashboard, go to frontend service
2. Click **"Variables"**
3. Add `VITE_API_URL` variable
4. Set value to your backend Railway URL

#### **4.3 Connect n8n to Backend**
1. In Railway dashboard, go to n8n service
2. Click **"Variables"**
3. Add `WEBHOOK_URL` variable
4. Set value to your n8n Railway URL

### **Step 5: Update Domain Names**

After deployment, Railway will provide URLs like:
- **Backend**: `https://autosell-backend-production.up.railway.app`
- **Frontend**: `https://autosell-frontend-production.up.railway.app`
- **n8n**: `https://autosell-n8n-production.up.railway.app`

Update your environment variables with the actual Railway URLs.

### **Step 6: Test Deployment**

#### **6.1 Test Backend**
```bash
curl https://autosell-backend-production.up.railway.app/health
```

#### **6.2 Test Frontend**
Visit your frontend Railway URL in browser.

#### **6.3 Test n8n**
Visit your n8n Railway URL and login with admin credentials.

## 🔧 **Railway vs Render Comparison**

| Feature | Render | Railway |
|---------|--------|---------|
| **Free Tier** | 30 days | $5 credit monthly |
| **PostgreSQL** | Included | Included |
| **Custom Domains** | ✅ | ✅ |
| **Environment Variables** | ✅ | ✅ |
| **GitHub Integration** | ✅ | ✅ |
| **Docker Support** | ✅ | ✅ |
| **Time Limits** | ❌ 30 days | ✅ No limits |

## 💰 **Cost Comparison**

### **Render Free Tier:**
- ❌ **30 days only**
- ❌ **Expires and requires payment**
- ❌ **$7/month after free tier**

### **Railway Free Tier:**
- ✅ **$5 credit monthly**
- ✅ **No time limits**
- ✅ **Enough for small apps**
- ✅ **Pay only if you exceed $5**

## 🚨 **Migration Checklist**

- [ ] Create Railway account
- [ ] Connect GitHub repository
- [ ] Deploy backend service
- [ ] Deploy frontend service
- [ ] Deploy n8n service
- [ ] Add PostgreSQL database
- [ ] Configure environment variables
- [ ] Test all services
- [ ] Update domain references
- [ ] Verify n8n workflows
- [ ] Test Facebook integration
- [ ] Test Google services

## 🎉 **Benefits of Railway Migration**

✅ **No time limits** on free tier
✅ **$5 monthly credit** (usually enough)
✅ **Better performance** than Render
✅ **Easier deployment** process
✅ **Same features** as Render
✅ **PostgreSQL included**
✅ **Custom domains** supported

## 📞 **Support**

If you encounter issues:
1. Check Railway deployment logs
2. Verify environment variables
3. Test individual services
4. Check database connections

**Railway is the perfect alternative to Render for your Autosell.mx system!** 🚀
