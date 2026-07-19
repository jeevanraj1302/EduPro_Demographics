# 🚀 Deployment Guide

## Option 1: Docker Deployment (Recommended)

### Prerequisites
- Docker Engine 20.10+
- Docker Compose v2+

### Steps

```bash
# Build and start the container
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at **http://localhost:8501**.

### Custom Configuration

Edit `docker-compose.yml` to customize:
- **Port mapping**: Change `8501:8501` to use a different port
- **Environment variables**: Add `LOG_LEVEL`, custom configs
- **Volumes**: Mount additional data directories

---

## Option 2: Streamlit Community Cloud

1. Push the project to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select the repository and branch
5. Set the main file path to `streamlit_app/app.py`
6. Click **Deploy**

> **Note:** Ensure `data/users.xlsx` is committed to the repository.

---

## Option 3: Cloud VM (AWS/GCP/Azure)

### Setup on Ubuntu Server

```bash
# Install Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-venv -y

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Clone and setup
cd /opt
git clone <your-repo-url> EduPro_Demographics
cd EduPro_Demographics
uv venv
uv sync

# Run with nohup (background)
nohup uv run streamlit run streamlit_app/app.py \
  --server.port 8501 \
  --server.address 0.0.0.0 \
  --server.headless true &
```

### Using systemd (Production)

Create `/etc/systemd/system/edupro.service`:

```ini
[Unit]
Description=EduPro Demographics Dashboard
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/EduPro_Demographics
ExecStart=/opt/EduPro_Demographics/.venv/bin/streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable edupro
sudo systemctl start edupro
```

---

## Option 4: Heroku

1. Add a `Procfile`:
   ```
   web: streamlit run streamlit_app/app.py --server.port $PORT --server.address 0.0.0.0
   ```

2. Deploy:
   ```bash
   heroku create edupro-demographics
   git push heroku main
   ```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `STREAMLIT_SERVER_PORT` | `8501` | Dashboard port |
| `STREAMLIT_SERVER_HEADLESS` | `true` | Run without browser auto-open |

---

## Health Check

The application exposes a health endpoint at:
```
http://localhost:8501/_stcore/health
```

Use this for container orchestration and monitoring.
