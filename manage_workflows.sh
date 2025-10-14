#!/bin/bash
# n8n Workflow Management for Autosell.mx
# Clean up unnecessary workflows and keep only essential ones

echo "🧹 Cleaning up n8n workflows..."
echo "================================"

# Create backup of current workflows
echo "📦 Creating backup..."
mkdir -p n8n_workflows_backup
cp n8n_workflows/*.json n8n_workflows_backup/ 2>/dev/null || true

# Remove unnecessary workflows
echo "🗑️  Removing unnecessary workflows..."

# Keep only essential workflows
ESSENTIAL_WORKFLOWS=(
    "google_sheets_sync.json"
    "facebook_automation_fixed.json"
)

# Remove all other workflows
for file in n8n_workflows/*.json; do
    filename=$(basename "$file")
    if [[ ! " ${ESSENTIAL_WORKFLOWS[@]} " =~ " ${filename} " ]]; then
        echo "❌ Removing: $filename"
        rm "$file"
    else
        echo "✅ Keeping: $filename"
    fi
done

echo ""
echo "📋 Essential Workflows:"
echo "======================="
echo "1. google_sheets_sync.json - Import 131 vehicles from Google Sheets"
echo "2. facebook_automation_fixed.json - Post vehicles to Facebook"
echo ""
echo "🎯 What you need to do:"
echo "1. Go to http://localhost:5678"
echo "2. Import these 2 workflows"
echo "3. Configure them for your data"
echo "4. Set to MANUAL execution only"
echo "5. Test with small batches first"
echo ""
echo "✅ Workflow cleanup completed!"
