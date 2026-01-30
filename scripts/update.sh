#!/bin/bash

#############################################
# Portfolio Update Script
# Run on EC2: bash ~/portfolio/scripts/update.sh
#############################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[1/5] Pulling latest code...${NC}"
cd ~/portfolio
git pull origin main

echo -e "${BLUE}[2/5] Updating backend dependencies...${NC}"
cd ~/portfolio/backend
source venv/bin/activate
pip install -r requirements.txt --quiet

echo -e "${BLUE}[3/5] Running database migrations...${NC}"
python -m app.database.seed 2>/dev/null || true

echo -e "${BLUE}[4/5] Building frontend...${NC}"
cd ~/portfolio/frontend
npm install --silent
npm run build

echo -e "${BLUE}[5/5] Deploying...${NC}"
sudo cp -r dist/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html
sudo systemctl restart portfolio-api

echo ""
echo -e "${GREEN}Update complete!${NC}"
echo -e "Check status: ${YELLOW}sudo systemctl status portfolio-api${NC}"
