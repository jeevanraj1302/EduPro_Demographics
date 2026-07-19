"""
EduPro Demographics — KPIs Page
=================================
Dedicated KPI dashboard with all computed metrics.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard import (
    inject_custom_css, render_page_header, render_section_header,
    render_sidebar_filters, render_kpi_card,
)
from src.data_loader import load_users_data
from src.preprocessing import preprocess_data
from src.analysis import compute_kpis, get_most_common_age

st.set_page_config(page_title="KPIs | EduPro", page_icon="📈", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    df = get_data()
    filtered = render_sidebar_filters(df)
    kpis = compute_kpis(filtered)

    render_page_header("📈 Key Performance Indicators", "All computed metrics for the EduPro platform")

    # ── Learner Metrics ──
    render_section_header("👥 Learner Metrics")

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("👥", f"{kpis['total_learners']:,}", "Total Learners")
    with cols[1]:
        render_kpi_card("📅", kpis["average_age"], "Average Age")
    with cols[2]:
        render_kpi_card("📊", kpis["median_age"], "Median Age")
    with cols[3]:
        render_kpi_card("🔢", get_most_common_age(filtered), "Most Common Age")

    st.markdown("")

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("⬇️", kpis["min_age"], "Youngest Learner")
    with cols[1]:
        render_kpi_card("⬆️", kpis["max_age"], "Oldest Learner")
    with cols[2]:
        render_kpi_card("🔞", f"{kpis['minor_count']:,}", "Minors (< 18)")
    with cols[3]:
        render_kpi_card("🧑", f"{kpis['adult_count']:,}", "Adults (≥ 18)")

    # ── Gender Metrics ──
    render_section_header("👤 Gender Metrics")

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("♂️", f"{kpis['male_count']:,}", "Male Learners")
    with cols[1]:
        render_kpi_card("♀️", f"{kpis['female_count']:,}", "Female Learners")
    with cols[2]:
        render_kpi_card("⚖️", kpis["gender_ratio"], "Gender Ratio (M:F)")
    with cols[3]:
        male_pct = round(kpis["male_count"] / kpis["total_learners"] * 100, 1) if kpis["total_learners"] > 0 else 0
        render_kpi_card("📊", f"{male_pct}%", "Male Percentage")

    # ── Digital Metrics ──
    render_section_header("📧 Digital & Communication Metrics")

    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("📧", kpis["most_common_provider"], "Top Email Provider")
    with cols[1]:
        render_kpi_card("🌐", kpis["unique_email_providers"], "Unique Providers")
    with cols[2]:
        render_kpi_card("📝", kpis["avg_username_length"], "Avg Username Length")
    with cols[3]:
        unique_domains = filtered["EmailDomain"].nunique() if "EmailDomain" in filtered.columns else 0
        render_kpi_card("🔗", unique_domains, "Unique Domains")

    # ── KPI Summary Table ──
    render_section_header("📋 KPI Summary Table")

    kpi_table_data = [
        {"Metric": "Total Learners", "Value": f"{kpis['total_learners']:,}", "Category": "Learner"},
        {"Metric": "Average Age", "Value": str(kpis["average_age"]), "Category": "Age"},
        {"Metric": "Median Age", "Value": str(kpis["median_age"]), "Category": "Age"},
        {"Metric": "Minimum Age", "Value": str(kpis["min_age"]), "Category": "Age"},
        {"Metric": "Maximum Age", "Value": str(kpis["max_age"]), "Category": "Age"},
        {"Metric": "Most Common Age", "Value": str(get_most_common_age(filtered)), "Category": "Age"},
        {"Metric": "Male Count", "Value": f"{kpis['male_count']:,}", "Category": "Gender"},
        {"Metric": "Female Count", "Value": f"{kpis['female_count']:,}", "Category": "Gender"},
        {"Metric": "Gender Ratio (M:F)", "Value": kpis["gender_ratio"], "Category": "Gender"},
        {"Metric": "Minor Count", "Value": f"{kpis['minor_count']:,}", "Category": "Age"},
        {"Metric": "Adult Count", "Value": f"{kpis['adult_count']:,}", "Category": "Age"},
        {"Metric": "Top Email Provider", "Value": kpis["most_common_provider"], "Category": "Email"},
        {"Metric": "Unique Email Providers", "Value": str(kpis["unique_email_providers"]), "Category": "Email"},
        {"Metric": "Avg Username Length", "Value": str(kpis["avg_username_length"]), "Category": "Email"},
    ]

    import pandas as pd
    kpi_df = pd.DataFrame(kpi_table_data)
    st.dataframe(kpi_df, use_container_width=True, hide_index=True, height=500)


main()
