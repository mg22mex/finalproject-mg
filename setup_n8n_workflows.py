#!/usr/bin/env python3
"""
n8n Workflow Setup Script for Autosell.mx
This script helps you set up all the automation workflows
"""

import json
import os
from datetime import datetime

def create_facebook_automation_workflow():
    """Create Facebook automation workflow"""
    print("🤖 Creating Facebook Automation Workflow...")
    
    workflow = {
        "name": "Facebook Auto Posting",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "facebook-post",
                    "options": {}
                },
                "id": "webhook-trigger",
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [240, 300],
                "webhookId": "facebook-post-webhook"
            },
            {
                "parameters": {
                    "conditions": {
                        "options": {
                            "caseSensitive": True,
                            "leftValue": "",
                            "typeValidation": "strict"
                        },
                        "conditions": [
                            {
                                "id": "condition-1",
                                "leftValue": "={{ $json.account_type }}",
                                "rightValue": "auto",
                                "operator": {
                                    "type": "string",
                                    "operation": "equals"
                                }
                            }
                        ],
                        "combinator": "and"
                    },
                    "options": {}
                },
                "id": "check-account-type",
                "name": "Check Account Type",
                "type": "n8n-nodes-base.if",
                "typeVersion": 2,
                "position": [460, 300]
            },
            {
                "parameters": {
                    "url": "http://localhost:8000/api/facebook/accounts",
                    "authentication": "none",
                    "requestMethod": "GET",
                    "options": {}
                },
                "id": "get-facebook-accounts",
                "name": "Get Facebook Accounts",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [680, 200]
            },
            {
                "parameters": {
                    "url": "https://graph.facebook.com/v18.0/me/feed",
                    "authentication": "none",
                    "requestMethod": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "message",
                                "value": "={{ $json.message }}"
                            },
                            {
                                "name": "access_token",
                                "value": "={{ $json.access_token }}"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "post-to-facebook",
                "name": "Post to Facebook",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [900, 300]
            },
            {
                "parameters": {
                    "url": "http://localhost:8000/api/facebook/log-activity",
                    "authentication": "none",
                    "requestMethod": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "account_id",
                                "value": "={{ $json.account_id }}"
                            },
                            {
                                "name": "action",
                                "value": "post_created"
                            },
                            {
                                "name": "status",
                                "value": "success"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "log-activity",
                "name": "Log Activity",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [1120, 300]
            }
        ],
        "connections": {
            "Webhook Trigger": {
                "main": [
                    [
                        {
                            "node": "Check Account Type",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Check Account Type": {
                "main": [
                    [
                        {
                            "node": "Get Facebook Accounts",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Get Facebook Accounts": {
                "main": [
                    [
                        {
                            "node": "Post to Facebook",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Post to Facebook": {
                "main": [
                    [
                        {
                            "node": "Log Activity",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True,
        "settings": {
            "executionOrder": "v1"
        },
        "versionId": "1",
        "meta": {
            "templateCredsSetupCompleted": True
        },
        "id": "facebook-automation",
        "tags": []
    }
    
    with open('n8n_workflows/facebook_automation.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print("✅ Facebook automation workflow created")

def create_google_sheets_workflow():
    """Create Google Sheets sync workflow"""
    print("📊 Creating Google Sheets Sync Workflow...")
    
    workflow = {
        "name": "Google Sheets Sync",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "sync-sheets",
                    "options": {}
                },
                "id": "webhook-trigger",
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [240, 300],
                "webhookId": "sync-sheets-webhook"
            },
            {
                "parameters": {
                    "url": "http://localhost:8000/api/vehicles",
                    "authentication": "none",
                    "requestMethod": "GET",
                    "options": {}
                },
                "id": "get-vehicles",
                "name": "Get Vehicles",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [460, 300]
            },
            {
                "parameters": {
                    "authentication": "oAuth2",
                    "resource": "spreadsheet",
                    "operation": "appendOrUpdate",
                    "documentId": "={{ $json.spreadsheet_id }}",
                    "sheetName": "Vehicles",
                    "columns": {
                        "mappingMode": "defineBelow",
                        "value": {
                            "id": "={{ $json.id }}",
                            "make": "={{ $json.make }}",
                            "model": "={{ $json.model }}",
                            "year": "={{ $json.year }}",
                            "price": "={{ $json.price }}",
                            "status": "={{ $json.status }}",
                            "created_at": "={{ $json.created_at }}"
                        }
                    },
                    "options": {}
                },
                "id": "update-google-sheets",
                "name": "Update Google Sheets",
                "type": "n8n-nodes-base.googleSheets",
                "typeVersion": 4.1,
                "position": [680, 300]
            },
            {
                "parameters": {
                    "url": "http://localhost:8000/api/vehicles/{{ $json.id }}/sync-status",
                    "authentication": "none",
                    "requestMethod": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "last_synced",
                                "value": "={{ $now }}"
                            },
                            {
                                "name": "sync_status",
                                "value": "success"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "update-sync-status",
                "name": "Update Sync Status",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [900, 300]
            }
        ],
        "connections": {
            "Webhook Trigger": {
                "main": [
                    [
                        {
                            "node": "Get Vehicles",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Get Vehicles": {
                "main": [
                    [
                        {
                            "node": "Update Google Sheets",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Update Google Sheets": {
                "main": [
                    [
                        {
                            "node": "Update Sync Status",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True,
        "settings": {
            "executionOrder": "v1"
        },
        "versionId": "1",
        "meta": {
            "templateCredsSetupCompleted": True
        },
        "id": "google-sheets-sync",
        "tags": []
    }
    
    with open('n8n_workflows/google_sheets_sync.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print("✅ Google Sheets sync workflow created")

def create_vehicle_processing_workflow():
    """Create vehicle processing workflow"""
    print("🚗 Creating Vehicle Processing Workflow...")
    
    workflow = {
        "name": "Vehicle Processing Pipeline",
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "process-vehicle",
                    "options": {}
                },
                "id": "webhook-trigger",
                "name": "Webhook Trigger",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [240, 300],
                "webhookId": "process-vehicle-webhook"
            },
            {
                "parameters": {
                    "url": "http://localhost:8000/api/vehicles/{{ $json.vehicle_id }}",
                    "authentication": "none",
                    "requestMethod": "GET",
                    "options": {}
                },
                "id": "get-vehicle-details",
                "name": "Get Vehicle Details",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [460, 300]
            },
            {
                "parameters": {
                    "conditions": {
                        "options": {
                            "caseSensitive": True,
                            "leftValue": "",
                            "typeValidation": "strict"
                        },
                        "conditions": [
                            {
                                "id": "condition-1",
                                "leftValue": "={{ $json.status }}",
                                "rightValue": "active",
                                "operator": {
                                    "type": "string",
                                    "operation": "equals"
                                }
                            }
                        ],
                        "combinator": "and"
                    },
                    "options": {}
                },
                "id": "check-vehicle-status",
                "name": "Check Vehicle Status",
                "type": "n8n-nodes-base.if",
                "typeVersion": 2,
                "position": [680, 300]
            },
            {
                "parameters": {
                    "url": "http://localhost:5678/webhook/sync-sheets",
                    "authentication": "none",
                    "requestMethod": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "vehicle_id",
                                "value": "={{ $json.id }}"
                            },
                            {
                                "name": "spreadsheet_id",
                                "value": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "sync-to-sheets",
                "name": "Sync to Sheets",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [900, 200]
            },
            {
                "parameters": {
                    "url": "http://localhost:5678/webhook/facebook-post",
                    "authentication": "none",
                    "requestMethod": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "account_type",
                                "value": "auto"
                            },
                            {
                                "name": "message",
                                "value": "🚗 Nuevo vehículo disponible: {{ $json.year }} {{ $json.make }} {{ $json.model }} - ${{ $json.price }}"
                            },
                            {
                                "name": "vehicle_id",
                                "value": "={{ $json.id }}"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "post-to-facebook",
                "name": "Post to Facebook",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [900, 400]
            },
            {
                "parameters": {
                    "url": "http://localhost:8000/api/vehicles/{{ $json.id }}/processing-complete",
                    "authentication": "none",
                    "requestMethod": "POST",
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {
                                "name": "processed_at",
                                "value": "={{ $now }}"
                            },
                            {
                                "name": "status",
                                "value": "completed"
                            }
                        ]
                    },
                    "options": {}
                },
                "id": "mark-complete",
                "name": "Mark Complete",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [1120, 300]
            }
        ],
        "connections": {
            "Webhook Trigger": {
                "main": [
                    [
                        {
                            "node": "Get Vehicle Details",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Get Vehicle Details": {
                "main": [
                    [
                        {
                            "node": "Check Vehicle Status",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Check Vehicle Status": {
                "main": [
                    [
                        {
                            "node": "Sync to Sheets",
                            "type": "main",
                            "index": 0
                        },
                        {
                            "node": "Post to Facebook",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Sync to Sheets": {
                "main": [
                    [
                        {
                            "node": "Mark Complete",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Post to Facebook": {
                "main": [
                    [
                        {
                            "node": "Mark Complete",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True,
        "settings": {
            "executionOrder": "v1"
        },
        "versionId": "1",
        "meta": {
            "templateCredsSetupCompleted": True
        },
        "id": "vehicle-processing",
        "tags": []
    }
    
    with open('n8n_workflows/vehicle_processing.json', 'w') as f:
        json.dump(workflow, f, indent=2)
    
    print("✅ Vehicle processing workflow created")

def create_workflow_import_guide():
    """Create workflow import guide"""
    print("📋 Creating Workflow Import Guide...")
    
    guide = f"""# 🤖 n8n Workflow Import Guide

## 🎯 **How to Import Your Workflows**

### **Step 1: Access n8n Dashboard**
1. Open your browser
2. Go to: http://localhost:5678
3. Login with: admin / AutosellN8n2025!

### **Step 2: Import Workflows**

#### **2.1 Import Facebook Automation**
1. Click **"Import from File"**
2. Select: `n8n_workflows/facebook_automation.json`
3. Click **"Import"**

#### **2.2 Import Google Sheets Sync**
1. Click **"Import from File"**
2. Select: `n8n_workflows/google_sheets_sync.json`
3. Click **"Import"**

#### **2.3 Import Vehicle Processing**
1. Click **"Import from File"**
2. Select: `n8n_workflows/vehicle_processing.json`
3. Click **"Import"**

### **Step 3: Configure Credentials**

#### **3.1 Google Sheets Credentials**
1. Go to **Settings** → **Credentials**
2. Click **"Add Credential"**
3. Select **"Google Sheets OAuth2 API"**
4. Follow the OAuth setup process

#### **3.2 Facebook App Credentials**
1. Go to **Settings** → **Credentials**
2. Click **"Add Credential"**
3. Select **"Facebook Graph API"**
4. Enter your App ID and App Secret

### **Step 4: Test Workflows**

#### **4.1 Test Facebook Posting**
```bash
curl -X POST http://localhost:5678/webhook/facebook-post \\
  -H "Content-Type: application/json" \\
  -d '{{"account_type": "auto", "message": "Test post from Autosell.mx!"}}'
```

#### **4.2 Test Google Sheets Sync**
```bash
curl -X POST http://localhost:5678/webhook/sync-sheets \\
  -H "Content-Type: application/json" \\
  -d '{{"spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"}}'
```

#### **4.3 Test Vehicle Processing**
```bash
curl -X POST http://localhost:5678/webhook/process-vehicle \\
  -H "Content-Type: application/json" \\
  -d '{{"vehicle_id": "123"}}'
```

## 🎉 **Your Workflows Are Ready!**

### **What Each Workflow Does:**

1. **Facebook Automation**: Auto-posts to Facebook when triggered
2. **Google Sheets Sync**: Syncs vehicle data to Google Sheets
3. **Vehicle Processing**: Complete vehicle processing pipeline

### **Webhook URLs:**
- **Facebook Posting**: http://localhost:5678/webhook/facebook-post
- **Google Sheets Sync**: http://localhost:5678/webhook/sync-sheets
- **Vehicle Processing**: http://localhost:5678/webhook/process-vehicle

## 🚀 **Next Steps:**

1. **Import all workflows** into n8n
2. **Configure credentials** for Google and Facebook
3. **Test each workflow** with the curl commands
4. **Connect to your backend** for full automation

**Your n8n automation system is ready to power Autosell.mx!** 🎉
"""
    
    with open('N8N_WORKFLOW_IMPORT_GUIDE.md', 'w') as f:
        f.write(guide)
    
    print("✅ Workflow import guide created")

def main():
    """Main setup function"""
    print("🤖 n8n Workflow Setup for Autosell.mx")
    print("=" * 50)
    print(f"⏰ Setup started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create workflow files
    create_facebook_automation_workflow()
    create_google_sheets_workflow()
    create_vehicle_processing_workflow()
    create_workflow_import_guide()
    
    print()
    print("🎉 n8n Workflow Setup Complete!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Go to: http://localhost:5678")
    print("2. Login with: admin / AutosellN8n2025!")
    print("3. Import the JSON files from n8n_workflows/ folder")
    print("4. Configure Google and Facebook credentials")
    print("5. Test your workflows!")
    print()
    print("🎯 Your automation system is ready!")

if __name__ == "__main__":
    main()
