"""
EduPro Demographics — Unit Tests for Preprocessing
====================================================
"""

import sys
from pathlib import Path

import pytest
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing import preprocess_data, engineer_features


def _make_raw_df() -> pd.DataFrame:
    """Create a raw test DataFrame simulating real data."""
    return pd.DataFrame({
        "UserID": ["U001", "U002", "U003", "U001"],  # Duplicate U001
        "UserName": ["  alice  ", "bob", "carol", "alice"],
        "Age": [25.0, 30.0, 17.0, 25.0],
        "Gender": ["female", "MALE", "Female", "female"],
        "Email": ["ALICE@Gmail.com", "bob@yahoo.com", "carol@outlook.com", "alice@gmail.com"],
    })


class TestPreprocessData:
    """Tests for the preprocess_data function."""

    def test_returns_dataframe(self):
        """Test that preprocessing returns a DataFrame."""
        df = _make_raw_df()
        result = preprocess_data(df, save=False)
        assert isinstance(result, pd.DataFrame)

    def test_duplicates_removed(self):
        """Test that duplicate records are removed."""
        df = _make_raw_df()
        result = preprocess_data(df, save=False)
        assert len(result) < len(df)
        assert result["UserID"].duplicated().sum() == 0

    def test_whitespace_trimmed(self):
        """Test that whitespace is trimmed from strings."""
        df = _make_raw_df()
        result = preprocess_data(df, save=False)
        for val in result["UserName"].dropna():
            assert val == val.strip()

    def test_gender_normalized(self):
        """Test that gender values are normalized."""
        df = _make_raw_df()
        result = preprocess_data(df, save=False)
        valid_genders = {"Male", "Female", "Other"}
        for gender in result["Gender"].dropna():
            assert gender in valid_genders, f"Unexpected gender: {gender}"

    def test_emails_lowercased(self):
        """Test that emails are lowercased."""
        df = _make_raw_df()
        result = preprocess_data(df, save=False)
        for email in result["Email"].dropna():
            assert email == email.lower()

    def test_feature_engineering_columns(self):
        """Test that engineered feature columns are created."""
        df = _make_raw_df()
        result = preprocess_data(df, save=False)
        expected_features = ["AgeGroup", "AgeCategory", "EmailDomain", "EmailProvider", "UserNameLength"]
        for col in expected_features:
            assert col in result.columns, f"Missing feature column: {col}"


class TestEngineerFeatures:
    """Tests for the engineer_features function."""

    def test_age_groups_created(self):
        """Test that AgeGroup column is created correctly."""
        df = pd.DataFrame({"Age": [15, 20, 30, 45, 55, 65]})
        result = engineer_features(df)
        assert "AgeGroup" in result.columns
        assert len(result["AgeGroup"].dropna()) == len(df)

    def test_age_category_created(self):
        """Test that AgeCategory column is created correctly."""
        df = pd.DataFrame({"Age": [15, 20]})
        result = engineer_features(df)
        assert "AgeCategory" in result.columns
        assert result.loc[0, "AgeCategory"] == "Minor"
        assert result.loc[1, "AgeCategory"] == "Adult"

    def test_email_domain_extracted(self):
        """Test that EmailDomain is correctly extracted."""
        df = pd.DataFrame({"Email": ["user@gmail.com", "test@yahoo.com"]})
        result = engineer_features(df)
        assert "EmailDomain" in result.columns
        assert result.loc[0, "EmailDomain"] == "gmail.com"
        assert result.loc[1, "EmailDomain"] == "yahoo.com"

    def test_email_provider_classified(self):
        """Test that EmailProvider is correctly classified."""
        df = pd.DataFrame({"Email": ["user@gmail.com", "test@yahoo.com", "x@custom.io"]})
        result = engineer_features(df)
        assert "EmailProvider" in result.columns
        assert result.loc[0, "EmailProvider"] == "Gmail"
        assert result.loc[1, "EmailProvider"] == "Yahoo"
        assert result.loc[2, "EmailProvider"] == "Other"

    def test_username_length(self):
        """Test that UserNameLength is correctly computed."""
        df = pd.DataFrame({"UserName": ["alice", "bob"]})
        result = engineer_features(df)
        assert "UserNameLength" in result.columns
        assert result.loc[0, "UserNameLength"] == 5
        assert result.loc[1, "UserNameLength"] == 3
