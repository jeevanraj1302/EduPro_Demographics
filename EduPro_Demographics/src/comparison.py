"""
EduPro Demographics — Period Comparison Module
================================================
Compare metrics across time periods: month-over-month,
quarter-over-quarter, year-over-year analysis.
"""

from typing import Any

import pandas as pd
import numpy as np
from loguru import logger


# ══════════════════════════════════════════════
# Period Splitting
# ══════════════════════════════════════════════
def split_by_period(
    df: pd.DataFrame,
    period_a_start: str,
    period_a_end: str,
    period_b_start: str,
    period_b_end: str,
    date_column: str = "EnrollmentDate",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into two time periods for comparison.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (period_a_df, period_b_df)
    """
    df[date_column] = pd.to_datetime(df[date_column])
    period_a = df[
        (df[date_column] >= pd.Timestamp(period_a_start)) &
        (df[date_column] <= pd.Timestamp(period_a_end))
    ]
    period_b = df[
        (df[date_column] >= pd.Timestamp(period_b_start)) &
        (df[date_column] <= pd.Timestamp(period_b_end))
    ]
    logger.info(
        f"Period split: A ({period_a_start} to {period_a_end}) = {len(period_a):,}, "
        f"B ({period_b_start} to {period_b_end}) = {len(period_b):,}"
    )
    return period_a, period_b


def get_available_periods(
    df: pd.DataFrame,
    date_column: str = "EnrollmentDate",
) -> dict[str, list[str]]:
    """Get available months, quarters, and years for period selection."""
    df[date_column] = pd.to_datetime(df[date_column])
    months = sorted(df[date_column].dt.to_period("M").unique().astype(str).tolist())
    quarters = sorted(df[date_column].dt.to_period("Q").unique().astype(str).tolist())
    years = sorted(df[date_column].dt.year.unique().astype(str).tolist())
    return {"months": months, "quarters": quarters, "years": years}


# ══════════════════════════════════════════════
# Period KPI Comparison
# ══════════════════════════════════════════════
def _safe_pct_change(old: float, new: float) -> float:
    """Calculate percentage change safely."""
    if old == 0:
        return 100.0 if new > 0 else 0.0
    return round((new - old) / old * 100, 1)


def compare_period_kpis(
    period_a: pd.DataFrame,
    period_b: pd.DataFrame,
    period_a_label: str = "Period A",
    period_b_label: str = "Period B",
) -> list[dict[str, Any]]:
    """
    Compare KPIs between two periods.

    Returns
    -------
    list[dict]
        List of metric comparison dicts with deltas.
    """
    metrics = []

    # Enrollment count
    a_count = len(period_a)
    b_count = len(period_b)
    metrics.append({
        "metric": "New Enrollments",
        "icon": "👥",
        "period_a": f"{a_count:,}",
        "period_b": f"{b_count:,}",
        "delta": b_count - a_count,
        "pct_change": _safe_pct_change(a_count, b_count),
        "trend": "up" if b_count > a_count else ("down" if b_count < a_count else "flat"),
    })

    # Average Age
    if "Age" in period_a.columns and "Age" in period_b.columns:
        a_avg = round(period_a["Age"].mean(), 1) if len(period_a) > 0 else 0
        b_avg = round(period_b["Age"].mean(), 1) if len(period_b) > 0 else 0
        metrics.append({
            "metric": "Average Age",
            "icon": "📅",
            "period_a": str(a_avg),
            "period_b": str(b_avg),
            "delta": round(b_avg - a_avg, 1),
            "pct_change": _safe_pct_change(a_avg, b_avg),
            "trend": "up" if b_avg > a_avg else ("down" if b_avg < a_avg else "flat"),
        })

    # Gender ratio
    if "Gender" in period_a.columns and "Gender" in period_b.columns:
        a_male = round((period_a["Gender"] == "Male").mean() * 100, 1) if len(period_a) > 0 else 0
        b_male = round((period_b["Gender"] == "Male").mean() * 100, 1) if len(period_b) > 0 else 0
        metrics.append({
            "metric": "Male %",
            "icon": "♂️",
            "period_a": f"{a_male}%",
            "period_b": f"{b_male}%",
            "delta": round(b_male - a_male, 1),
            "pct_change": _safe_pct_change(a_male, b_male),
            "trend": "up" if b_male > a_male else ("down" if b_male < a_male else "flat"),
        })

    # Minor percentage
    if "AgeCategory" in period_a.columns and "AgeCategory" in period_b.columns:
        a_minor = round((period_a["AgeCategory"] == "Minor").mean() * 100, 1) if len(period_a) > 0 else 0
        b_minor = round((period_b["AgeCategory"] == "Minor").mean() * 100, 1) if len(period_b) > 0 else 0
        metrics.append({
            "metric": "Minor %",
            "icon": "🔞",
            "period_a": f"{a_minor}%",
            "period_b": f"{b_minor}%",
            "delta": round(b_minor - a_minor, 1),
            "pct_change": _safe_pct_change(a_minor, b_minor),
            "trend": "up" if b_minor > a_minor else ("down" if b_minor < a_minor else "flat"),
        })

    # Unique email providers
    if "EmailProvider" in period_a.columns and "EmailProvider" in period_b.columns:
        a_providers = period_a["EmailProvider"].nunique() if len(period_a) > 0 else 0
        b_providers = period_b["EmailProvider"].nunique() if len(period_b) > 0 else 0
        metrics.append({
            "metric": "Email Providers",
            "icon": "📧",
            "period_a": str(a_providers),
            "period_b": str(b_providers),
            "delta": b_providers - a_providers,
            "pct_change": _safe_pct_change(a_providers, b_providers),
            "trend": "up" if b_providers > a_providers else ("down" if b_providers < a_providers else "flat"),
        })

    return metrics


# ══════════════════════════════════════════════
# Trend Analysis
# ══════════════════════════════════════════════
def get_monthly_growth_rates(
    df: pd.DataFrame,
    date_column: str = "EnrollmentDate",
) -> pd.DataFrame:
    """
    Calculate month-over-month growth rates.

    Returns
    -------
    pd.DataFrame
        Monthly enrollment counts and growth rates.
    """
    if date_column not in df.columns:
        return pd.DataFrame()

    df[date_column] = pd.to_datetime(df[date_column])
    monthly = (
        df.groupby(df[date_column].dt.to_period("M"))
        .size()
        .reset_index(name="Count")
    )
    monthly.columns = ["Month", "Count"]
    monthly["Month"] = monthly["Month"].astype(str)
    monthly["Growth_Rate"] = monthly["Count"].pct_change() * 100
    monthly["Growth_Rate"] = monthly["Growth_Rate"].round(1)
    monthly["Cumulative"] = monthly["Count"].cumsum()
    return monthly


def get_quarterly_comparison(
    df: pd.DataFrame,
    date_column: str = "EnrollmentDate",
) -> pd.DataFrame:
    """Get quarterly enrollment comparison."""
    if date_column not in df.columns:
        return pd.DataFrame()

    df[date_column] = pd.to_datetime(df[date_column])
    quarterly = (
        df.groupby(df[date_column].dt.to_period("Q"))
        .size()
        .reset_index(name="Count")
    )
    quarterly.columns = ["Quarter", "Count"]
    quarterly["Quarter"] = quarterly["Quarter"].astype(str)
    quarterly["Growth_Rate"] = quarterly["Count"].pct_change() * 100
    quarterly["Growth_Rate"] = quarterly["Growth_Rate"].round(1)
    return quarterly


def get_demographic_trends(
    df: pd.DataFrame,
    date_column: str = "EnrollmentDate",
) -> pd.DataFrame:
    """Track how demographics change over time (monthly)."""
    if date_column not in df.columns:
        return pd.DataFrame()

    df[date_column] = pd.to_datetime(df[date_column])
    df["_month"] = df[date_column].dt.to_period("M").astype(str)

    trends = []
    for month in sorted(df["_month"].unique()):
        month_df = df[df["_month"] == month]
        trends.append({
            "Month": month,
            "Enrollments": len(month_df),
            "Avg_Age": round(month_df["Age"].mean(), 1) if "Age" in month_df.columns else 0,
            "Male_Pct": round(
                (month_df["Gender"] == "Male").sum() / len(month_df) * 100, 1
            ) if "Gender" in month_df.columns and len(month_df) > 0 else 0,
            "Minor_Pct": round(
                (month_df["AgeCategory"] == "Minor").sum() / len(month_df) * 100, 1
            ) if "AgeCategory" in month_df.columns and len(month_df) > 0 else 0,
        })

    df.drop("_month", axis=1, inplace=True, errors="ignore")
    return pd.DataFrame(trends)
