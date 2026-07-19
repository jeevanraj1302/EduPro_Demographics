"""
EduPro Demographics — Email Analysis Page
===========================================
Analysis of learner email domains and providers.
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
from src.analysis import (
    compute_kpis, get_email_provider_distribution, get_email_domain_distribution,
    get_email_provider_by_gender, get_email_provider_by_age_group,
)
from src.visualization import (
    plot_email_provider_bar, plot_email_provider_pie, plot_email_provider_donut,
    plot_email_domain_horizontal_bar, plot_email_provider_by_gender,
    plot_username_length_histogram,
)

st.set_page_config(page_title="Email Analysis | EduPro", page_icon="📧", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    df = get_data()
    filtered = render_sidebar_filters(df)
    kpis = compute_kpis(filtered)

    render_page_header("📧 Email Analysis", "Email provider usage patterns across learners")

    # ── KPIs ──
    st.markdown("")
    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("📧", kpis["most_common_provider"], "Top Provider")
    with cols[1]:
        render_kpi_card("🌐", kpis["unique_email_providers"], "Unique Providers")
    with cols[2]:
        render_kpi_card("📝", kpis["avg_username_length"], "Avg Username Len")
    with cols[3]:
        unique_domains = filtered["EmailDomain"].nunique() if "EmailDomain" in filtered.columns else 0
        render_kpi_card("🔗", unique_domains, "Unique Domains")

    # ── Email Provider Distribution ──
    render_section_header("📧 Email Provider Distribution", "Which email services learners prefer")

    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart", "🍩 Donut Chart"])
    with tab1:
        st.plotly_chart(plot_email_provider_bar(filtered), use_container_width=True, key="ep_bar")
    with tab2:
        st.plotly_chart(plot_email_provider_pie(filtered), use_container_width=True, key="ep_pie")
    with tab3:
        st.plotly_chart(plot_email_provider_donut(filtered), use_container_width=True, key="ep_donut")

    # ── Provider Distribution Table ──
    ep_dist = get_email_provider_distribution(filtered)
    if not ep_dist.empty:
        st.dataframe(ep_dist, use_container_width=True, hide_index=True)

    # ── Top Email Domains ──
    render_section_header("🌐 Top Email Domains", "Most frequently used email domains")

    top_n = st.slider("Number of domains to display", 5, 20, 10, key="domain_slider")
    st.plotly_chart(
        plot_email_domain_horizontal_bar(filtered, top_n=top_n),
        use_container_width=True,
        key="ed_hbar",
    )

    ed_dist = get_email_domain_distribution(filtered, top_n=top_n)
    if not ed_dist.empty:
        st.dataframe(ed_dist, use_container_width=True, hide_index=True)

    # ── Email Provider by Gender ──
    render_section_header("📧 × 👥 Email Provider by Gender", "Cross-analysis of email usage by gender")

    st.plotly_chart(plot_email_provider_by_gender(filtered), use_container_width=True, key="ep_gender")

    ep_gender = get_email_provider_by_gender(filtered)
    if not ep_gender.empty:
        st.dataframe(ep_gender, use_container_width=True, hide_index=True)

    # ── Email Provider by Age Group ──
    render_section_header("📧 × 📅 Email Provider by Age Group")
    ep_age = get_email_provider_by_age_group(filtered)
    if not ep_age.empty:
        st.dataframe(ep_age, use_container_width=True, hide_index=True)

    # ── Username Length ──
    render_section_header("📝 Username Length Analysis", "Distribution of learner username lengths")
    st.plotly_chart(
        plot_username_length_histogram(filtered),
        use_container_width=True,
        key="uname_hist",
    )


main()
