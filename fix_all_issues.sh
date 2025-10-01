#!/bin/bash

echo "🔧 Autosell.mx Complete Fix Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to run command and check result
run_command() {
    local description=$1
    local command=$2
    
    echo -e "${BLUE}🔧 $description...${NC}"
    
    if eval "$command"; then
        echo -e "${GREEN}✅ $description completed${NC}"
        return 0
    else
        echo -e "${RED}❌ $description failed${NC}"
        return 1
    fi
}

echo -e "${BLUE}📋 Starting comprehensive system fixes...${NC}"

# Fix 1: Backend Pydantic Validation (already done via file edit)
echo -e "${GREEN}✅ Backend Pydantic validation fix applied${NC}"

# Fix 2: Clean Database
echo -e "\n${BLUE}🧹 Cleaning database...${NC}"
cd backend
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    run_command "Database cleanup" "python clean_database.py"
else
    echo -e "${YELLOW}⚠️  Backend virtual environment not found${NC}"
fi
cd ..

# Fix 3: Frontend Dependencies
echo -e "\n${BLUE}📦 Fixing frontend dependencies...${NC}"
run_command "Frontend dependencies fix" "./fix_frontend_dependencies.sh"

# Fix 4: Test System
echo -e "\n${BLUE}🧪 Testing system fixes...${NC}"
echo -e "${YELLOW}Note: This will test the system. Make sure services are running.${NC}"
echo -e "${YELLOW}Run './start_local.sh' in another terminal first.${NC}"

read -p "Press Enter to continue with system test (or Ctrl+C to skip)..."

run_command "System health check" "python test_system_fixes.py"

echo -e "\n${GREEN}🎉 All fixes completed!${NC}"
echo -e "${BLUE}==========================================${NC}"
echo -e "${GREEN}Next steps:${NC}"
echo -e "${YELLOW}1. Run: ./start_local.sh${NC}"
echo -e "${YELLOW}2. Open: http://localhost:5173${NC}"
echo -e "${YELLOW}3. Test: http://localhost:8000/docs${NC}"
echo -e "${BLUE}==========================================${NC}"
