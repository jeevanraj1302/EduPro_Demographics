"""
EduPro Demographics — Dashboard Utilities Module
==================================================
Helper functions used across Streamlit dashboard pages
for rendering KPI cards, filters, and styled components.
"""

from typing import Any, Optional

import streamlit as st
import pandas as pd
from src.config import COLORS


# ══════════════════════════════════════════════
# Custom CSS Injection
# ══════════════════════════════════════════════
def inject_custom_css() -> None:
    """Inject custom CSS for the premium dark-theme dashboard."""
    st.markdown("""
    <style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Styles ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Main Container ── */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12141D 0%, #1A1D29 100%);
        border-right: 1px solid #2D3142;
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #FAFAFA;
    }

    /* ── KPI Card ── */
    .kpi-card {
        background: linear-gradient(135deg, #1A1D29 0%, #252836 100%);
        border: 1px solid #2D3142;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6C63FF, #FF6584);
        border-radius: 16px 16px 0 0;
    }

    .kpi-card:hover {
        border-color: #6C63FF;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(108, 99, 255, 0.15);
    }

    .kpi-icon {
        font-size: 1.8rem;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C63FF, #FF6584);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.2rem 0;
        line-height: 1.2;
    }

    .kpi-label {
        font-size: 0.85rem;
        color: #A0A3B1;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Section Header ── */
    .section-header {
        background: linear-gradient(135deg, #1A1D29 0%, #252836 100%);
        border: 1px solid #2D3142;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #6C63FF;
    }

    .section-header h2 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
        color: #FAFAFA;
    }

    .section-header p {
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
        color: #A0A3B1;
    }

    /* ── Insight Card ── */
    .insight-card {
        background: linear-gradient(135deg, #1A1D29 0%, #1E2130 100%);
        border: 1px solid #2D3142;
        border-left: 4px solid #00C896;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
    }

    .insight-card.warning {
        border-left-color: #FFB547;
    }

    .insight-card.info {
        border-left-color: #00D2FF;
    }

    .insight-card.danger {
        border-left-color: #FF4757;
    }

    .insight-card h4 {
        margin: 0 0 0.5rem 0;
        color: #FAFAFA;
        font-size: 1rem;
    }

    .insight-card p {
        margin: 0;
        color: #A0A3B1;
        font-size: 0.92rem;
        line-height: 1.5;
    }

    /* ── Data Table Styling ── */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }

    /* ── Tab Styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: #1A1D29;
        border: 1px solid #2D3142;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        color: #A0A3B1;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6C63FF, #8B83FF) !important;
        color: white !important;
        border-color: #6C63FF !important;
    }

    /* ── Button Styling ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6C63FF, #8B83FF);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #4A42D4, #6C63FF);
        box-shadow: 0 4px 15px rgba(108, 99, 255, 0.3);
    }

    /* ── Metric Container ── */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #6C63FF;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #A0A3B1;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Divider ── */
    hr {
        border-color: #2D3142;
        margin: 1.5rem 0;
    }

    /* ── Hide Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# KPI Card Renderer
# ══════════════════════════════════════════════
def render_kpi_card(icon: str, value: Any, label: str) -> None:
    """
    Render a single KPI metric card with gradient styling.

    Parameters
    ----------
    icon : str
        Emoji icon to display.
    value : Any
        The KPI value (number, string, etc.).
    label : str
        Short descriptive label for the metric.
    """
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_row(kpis: dict[str, Any]) -> None:
    """
    Render a row of key KPI cards in a 4-column grid.

    Parameters
    ----------
    kpis : dict
        Dictionary of KPI values from ``compute_kpis()``.
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card("👥", f"{kpis['total_learners']:,}", "Total Learners")
    with col2:
        render_kpi_card("📅", kpis["average_age"], "Average Age")
    with col3:
        render_kpi_card("♂️", f"{kpis['male_count']:,}", "Male Learners")
    with col4:
        render_kpi_card("♀️", f"{kpis['female_count']:,}", "Female Learners")


# ══════════════════════════════════════════════
# Section Header
# ══════════════════════════════════════════════
def render_section_header(title: str, subtitle: str = "") -> None:
    """Render a styled section header with optional subtitle."""
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="section-header">
        <h2>{title}</h2>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# Insight Card
# ══════════════════════════════════════════════
def render_insight_card(
    title: str,
    content: str,
    style: str = "default",
) -> None:
    """
    Render a styled insight card.

    Parameters
    ----------
    title : str
        Card heading.
    content : str
        Card body text (supports HTML).
    style : str
        Card style: "default", "warning", "info", or "danger".
    """
    css_class = f"insight-card {style}" if style != "default" else "insight-card"
    st.markdown(f"""
    <div class="{css_class}">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# Page Header
# ══════════════════════════════════════════════
def render_page_header(title: str, subtitle: str = "") -> None:
    """Render a page-level header with gradient title."""
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <h1 style="
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6C63FF, #FF6584);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
        ">{title}</h1>
        <p style="color: #A0A3B1; font-size: 1rem; margin-top: 0.3rem;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# Sidebar Filters
# ══════════════════════════════════════════════
def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render sidebar filters and return the filtered DataFrame.

    Filters
    -------
    - Age Range Slider
    - Gender Multiselect
    - Age Group Multiselect
    - Email Provider Multiselect

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned data to filter.

    Returns
    -------
    pd.DataFrame
        Filtered DataFrame based on user selections.
    """
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 0.8rem 0;">
            <h1 style="
                font-size: 1.6rem;
                font-weight: 800;
                background: linear-gradient(135deg, #6C63FF, #FF6584);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
            ">🎓 EduPro</h1>
            <p style="color: #A0A3B1; font-size: 0.8rem; margin: 0.2rem 0;">
                Demographics Analytics
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🔍 Filters")

        filtered = df.copy()

        # Age Range
        if "Age" in df.columns:
            min_age = int(df["Age"].min())
            max_age = int(df["Age"].max())
            age_range = st.slider(
                "📅 Age Range",
                min_value=min_age,
                max_value=max_age,
                value=(min_age, max_age),
                key="filter_age_range",
            )
            filtered = filtered[
                (filtered["Age"] >= age_range[0]) &
                (filtered["Age"] <= age_range[1])
            ]

        # Gender
        if "Gender" in df.columns:
            genders = df["Gender"].unique().tolist()
            selected_genders = st.multiselect(
                "👤 Gender",
                options=genders,
                default=genders,
                key="filter_gender",
            )
            if selected_genders:
                filtered = filtered[filtered["Gender"].isin(selected_genders)]

        # Age Group
        if "AgeGroup" in df.columns:
            age_groups = sorted(df["AgeGroup"].dropna().unique().tolist(), key=str)
            selected_groups = st.multiselect(
                "📊 Age Group",
                options=age_groups,
                default=age_groups,
                key="filter_age_group",
            )
            if selected_groups:
                filtered = filtered[filtered["AgeGroup"].isin(selected_groups)]

        # Email Provider
        if "EmailProvider" in df.columns:
            providers = sorted(df["EmailProvider"].unique().tolist())
            selected_providers = st.multiselect(
                "📧 Email Provider",
                options=providers,
                default=providers,
                key="filter_email_provider",
            )
            if selected_providers:
                filtered = filtered[filtered["EmailProvider"].isin(selected_providers)]

        # Filter summary
        st.markdown("---")
        st.markdown(f"""
        <div style="
            background: rgba(108, 99, 255, 0.1);
            border: 1px solid #6C63FF;
            border-radius: 8px;
            padding: 0.8rem;
            text-align: center;
        ">
            <p style="margin: 0; color: #A0A3B1; font-size: 0.8rem;">Showing</p>
            <p style="margin: 0; font-size: 1.4rem; font-weight: 700; color: #6C63FF;">
                {len(filtered):,}
            </p>
            <p style="margin: 0; color: #A0A3B1; font-size: 0.8rem;">
                of {len(df):,} learners
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #6B7280; font-size: 0.75rem;'>"
            "EduPro Analytics v1.0.0<br>© 2026</p>",
            unsafe_allow_html=True,
        )

    return filtered
