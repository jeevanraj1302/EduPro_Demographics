# 📦 Installation Guide

## Prerequisites

- **Python 3.10 or higher**
- **UV** (Astral's fast Python package manager)

---

## Step 1: Install UV

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### macOS / Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verify Installation
```bash
uv --version
```

---

## Step 2: Project Setup

```bash
# Navigate to the project directory
cd EduPro_Demographics

# Create virtual environment
uv venv

# Activate the virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install all dependencies
uv sync
```

---

## Step 3: Verify Data

Ensure your dataset file `users.xlsx` exists in the `data/` directory:

```
EduPro_Demographics/
└── data/
    └── users.xlsx   ← Your data file
```

The Excel file must contain a sheet with columns:
- `UserID` — Unique learner identifier
- `UserName` — Learner username
- `Age` — Learner age (numeric)
- `Gender` — Male/Female
- `Email` — Email address

---

## Step 4: Run the Application

```bash
uv run streamlit run streamlit_app/app.py
```

The dashboard will open automatically at **http://localhost:8501**.

---

## Step 5: Run Tests (Optional)

```bash
uv run pytest tests/ -v
```

---

## Troubleshooting

### UV not found
Restart your terminal after installing UV, or add it to your PATH manually.

### Missing dependencies
```bash
uv sync --reinstall
```

### Port 8501 already in use
```bash
uv run streamlit run streamlit_app/app.py --server.port 8502
```

### Data file not found
Ensure `users.xlsx` is in the `data/` directory relative to the project root.
