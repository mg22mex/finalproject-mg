# 🚀 Facebook Reposting System - Autosell.mx

## 📋 Overview

The Facebook Reposting System is a comprehensive automation solution that provides **daily automated reposting** of vehicle listings to Facebook and Facebook Marketplace. This ensures maximum visibility and presence for your vehicle inventory.

## ✨ Key Features

- **🔄 Daily Automated Reposting**: Automatically reposts vehicles every 24 hours
- **📱 Dual Platform Posting**: Posts to both Facebook Page and Facebook Marketplace
- **🎯 Smart Content Generation**: Creates engaging, SEO-optimized post content
- **📊 Performance Analytics**: Tracks posting statistics and engagement metrics
- **⚡ Manual Control**: Ability to manually trigger reposting for specific vehicles
- **🔧 Easy Configuration**: Simple setup with environment variables

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vehicle DB   │───▶│ Facebook Service │───▶│ Facebook Graph  │
│                 │    │                  │    │      API       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Social Posts    │
                       │  DB Tracking     │
                       └──────────────────┘
```

## 🚀 Quick Start

### 1. Environment Configuration

Create a `.env` file in the backend directory with your Facebook credentials:

```bash
# Facebook API Configuration
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
FACEBOOK_PAGE_ID=your_facebook_page_id_here
FACEBOOK_USER_ID=your_facebook_user_id_here
FACEBOOK_APP_ID=your_facebook_app_id_here
FACEBOOK_APP_SECRET=your_facebook_app_secret_here
```

### 2. Get Facebook Credentials

#### Step 1: Create Facebook App
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use existing one
3. Go to Settings > Basic
4. Copy **App ID** and **App Secret**

#### Step 2: Generate Access Token
1. Go to [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Select your app
3. Click "Generate Access Token"
4. Grant permissions: `pages_manage_posts`, `marketplace_manage_listings`
5. Copy the **User Access Token**

#### Step 3: Get Page Access Token
1. Use Graph API Explorer
2. Make GET request: `/{page_id}?fields=access_token`
3. Use your user access token
4. Copy the **Page Access Token**

#### Step 4: Get Page ID
1. Go to your Facebook page
2. Look at URL: `facebook.com/YourPageName`
3. Or check page settings for Page ID

#### Step 5: Get User ID
1. Use Graph API Explorer
2. Make GET request: `/me`
3. Copy the **id** field

### 3. Required Permissions

- `pages_manage_posts` - For posting to Facebook page
- `marketplace_manage_listings` - For Marketplace integration
- `pages_read_engagement` - For reading page data

## 📡 API Endpoints

### Facebook Service Status
```http
GET /api/facebook/status
```
Returns the configuration status of the Facebook service.

### Facebook Statistics
```http
GET /api/facebook/stats
```
Returns posting statistics and performance metrics.

### Vehicles for Reposting
```http
GET /api/facebook/vehicles/for-reposting
```
Returns list of vehicles that need reposting.

### Manual Vehicle Reposting
```http
POST /api/facebook/repost/vehicle/{vehicle_id}
```
Manually repost a specific vehicle to Facebook.

### Daily Reposting Job
```http
POST /api/facebook/repost/daily
```
Execute the daily reposting job manually.

### Test Facebook Post
```http
POST /api/facebook/test/post
```
Send a test post to Facebook using a sample vehicle.

## 🔄 Daily Reposting Logic

### How It Works

1. **Vehicle Selection**: System identifies vehicles with status `DISPONIBLE`
2. **Reposting Check**: Checks if vehicle was posted in last 24 hours
3. **Content Generation**: Creates engaging post content with vehicle details
4. **Dual Posting**: Posts to both Facebook Page and Marketplace
5. **Database Tracking**: Records all posts and marketplace listings
6. **Performance Monitoring**: Tracks engagement and success rates

### Post Content Structure

```
🚗 2020 Toyota Camry

🎨 Color: Blanco
📏 Kilometraje: 45,000 km
📍 Ubicación: CDMX
💰 Precio: $250,000.00 MXN

📝 Toyota Camry en excelente estado

🔥 ¡Excelente oportunidad! 🔥
📞 Contáctanos para más información
🌐 www.autosell.mx

#AutosellMX #Vehículos #Oportunidad #Confianza
```

## 🎛️ Manual Controls

### Execute Daily Reposting
```bash
curl -X POST http://localhost:8000/api/facebook/repost/daily
```

### Repost Specific Vehicle
```bash
curl -X POST http://localhost:8000/api/facebook/repost/vehicle/1
```

### Test Facebook Connection
```bash
curl -X POST http://localhost:8000/api/facebook/test/post
```

## 📊 Monitoring & Analytics

### Key Metrics Tracked

- **Total Posts**: Cumulative Facebook posts
- **Weekly Posts**: Posts in last 7 days
- **Active Marketplace Listings**: Current Marketplace presence
- **Repost Count**: Number of times each vehicle reposted
- **Success Rate**: Percentage of successful posts
- **Error Tracking**: Detailed error logging for failed posts

### Dashboard Integration

The system integrates with the main dashboard to show:
- Facebook posting status
- Recent posting activity
- Performance metrics
- Configuration status

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `FACEBOOK_ACCESS_TOKEN` | User access token for API calls | ✅ |
| `FACEBOOK_PAGE_ID` | Facebook page ID for posting | ✅ |
| `FACEBOOK_USER_ID` | User ID for Marketplace | ✅ |
| `FACEBOOK_APP_ID` | Facebook app ID | ✅ |
| `FACEBOOK_APP_SECRET` | Facebook app secret | ✅ |

### Posting Schedule

- **Default**: Every 24 hours
- **Customizable**: Can be adjusted via cron jobs
- **Manual Trigger**: Available via API endpoints
- **Smart Logic**: Only reposts vehicles that need it

## 🚨 Troubleshooting

### Common Issues

#### 1. "Facebook credentials not configured"
- Check all environment variables are set
- Verify `.env` file is in backend directory
- Restart backend server after configuration

#### 2. "Permission denied" errors
- Ensure app has required permissions
- Check access token hasn't expired
- Verify page access token is correct

#### 3. "Rate limit exceeded"
- Facebook has posting limits
- System automatically handles rate limiting
- Consider reducing posting frequency

### Debug Mode

Enable debug logging by setting:
```bash
DEBUG=true
```

### Health Checks

Monitor system health via:
```bash
curl http://localhost:8000/api/facebook/status
```

## 🔮 Future Enhancements

### Planned Features

- **📅 Advanced Scheduling**: Custom posting schedules
- **🎨 Content Templates**: Multiple post templates
- **📱 Multi-Platform**: Instagram, Twitter integration
- **🤖 AI Content**: AI-generated post content
- **📊 Advanced Analytics**: Detailed performance insights
- **🔔 Notifications**: Success/failure alerts

### Integration Possibilities

- **n8n Workflows**: Advanced automation
- **Zapier**: Third-party integrations
- **Slack**: Team notifications
- **Email**: Performance reports

## 📚 API Documentation

Full API documentation available at:
```
http://localhost:8000/docs
```

## 🤝 Support

For technical support or questions:
- Check the logs in backend console
- Verify Facebook app configuration
- Test individual API endpoints
- Review environment variable setup

## 📄 License

This system is part of Autosell.mx and follows the project's licensing terms.

---

**🚀 Ready to maximize your vehicle visibility on Facebook!**
