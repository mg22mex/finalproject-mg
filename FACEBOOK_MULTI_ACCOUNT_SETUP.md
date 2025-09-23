# 🚗 Facebook Multi-Account Setup Guide
## Complete Guide for Setting Up Multiple Facebook Apps

---

## 📋 **OVERVIEW**

This guide will help you set up Facebook apps for multiple accounts to ensure your Autosell.mx system can work with all three Facebook accounts (Manual + 2 Auto accounts).

### **Why Multiple Apps?**
- **Account Isolation**: Each Facebook account needs its own app
- **Permission Management**: Different permissions for different account types
- **Compliance**: Facebook requires separate apps for different business entities
- **Reliability**: If one app gets suspended, others continue working

---

## 🎯 **SETUP STRATEGY**

### **Current Status:**
- **Account 1 (Manual)**: App pending Facebook approval
- **Account 2 (Auto Account 1)**: Create new app
- **Account 3 (Auto Account 2)**: Create new app

### **Recommended Approach:**
1. **Keep existing app** for Manual Account (wait for approval)
2. **Create new apps** for Auto Account 1 and Auto Account 2
3. **Configure each app** with appropriate permissions
4. **Test all integrations** before going live

---

## 🚀 **STEP-BY-STEP SETUP**

### **Phase 1: Auto Account 1 Setup**

