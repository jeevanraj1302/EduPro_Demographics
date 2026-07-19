"""
EduPro Demographics — Geographic Analysis Module
==================================================
Provides geographic analysis functions for country and region data.
"""

from typing import Optional

import pandas as pd
from loguru import logger

from src.config import COUNTRY_ISO_MAP, COUNTRY_REGION_MAP


# ══════════════════════════════════════════════
# Country Analysis
# ══════════════════════════════════════════════
def get_country_distribution(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """Get the top N countries by learner count."""
    if "Country" not in df.columns:
        return pd.DataFrame()
    dist = df["Country"].value_counts().head(top_n).reset_index()
    dist.columns = ["Country", "Count"]
    dist["Percentage"] = (dist["Count"] / len(df) * 100).round(1)
    dist["ISO"] = dist["Country"].map(COUNTRY_ISO_MAP).fillna("OTH")
    return dist


def get_region_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Get distribution by geographic region."""
    if "Region" not in df.columns:
        return pd.DataFrame()
    dist = df["Region"].value_counts().reset_index()
    dist.columns = ["Region", "Count"]
    dist["Percentage"] = (dist["Count"] / len(df) * 100).round(1)
    return dist


def get_country_age_stats(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Get age statistics grouped by country."""
    if "Country" not in df.columns or "Age" not in df.columns:
        return pd.DataFrame()
    top_countries = df["Country"].value_counts().head(top_n).index
    filtered = df[df["Country"].isin(top_countries)]
    return (
        filtered.groupby("Country")["Age"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(1)
        .sort_values("count", ascending=False)
        .reset_index()
    )


def get_country_gender_distribution(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Cross-tabulation of country by gender."""
    if "Country" not in df.columns or "Gender" not in df.columns:
        return pd.DataFrame()
    top_countries = df["Country"].value_counts().head(top_n).index
    filtered = df[df["Country"].isin(top_countries)]
    return pd.crosstab(
        filtered["Country"], filtered["Gender"],
        margins=True, margins_name="Total"
    ).reset_index()


def get_region_age_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Get age statistics grouped by region."""
    if "Region" not in df.columns or "Age" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("Region")["Age"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(1)
        .sort_values("count", ascending=False)
        .reset_index()
    )


def get_country_email_distribution(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Cross-tabulation of top countries by email provider."""
    if "Country" not in df.columns or "EmailProvider" not in df.columns:
        return pd.DataFrame()
    top_countries = df["Country"].value_counts().head(top_n).index
    filtered = df[df["Country"].isin(top_countries)]
    return pd.crosstab(
        filtered["Country"], filtered["EmailProvider"],
        margins=True, margins_name="Total"
    ).reset_index()


def get_geo_kpis(df: pd.DataFrame) -> dict:
    """Compute geographic-specific KPIs."""
    if "Country" not in df.columns:
        return {}

    top_country = df["Country"].mode().iloc[0] if not df["Country"].mode().empty else "N/A"
    top_region = df["Region"].mode().iloc[0] if "Region" in df.columns and not df["Region"].mode().empty else "N/A"

    return {
        "unique_countries": df["Country"].nunique(),
        "unique_regions": df["Region"].nunique() if "Region" in df.columns else 0,
        "top_country": top_country,
        "top_country_pct": round(
            (df["Country"] == top_country).sum() / len(df) * 100, 1
        ),
        "top_region": top_region,
        "top_region_pct": round(
            (df["Region"] == top_region).sum() / len(df) * 100, 1
        ) if "Region" in df.columns else 0,
    }


def get_choropleth_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare data for a Plotly choropleth world map."""
    if "Country" not in df.columns:
        return pd.DataFrame()

    dist = df["Country"].value_counts().reset_index()
    dist.columns = ["Country", "Count"]
    dist["ISO"] = dist["Country"].map(COUNTRY_ISO_MAP).fillna("OTH")
    dist["Percentage"] = (dist["Count"] / len(df) * 100).round(1)
    return dist
