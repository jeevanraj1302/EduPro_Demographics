"""
EduPro Demographics — Utility Functions
=========================================
General-purpose helper functions used across the application.
"""

from typing import Any
from datetime import datetime

import pandas as pd
from loguru import logger


def format_number(value: Any, decimals: int = 0) -> str:
    """
    Format a number with comma separators.

    Parameters
    ----------
    value : Any
        Numeric value to format.
    decimals : int
        Number of decimal places.

    Returns
    -------
    str
        Formatted number string.
    """
    try:
        if decimals > 0:
            return f"{float(value):,.{decimals}f}"
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a value as a percentage string."""
    try:
        return f"{float(value):.{decimals}f}%"
    except (ValueError, TypeError):
        return "N/A"


def get_timestamp() -> str:
    """Return the current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date_string() -> str:
    """Return the current date as a formatted string for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to a maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def dataframe_info(df: pd.DataFrame) -> dict:
    """
    Get a quick summary dictionary of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to summarize.

    Returns
    -------
    dict
        Summary with rows, columns, memory, null counts, etc.
    """
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 3),
    }


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero."""
    if denominator == 0:
        return default
    return numerator / denominator


def generate_insights_text(df: pd.DataFrame, kpis: dict) -> list[dict]:
    """
    Generate a list of professional business insight dictionaries.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned user data.
    kpis : dict
        Computed KPI values.

    Returns
    -------
    list[dict]
        List of insight dictionaries with title, content, and style.
    """
    insights = []

    # 1. Age demographics
    total = kpis["total_learners"]
    insights.append({
        "title": "📊 Age Demographics Overview",
        "content": (
            f"The EduPro platform serves <b>{total:,}</b> learners with an average age of "
            f"<b>{kpis['average_age']}</b> years (median: {kpis['median_age']}). "
            f"Ages range from <b>{kpis['min_age']}</b> to <b>{kpis['max_age']}</b> years, "
            f"indicating a predominantly young user base. "
            f"The most common age is <b>{int(df['Age'].mode().iloc[0])}</b> years."
        ),
        "style": "info",
    })

    # 2. Minor/Adult split
    minor_pct = round(kpis["minor_count"] / total * 100, 1)
    adult_pct = round(kpis["adult_count"] / total * 100, 1)
    insights.append({
        "title": "🔒 Minor vs Adult Analysis",
        "content": (
            f"<b>{kpis['minor_count']:,}</b> learners ({minor_pct}%) are minors (under 18), "
            f"while <b>{kpis['adult_count']:,}</b> ({adult_pct}%) are adults. "
            f"{'This significant minor population requires compliance with child data protection regulations (COPPA/GDPR).' if minor_pct > 10 else 'The minor population is relatively small.'}"
        ),
        "style": "warning" if minor_pct > 10 else "default",
    })

    # 3. Gender balance
    male_pct = round(kpis["male_count"] / total * 100, 1)
    female_pct = round(kpis["female_count"] / total * 100, 1)
    balance_status = "well-balanced" if abs(male_pct - female_pct) < 10 else "imbalanced"
    insights.append({
        "title": "👥 Gender Balance Assessment",
        "content": (
            f"Gender distribution is <b>{balance_status}</b>: "
            f"Male {male_pct}% vs Female {female_pct}% "
            f"(Ratio: {kpis['gender_ratio']}). "
            f"{'Consider targeted outreach to improve representation.' if balance_status == 'imbalanced' else 'The platform demonstrates inclusive participation.'}"
        ),
        "style": "default" if balance_status == "well-balanced" else "warning",
    })

    # 4. Email providers
    insights.append({
        "title": "📧 Email Provider Intelligence",
        "content": (
            f"Learners use <b>{kpis['unique_email_providers']}</b> different email providers. "
            f"<b>{kpis['most_common_provider']}</b> is the most popular provider. "
            f"Marketing emails should be optimized for {kpis['most_common_provider']} deliverability standards."
        ),
        "style": "info",
    })

    # 5. Recommendations
    insights.append({
        "title": "💡 Strategic Recommendations",
        "content": (
            f"<b>1. Content Strategy:</b> Design courses for the {kpis['min_age']}–{kpis['max_age']} age range. "
            f"<b>2. Compliance:</b> Implement age verification for {kpis['minor_count']:,} minor learners. "
            f"<b>3. Growth:</b> Target underrepresented demographics to expand the user base. "
            f"<b>4. Communication:</b> Optimize email campaigns for {kpis['most_common_provider']} users."
        ),
        "style": "default",
    })

    return insights
