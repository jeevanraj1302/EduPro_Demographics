"""
EduPro Demographics — Overview Page
=====================================
High-level platform summary with KPIs, data quality status,
and top-level distributions.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard import inject_custom_css, render_page_header, render_kpi_card, render_section_header
from src.analysis import (
    compute_kpis, get_gender_distribution, get_age_group_distribution,
    get_age_category_distribution, get_email_provider_distribution,
    get_descriptive_stats,
)
from src.data_loader import load_users_data, get_data_summary
from src.preprocessing import preprocess_data
from src.validator import validate_dataset

st.set_page_config(page_title="Overview | EduPro", page_icon="🎓", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    vr = validate_dataset(raw)
    cleaned = preprocess_data(raw, save=False)
    kpis = compute_kpis(cleaned)
    return raw, cleaned, vr, kpis


def main():
    inject_custom_css()
    raw_df, df, vr, kpis = get_data()

    render_page_header("📋 Platform Overview", "Complete summary of the EduPro learner database")

    # ── KPI Grid: 4 + 4 + 4 ──
    st.markdown("")
    row1 = st.columns(4)
    with row1[0]:
        render_kpi_card("👥", f"{kpis['total_learners']:,}", "Total Learners")
    with row1[1]:
        render_kpi_card("📅", kpis["average_age"], "Average Age")
    with row1[2]:
        render_kpi_card("📊", kpis["median_age"], "Median Age")
    with row1[3]:
        render_kpi_card("🔢", f"{kpis['min_age']}–{kpis['max_age']}", "Age Range")

    st.markdown("")
    row2 = st.columns(4)
    with row2[0]:
        render_kpi_card("♂️", f"{kpis['male_count']:,}", "Male Learners")
    with row2[1]:
        render_kpi_card("♀️", f"{kpis['female_count']:,}", "Female Learners")
    with row2[2]:
        render_kpi_card("⚖️", kpis["gender_ratio"], "Gender Ratio (M:F)")
    with row2[3]:
        render_kpi_card("📧", kpis["most_common_provider"], "Top Email Provider")

    st.markdown("")
    row3 = st.columns(4)
    with row3[0]:
        render_kpi_card("🔞", f"{kpis['minor_count']:,}", "Minors (< 18)")
    with row3[1]:
        render_kpi_card("🧑", f"{kpis['adult_count']:,}", "Adults (≥ 18)")
    with row3[2]:
        render_kpi_card("🌐", kpis["unique_email_providers"], "Email Providers")
    with row3[3]:
        render_kpi_card("📝", kpis["avg_username_length"], "Avg Username Len")

    # ── Data Quality Status ──
    render_section_header("🔍 Data Quality Status", "Automated validation results")

    errors = vr.get_issues_by_severity("ERROR")
    warnings = vr.get_issues_by_severity("WARNING")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Overall Status", "✅ Passed" if vr.is_valid else "❌ Issues Found")
    with col2:
        st.metric("Errors", len(errors))
    with col3:
        st.metric("Warnings", len(warnings))

    with st.expander("📋 Detailed Validation Results", expanded=False):
        for issue in vr.issues:
            icon = "✅" if issue.count == 0 else ("⚠️" if issue.severity == "WARNING" else "❌")
            st.markdown(f"**{icon} {issue.check_name}** — {issue.message}")

    # ── Quick Distribution Tables ──
    render_section_header("📊 Quick Distributions", "At-a-glance breakdown of key demographics")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👤 Gender Distribution")
        gender_dist = get_gender_distribution(df)
        if not gender_dist.empty:
            st.dataframe(gender_dist, use_container_width=True, hide_index=True)

        st.markdown("#### 🔢 Age Group Distribution")
        age_dist = get_age_group_distribution(df)
        if not age_dist.empty:
            st.dataframe(age_dist, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### 📧 Email Provider Distribution")
        email_dist = get_email_provider_distribution(df)
        if not email_dist.empty:
            st.dataframe(email_dist, use_container_width=True, hide_index=True)

        st.markdown("#### 🧑 Age Category Distribution")
        cat_dist = get_age_category_distribution(df)
        if not cat_dist.empty:
            st.dataframe(cat_dist, use_container_width=True, hide_index=True)

    # ── Descriptive Statistics ──
    render_section_header("📈 Descriptive Statistics", "Numerical summary of the dataset")
    stats = get_descriptive_stats(df)
    if not stats.empty:
        st.dataframe(stats, use_container_width=True)


main()
