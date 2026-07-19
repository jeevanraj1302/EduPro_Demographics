"""
EduPro Demographics — Downloads Page
======================================
Export data, charts, and reports in multiple formats.
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
from src.validator import validate_dataset
from src.analysis import compute_kpis
from src.export import (
    export_to_csv, export_to_excel,
    generate_executive_summary, generate_data_quality_report,
    generate_business_report,
)

st.set_page_config(page_title="Downloads | EduPro", page_icon="📥", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    vr = validate_dataset(raw)
    cleaned = preprocess_data(raw, save=False)
    kpis = compute_kpis(cleaned)
    return raw, cleaned, vr, kpis


def main():
    inject_custom_css()
    raw_df, cleaned_df, vr, kpis = get_data()
    filtered = render_sidebar_filters(cleaned_df)
    filtered_kpis = compute_kpis(filtered)

    render_page_header("📥 Downloads Center", "Export data and reports in multiple formats")

    # ── Data Exports ──
    render_section_header("💾 Data Exports", "Download the dataset in various formats")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📋</div>
            <div class="kpi-label">Filtered Data (CSV)</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "📥 Download Filtered CSV",
            data=export_to_csv(filtered),
            file_name="edupro_filtered_users.csv",
            mime="text/csv",
            key="dl_filtered_csv",
            use_container_width=True,
        )

    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Filtered Data (Excel)</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "📥 Download Filtered Excel",
            data=export_to_excel(filtered),
            file_name="edupro_filtered_users.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_filtered_xlsx",
            use_container_width=True,
        )

    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🗃️</div>
            <div class="kpi-label">Complete Cleaned Data (Excel)</div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button(
            "📥 Download Full Cleaned Excel",
            data=export_to_excel(cleaned_df, sheet_name="Cleaned Users"),
            file_name="edupro_cleaned_users.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="dl_full_xlsx",
            use_container_width=True,
        )

    st.markdown("")

    # ── Report Exports ──
    render_section_header("📝 Report Exports", "Download professionally formatted reports")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📄</div>
            <div class="kpi-label">Executive Summary</div>
        </div>
        """, unsafe_allow_html=True)
        exec_report = generate_executive_summary(filtered, filtered_kpis)
        st.download_button(
            "📥 Download Executive Summary",
            data=exec_report.encode("utf-8"),
            file_name="edupro_executive_summary.txt",
            mime="text/plain",
            key="dl_exec",
            use_container_width=True,
        )

    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">🔍</div>
            <div class="kpi-label">Data Quality Report</div>
        </div>
        """, unsafe_allow_html=True)
        dq_report = generate_data_quality_report(cleaned_df, vr)
        st.download_button(
            "📥 Download Quality Report",
            data=dq_report.encode("utf-8"),
            file_name="edupro_data_quality_report.txt",
            mime="text/plain",
            key="dl_dq",
            use_container_width=True,
        )

    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Business Analytics Report</div>
        </div>
        """, unsafe_allow_html=True)
        biz_report = generate_business_report(filtered, filtered_kpis)
        st.download_button(
            "📥 Download Business Report",
            data=biz_report.encode("utf-8"),
            file_name="edupro_business_report.txt",
            mime="text/plain",
            key="dl_biz",
            use_container_width=True,
        )

    # ── Report Previews ──
    st.markdown("")
    render_section_header("👁️ Report Previews", "Preview reports before downloading")

    tab1, tab2, tab3 = st.tabs([
        "📄 Executive Summary",
        "🔍 Data Quality Report",
        "📊 Business Report",
    ])

    with tab1:
        st.text(exec_report)

    with tab2:
        st.text(dq_report)

    with tab3:
        st.text(biz_report)

    # ── Export Info ──
    st.markdown("---")
    st.info(
        "💡 **Export Tip:** All data exports respect the current sidebar filters. "
        "Adjust filters to export specific subsets of the data. "
        "Reports are auto-generated from the filtered dataset."
    )


main()
