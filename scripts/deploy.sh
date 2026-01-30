#!/bin/bash

#############################################
# Portfolio Auto-Deploy Script for AWS EC2
# Run: curl -sSL https://raw.githubusercontent.com/ptheson1902/portfolio/main/scripts/deploy.sh | bash
#############################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║     PHAM THE SON - Portfolio Auto Deploy          ║"
echo "║     AWS EC2 Ubuntu 22.04                          ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}Please run as normal user, not root${NC}"
    exit 1
fi

# Get EC2 Public IP
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "YOUR_EC2_IP")

echo -e "${YELLOW}[1/7] Updating system...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${YELLOW}[2/7] Installing dependencies...${NC}"
sudo apt install -y python3-pip python3-venv python3-dev git nginx \
    libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Install Node.js (latest)
echo -e "${YELLOW}[3/7] Installing Node.js...${NC}"
curl -fsSL https://deb.nodesource.com/setup_current.x | sudo -E bash -
sudo apt install -y nodejs

# Clone repository if not exists
echo -e "${YELLOW}[4/7] Setting up project...${NC}"
cd ~
if [ ! -d "portfolio" ]; then
    git clone https://github.com/ptheson1902/portfolio.git
fi
cd portfolio

# Setup Backend
echo -e "${YELLOW}[5/7] Setting up Backend...${NC}"
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
mkdir -p data

# Create .env file if not exists
if [ ! -f ".env" ]; then
    cat > .env << EOF
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
CORS_ORIGINS=http://${EC2_IP},http://localhost
ADMIN_TOKEN=$(openssl rand -hex 16)
DATABASE_URL=sqlite:///./data/portfolio.db
EOF
    echo -e "${GREEN}Created .env file. Please update OPENAI_API_KEY!${NC}"
fi

# Seed database
python -m app.database.seed

# Create systemd service
echo -e "${YELLOW}Creating systemd service...${NC}"
sudo tee /etc/systemd/system/portfolio-api.service > /dev/null << EOF
[Unit]
Description=Portfolio FastAPI Backend
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$HOME/portfolio/backend
Environment="PATH=$HOME/portfolio/backend/venv/bin"
EnvironmentFile=$HOME/portfolio/backend/.env
ExecStart=$HOME/portfolio/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable portfolio-api
sudo systemctl start portfolio-api

# Setup Frontend
echo -e "${YELLOW}[6/7] Building Frontend...${NC}"
cd ~/portfolio/frontend
npm install
npm run build

# Copy to nginx
sudo rm -rf /var/www/html/*
sudo cp -r dist/* /var/www/html/
sudo chown -R www-data:www-data /var/www/html

# Configure Nginx
echo -e "${YELLOW}[7/7] Configuring Nginx...${NC}"
sudo tee /etc/nginx/sites-available/portfolio > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # Frontend
    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml;
}
EOF

sudo ln -sf /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Get admin token
ADMIN_TOKEN=$(grep ADMIN_TOKEN ~/portfolio/backend/.env | cut -d '=' -f2)

echo ""
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════╗"
echo "║           🎉 DEPLOYMENT COMPLETE! 🎉              ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo -e "${BLUE}📌 Access your portfolio:${NC}"
echo -e "   Website: ${GREEN}http://${EC2_IP}${NC}"
echo -e "   API:     ${GREEN}http://${EC2_IP}/api${NC}"
echo ""
echo -e "${BLUE}🔐 Admin Token:${NC}"
echo -e "   ${YELLOW}${ADMIN_TOKEN}${NC}"
echo ""
echo -e "${BLUE}⚠️  IMPORTANT - Update your .env file:${NC}"
echo -e "   ${YELLOW}nano ~/portfolio/backend/.env${NC}"
echo -e "   Add your OpenAI API key, then restart:"
echo -e "   ${YELLOW}sudo systemctl restart portfolio-api${NC}"
echo ""
echo -e "${BLUE}📋 Useful commands:${NC}"
echo "   View logs:    sudo journalctl -u portfolio-api -f"
echo "   Restart API:  sudo systemctl restart portfolio-api"
echo "   Restart web:  sudo systemctl restart nginx"
echo ""
echo -e "${BLUE}🔒 To add SSL (requires domain):${NC}"
echo "   sudo apt install certbot python3-certbot-nginx"
echo "   sudo certbot --nginx -d your-domain.com"
echo ""
