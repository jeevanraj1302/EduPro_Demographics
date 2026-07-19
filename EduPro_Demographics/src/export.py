"""
EduPro Demographics — Export Module
=====================================
Handles exporting data and reports in CSV, Excel, and PDF formats.
"""

import io
from datetime import datetime
from typing import Optional

import pandas as pd
from loguru import logger

from src.config import REPORTS_DIR, CLEANED_DATA_DIR


# ══════════════════════════════════════════════
# Data Export Functions
# ══════════════════════════════════════════════
def export_to_csv(df: pd.DataFrame) -> bytes:
    """
    Export DataFrame to CSV bytes for Streamlit download.

    Parameters
    ----------
    df : pd.DataFrame
        Data to export.

    Returns
    -------
    bytes
        CSV content as bytes.
    """
    logger.info(f"Exporting {len(df):,} rows to CSV.")
    return df.to_csv(index=False).encode("utf-8")


def export_to_excel(df: pd.DataFrame, sheet_name: str = "Users") -> bytes:
    """
    Export DataFrame to Excel bytes for Streamlit download.

    Parameters
    ----------
    df : pd.DataFrame
        Data to export.
    sheet_name : str
        Name of the worksheet.

    Returns
    -------
    bytes
        Excel file content as bytes.
    """
    logger.info(f"Exporting {len(df):,} rows to Excel.")
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)

        # Style the header
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        header_format = workbook.add_format({
            "bold": True,
            "text_wrap": True,
            "valign": "vcenter",
            "fg_color": "#6C63FF",
            "font_color": "#FFFFFF",
            "border": 1,
            "font_size": 11,
        })
        for col_num, value in enumerate(df.columns):
            worksheet.write(0, col_num, value, header_format)
            # Auto-width columns
            max_len = max(
                df[value].astype(str).str.len().max(),
                len(str(value))
            ) + 2
            worksheet.set_column(col_num, col_num, min(max_len, 40))

    buffer.seek(0)
    return buffer.getvalue()


# ══════════════════════════════════════════════
# Report Generation
# ══════════════════════════════════════════════
def generate_executive_summary(df: pd.DataFrame, kpis: dict) -> str:
    """
    Generate a professional executive summary report as text.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned user data.
    kpis : dict
        Computed KPI values.

    Returns
    -------
    str
        Formatted executive summary text.
    """
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Gender breakdown
    gender_dist = df["Gender"].value_counts()
    gender_lines = "\n".join(
        f"    • {g}: {c:,} ({c/len(df)*100:.1f}%)"
        for g, c in gender_dist.items()
    )

    # Age group breakdown
    age_group_lines = ""
    if "AgeGroup" in df.columns:
        ag_dist = df["AgeGroup"].value_counts().sort_index()
        age_group_lines = "\n".join(
            f"    • {g}: {c:,} ({c/len(df)*100:.1f}%)"
            for g, c in ag_dist.items()
        )

    # Email provider breakdown
    provider_lines = ""
    if "EmailProvider" in df.columns:
        ep_dist = df["EmailProvider"].value_counts()
        provider_lines = "\n".join(
            f"    • {p}: {c:,} ({c/len(df)*100:.1f}%)"
            for p, c in ep_dist.items()
        )

    report = f"""
{'='*70}
EDUPRO LEARNER DEMOGRAPHICS — EXECUTIVE SUMMARY
{'='*70}

Generated: {timestamp}
Report Type: Executive Summary
Data Source: EduPro Platform — Users Dataset

{'─'*70}
1. OVERVIEW
{'─'*70}

    Total Learners:           {kpis['total_learners']:,}
    Average Age:              {kpis['average_age']} years
    Median Age:               {kpis['median_age']} years
    Age Range:                {kpis['min_age']} – {kpis['max_age']} years
    Gender Ratio (M:F):       {kpis['gender_ratio']}

{'─'*70}
2. GENDER DISTRIBUTION
{'─'*70}

{gender_lines}

{'─'*70}
3. AGE GROUP DISTRIBUTION
{'─'*70}

{age_group_lines}

    Minors (< 18):            {kpis['minor_count']:,}
    Adults (≥ 18):            {kpis['adult_count']:,}

{'─'*70}
4. EMAIL PROVIDER DISTRIBUTION
{'─'*70}

{provider_lines}

    Unique Providers:         {kpis['unique_email_providers']}
    Most Common Provider:     {kpis['most_common_provider']}

{'─'*70}
5. USERNAME ANALYSIS
{'─'*70}

    Average Username Length:  {kpis['avg_username_length']} characters

{'─'*70}
6. KEY FINDINGS
{'─'*70}

    • The EduPro platform has {kpis['total_learners']:,} registered learners.
    • The average learner age is {kpis['average_age']} years, suggesting a
      predominantly young user base.
    • Gender distribution shows a ratio of {kpis['gender_ratio']} (Male to Female).
    • {kpis['minor_count']:,} learners ({kpis['minor_count']/kpis['total_learners']*100:.1f}%) are minors (under 18).
    • {kpis['most_common_provider']} is the most popular email provider.

{'─'*70}
7. RECOMMENDATIONS
{'─'*70}

    • Develop age-appropriate content for the {kpis['minor_count']:,} minor learners.
    • Consider targeted engagement strategies for underrepresented
      age groups to broaden the learner demographic.
    • Monitor gender balance and implement inclusive marketing campaigns.
    • Leverage email provider data for communication channel optimization.
    • Implement age verification for compliance with data protection
      regulations for minor learners.

{'='*70}
END OF REPORT
{'='*70}
"""

    # Save to file
    try:
        report_path = REPORTS_DIR / "executive_summary.txt"
        report_path.write_text(report, encoding="utf-8")
        logger.success(f"Executive summary saved to: {report_path}")
    except Exception as exc:
        logger.warning(f"Could not save report file: {exc}")

    return report


