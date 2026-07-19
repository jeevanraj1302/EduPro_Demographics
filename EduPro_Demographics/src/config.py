"""
EduPro Demographics — Configuration Module
============================================
Centralized configuration for paths, constants, color palettes,
and application-wide settings.
"""

from pathlib import Path
from typing import Final
import os

# ──────────────────────────────────────────────
# Path Configuration
# ──────────────────────────────────────────────
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
OUTPUT_DIR: Final[Path] = PROJECT_ROOT / "outputs"
CHARTS_DIR: Final[Path] = OUTPUT_DIR / "charts"
CLEANED_DATA_DIR: Final[Path] = OUTPUT_DIR / "cleaned_data"
REPORTS_DIR: Final[Path] = OUTPUT_DIR / "reports"
LOGS_DIR: Final[Path] = OUTPUT_DIR / "logs"
EMAILS_DIR: Final[Path] = OUTPUT_DIR / "emails"

# Source data file
DATA_FILE: Final[Path] = DATA_DIR / "users.xlsx"
CLEANED_DATA_FILE: Final[Path] = CLEANED_DATA_DIR / "cleaned_users.xlsx"

# Auth configuration
AUTH_CONFIG_FILE: Final[Path] = PROJECT_ROOT / ".streamlit" / "auth_config.yaml"

# ──────────────────────────────────────────────
# Ensure output directories exist
# ──────────────────────────────────────────────
for _dir in [CHARTS_DIR, CLEANED_DATA_DIR, REPORTS_DIR, LOGS_DIR, EMAILS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────
# Application Constants
# ──────────────────────────────────────────────
APP_TITLE: Final[str] = "EduPro Demographics Analytics"
APP_ICON: Final[str] = "🎓"
APP_VERSION: Final[str] = "1.0.0"
APP_DESCRIPTION: Final[str] = (
    "Industry-grade Business Intelligence dashboard for analyzing "
    "learner demographics on the EduPro platform."
)

# ──────────────────────────────────────────────
# Dataset Schema
# ──────────────────────────────────────────────
EXPECTED_COLUMNS: Final[list[str]] = [
    "UserID", "UserName", "Age", "Gender", "Email"
]

# ──────────────────────────────────────────────
# Age Group Bins
# ──────────────────────────────────────────────
AGE_BINS: Final[list[int]] = [0, 17, 25, 35, 45, 60, 120]
AGE_LABELS: Final[list[str]] = [
    "0–17", "18–25", "26–35", "36–45", "46–60", "60+"
]

# ──────────────────────────────────────────────
# Gender Normalization Map
# ──────────────────────────────────────────────
GENDER_MAP: Final[dict[str, str]] = {
    "male": "Male",
    "m": "Male",
    "man": "Male",
    "boy": "Male",
    "female": "Female",
    "f": "Female",
    "woman": "Female",
    "girl": "Female",
    "other": "Other",
    "non-binary": "Other",
    "nonbinary": "Other",
    "prefer not to say": "Other",
}

VALID_GENDERS: Final[list[str]] = ["Male", "Female", "Other"]

# ──────────────────────────────────────────────
# Color Palette — Professional Purple Theme
# ──────────────────────────────────────────────
COLORS: Final[dict[str, str]] = {
    "primary": "#6C63FF",
    "primary_light": "#8B83FF",
    "primary_dark": "#4A42D4",
    "secondary": "#FF6584",
    "accent": "#00D2FF",
    "success": "#00C896",
    "warning": "#FFB547",
    "danger": "#FF4757",
    "bg_dark": "#0E1117",
    "bg_card": "#1A1D29",
    "bg_card_hover": "#252836",
    "text_primary": "#FAFAFA",
    "text_secondary": "#A0A3B1",
    "text_muted": "#6B7280",
    "border": "#2D3142",
    "gradient_start": "#6C63FF",
    "gradient_end": "#FF6584",
}

# Chart color sequence for Plotly
CHART_COLORS: Final[list[str]] = [
    "#6C63FF", "#FF6584", "#00D2FF", "#00C896", "#FFB547",
    "#FF4757", "#8B83FF", "#FF8FA3", "#36D7B7", "#F39C12",
    "#9B59B6", "#3498DB", "#E74C3C", "#1ABC9C", "#F1C40F",
    "#E67E22", "#2ECC71", "#C0392B", "#16A085", "#D35400",
]

# Gender-specific colors
GENDER_COLORS: Final[dict[str, str]] = {
    "Male": "#00D2FF",
    "Female": "#FF6584",
    "Other": "#FFB547",
}

# ──────────────────────────────────────────────
# Plotly Layout Defaults
# ──────────────────────────────────────────────
PLOTLY_LAYOUT: Final[dict] = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": {"family": "Inter, sans-serif", "color": "#FAFAFA", "size": 13},
    "title_font": {"size": 18, "color": "#FAFAFA", "family": "Inter, sans-serif"},
    "hoverlabel": {
        "bgcolor": "#1A1D29",
        "font_size": 13,
        "font_family": "Inter, sans-serif",
        "bordercolor": "#6C63FF",
    },
    "margin": {"l": 40, "r": 30, "t": 60, "b": 40},
    "colorway": CHART_COLORS,
}

