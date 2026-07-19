"""
EduPro Demographics — Main Streamlit Application
==================================================
Entry point for the Streamlit dashboard.
Handles data loading, caching, preprocessing, and navigation setup.
"""

import sys
from pathlib import Path

import streamlit as st

# ── Ensure project root is on sys.path ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import APP_TITLE, APP_ICON, APP_DESCRIPTION
from src.data_loader import load_users_data
from src.preprocessing import preprocess_data
from src.validator import validate_dataset
from src.analysis import compute_kpis
from src.dashboard import inject_custom_css, render_page_header, render_kpi_row, render_sidebar_filters
from src.visualization import (
    plot_age_histogram, plot_gender_donut, plot_age_group_bar, plot_email_provider_bar,
)
from src.utils import generate_insights_text
from src.dashboard import render_insight_card


# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────
# Data Loading & Caching
# ──────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_and_process_data():
    """Load, validate, preprocess data and compute KPIs. Cached for performance."""
    raw_df = load_users_data()
    validation_report = validate_dataset(raw_df)
    cleaned_df = preprocess_data(raw_df, save=True)
    kpis = compute_kpis(cleaned_df)
    return raw_df, cleaned_df, validation_report, kpis


# ──────────────────────────────────────────────
# Main App
# ──────────────────────────────────────────────
def main():
    """Main entry point for the EduPro Demographics Dashboard."""
    # Inject custom CSS
    inject_custom_css()

    # Load data with spinner
    with st.spinner("🔄 Loading and processing data..."):
        try:
            raw_df, cleaned_df, validation_report, kpis = load_and_process_data()
        except FileNotFoundError as e:
            st.error(f"❌ {e}")
            st.info("💡 Please place your `users.xlsx` file in the `data/` directory.")
            st.stop()
        except Exception as e:
            st.error(f"❌ An error occurred while loading data: {e}")
            st.stop()

    # Store data in session state for pages to access
    st.session_state["raw_df"] = raw_df
    st.session_state["cleaned_df"] = cleaned_df
    st.session_state["validation_report"] = validation_report
    st.session_state["kpis"] = kpis

    # Sidebar filters
    filtered_df = render_sidebar_filters(cleaned_df)
    st.session_state["filtered_df"] = filtered_df

    # Recompute KPIs for filtered data
    filtered_kpis = compute_kpis(filtered_df)
    st.session_state["filtered_kpis"] = filtered_kpis

    # ── Page Header ──
    render_page_header(
        f"{APP_ICON} EduPro Demographics Dashboard",
        APP_DESCRIPTION,
    )

    st.markdown("")

    # ── KPI Cards ──
    render_kpi_row(filtered_kpis)

    st.markdown("")

    # ── Quick Charts Row ──
    col1, col2 = st.columns(2)
    with col1:
        fig = plot_age_histogram(filtered_df)
        st.plotly_chart(fig, use_container_width=True, key="home_age_hist")
    with col2:
        fig = plot_gender_donut(filtered_df)
        st.plotly_chart(fig, use_container_width=True, key="home_gender_donut")

    col3, col4 = st.columns(2)
    with col3:
        fig = plot_age_group_bar(filtered_df)
        st.plotly_chart(fig, use_container_width=True, key="home_age_group")
    with col4:
        fig = plot_email_provider_bar(filtered_df)
        st.plotly_chart(fig, use_container_width=True, key="home_email_provider")

    # ── Quick Insights ──
    st.markdown("")
    st.markdown("### 💡 Key Insights")
    insights = generate_insights_text(filtered_df, filtered_kpis)
    for insight in insights[:3]:
        render_insight_card(
            insight["title"],
            insight["content"],
            insight["style"],
        )

    # ── Footer ──
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #6B7280; font-size: 0.8rem;'>"
        "🎓 EduPro Demographics Analytics Dashboard v1.0.0 | "
        "Built with Streamlit & Plotly | © 2026 EduPro Analytics Team"
        "</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
