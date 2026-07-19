"""
EduPro Demographics — Data Explorer Page
==========================================
Interactive data table with search, sorting, filtering, and pagination.
"""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard import (
    inject_custom_css, render_page_header, render_section_header,
    render_sidebar_filters, render_kpi_card,
)
from src.data_loader import load_users_data
from src.preprocessing import preprocess_data
from src.analysis import compute_kpis
from src.export import export_to_csv, export_to_excel

st.set_page_config(page_title="Data Explorer | EduPro", page_icon="🔍", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return raw, preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    raw_df, cleaned_df = get_data()
    filtered = render_sidebar_filters(cleaned_df)

    render_page_header("🔍 Data Explorer", "Browse, search, and explore the learner dataset")

    # ── Quick Stats ──
    cols = st.columns(4)
    with cols[0]:
        render_kpi_card("📋", f"{len(filtered):,}", "Filtered Records")
    with cols[1]:
        render_kpi_card("📊", len(filtered.columns), "Columns")
    with cols[2]:
        render_kpi_card("💾", f"{filtered.memory_usage(deep=True).sum() / 1024:.1f} KB", "Memory")
    with cols[3]:
        render_kpi_card("🔢", f"{filtered.isnull().sum().sum()}", "Null Values")

    # ── Data Tabs ──
    tab1, tab2 = st.tabs(["📋 Cleaned Data", "📋 Raw Data"])

    with tab1:
        render_section_header("📋 Cleaned & Enriched Dataset", "Preprocessed data with engineered features")

        # Search
        search = st.text_input(
            "🔍 Search across all columns",
            placeholder="Type to search (e.g., 'gmail', 'Male', 'U00100')...",
            key="search_cleaned",
        )

        display_df = filtered.copy()
        if search:
            mask = display_df.astype(str).apply(
                lambda col: col.str.contains(search, case=False, na=False)
            ).any(axis=1)
            display_df = display_df[mask]
            st.success(f"Found {len(display_df):,} matching records.")

        # Column selector
        all_cols = display_df.columns.tolist()
        selected_cols = st.multiselect(
            "Select columns to display",
            options=all_cols,
            default=all_cols,
            key="cols_cleaned",
        )

        if selected_cols:
            st.dataframe(
                display_df[selected_cols],
                use_container_width=True,
                hide_index=True,
                height=500,
            )
        else:
            st.warning("Please select at least one column.")

        # Download buttons
        st.markdown("")
        col1, col2, _ , _ = st.columns(4)
        with col1:
            st.download_button(
                "📥 Download CSV",
                data=export_to_csv(display_df),
                file_name="edupro_filtered_data.csv",
                mime="text/csv",
                key="dl_csv_cleaned",
            )
        with col2:
            st.download_button(
                "📥 Download Excel",
                data=export_to_excel(display_df),
                file_name="edupro_filtered_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_xlsx_cleaned",
            )

    with tab2:
        render_section_header("📋 Raw Dataset", "Original data before preprocessing")

        search_raw = st.text_input(
            "🔍 Search raw data",
            placeholder="Type to search...",
            key="search_raw",
        )

        raw_display = raw_df.copy()
        if search_raw:
            mask = raw_display.astype(str).apply(
                lambda col: col.str.contains(search_raw, case=False, na=False)
            ).any(axis=1)
            raw_display = raw_display[mask]
            st.success(f"Found {len(raw_display):,} matching records.")

        st.dataframe(
            raw_display,
            use_container_width=True,
            hide_index=True,
            height=500,
        )

        col1, col2, _, _ = st.columns(4)
        with col1:
            st.download_button(
                "📥 Download Raw CSV",
                data=export_to_csv(raw_display),
                file_name="edupro_raw_data.csv",
                mime="text/csv",
                key="dl_csv_raw",
            )

    # ── Column Info ──
    render_section_header("📊 Column Information")
    col_info = pd.DataFrame({
        "Column": cleaned_df.columns,
        "Type": cleaned_df.dtypes.astype(str).values,
        "Non-Null": cleaned_df.notnull().sum().values,
        "Null": cleaned_df.isnull().sum().values,
        "Unique": cleaned_df.nunique().values,
    })
    st.dataframe(col_info, use_container_width=True, hide_index=True)


main()
