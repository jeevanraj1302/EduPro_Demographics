# 🎓 EduPro Learner Demographics Analytics Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![UV](https://img.shields.io/badge/UV-Package_Manager-DE5FE9?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Industry-grade Business Intelligence dashboard for analyzing learner demographics on the EduPro platform.**

[Features](#-features) •
[Installation](#-installation) •
[Quick Start](#-quick-start) •
[Architecture](#-architecture) •
[Documentation](#-documentation)

</div>

---

## 📋 Project Overview

EduPro Demographics Analytics is a **production-ready** Business Intelligence application that performs comprehensive descriptive analytics on learner demographics data. Built with Python, Streamlit, and Plotly, it delivers interactive visualizations, automated data quality checks, KPI calculations, and professional business reports.

### Who Is This For?

- 🎓 **Final Year Engineering Projects** — Complete, well-documented, and deployment-ready
- 💼 **Professional Portfolio** — Demonstrates real-world data analytics skills
- 🏢 **Business Stakeholders** — Actionable insights from learner demographics
- 📊 **Data Analysts** — Modular codebase easily adaptable to other datasets

## ✨ Features

### Core Analytics
- ✅ **Automated Data Validation** — 10+ quality checks (duplicates, missing values, email format, age range)
- ✅ **Data Preprocessing** — Cleaning, normalization, and feature engineering pipeline
- ✅ **KPI Dashboard** — 14+ key performance indicators computed automatically
- ✅ **25+ Interactive Charts** — Plotly-powered visualizations with hover tooltips and download options
- ✅ **Business Insights** — Auto-generated findings and strategic recommendations
- ✅ **Report Generation** — Executive Summary, Business Report, Data Quality Report

### Dashboard Features
- 🎨 **Modern Dark Theme** — Professional gradient-based UI with Inter font
- 🔍 **Interactive Filters** — Age range, gender, age group, email provider
- 📊 **9 Dashboard Pages** — Overview, Age, Gender, Email, KPIs, Charts, Explorer, Insights, Downloads
- 📥 **Multi-format Export** — CSV, Excel (styled), and text reports
- 🔎 **Global Search** — Search across all data columns instantly
- ⚡ **Performance Caching** — Lightning-fast data loading with Streamlit caching

### Technical Quality
- 📝 **Type Hints** — Complete type annotations across all modules
- 📖 **Docstrings** — Comprehensive Google-style documentation
- 🧪 **Unit Tests** — 30+ tests covering core modules
- 📋 **Logging** — Structured logging with Loguru (console + file)
- 🐳 **Docker Ready** — Dockerfile and docker-compose.yml included
- 📦 **UV Managed** — Modern Python package management

## 🏗️ Architecture

```
EduPro_Demographics/
│
├── data/                          # Source data
│   └── users.xlsx                 # Learner demographics dataset
│
├── src/                           # Core source modules
│   ├── config.py                  # Centralized configuration
│   ├── logger.py                  # Loguru logging setup
│   ├── data_loader.py             # Data loading & validation
│   ├── validator.py               # Data quality checks
│   ├── preprocessing.py           # Cleaning & feature engineering
│   ├── analysis.py                # KPIs & analytical functions
│   ├── visualization.py           # 25+ Plotly chart generators
│   ├── dashboard.py               # UI components & CSS
│   ├── export.py                  # CSV/Excel/Report export
│   └── utils.py                   # Helper functions
│
├── streamlit_app/                 # Streamlit dashboard
│   ├── app.py                     # Main entry point
│   ├── pages/                     # Multi-page dashboard
│   │   ├── 01_Overview.py
│   │   ├── 02_Age_Analysis.py
│   │   ├── 03_Gender_Analysis.py
│   │   ├── 04_Email_Analysis.py
│   │   ├── 05_KPIs.py
│   │   ├── 06_Charts.py
│   │   ├── 07_Data_Explorer.py
│   │   ├── 08_Insights.py
│   │   └── 09_Downloads.py
│   ├── components/                # Reusable UI components
│   └── assets/                    # Static assets
│
├── outputs/                       # Generated outputs
│   ├── charts/                    # Exported chart images
│   ├── cleaned_data/              # Cleaned datasets
│   ├── reports/                   # Generated reports
│   └── logs/                      # Application logs
│
├── tests/                         # Unit tests (pytest)
├── docs/                          # Documentation
├── notebooks/                     # Jupyter notebooks
│
├── .streamlit/config.toml         # Streamlit configuration
├── pyproject.toml                 # UV project configuration
├── Dockerfile                     # Container configuration
├── docker-compose.yml             # Container orchestration
├── README.md                      # This file
├── LICENSE                        # MIT License
└── .gitignore                     # Git ignore rules
```

## 🚀 Installation

### Prerequisites
- **Python 3.10+**
- **UV** (Python package manager)

### Step 1: Install UV

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone & Setup

```bash
# Navigate to project directory
cd EduPro_Demographics

# Initialize UV environment
uv venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv sync
```

### Step 3: Place Your Data

Ensure `users.xlsx` is in the `data/` directory with columns:
- `UserID`, `UserName`, `Age`, `Gender`, `Email`

## ⚡ Quick Start

```powershell
# Windows PowerShell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app/app.py
```

If `uv` is blocked by Windows Application Control policy, use the command above to start the dashboard directly from the project virtual environment. Once Streamlit starts successfully, the dashboard will open in your browser at **http://localhost:8501**. If it does not open automatically, visit the URL manually. 🎉

## 🐳 Running with Docker

```bash
# Build and run
docker-compose up --build

# Access at http://localhost:8501
```

## 🧪 Running Tests

```bash
uv run pytest tests/ -v
```

## 📊 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.12** | Core programming language |
| **Streamlit** | Web dashboard framework |
| **Plotly** | Interactive data visualizations |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Loguru** | Structured logging |
| **UV** | Package management |
| **Docker** | Containerized deployment |
| **Pytest** | Unit testing framework |
| **XlsxWriter** | Excel export with styling |

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/installation.md) | Detailed setup instructions |
| [Deployment Guide](docs/deployment.md) | Production deployment options |
| [Developer Guide](docs/developer_guide.md) | Architecture & contribution guidelines |

## 🔮 Future Improvements

- [ ] Add time-series analysis for enrollment trends
- [ ] Implement PDF report generation with charts
- [ ] Add user authentication for dashboard access
- [ ] Integrate with cloud databases (PostgreSQL, MongoDB)
- [ ] Add real-time data streaming capabilities
- [ ] Implement A/B testing analysis module
- [ ] Add geographic analysis with location data
- [ ] Create REST API endpoints for programmatic access
- [ ] Add automated email scheduling for reports
- [ ] Implement data comparison across time periods

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by EduPro Analytics Team**

🎓 EduPro Demographics Analytics Dashboard v1.0.0

</div>
