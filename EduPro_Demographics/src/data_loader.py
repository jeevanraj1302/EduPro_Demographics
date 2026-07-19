"""
EduPro Demographics — Data Loader Module
==========================================
Handles loading, caching, and initial inspection of the users dataset.
"""

from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger

from src.config import DATA_FILE, EXPECTED_COLUMNS


def load_users_data(filepath: Optional[Path] = None) -> pd.DataFrame:
    """
    Load user data from the Excel file.

    Parameters
    ----------
    filepath : Path, optional
        Path to the Excel file. Defaults to ``DATA_FILE`` from config.

    Returns
    -------
    pd.DataFrame
        Raw user data as a DataFrame.

    Raises
    ------
    FileNotFoundError
        If the data file does not exist.
    ValueError
        If required columns are missing from the dataset.
    """
    filepath = filepath or DATA_FILE

    if not filepath.exists():
        logger.error(f"Data file not found: {filepath}")
        raise FileNotFoundError(
            f"Data file not found at '{filepath}'. "
            f"Please place 'users.xlsx' in the 'data/' directory."
        )

    logger.info(f"Loading data from: {filepath}")

    try:
        df = pd.read_excel(filepath, engine="openpyxl")
        logger.success(f"Loaded {len(df):,} records with {len(df.columns)} columns.")
    except Exception as exc:
        logger.error(f"Failed to read Excel file: {exc}")
        raise

    # Validate expected columns
    _validate_columns(df)

    return df


def _validate_columns(df: pd.DataFrame) -> None:
    """
    Verify that all expected columns are present in the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The loaded DataFrame to validate.

    Raises
    ------
    ValueError
        If any expected column is missing.
    """
    missing = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing:
        logger.error(f"Missing columns: {missing}")
        raise ValueError(
            f"Dataset is missing required columns: {missing}. "
            f"Expected: {EXPECTED_COLUMNS}. Found: {list(df.columns)}."
        )
    logger.info("All expected columns present.")


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate a quick summary of the loaded dataset.

    Parameters
    ----------
    df : pd.DataFrame
        The user data.

    Returns
    -------
    dict
        Summary statistics including shape, dtypes, nulls, and uniques.
    """
    summary = {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "null_percentages": (df.isnull().mean() * 100).round(2).to_dict(),
        "unique_counts": df.nunique().to_dict(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 3),
    }
    logger.info(
        f"Data summary: {summary['total_rows']:,} rows × "
        f"{summary['total_columns']} cols, "
        f"{summary['memory_usage_mb']} MB"
    )
    return summary
