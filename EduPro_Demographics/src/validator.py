"""
EduPro Demographics — Data Validator Module
=============================================
Performs comprehensive data quality checks on the users dataset.
Returns a structured validation report identifying all issues.
"""

import re
from dataclasses import dataclass, field
from typing import Any

import pandas as pd
from loguru import logger

from src.config import VALID_GENDERS


# ──────────────────────────────────────────────
# Validation Result Model
# ──────────────────────────────────────────────
@dataclass
class ValidationIssue:
    """Represents a single data quality issue."""
    check_name: str
    severity: str  # "ERROR", "WARNING", "INFO"
    count: int
    message: str
    details: Any = None


@dataclass
class ValidationReport:
    """Complete validation report for the dataset."""
    total_records: int = 0
    total_issues: int = 0
    is_valid: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)
    summary_stats: dict = field(default_factory=dict)

    def add_issue(self, issue: ValidationIssue) -> None:
        """Add an issue and update counters."""
        self.issues.append(issue)
        self.total_issues += issue.count
        if issue.severity == "ERROR" and issue.count > 0:
            self.is_valid = False

    def get_issues_by_severity(self, severity: str) -> list[ValidationIssue]:
        """Filter issues by severity level."""
        return [i for i in self.issues if i.severity == severity and i.count > 0]


# ──────────────────────────────────────────────
# Email Validation Regex
# ──────────────────────────────────────────────
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


# ──────────────────────────────────────────────
# Validation Functions
# ──────────────────────────────────────────────
def validate_dataset(df: pd.DataFrame) -> ValidationReport:
    """
    Run all validation checks on the users DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Raw user data to validate.

    Returns
    -------
    ValidationReport
        Comprehensive report of all data quality issues found.
    """
    logger.info("Starting dataset validation...")
    report = ValidationReport(total_records=len(df))

    # Run all checks
    _check_missing_values(df, report)
    _check_duplicate_rows(df, report)
    _check_duplicate_user_ids(df, report)
    _check_duplicate_emails(df, report)
    _check_invalid_emails(df, report)
    _check_missing_usernames(df, report)
    _check_age_range(df, report)
    _check_invalid_genders(df, report)
    _check_data_types(df, report)
    _compute_summary_stats(df, report)

    # Log summary
    errors = len(report.get_issues_by_severity("ERROR"))
    warnings = len(report.get_issues_by_severity("WARNING"))
    infos = len(report.get_issues_by_severity("INFO"))
    logger.info(
        f"Validation complete: {errors} errors, {warnings} warnings, "
        f"{infos} info items. Dataset valid: {report.is_valid}"
    )

    return report


