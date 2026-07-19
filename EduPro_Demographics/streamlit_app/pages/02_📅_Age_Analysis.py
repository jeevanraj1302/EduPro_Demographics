"""
EduPro Demographics — Age Analysis Page
=========================================
In-depth analysis of learner age demographics.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard import inject_custom_css, render_page_header, render_section_header, render_sidebar_filters
from src.data_loader import load_users_data
from src.preprocessing import preprocess_data
from src.analysis import (
    compute_kpis, get_age_distribution, get_age_group_distribution,
    get_age_category_distribution, get_top_oldest_learners, get_top_youngest_learners,
    get_most_common_age, get_age_by_gender,
)
from src.visualization import (
    plot_age_histogram, plot_age_boxplot, plot_age_violin,
    plot_age_group_bar, plot_age_group_pie, plot_age_group_donut,
    plot_age_line, plot_age_area, plot_minor_adult_bar,
    plot_age_scatter,
)
from src.dashboard import render_kpi_card

st.set_page_config(page_title="Age Analysis | EduPro", page_icon="📅", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    df = get_data()
    filtered = render_sidebar_filters(df)
    kpis = compute_kpis(filtered)

    render_page_header("📅 Age Analysis", "Comprehensive age demographics of EduPro learners")

    # ── KPIs ──
    st.markdown("")
    cols = st.columns(6)
    with cols[0]:
        render_kpi_card("📅", kpis["average_age"], "Average Age")
    with cols[1]:
        render_kpi_card("📊", kpis["median_age"], "Median Age")
    with cols[2]:
        render_kpi_card("⬇️", kpis["min_age"], "Youngest")
    with cols[3]:
        render_kpi_card("⬆️", kpis["max_age"], "Oldest")
    with cols[4]:
        render_kpi_card("🔢", get_most_common_age(filtered), "Most Common Age")
    with cols[5]:
        render_kpi_card("🔞", f"{kpis['minor_count']:,}", "Minors")

    # ── Age Distribution Charts ──
    render_section_header("📊 Age Distribution", "How learner ages are distributed across the platform")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogram", "📈 Line", "📈 Area", "🔬 Scatter"])

    with tab1:
        st.plotly_chart(plot_age_histogram(filtered), use_container_width=True, key="age_hist")
    with tab2:
        st.plotly_chart(plot_age_line(filtered), use_container_width=True, key="age_line")
    with tab3:
        st.plotly_chart(plot_age_area(filtered), use_container_width=True, key="age_area")
    with tab4:
        st.plotly_chart(plot_age_scatter(filtered), use_container_width=True, key="age_scatter")

    # ── Age Spread Charts ──
    render_section_header("📦 Age Spread Analysis", "Box plot and violin plot showing age variability")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_age_boxplot(filtered), use_container_width=True, key="age_box")
    with col2:
        st.plotly_chart(plot_age_violin(filtered), use_container_width=True, key="age_violin")

    # ── Age Group Analysis ──
    render_section_header("🏷️ Age Group Analysis", "Learners segmented by age brackets")

    tab1, tab2, tab3 = st.tabs(["📊 Bar Chart", "🥧 Pie Chart", "🍩 Donut Chart"])
    with tab1:
        st.plotly_chart(plot_age_group_bar(filtered), use_container_width=True, key="ag_bar")
    with tab2:
        st.plotly_chart(plot_age_group_pie(filtered), use_container_width=True, key="ag_pie")
    with tab3:
        st.plotly_chart(plot_age_group_donut(filtered), use_container_width=True, key="ag_donut")

    # ── Minor vs Adult ──
    render_section_header("🔞 Minor vs Adult", "Age category breakdown")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(plot_minor_adult_bar(filtered), use_container_width=True, key="minor_adult")
    with col2:
        cat_dist = get_age_category_distribution(filtered)
        if not cat_dist.empty:
            st.markdown("#### 📋 Age Category Summary")
            st.dataframe(cat_dist, use_container_width=True, hide_index=True)

        age_gender = get_age_by_gender(filtered)
        if not age_gender.empty:
            st.markdown("#### 📊 Age Stats by Gender")
            st.dataframe(age_gender, use_container_width=True, hide_index=True)

    # ── Age Frequency Table ──
    render_section_header("📋 Age Frequency Table")
    age_dist = get_age_distribution(filtered)
    if not age_dist.empty:
        st.dataframe(age_dist, use_container_width=True, hide_index=True, height=300)

    # ── Age Group Table ──
    render_section_header("📋 Age Group Summary Table")
    ag_dist = get_age_group_distribution(filtered)
    if not ag_dist.empty:
        st.dataframe(ag_dist, use_container_width=True, hide_index=True)

    # ── Top Learners ──
    render_section_header("🏆 Top Learners by Age")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👴 Top 20 Oldest Learners")
        oldest = get_top_oldest_learners(filtered)
        if not oldest.empty:
            st.dataframe(oldest, use_container_width=True, hide_index=True, height=400)
    with col2:
        st.markdown("#### 👶 Top 20 Youngest Learners")
        youngest = get_top_youngest_learners(filtered)
        if not youngest.empty:
            st.dataframe(youngest, use_container_width=True, hide_index=True, height=400)


main()
