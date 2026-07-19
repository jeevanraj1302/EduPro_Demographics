"""
EduPro Demographics — Preprocessing Module
============================================
Handles data cleaning, normalization, feature engineering,
and export of the cleaned dataset. Never overwrites original files.
"""

import re
from typing import Optional

import numpy as np
import pandas as pd
from loguru import logger

from src.config import (
    AGE_BINS, AGE_LABELS, CLEANED_DATA_FILE, GENDER_MAP,
    ENROLLMENT_START_DATE, ENROLLMENT_END_DATE,
    COUNTRIES_DISTRIBUTION, COUNTRY_REGION_MAP,
)


# ──────────────────────────────────────────────
# Main Preprocessing Pipeline
# ──────────────────────────────────────────────
def preprocess_data(df: pd.DataFrame, save: bool = True) -> pd.DataFrame:
    """
    Execute the full preprocessing pipeline on raw user data.

    Steps
    -----
    1. Remove duplicate rows
    2. Trim whitespace from string columns
    3. Convert data types
    4. Normalize gender values
    5. Validate and clean emails
    6. Handle missing values
    7. Engineer new features (age groups, email domains, etc.)
    8. Save cleaned dataset

    Parameters
    ----------
    df : pd.DataFrame
        Raw user data.
    save : bool
        Whether to save the cleaned DataFrame to disk.

    Returns
    -------
    pd.DataFrame
        Cleaned and feature-enriched DataFrame.
    """
    logger.info("Starting preprocessing pipeline...")
    original_count = len(df)

    # Work on a copy so we never mutate the original
    df = df.copy()

    # Step 1: Remove duplicates
    df = _remove_duplicates(df)

    # Step 2: Trim whitespace
    df = _trim_whitespace(df)

    # Step 3: Convert data types
    df = _convert_types(df)

    # Step 4: Normalize gender
    df = _normalize_gender(df)

    # Step 5: Validate emails
    df = _clean_emails(df)

    # Step 6: Handle missing values
    df = _handle_missing_values(df)

    # Step 7: Feature engineering
    df = engineer_features(df)

    # Step 8: Reset index
    df = df.reset_index(drop=True)

    logger.success(
        f"Preprocessing complete: {original_count:,} → {len(df):,} records "
        f"({original_count - len(df)} removed). "
        f"Columns: {len(df.columns)}."
    )

    # Step 9: Save cleaned data
    if save:
        _save_cleaned_data(df)

    return df


# ──────────────────────────────────────────────
# Individual Cleaning Steps
# ──────────────────────────────────────────────
def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove fully duplicate rows and duplicate UserIDs."""
    before = len(df)
    df = df.drop_duplicates()
    after_full = len(df)

    if "UserID" in df.columns:
        df = df.drop_duplicates(subset=["UserID"], keep="first")

    after_id = len(df)
    removed = before - after_id
    if removed > 0:
        logger.info(f"Removed {removed} duplicate records.")
    else:
        logger.info("No duplicates found.")
    return df


def _trim_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all string columns."""
    str_cols = df.select_dtypes(include=["object"]).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()
        # Restore actual NaN values (they become 'nan' after str conversion)
        df[col] = df[col].replace({"nan": np.nan, "None": np.nan, "": np.nan})
    logger.info(f"Trimmed whitespace in {len(str_cols)} string columns.")
    return df