#### **Step 1: Access Facebook Developer Console**
1. **Log into Facebook** with your Auto Account 1 credentials
2. **Go to**: [developers.facebook.com](https://developers.facebook.com)
3. **Click "My Apps"** → **"Create App"**

#### **Step 2: Create New App**
1. **Select "Business"** as the app type
2. **Fill in the details**:
   - **App Name**: `Autosell-Auto1-2025`
   - **App Contact Email**: Your Auto Account 1 email
   - **Business Account**: Select your business account
3. **Click "Create App"**

#### **Step 3: Add Facebook Login Product**
1. **Go to Products** → **Add Product**
2. **Find "Facebook Login"** → **Click "Set Up"**
3. **Configure Facebook Login**:
   - **Valid OAuth Redirect URIs**:
     - `https://autosell-backend.onrender.com/auth/facebook/callback`
     - `http://localhost:8000/auth/facebook/callback`
   - **App Domains**: `autosell-backend.onrender.com`

#### **Step 4: Configure App Settings**
1. **Go to App Settings** → **Basic**
2. **Add App Domains**: `autosell-backend.onrender.com`
3. **Privacy Policy URL**: `https://mg22mex.github.io/autosell-privacy-policy/`
4. **Terms of Service URL**: `https://mg22mex.github.io/autosell-privacy-policy/`

#### **Step 5: Request Permissions**
1. **Go to App Review** → **Permissions and Features**
2. **Request these permissions**:
   - `pages_manage_posts` - Post to Facebook pages
   - `pages_read_engagement` - Read page insights
   - `pages_show_list` - List user's pages
   - `publish_to_groups` - Post to groups (if needed)
   - `user_posts` - Access user posts

#### **Step 6: Get App Credentials**
1. **Copy App ID** from the app dashboard
2. **Copy App Secret** from the app dashboard
3. **Note down the credentials** for configuration

### **Phase 2: Auto Account 2 Setup**

Repeat the same process for Auto Account 2:
- **App Name**: `Autosell-Auto2-2025`
- **Use Auto Account 2 credentials**
- **Follow the same configuration steps**

---

## 🔧 **CONFIGURATION SCRIPTS**

### **Auto Account 1 Configuration**

Edit the generated script: `configure_auto_account_1_account.py`

```python
# Replace these with your actual credentials
account.app_id = "YOUR_APP_ID_HERE"
account.app_secret = "YOUR_APP_SECRET_HERE"
```

### **Auto Account 2 Configuration**

Edit the generated script: `configure_auto_account_2_account.py`

```python
# Replace these with your actual credentials
account.app_id = "YOUR_APP_ID_HERE"
account.app_secret = "YOUR_APP_SECRET_HERE"
```

---

## 🧪 **TESTING YOUR SETUP**

### **Test All Accounts**

Run the test script to verify all accounts:

```bash
cd backend
source venv/bin/activate
python test_multiple_facebook_accounts.py
```

### **Expected Output:**
```
🚗 Autosell.mx - Facebook Accounts Test
==================================================

📊 Found 3 Facebook account(s):

🔍 Testing Account: Manual Account
   Type: manual
   Active: True
   Configured: True
   ✅ Service configured successfully
   ✅ API connection successful
   👤 User: Your Name

🔍 Testing Account: Auto Account 1
   Type: auto
   Active: True
   Configured: True
   ✅ Service configured successfully
   ✅ API connection successful
   👤 User: Auto Account 1 Name

🔍 Testing Account: Auto Account 2
   Type: auto
   Active: True
   Configured: True
   ✅ Service configured successfully
   ✅ API connection successful
   👤 User: Auto Account 2 Name

📈 Summary:
   Total accounts: 3
   Configured: 3
   Active: 3
   ✅ At least one account is ready for use!
```

---

## 🌐 **WEB INTERFACE CONFIGURATION**

### **Access the Frontend**
1. **Go to**: [https://autosell-frontend.onrender.com](https://autosell-frontend.onrender.com)
2. **Navigate to**: Facebook Reposting section
3. **Configure each account**:
   - **Manual Account**: Use existing credentials
   - **Auto Account 1**: Use new app credentials
   - **Auto Account 2**: Use new app credentials

### **Account Configuration Steps**
1. **Click "Configure Account"** for each account
2. **Enter App ID and App Secret**
3. **Authorize with Facebook** (OAuth flow)
4. **Select Facebook Page** for posting
5. **Test posting** to verify setup

---

## 🔐 **SECURITY CONSIDERATIONS**

### **App Security**
- **Keep App Secrets secure** - never commit to version control
- **Use environment variables** for sensitive data
- **Regular token rotation** for long-term access tokens
- **Monitor app usage** in Facebook Developer Console

### **Permission Management**
- **Request only necessary permissions**
- **Review permissions regularly**
- **Remove unused permissions**
- **Monitor permission usage**

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**

#### **"App Not Found" Error**
- **Check App ID** is correct
- **Verify app is published** (if required)
- **Ensure app is in correct Facebook account**

#### **"Invalid App Secret" Error**
- **Check App Secret** is correct
- **Verify secret is not expired**
- **Ensure secret matches the App ID**

#### **"Permission Denied" Error**
- **Check required permissions** are granted
- **Verify user has authorized the app**
- **Check app review status**

#### **"OAuth Redirect URI Mismatch" Error**
- **Verify redirect URIs** in app settings
- **Check URIs match exactly** (including protocol)
- **Ensure URIs are added to app configuration**

### **Debug Steps**
1. **Check app status** in Facebook Developer Console
2. **Verify permissions** are granted
3. **Test with Facebook Graph API Explorer**
4. **Check app logs** for detailed error messages

---

## 📊 **MONITORING AND MAINTENANCE**

### **Regular Checks**
- **Monitor app usage** in Facebook Developer Console
- **Check for policy violations**
- **Review permission usage**
- **Update tokens** as needed

### **Performance Monitoring**
- **Track API call limits**
- **Monitor response times**
- **Check error rates**
- **Review posting success rates**

---

## 🎯 **SUCCESS CRITERIA**

### **Setup Complete When:**
- ✅ **All 3 Facebook accounts** are configured
- ✅ **All apps are approved** by Facebook
- ✅ **All permissions are granted**
- ✅ **Test posting works** for all accounts
- ✅ **Web interface shows** all accounts as active
- ✅ **API calls succeed** for all accounts

### **Ready for Production When:**
- ✅ **All accounts tested** and working
- ✅ **Error handling** is in place
- ✅ **Monitoring** is configured
- ✅ **Backup procedures** are in place
- ✅ **Documentation** is complete

---

## 📞 **SUPPORT RESOURCES**

### **Facebook Developer Resources**
- **Documentation**: [developers.facebook.com/docs](https://developers.facebook.com/docs)
- **Graph API Explorer**: [developers.facebook.com/tools/explorer](https://developers.facebook.com/tools/explorer)
- **App Review**: [developers.facebook.com/apps](https://developers.facebook.com/apps)

### **Autosell.mx Support**
- **GitHub Repository**: [github.com/mg22mex/finalproject-mg](https://github.com/mg22mex/finalproject-mg)
- **Live System**: [autosell-frontend.onrender.com](https://autosell-frontend.onrender.com)
- **API Documentation**: [autosell-backend.onrender.com/docs](https://autosell-backend.onrender.com)

---

*This guide ensures your Autosell.mx system can work with multiple Facebook accounts for maximum flexibility and reliability.*