def _check_missing_values(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for missing values in each column."""
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()

    null_details = {
        col: {"count": int(count), "percentage": round(count / len(df) * 100, 2)}
        for col, count in null_counts.items() if count > 0
    }

    report.add_issue(ValidationIssue(
        check_name="Missing Values",
        severity="WARNING" if total_nulls > 0 else "INFO",
        count=int(total_nulls),
        message=f"{total_nulls} missing values found across {len(null_details)} columns."
        if total_nulls > 0 else "No missing values found.",
        details=null_details,
    ))
    logger.debug(f"Missing values: {total_nulls}")


def _check_duplicate_rows(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for fully duplicate rows."""
    dup_count = int(df.duplicated().sum())
    report.add_issue(ValidationIssue(
        check_name="Duplicate Rows",
        severity="WARNING" if dup_count > 0 else "INFO",
        count=dup_count,
        message=f"{dup_count} duplicate rows detected."
        if dup_count > 0 else "No duplicate rows.",
    ))
    logger.debug(f"Duplicate rows: {dup_count}")


def _check_duplicate_user_ids(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for duplicate UserID values."""
    if "UserID" not in df.columns:
        return
    dup_count = int(df["UserID"].dropna().duplicated().sum())
    report.add_issue(ValidationIssue(
        check_name="Duplicate UserIDs",
        severity="ERROR" if dup_count > 0 else "INFO",
        count=dup_count,
        message=f"{dup_count} duplicate UserIDs found."
        if dup_count > 0 else "All UserIDs are unique.",
    ))
    logger.debug(f"Duplicate UserIDs: {dup_count}")


def _check_duplicate_emails(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for duplicate Email addresses."""
    if "Email" not in df.columns:
        return
    dup_count = int(df["Email"].dropna().duplicated().sum())
    report.add_issue(ValidationIssue(
        check_name="Duplicate Emails",
        severity="WARNING" if dup_count > 0 else "INFO",
        count=dup_count,
        message=f"{dup_count} duplicate email addresses found."
        if dup_count > 0 else "All email addresses are unique.",
    ))
    logger.debug(f"Duplicate emails: {dup_count}")


def _check_invalid_emails(df: pd.DataFrame, report: ValidationReport) -> None:
    """Validate email format using regex."""
    if "Email" not in df.columns:
        return
    emails = df["Email"].dropna().astype(str)
    invalid_mask = ~emails.apply(lambda e: bool(EMAIL_REGEX.match(e.strip())))
    invalid_count = int(invalid_mask.sum())
    report.add_issue(ValidationIssue(
        check_name="Invalid Emails",
        severity="WARNING" if invalid_count > 0 else "INFO",
        count=invalid_count,
        message=f"{invalid_count} invalid email addresses detected."
        if invalid_count > 0 else "All email addresses are valid.",
    ))
    logger.debug(f"Invalid emails: {invalid_count}")


def _check_missing_usernames(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for missing or empty UserName values."""
    if "UserName" not in df.columns:
        return
    empty_count = int(
        df["UserName"].isnull().sum()
        + (df["UserName"].astype(str).str.strip() == "").sum()
    )
    report.add_issue(ValidationIssue(
        check_name="Missing Usernames",
        severity="WARNING" if empty_count > 0 else "INFO",
        count=empty_count,
        message=f"{empty_count} records with missing or empty usernames."
        if empty_count > 0 else "All records have usernames.",
    ))
    logger.debug(f"Missing usernames: {empty_count}")


def _check_age_range(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for ages below 0 or above 120."""
    if "Age" not in df.columns:
        return
    ages = pd.to_numeric(df["Age"], errors="coerce")
    below_zero = int((ages < 0).sum())
    above_120 = int((ages > 120).sum())
    null_ages = int(ages.isnull().sum())
    total_invalid = below_zero + above_120

    report.add_issue(ValidationIssue(
        check_name="Invalid Ages",
        severity="ERROR" if total_invalid > 0 else "INFO",
        count=total_invalid,
        message=(
            f"{total_invalid} invalid ages: {below_zero} below 0, "
            f"{above_120} above 120, {null_ages} non-numeric."
        ) if total_invalid > 0 else f"All ages valid. Range: {int(ages.min())}–{int(ages.max())}.",
        details={"below_zero": below_zero, "above_120": above_120, "non_numeric": null_ages},
    ))
    logger.debug(f"Invalid ages: {total_invalid}")


def _check_invalid_genders(df: pd.DataFrame, report: ValidationReport) -> None:
    """Check for gender values not in the valid set."""
    if "Gender" not in df.columns:
        return
    genders = df["Gender"].dropna().astype(str).str.strip().str.title()
    invalid_mask = ~genders.isin(VALID_GENDERS)
    invalid_count = int(invalid_mask.sum())
    invalid_values = genders[invalid_mask].unique().tolist() if invalid_count > 0 else []

    report.add_issue(ValidationIssue(
        check_name="Invalid Genders",
        severity="WARNING" if invalid_count > 0 else "INFO",
        count=invalid_count,
        message=f"{invalid_count} records with invalid gender values: {invalid_values}"
        if invalid_count > 0 else f"All genders valid. Values: {genders.unique().tolist()}.",
        details={"invalid_values": invalid_values},
    ))
    logger.debug(f"Invalid genders: {invalid_count}")


def _check_data_types(df: pd.DataFrame, report: ValidationReport) -> None:
    """Report on current data types for each column."""
    dtype_info = {col: str(dtype) for col, dtype in df.dtypes.items()}
    report.add_issue(ValidationIssue(
        check_name="Data Types",
        severity="INFO",
        count=0,
        message=f"Column types: {dtype_info}",
        details=dtype_info,
    ))


def _compute_summary_stats(df: pd.DataFrame, report: ValidationReport) -> None:
    """Compute and attach summary statistics to the report."""
    report.summary_stats = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "null_percentage": round(df.isnull().mean().mean() * 100, 2),
        "unique_counts": df.nunique().to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 3),
    }