def generate_data_quality_report(df: pd.DataFrame, validation_report) -> str:
    """
    Generate a data quality report from validation results.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset being analyzed.
    validation_report : ValidationReport
        The validation results object.

    Returns
    -------
    str
        Formatted data quality report.
    """
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    issues_text = ""
    for issue in validation_report.issues:
        status = "✅" if issue.count == 0 else ("⚠️" if issue.severity == "WARNING" else "❌")
        issues_text += f"    {status} {issue.check_name}: {issue.message}\n"

    report = f"""
{'='*70}
EDUPRO — DATA QUALITY REPORT
{'='*70}

Generated: {timestamp}
Total Records: {validation_report.total_records:,}
Overall Status: {'✅ PASSED' if validation_report.is_valid else '❌ ISSUES FOUND'}
Total Issues: {validation_report.total_issues}

{'─'*70}
VALIDATION RESULTS
{'─'*70}

{issues_text}

{'─'*70}
SUMMARY STATISTICS
{'─'*70}

    Records:     {validation_report.summary_stats.get('total_records', 'N/A'):,}
    Columns:     {validation_report.summary_stats.get('total_columns', 'N/A')}
    Null %:      {validation_report.summary_stats.get('null_percentage', 'N/A')}%
    Memory:      {validation_report.summary_stats.get('memory_mb', 'N/A')} MB

{'='*70}
END OF DATA QUALITY REPORT
{'='*70}
"""

    try:
        report_path = REPORTS_DIR / "data_quality_report.txt"
        report_path.write_text(report, encoding="utf-8")
        logger.success(f"Data quality report saved to: {report_path}")
    except Exception as exc:
        logger.warning(f"Could not save report file: {exc}")

    return report


def generate_business_report(df: pd.DataFrame, kpis: dict) -> str:
    """
    Generate a detailed business analytics report.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned user data.
    kpis : dict
        Computed KPI values.

    Returns
    -------
    str
        Formatted business report.
    """
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")

    # Most common age
    most_common_age = int(df["Age"].mode().iloc[0]) if "Age" in df.columns else "N/A"

    report = f"""
{'='*70}
EDUPRO — BUSINESS ANALYTICS REPORT
{'='*70}

Generated: {timestamp}
Report Type: Comprehensive Business Analysis

{'─'*70}
1. PLATFORM METRICS
{'─'*70}

    Total Registered Learners:    {kpis['total_learners']:,}
    Average Learner Age:          {kpis['average_age']} years
    Median Learner Age:           {kpis['median_age']} years
    Most Common Age:              {most_common_age} years
    Youngest Learner:             {kpis['min_age']} years
    Oldest Learner:               {kpis['max_age']} years

{'─'*70}
2. DEMOGRAPHIC ANALYSIS
{'─'*70}

  2.1 Gender Analysis
    Male Learners:    {kpis['male_count']:,} ({kpis['male_count']/kpis['total_learners']*100:.1f}%)
    Female Learners:  {kpis['female_count']:,} ({kpis['female_count']/kpis['total_learners']*100:.1f}%)
    Gender Ratio:     {kpis['gender_ratio']}

  2.2 Age Segmentation
    Minors (< 18):    {kpis['minor_count']:,} ({kpis['minor_count']/kpis['total_learners']*100:.1f}%)
    Adults (≥ 18):    {kpis['adult_count']:,} ({kpis['adult_count']/kpis['total_learners']*100:.1f}%)

{'─'*70}
3. DIGITAL COMMUNICATION
{'─'*70}

    Unique Email Providers:       {kpis['unique_email_providers']}
    Most Popular Provider:        {kpis['most_common_provider']}
    Average Username Length:      {kpis['avg_username_length']} characters

{'─'*70}
4. STRATEGIC RECOMMENDATIONS
{'─'*70}

    a) CONTENT STRATEGY
       - Develop curriculum tailored to the {kpis['min_age']}–{kpis['max_age']} age range.
       - Create age-appropriate content for the {kpis['minor_count']:,} minor learners.

    b) MARKETING STRATEGY
       - Use {kpis['most_common_provider']} as the primary email communication channel.
       - Target marketing towards the dominant age demographic.
       - Implement gender-balanced marketing campaigns.

    c) COMPLIANCE
       - Ensure COPPA/GDPR compliance for {kpis['minor_count']:,} minor users.
       - Implement parental consent mechanisms where required.

    d) GROWTH OPPORTUNITIES
       - Expand outreach to underrepresented age groups.
       - Develop referral programs targeting the most active demographic.

{'='*70}
END OF BUSINESS REPORT
{'='*70}
"""

    try:
        report_path = REPORTS_DIR / "business_report.txt"
        report_path.write_text(report, encoding="utf-8")
        logger.success(f"Business report saved to: {report_path}")
    except Exception as exc:
        logger.warning(f"Could not save report file: {exc}")

    return report
