"""
EduPro Demographics — Gender Analysis Page
============================================
In-depth analysis of learner gender demographics.
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
    compute_kpis, get_gender_distribution, get_age_group_by_gender,
    get_email_provider_by_gender,
)
from src.visualization import (
    plot_gender_bar, plot_gender_pie, plot_gender_donut,
    plot_gender_horizontal_bar, plot_age_by_gender_box,
    plot_age_group_by_gender_grouped, plot_age_group_by_gender_stacked,
    plot_heatmap_age_gender,
)

st.set_page_config(page_title="Gender Analysis | EduPro", page_icon="👥", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    df = get_data()
    filtered = render_sidebar_filters(df)
    kpis = compute_kpis(filtered)

    render_page_header("👥 Gender Analysis", "Comprehensive gender demographics and cross-analysis")

    # ── KPIs ──
    st.markdown("")
    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("♂️", f"{kpis['male_count']:,}", "Male Learners")
    with cols[1]:
        render_kpi_card("♀️", f"{kpis['female_count']:,}", "Female Learners")
    with cols[2]:
        render_kpi_card("⚖️", kpis["gender_ratio"], "Ratio (M:F)")
    with cols[3]:
        render_kpi_card("👥", f"{len(filtered):,}", "Total (Filtered)")

    # ── Gender Distribution Charts ──
    render_section_header("📊 Gender Distribution", "How learners are distributed by gender")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Bar", "📊 Horizontal", "🥧 Pie", "🍩 Donut"])
    with tab1:
        st.plotly_chart(plot_gender_bar(filtered), use_container_width=True, key="g_bar")
    with tab2:
        st.plotly_chart(plot_gender_horizontal_bar(filtered), use_container_width=True, key="g_hbar")
    with tab3:
        st.plotly_chart(plot_gender_pie(filtered), use_container_width=True, key="g_pie")
    with tab4:
        st.plotly_chart(plot_gender_donut(filtered), use_container_width=True, key="g_donut")

    # ── Gender Distribution Table ──
    gender_dist = get_gender_distribution(filtered)
    if not gender_dist.empty:
        st.dataframe(gender_dist, use_container_width=True, hide_index=True)

    # ── Gender × Age Analysis ──
    render_section_header("📊 Gender × Age Cross-Analysis", "How age patterns differ across genders")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_age_by_gender_box(filtered), use_container_width=True, key="g_age_box")
    with col2:
        st.plotly_chart(plot_heatmap_age_gender(filtered), use_container_width=True, key="g_heatmap")

    # ── Grouped and Stacked ──
    tab1, tab2 = st.tabs(["📊 Grouped Bar", "📊 Stacked Bar"])
    with tab1:
        st.plotly_chart(plot_age_group_by_gender_grouped(filtered), use_container_width=True, key="g_grouped")
    with tab2:
        st.plotly_chart(plot_age_group_by_gender_stacked(filtered), use_container_width=True, key="g_stacked")

    # ── Cross-tabulation Tables ──
    render_section_header("📋 Cross-Tabulation Tables")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Age Group × Gender")
        ct = get_age_group_by_gender(filtered)
        if not ct.empty:
            st.dataframe(ct, use_container_width=True, hide_index=True)
    with col2:
        st.markdown("#### Email Provider × Gender")
        ct2 = get_email_provider_by_gender(filtered)
        if not ct2.empty:
            st.dataframe(ct2, use_container_width=True, hide_index=True)


main()