def _convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to appropriate data types."""
    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    if "UserID" in df.columns:
        df["UserID"] = df["UserID"].astype(str)
    logger.info("Data types converted.")
    return df


def _normalize_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize gender values using the mapping dictionary."""
    if "Gender" not in df.columns:
        return df

    df["Gender"] = (
        df["Gender"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map(GENDER_MAP)
        .fillna("Other")
    )
    logger.info(f"Gender normalized. Unique values: {df['Gender'].unique().tolist()}")
    return df


def _clean_emails(df: pd.DataFrame) -> pd.DataFrame:
    """Clean email addresses — lowercase and strip."""
    if "Email" not in df.columns:
        return df
    df["Email"] = df["Email"].astype(str).str.strip().str.lower()
    df["Email"] = df["Email"].replace({"nan": np.nan})
    logger.info("Emails cleaned and lowercased.")
    return df


def _handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values with appropriate strategies."""
    if "Age" in df.columns:
        median_age = df["Age"].median()
        null_ages = df["Age"].isnull().sum()
        if null_ages > 0:
            df["Age"] = df["Age"].fillna(median_age)
            logger.info(f"Filled {null_ages} missing ages with median ({median_age}).")

    if "Gender" in df.columns:
        null_genders = df["Gender"].isnull().sum()
        if null_genders > 0:
            df["Gender"] = df["Gender"].fillna("Other")
            logger.info(f"Filled {null_genders} missing genders with 'Other'.")

    if "UserName" in df.columns:
        null_names = df["UserName"].isnull().sum()
        if null_names > 0:
            df["UserName"] = df["UserName"].fillna("Unknown")
            logger.info(f"Filled {null_names} missing usernames with 'Unknown'.")

    return df


# ──────────────────────────────────────────────
# Feature Engineering
# ──────────────────────────────────────────────
def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new analytical features from existing columns.

    New Columns
    -----------
    - AgeGroup : Categorical age bucket
    - AgeCategory : "Minor" (< 18) or "Adult"
    - EmailDomain : Full domain of the email (e.g., gmail.com)
    - EmailProvider : Simplified provider name (Gmail, Yahoo, etc.)
    - UserNameLength : Length of the username string
    - EnrollmentDate : Synthetic enrollment date
    - EnrollmentMonth : Month extracted from EnrollmentDate
    - EnrollmentYear : Year extracted from EnrollmentDate
    - Country : Synthetic country of the learner
    - Region : Region derived from Country
    """
    logger.info("Engineering features...")

    # Age Group
    if "Age" in df.columns:
        df["AgeGroup"] = pd.cut(
            df["Age"],
            bins=AGE_BINS,
            labels=AGE_LABELS,
            right=True,
            include_lowest=True,
        )
        df["AgeCategory"] = df["Age"].apply(
            lambda x: "Minor" if x < 18 else "Adult"
        )
        logger.info("Created AgeGroup and AgeCategory columns.")

    # Email features
    if "Email" in df.columns:
        df["EmailDomain"] = df["Email"].apply(_extract_domain)
        df["EmailProvider"] = df["EmailDomain"].apply(_classify_provider)
        logger.info("Created EmailDomain and EmailProvider columns.")

    # Username length
    if "UserName" in df.columns:
        df["UserNameLength"] = df["UserName"].astype(str).str.len()
        logger.info("Created UserNameLength column.")

    # Enrollment Date (synthetic — seeded for reproducibility)
    if "EnrollmentDate" not in df.columns:
        rng = np.random.default_rng(seed=42)
        start = pd.Timestamp(ENROLLMENT_START_DATE)
        end = pd.Timestamp(ENROLLMENT_END_DATE)
        total_days = (end - start).days
        random_days = rng.integers(0, total_days, size=len(df))
        # Sort to simulate chronological enrollment
        random_days.sort()
        df["EnrollmentDate"] = pd.to_datetime(
            [start + pd.Timedelta(days=int(d)) for d in random_days]
        )
        df["EnrollmentMonth"] = df["EnrollmentDate"].dt.to_period("M").astype(str)
        df["EnrollmentYear"] = df["EnrollmentDate"].dt.year
        df["EnrollmentQuarter"] = (
            df["EnrollmentDate"].dt.year.astype(str)
            + "-Q"
            + df["EnrollmentDate"].dt.quarter.astype(str)
        )
        logger.info("Created EnrollmentDate, EnrollmentMonth, EnrollmentYear, EnrollmentQuarter columns.")

    # Country & Region (synthetic — seeded for reproducibility)
    if "Country" not in df.columns:
        rng = np.random.default_rng(seed=123)
        countries = list(COUNTRIES_DISTRIBUTION.keys())
        weights = list(COUNTRIES_DISTRIBUTION.values())
        # Normalize weights to sum to 1.0
        total_w = sum(weights)
        weights = [w / total_w for w in weights]
        df["Country"] = rng.choice(countries, size=len(df), p=weights)
        df["Region"] = df["Country"].map(COUNTRY_REGION_MAP).fillna("Other")
        logger.info("Created Country and Region columns.")

    return df


def _extract_domain(email: Optional[str]) -> str:
    """Extract the domain from an email address."""
    if pd.isna(email) or "@" not in str(email):
        return "unknown"
    return str(email).split("@")[-1].strip().lower()


def _classify_provider(domain: str) -> str:
    """Classify an email domain into a provider category."""
    provider_map = {
        "gmail.com": "Gmail",
        "yahoo.com": "Yahoo",
        "hotmail.com": "Hotmail",
        "outlook.com": "Outlook",
        "aol.com": "AOL",
        "icloud.com": "iCloud",
        "protonmail.com": "ProtonMail",
        "mail.com": "Mail.com",
        "zoho.com": "Zoho",
        "yandex.com": "Yandex",
    }
    return provider_map.get(domain, "Other")


# ──────────────────────────────────────────────
# Save Cleaned Data
# ──────────────────────────────────────────────
def _save_cleaned_data(df: pd.DataFrame) -> None:
    """Save the cleaned DataFrame to the outputs directory."""
    try:
        CLEANED_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.to_excel(str(CLEANED_DATA_FILE), index=False, engine="openpyxl")
        logger.success(f"Cleaned data saved to: {CLEANED_DATA_FILE}")
    except Exception as exc:
        logger.error(f"Failed to save cleaned data: {exc}")
