# 🛠️ Developer Guide

## Architecture Overview

The application follows a **modular layered architecture**:

```
┌─────────────────────────────────────┐
│         Streamlit Dashboard         │  ← Presentation Layer
│  (app.py + pages/ + components/)    │
├─────────────────────────────────────┤
│          src/ Modules               │  ← Business Logic Layer
│  analysis │ visualization │ export  │
├─────────────────────────────────────┤
│      Data Processing Pipeline       │  ← Data Layer
│  data_loader │ validator │ preproc  │
├─────────────────────────────────────┤
│         Infrastructure              │  ← Infrastructure Layer
│   config │ logger │ utils           │
└─────────────────────────────────────┘
```

---

## Module Responsibilities

| Module | Purpose |
|--------|---------|
| `config.py` | Centralized paths, constants, colors, Plotly defaults |
| `logger.py` | Loguru-based structured logging (console + file) |
| `data_loader.py` | Excel loading, column validation, data summary |
| `validator.py` | 10+ data quality checks → ValidationReport |
| `preprocessing.py` | Cleaning pipeline + feature engineering |
| `analysis.py` | KPIs, distributions, cross-tabs, rankings |
| `visualization.py` | 25+ Plotly chart generators |
| `dashboard.py` | Custom CSS, KPI cards, sidebar filters, UI components |
| `export.py` | CSV/Excel export + report generation |
| `utils.py` | Number formatting, insights, helper functions |

---

## Data Flow

```
users.xlsx → data_loader → validator → preprocessing → analysis → visualization
                                                         ↓
                                                    dashboard (Streamlit)
                                                         ↓
                                                    export (CSV/Excel/Reports)
```

---

## Adding a New Chart

1. **Create the chart function** in `src/visualization.py`:
   ```python
   def plot_new_chart(df: pd.DataFrame) -> go.Figure:
       fig = px.bar(df, x="column", y="count")
       return _apply_layout(fig, "Chart Title")
   ```

2. **Import and use** in the appropriate page:
   ```python
   from src.visualization import plot_new_chart
   st.plotly_chart(plot_new_chart(filtered), use_container_width=True)
   ```

---

## Adding a New Analysis Function

1. **Add the function** in `src/analysis.py`
2. **Write tests** in `tests/test_analysis.py`
3. **Import and use** in the relevant Streamlit page

---

## Adding a New Page

1. Create a new file in `streamlit_app/pages/`:
   ```
   10_🆕_NewPage.py
   ```

2. Follow the page template pattern:
   ```python
   import sys
   from pathlib import Path
   import streamlit as st

   PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
   sys.path.insert(0, str(PROJECT_ROOT))

   from src.dashboard import inject_custom_css, render_page_header
   # ... imports ...

   st.set_page_config(page_title="New Page | EduPro", page_icon="🆕", layout="wide")

   @st.cache_data(show_spinner=False)
   def get_data():
       # Load and process data
       pass

   def main():
       inject_custom_css()
       # Page content
       pass

   main()
   ```

---

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=src

# Run specific test file
uv run pytest tests/test_analysis.py -v
```

---

## Code Style

- **PEP 8** compliance
- **Type hints** on all function signatures
- **Google-style docstrings** for all public functions
- **Loguru logging** for all significant operations
- **Exception handling** with descriptive error messages

---

## Git Workflow

```bash
git init
git add .
git commit -m "Initial commit: EduPro Demographics Analytics Dashboard"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
