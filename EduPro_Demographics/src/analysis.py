"""
EduPro Demographics — Analysis Module
=======================================
Contains all analytical functions for computing KPIs, distributions,
rankings, and business metrics from the cleaned users dataset.
"""

from typing import Any

import numpy as np
import pandas as pd
from loguru import logger


# ══════════════════════════════════════════════
# KPI Calculations
# ══════════════════════════════════════════════
def compute_kpis(df: pd.DataFrame) -> dict[str, Any]:
    """
    Calculate all Key Performance Indicators for the dashboard.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned user data with engineered features.

    Returns
    -------
    dict
        Dictionary of all KPI values.
    """
    logger.info("Computing KPIs...")

    total_learners = len(df)
    avg_age = round(df["Age"].mean(), 1) if "Age" in df.columns else 0
    median_age = round(df["Age"].median(), 1) if "Age" in df.columns else 0
    min_age = int(df["Age"].min()) if "Age" in df.columns else 0
    max_age = int(df["Age"].max()) if "Age" in df.columns else 0

    # Gender counts
    gender_counts = df["Gender"].value_counts().to_dict() if "Gender" in df.columns else {}
    male_count = gender_counts.get("Male", 0)
    female_count = gender_counts.get("Female", 0)
    other_count = gender_counts.get("Other", 0)

    # Gender ratio
    gender_ratio = (
        f"{round(male_count / female_count, 2)}:1"
        if female_count > 0
        else "N/A"
    )

    # Age categories
    minor_count = int((df["Age"] < 18).sum()) if "Age" in df.columns else 0
    adult_count = int((df["Age"] >= 18).sum()) if "Age" in df.columns else 0

    # Email providers
    unique_providers = (
        df["EmailProvider"].nunique()
        if "EmailProvider" in df.columns else 0
    )
    most_common_provider = (
        df["EmailProvider"].mode().iloc[0]
        if "EmailProvider" in df.columns and not df["EmailProvider"].mode().empty
        else "N/A"
    )

    # Username length
    avg_username_len = (
        round(df["UserNameLength"].mean(), 1)
        if "UserNameLength" in df.columns else 0
    )

    kpis = {
        "total_learners": total_learners,
        "average_age": avg_age,
        "median_age": median_age,
        "min_age": min_age,
        "max_age": max_age,
        "male_count": male_count,
        "female_count": female_count,
        "other_gender_count": other_count,
        "gender_ratio": gender_ratio,
        "minor_count": minor_count,
        "adult_count": adult_count,
        "unique_email_providers": unique_providers,
        "most_common_provider": most_common_provider,
        "avg_username_length": avg_username_len,
    }

    logger.success(f"KPIs computed: {len(kpis)} metrics.")
    return kpis


# ══════════════════════════════════════════════
# Distribution Analysis
# ══════════════════════════════════════════════
def get_age_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get the frequency distribution of ages."""
    if "Age" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["Age"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    dist.columns = ["Age", "Count"]
    return dist


def get_age_group_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get the count distribution by age group."""
    if "AgeGroup" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["AgeGroup"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    dist.columns = ["AgeGroup", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)
    return dist


def get_gender_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get the count and percentage distribution by gender."""
    if "Gender" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["Gender"]
        .value_counts()
        .reset_index()
    )
    dist.columns = ["Gender", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)
    return dist


def get_email_provider_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get the distribution of email providers."""
    if "EmailProvider" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["EmailProvider"]
        .value_counts()
        .reset_index()
    )
    dist.columns = ["EmailProvider", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)
    return dist


def get_email_domain_distribution(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Get the top N email domains by frequency."""
    if "EmailDomain" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["EmailDomain"]
        .value_counts()
        .head(top_n)
        .reset_index()
    )
    dist.columns = ["EmailDomain", "Count"]
    dist["Percentage"] = (dist["Count"] / len(df) * 100).round(1)
    return dist


def get_username_length_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get the distribution of username lengths."""
    if "UserNameLength" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["UserNameLength"]
        .value_counts()
        .sort_index()
        .reset_index()
    )
    dist.columns = ["Length", "Count"]
    return dist


def get_age_category_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get Minor vs Adult distribution."""
    if "AgeCategory" not in df.columns:
        return pd.DataFrame()
    dist = (
        df["AgeCategory"]
        .value_counts()
        .reset_index()
    )
    dist.columns = ["Category", "Count"]
    dist["Percentage"] = (dist["Count"] / dist["Count"].sum() * 100).round(1)
    return dist


# ══════════════════════════════════════════════
# Cross-Analysis
# ══════════════════════════════════════════════
def get_age_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Get age statistics grouped by gender."""
    if "Age" not in df.columns or "Gender" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("Gender")["Age"]
        .agg(["count", "mean", "median", "min", "max", "std"])
        .round(2)
        .reset_index()
    )


