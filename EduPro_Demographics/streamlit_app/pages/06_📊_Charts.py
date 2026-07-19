"""
EduPro Demographics — Charts Gallery Page
===========================================
Complete gallery of all available interactive visualizations.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard import (
    inject_custom_css, render_page_header, render_section_header,
    render_sidebar_filters,
)
from src.data_loader import load_users_data
from src.preprocessing import preprocess_data
from src.visualization import (
    plot_age_histogram, plot_age_boxplot, plot_age_violin,
    plot_age_group_bar, plot_age_group_pie, plot_age_group_donut,
    plot_age_line, plot_age_area, plot_age_scatter,
    plot_minor_adult_bar,
    plot_gender_bar, plot_gender_pie, plot_gender_donut,
    plot_gender_horizontal_bar, plot_age_by_gender_box,
    plot_age_group_by_gender_grouped, plot_age_group_by_gender_stacked,
    plot_heatmap_age_gender,
    plot_email_provider_bar, plot_email_provider_pie, plot_email_provider_donut,
    plot_email_domain_horizontal_bar, plot_email_provider_by_gender,
    plot_username_length_histogram,
    plot_sunburst, plot_treemap,
)

st.set_page_config(page_title="Charts | EduPro", page_icon="📊", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    df = get_data()
    filtered = render_sidebar_filters(df)

    render_page_header("📊 Charts Gallery", "Complete collection of all interactive visualizations")

    # Chart category selector
    category = st.selectbox(
        "Select Chart Category",
        [
            "🔥 All Charts",
            "📅 Age Charts",
            "👥 Gender Charts",
            "📧 Email Charts",
            "🌟 Advanced Charts",
        ],
        key="chart_category",
    )

    if category in ["🔥 All Charts", "📅 Age Charts"]:
        render_section_header("📅 Age Visualizations")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_histogram(filtered), use_container_width=True, key="c_age_hist")
        with col2:
            st.plotly_chart(plot_age_line(filtered), use_container_width=True, key="c_age_line")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_area(filtered), use_container_width=True, key="c_age_area")
        with col2:
            st.plotly_chart(plot_age_scatter(filtered), use_container_width=True, key="c_age_scatter")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_boxplot(filtered), use_container_width=True, key="c_age_box")
        with col2:
            st.plotly_chart(plot_age_violin(filtered), use_container_width=True, key="c_age_violin")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_group_bar(filtered), use_container_width=True, key="c_ag_bar")
        with col2:
            st.plotly_chart(plot_age_group_pie(filtered), use_container_width=True, key="c_ag_pie")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_group_donut(filtered), use_container_width=True, key="c_ag_donut")
        with col2:
            st.plotly_chart(plot_minor_adult_bar(filtered), use_container_width=True, key="c_minor")

    if category in ["🔥 All Charts", "👥 Gender Charts"]:
        render_section_header("👥 Gender Visualizations")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_gender_bar(filtered), use_container_width=True, key="c_g_bar")
        with col2:
            st.plotly_chart(plot_gender_horizontal_bar(filtered), use_container_width=True, key="c_g_hbar")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_gender_pie(filtered), use_container_width=True, key="c_g_pie")
        with col2:
            st.plotly_chart(plot_gender_donut(filtered), use_container_width=True, key="c_g_donut")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_by_gender_box(filtered), use_container_width=True, key="c_g_box")
        with col2:
            st.plotly_chart(plot_heatmap_age_gender(filtered), use_container_width=True, key="c_g_heat")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_age_group_by_gender_grouped(filtered), use_container_width=True, key="c_g_grouped")
        with col2:
            st.plotly_chart(plot_age_group_by_gender_stacked(filtered), use_container_width=True, key="c_g_stacked")

    if category in ["🔥 All Charts", "📧 Email Charts"]:
        render_section_header("📧 Email Visualizations")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_email_provider_bar(filtered), use_container_width=True, key="c_ep_bar")
        with col2:
            st.plotly_chart(plot_email_provider_pie(filtered), use_container_width=True, key="c_ep_pie")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_email_provider_donut(filtered), use_container_width=True, key="c_ep_donut")
        with col2:
            st.plotly_chart(plot_email_domain_horizontal_bar(filtered), use_container_width=True, key="c_ed_hbar")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_email_provider_by_gender(filtered), use_container_width=True, key="c_ep_gender")
        with col2:
            st.plotly_chart(plot_username_length_histogram(filtered), use_container_width=True, key="c_uname")

    if category in ["🔥 All Charts", "🌟 Advanced Charts"]:
        render_section_header("🌟 Advanced Visualizations")

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_sunburst(filtered), use_container_width=True, key="c_sunburst")
        with col2:
            st.plotly_chart(plot_treemap(filtered), use_container_width=True, key="c_treemap")

    st.markdown("---")
    st.info(f"💡 **Tip:** All charts are interactive — hover for details, click legend items to filter, and use the camera icon to download as PNG.")


main()
