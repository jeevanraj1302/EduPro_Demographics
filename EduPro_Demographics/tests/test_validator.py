"""
EduPro Demographics — Unit Tests for Validator
================================================
"""

import sys
from pathlib import Path

import pytest
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.validator import validate_dataset, ValidationReport


def _make_valid_df() -> pd.DataFrame:
    """Create a minimal valid test DataFrame."""
    return pd.DataFrame({
        "UserID": ["U001", "U002", "U003"],
        "UserName": ["alice", "bob", "carol"],
        "Age": [25, 30, 22],
        "Gender": ["Female", "Male", "Female"],
        "Email": ["alice@gmail.com", "bob@yahoo.com", "carol@outlook.com"],
    })


class TestValidateDataset:
    """Tests for the validate_dataset function."""

    def test_returns_validation_report(self):
        """Test that the function returns a ValidationReport."""
        df = _make_valid_df()
        report = validate_dataset(df)
        assert isinstance(report, ValidationReport)

    def test_valid_data_passes(self):
        """Test that valid data passes validation."""
        df = _make_valid_df()
        report = validate_dataset(df)
        assert report.is_valid is True

    def test_duplicate_user_ids_detected(self):
        """Test that duplicate UserIDs are detected."""
        df = _make_valid_df()
        df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
        report = validate_dataset(df)
        dup_issues = [i for i in report.issues if i.check_name == "Duplicate UserIDs"]
        assert len(dup_issues) == 1
        assert dup_issues[0].count > 0

    def test_invalid_age_detected(self):
        """Test that ages below 0 are detected."""
        df = _make_valid_df()
        df.loc[0, "Age"] = -5
        report = validate_dataset(df)
        age_issues = [i for i in report.issues if i.check_name == "Invalid Ages"]
        assert len(age_issues) == 1
        assert age_issues[0].count > 0

    def test_invalid_email_detected(self):
        """Test that invalid email formats are detected."""
        df = _make_valid_df()
        df.loc[0, "Email"] = "not-an-email"
        report = validate_dataset(df)
        email_issues = [i for i in report.issues if i.check_name == "Invalid Emails"]
        assert len(email_issues) == 1
        assert email_issues[0].count > 0

    def test_missing_values_detected(self):
        """Test that missing values are detected."""
        df = _make_valid_df()
        df.loc[0, "UserName"] = None
        report = validate_dataset(df)
        missing_issues = [i for i in report.issues if i.check_name == "Missing Values"]
        assert len(missing_issues) == 1
        assert missing_issues[0].count > 0

    def test_invalid_gender_detected(self):
        """Test that invalid gender values are detected."""
        df = _make_valid_df()
        df.loc[0, "Gender"] = "InvalidGender"
        report = validate_dataset(df)
        gender_issues = [i for i in report.issues if i.check_name == "Invalid Genders"]
        assert len(gender_issues) == 1
        assert gender_issues[0].count > 0

    def test_summary_stats_computed(self):
        """Test that summary statistics are computed."""
        df = _make_valid_df()
        report = validate_dataset(df)
        assert "total_records" in report.summary_stats
        assert report.summary_stats["total_records"] == 3