def get_age_group_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tabulation of age groups by gender."""
    if "AgeGroup" not in df.columns or "Gender" not in df.columns:
        return pd.DataFrame()
    return pd.crosstab(
        df["AgeGroup"], df["Gender"], margins=True, margins_name="Total"
    ).reset_index()


def get_email_provider_by_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tabulation of email providers by gender."""
    if "EmailProvider" not in df.columns or "Gender" not in df.columns:
        return pd.DataFrame()
    return pd.crosstab(
        df["EmailProvider"], df["Gender"], margins=True, margins_name="Total"
    ).reset_index()


def get_email_provider_by_age_group(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-tabulation of email providers by age group."""
    if "EmailProvider" not in df.columns or "AgeGroup" not in df.columns:
        return pd.DataFrame()
    return pd.crosstab(
        df["EmailProvider"], df["AgeGroup"], margins=True, margins_name="Total"
    ).reset_index()


# ══════════════════════════════════════════════
# Rankings
# ══════════════════════════════════════════════
def get_top_oldest_learners(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Get the top N oldest learners."""
    if "Age" not in df.columns:
        return pd.DataFrame()
    return (
        df.nlargest(n, "Age")[["UserID", "UserName", "Age", "Gender", "Email"]]
        .reset_index(drop=True)
    )


def get_top_youngest_learners(df: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    """Get the top N youngest learners."""
    if "Age" not in df.columns:
        return pd.DataFrame()
    return (
        df.nsmallest(n, "Age")[["UserID", "UserName", "Age", "Gender", "Email"]]
        .reset_index(drop=True)
    )


def get_most_common_age(df: pd.DataFrame) -> int:
    """Return the most frequently occurring age."""
    if "Age" not in df.columns or df.empty:
        return 0
    return int(df["Age"].mode().iloc[0])


# ══════════════════════════════════════════════
# Summary Statistics
# ══════════════════════════════════════════════
def get_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Generate descriptive statistics for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame()
    stats = numeric_df.describe().T
    stats["missing"] = df[numeric_df.columns].isnull().sum()
    stats["missing_%"] = (stats["missing"] / len(df) * 100).round(2)
    return stats.round(2)


# ══════════════════════════════════════════════
# Time-Series / Enrollment Analysis
# ══════════════════════════════════════════════
def get_enrollment_trends(df: pd.DataFrame, freq: str = "M") -> pd.DataFrame:
    """
    Get enrollment counts aggregated by time frequency.

    Parameters
    ----------
    df : pd.DataFrame
        Data with EnrollmentDate column.
    freq : str
        Frequency: 'M' (monthly), 'W' (weekly), 'Q' (quarterly).

    Returns
    -------
    pd.DataFrame
        Time-series of enrollment counts.
    """
    if "EnrollmentDate" not in df.columns:
        return pd.DataFrame()

    df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
    grouped = (
        df.groupby(df["EnrollmentDate"].dt.to_period(freq))
        .size()
        .reset_index(name="Count")
    )
    grouped.columns = ["Period", "Count"]
    grouped["Period"] = grouped["Period"].astype(str)
    return grouped


def get_cumulative_enrollment(df: pd.DataFrame) -> pd.DataFrame:
    """Get cumulative enrollment over time (monthly)."""
    if "EnrollmentDate" not in df.columns:
        return pd.DataFrame()

    df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
    monthly = (
        df.groupby(df["EnrollmentDate"].dt.to_period("M"))
        .size()
        .reset_index(name="Count")
    )
    monthly.columns = ["Month", "Count"]
    monthly["Month"] = monthly["Month"].astype(str)
    monthly["Cumulative"] = monthly["Count"].cumsum()
    return monthly


def get_enrollment_seasonality(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze enrollment patterns by day-of-week and month."""
    if "EnrollmentDate" not in df.columns:
        return pd.DataFrame()

    df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
    df_temp = df.copy()
    df_temp["DayOfWeek"] = df_temp["EnrollmentDate"].dt.day_name()
    df_temp["MonthName"] = df_temp["EnrollmentDate"].dt.month_name()

    seasonality = pd.crosstab(df_temp["MonthName"], df_temp["DayOfWeek"])

    # Reorder
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December",
    ]
    seasonality = seasonality.reindex(
        index=[m for m in month_order if m in seasonality.index],
        columns=[d for d in day_order if d in seasonality.columns],
    )
    return seasonality


def get_enrollment_rate(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly enrollment growth rate."""
    if "EnrollmentDate" not in df.columns:
        return pd.DataFrame()

    df["EnrollmentDate"] = pd.to_datetime(df["EnrollmentDate"])
    monthly = (
        df.groupby(df["EnrollmentDate"].dt.to_period("M"))
        .size()
        .reset_index(name="Count")
    )
    monthly.columns = ["Month", "Count"]
    monthly["Month"] = monthly["Month"].astype(str)
    monthly["GrowthRate"] = (monthly["Count"].pct_change() * 100).round(1)
    monthly["AvgDailyRate"] = (monthly["Count"] / 30).round(1)
    return monthly

