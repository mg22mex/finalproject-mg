# 🤖 n8n Local Setup (Free)

## Step 1: Install n8n
```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

## Step 2: Access n8n Dashboard
- URL: http://localhost:5678
- Username: admin
- Password: AutosellN8n2025!

## Step 3: Configure Webhooks
Update webhook URLs in n8n workflows:
- Facebook: https://autosell-backend.vercel.app/api/facebook/post
- Sheets: https://autosell-backend.vercel.app/api/sheets/sync
- Drive: https://autosell-backend.vercel.app/api/drive/upload

## Step 4: Import Workflows
1. Go to n8n dashboard
2. Click "Import from File"
3. Upload JSON files from n8n_workflows/ folder

## Step 5: Test Workflows
```bash
# Test webhook connectivity
curl -X POST http://localhost:5678/webhook/facebook-post \
  -H "Content-Type: application/json" \
  -d '{"message": "Test post"}'
```
