# PHAM THE SON - Portfolio

Production-ready portfolio website with database, admin panel, and resume export.

## ✨ Features

- **Role-based content**: Engineering Leader, BrSE, Fullstack Engineer
- **Multi-language**: Japanese, Vietnamese, English
- **AI Chat**: Answer questions based on skill sheet data
- **Admin Panel**: Inline editing with token authentication
- **Resume Export**: 職務経歴書 in PDF/DOCX/HTML
- **Dark/Light mode**: Toggle between themes
- **Responsive**: Mobile-first design

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React, TypeScript, Tailwind CSS, Framer Motion |
| Backend | Python, FastAPI, SQLAlchemy |
| Database | SQLite (easily switchable to PostgreSQL) |
| AI | OpenAI GPT-4o-mini |

## 🚀 Quick Start (Local Development)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Edit with your API keys
python -m app.database.seed
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

---

## ☁️ AWS EC2 Deployment

### Prerequisites
- AWS Account (Free tier eligible)
- Domain name (optional, for SSL)

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Configure:
   - **Name**: `portfolio-server`
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance type**: `t2.micro` (Free tier)
   - **Key pair**: Create new, download `.pem` file
   - **Security Group**: Allow SSH(22), HTTP(80), HTTPS(443)

3. Launch and note the **Public IP**

### Step 2: Connect to EC2

```bash
# From your local machine
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### Step 3: One-Click Deploy 🎯

Copy and run this script on your EC2:

```bash
curl -sSL https://raw.githubusercontent.com/ptheson1902/portfolio/main/scripts/deploy.sh | bash
```

**Or manually:**

```bash
# Clone and run setup script
git clone https://github.com/ptheson1902/portfolio.git
cd portfolio
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

### Step 4: Configure Environment

```bash
# Edit backend .env
nano ~/portfolio/backend/.env
```

Add your keys:
```env
OPENAI_API_KEY=sk-your-openai-key
ADMIN_TOKEN=your-secure-admin-token
CORS_ORIGINS=http://YOUR_EC2_IP
```

Restart:
```bash
sudo systemctl restart portfolio-api
```

### Step 5: Access Your Site

Open in browser: `http://YOUR_EC2_IP`

---

## 🔐 Admin Access

1. Click the 🔑 button (bottom-right)
2. Enter your `ADMIN_TOKEN`
3. Click ✏️ to enable edit mode
4. Click 📥 to export resume

---

## 📡 API Endpoints

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile?lang=ja&role=fullstack` | Get profile |
| GET | `/api/skills?lang=ja` | Get skills |
| GET | `/api/projects?lang=ja&role=leader` | Get projects |
| POST | `/api/chat` | AI chat |
| GET | `/api/export/resume?lang=ja&format=pdf` | Export resume |

### Protected (requires `Authorization: Bearer TOKEN`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT | `/api/profile` | Update profile |
| POST/PUT/DELETE | `/api/skills/{id}` | CRUD skills |
| POST/PUT/DELETE | `/api/projects/{id}` | CRUD projects |

---

## 🗂 Project Structure

```
portfolio/
├── backend/
│   ├── app/
│   │   ├── database/      # SQLAlchemy connection
│   │   ├── models/        # Pydantic + ORM models
│   │   ├── repositories/  # Data access layer
│   │   ├── services/      # Business logic
│   │   ├── routers/       # API routes
│   │   ├── middleware/    # Auth middleware
│   │   └── main.py
│   ├── templates/         # Resume HTML templates
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── context/       # Auth + App context
│   │   ├── hooks/         # API hooks
│   │   ├── i18n/          # Translations
│   │   └── pages/         # Page sections
│   └── package.json
├── scripts/
│   └── deploy.sh          # Auto-deploy script
├── docker-compose.yml
└── README.md
```

---

## 🔧 Useful Commands

```bash
# View logs
sudo journalctl -u portfolio-api -f

# Restart services
sudo systemctl restart portfolio-api
sudo systemctl restart nginx

# Update deployment
cd ~/portfolio
git pull
cd frontend && npm run build && sudo cp -r dist/* /var/www/html/
sudo systemctl restart portfolio-api

# Check status
sudo systemctl status portfolio-api
sudo systemctl status nginx
```

---

## 💰 AWS Cost (Free Tier)

| Resource | Free Tier (12 months) | After |
|----------|----------------------|-------|
| EC2 t2.micro | 750 hrs/month | ~$8/mo |
| EBS Storage | 30 GB | ~$1/mo |
| Data Transfer | 15 GB/month | $0.09/GB |

---

## 📝 License

MIT
