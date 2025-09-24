# 🗄️ Supabase Database Setup

## Step 1: Create Supabase Account
1. Go to: https://supabase.com
2. Sign up with GitHub
3. No credit card required!

## Step 2: Create New Project
1. Click "New Project"
2. Choose organization
3. Enter project name: autosell-mx
4. Choose region: US East
5. Click "Create new project"

## Step 3: Get Database URL
1. Go to Settings → Database
2. Copy "Connection string"
3. Update backend environment variables

## Step 4: Run Database Migrations
```bash
# Install Supabase CLI
npm install -g supabase

# Initialize project
supabase init

# Push database schema
supabase db push
```

## Step 5: Test Database Connection
```bash
# Test connection
supabase db ping
```
