#!/bin/bash

# Script to setup and run the Travel Agent Management System

# Define colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PROJECT_DIR="$(pwd)"

echo -e "${BLUE}=== Travel Agent Management System ===${NC}"
echo -e "${BLUE}=== Setup and Run Script ===${NC}"
echo

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo -e "${YELLOW}Python is not installed. Please install Python 3.8+ and try again.${NC}"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "oose" ]; then
    echo -e "${GREEN}Creating virtual environment...${NC}"
    python -m venv oose
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}Failed to create virtual environment. Make sure you have Python 3.8+ installed.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source oose/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Failed to install dependencies.${NC}"
    exit 1
fi

# Prompt user for which version to run
echo 
echo -e "${BLUE}Which version would you like to run?${NC}"
echo "1) Simple single-file application (recommended for quick testing)"
echo "2) Full structured application"
echo "3) Upgrade database and run full application"

read -p "Enter your choice (1/2/3): " choice

case $choice in
    1)
        # Run simple application
        echo -e "${GREEN}Running simple application...${NC}"
        echo -e "${GREEN}The application will be available at http://127.0.0.1:5000${NC}"
        python simple_app_new.py
        ;;
    2)
        # Initialize database for the full application
        echo -e "${GREEN}Initializing database...${NC}"
        python init_db.py
        
        # Run full application
        echo -e "${GREEN}Running full application...${NC}"
        echo -e "${GREEN}The application will be available at http://127.0.0.1:5000${NC}"
        python app.py
        ;;
    3)
        # Upgrade existing database
        echo -e "${GREEN}Upgrading database schema...${NC}"
        python upgrade_db.py
        
        # Run full application
        echo -e "${GREEN}Running full application with customer login support...${NC}"
        echo -e "${GREEN}The application will be available at http://127.0.0.1:5000${NC}"
        python app.py
        ;;
    *)
        echo -e "${YELLOW}Invalid choice. Exiting.${NC}"
        deactivate
        exit 1
        ;;
esac

# Deactivate virtual environment on exit
deactivate
