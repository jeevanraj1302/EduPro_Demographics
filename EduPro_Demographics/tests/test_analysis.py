"""
EduPro Demographics — Unit Tests for Analysis
================================================
"""

import sys
from pathlib import Path

import pytest
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis import (
    compute_kpis, get_age_distribution, get_gender_distribution,
    get_age_group_distribution, get_email_provider_distribution,
    get_top_oldest_learners, get_top_youngest_learners,
    get_most_common_age, get_descriptive_stats,
)


def _make_test_df() -> pd.DataFrame:
    """Create a test DataFrame with engineered features."""
    return pd.DataFrame({
        "UserID": ["U001", "U002", "U003", "U004", "U005"],
        "UserName": ["alice", "bob", "carol", "dave", "eve"],
        "Age": [15, 25, 30, 20, 18],
        "Gender": ["Female", "Male", "Female", "Male", "Female"],
        "Email": ["a@gmail.com", "b@yahoo.com", "c@gmail.com", "d@outlook.com", "e@gmail.com"],
        "AgeGroup": ["0–17", "18–25", "26–35", "18–25", "18–25"],
        "AgeCategory": ["Minor", "Adult", "Adult", "Adult", "Adult"],
        "EmailDomain": ["gmail.com", "yahoo.com", "gmail.com", "outlook.com", "gmail.com"],
        "EmailProvider": ["Gmail", "Yahoo", "Gmail", "Outlook", "Gmail"],
        "UserNameLength": [5, 3, 5, 4, 3],
    })


class TestComputeKPIs:
    """Tests for compute_kpis function."""

    def test_returns_dict(self):
        """Test that KPIs return a dictionary."""
        df = _make_test_df()
        kpis = compute_kpis(df)
        assert isinstance(kpis, dict)

    def test_total_learners(self):
        """Test total learner count."""
        df = _make_test_df()
        kpis = compute_kpis(df)
        assert kpis["total_learners"] == 5

    def test_gender_counts(self):
        """Test gender count accuracy."""
        df = _make_test_df()
        kpis = compute_kpis(df)
        assert kpis["male_count"] == 2
        assert kpis["female_count"] == 3

    def test_age_stats(self):
        """Test age statistics."""
        df = _make_test_df()
        kpis = compute_kpis(df)
        assert kpis["min_age"] == 15
        assert kpis["max_age"] == 30
        assert kpis["average_age"] > 0

    def test_minor_adult_counts(self):
        """Test minor and adult counts."""
        df = _make_test_df()
        kpis = compute_kpis(df)
        assert kpis["minor_count"] == 1
        assert kpis["adult_count"] == 4


class TestDistributions:
    """Tests for distribution analysis functions."""

    def test_age_distribution(self):
        """Test age distribution returns correct format."""
        df = _make_test_df()
        result = get_age_distribution(df)
        assert isinstance(result, pd.DataFrame)
        assert "Age" in result.columns
        assert "Count" in result.columns

    def test_gender_distribution(self):
        """Test gender distribution."""
        df = _make_test_df()
        result = get_gender_distribution(df)
        assert isinstance(result, pd.DataFrame)
        assert "Gender" in result.columns
        assert result["Count"].sum() == 5

    def test_age_group_distribution(self):
        """Test age group distribution."""
        df = _make_test_df()
        result = get_age_group_distribution(df)
        assert isinstance(result, pd.DataFrame)
        assert "AgeGroup" in result.columns

    def test_email_provider_distribution(self):
        """Test email provider distribution."""
        df = _make_test_df()
        result = get_email_provider_distribution(df)
        assert isinstance(result, pd.DataFrame)
        assert "EmailProvider" in result.columns


class TestRankings:
    """Tests for ranking functions."""

    def test_top_oldest(self):
        """Test top oldest learners."""
        df = _make_test_df()
        result = get_top_oldest_learners(df, n=3)
        assert len(result) == 3
        assert result.iloc[0]["Age"] == 30  # Oldest first

    def test_top_youngest(self):
        """Test top youngest learners."""
        df = _make_test_df()
        result = get_top_youngest_learners(df, n=3)
        assert len(result) == 3
        assert result.iloc[0]["Age"] == 15  # Youngest first

    def test_most_common_age(self):
        """Test most common age."""
        df = _make_test_df()
        result = get_most_common_age(df)
        assert isinstance(result, int)


class TestDescriptiveStats:
    """Tests for descriptive statistics."""

    def test_returns_dataframe(self):
        """Test that descriptive stats returns a DataFrame."""
        df = _make_test_df()
        result = get_descriptive_stats(df)
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