# ──────────────────────────────────────────────
# Logging Configuration
# ──────────────────────────────────────────────
LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE: Final[Path] = LOGS_DIR / "edupro.log"
LOG_ROTATION: Final[str] = "10 MB"
LOG_RETENTION: Final[str] = "7 days"

# ──────────────────────────────────────────────
# Enrollment Date Configuration (Synthetic)
# ──────────────────────────────────────────────
ENROLLMENT_START_DATE: Final[str] = "2024-01-01"
ENROLLMENT_END_DATE: Final[str] = "2025-12-31"

# ──────────────────────────────────────────────
# Geographic Configuration (Synthetic)
# ──────────────────────────────────────────────
COUNTRIES_DISTRIBUTION: Final[dict[str, float]] = {
    "India": 0.30, "United States": 0.18, "United Kingdom": 0.10,
    "Canada": 0.07, "Australia": 0.06, "Germany": 0.05,
    "Nigeria": 0.05, "Brazil": 0.04, "Singapore": 0.03,
    "South Africa": 0.03, "UAE": 0.02, "France": 0.02,
    "Japan": 0.02, "Kenya": 0.02, "Other": 0.01,
}

COUNTRY_ISO_MAP: Final[dict[str, str]] = {
    "India": "IND", "United States": "USA", "United Kingdom": "GBR",
    "Canada": "CAN", "Australia": "AUS", "Germany": "DEU",
    "Nigeria": "NGA", "Brazil": "BRA", "Singapore": "SGP",
    "South Africa": "ZAF", "UAE": "ARE", "France": "FRA",
    "Japan": "JPN", "Kenya": "KEN", "Other": "OTH",
}

COUNTRY_REGION_MAP: Final[dict[str, str]] = {
    "India": "Asia", "United States": "North America",
    "United Kingdom": "Europe", "Canada": "North America",
    "Australia": "Oceania", "Germany": "Europe",
    "Nigeria": "Africa", "Brazil": "South America",
    "Singapore": "Asia", "South Africa": "Africa",
    "UAE": "Middle East", "France": "Europe",
    "Japan": "Asia", "Kenya": "Africa", "Other": "Other",
}

# ──────────────────────────────────────────────
# Database Configuration
# ──────────────────────────────────────────────
DB_TYPE: Final[str] = os.getenv("DB_TYPE", "sqlite")  # sqlite, postgresql, mongodb
DB_CONNECTION_STRING: Final[str] = os.getenv(
    "DB_CONNECTION_STRING",
    f"sqlite:///{OUTPUT_DIR / 'edupro.db'}",
)

# ──────────────────────────────────────────────
# Streaming Configuration
# ──────────────────────────────────────────────
STREAM_INTERVAL_SECONDS: Final[int] = int(os.getenv("STREAM_INTERVAL", "5"))
STREAM_BATCH_SIZE: Final[int] = int(os.getenv("STREAM_BATCH_SIZE", "3"))

# ──────────────────────────────────────────────
# Email Configuration
# ──────────────────────────────────────────────
SMTP_HOST: Final[str] = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT: Final[int] = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER: Final[str] = os.getenv("SMTP_USER", "")
SMTP_PASSWORD: Final[str] = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM: Final[str] = os.getenv("EMAIL_FROM", "edupro-analytics@example.com")
EMAIL_DEMO_MODE: Final[bool] = os.getenv("EMAIL_DEMO_MODE", "true").lower() == "true"
