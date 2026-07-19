"""
EduPro Demographics — Unit Tests for Data Loader
==================================================
"""

import sys
from pathlib import Path

import pytest
import pandas as pd

# Ensure src is importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_users_data, get_data_summary, _validate_columns
from src.config import DATA_FILE, EXPECTED_COLUMNS


class TestLoadUsersData:
    """Tests for the load_users_data function."""

    def test_loads_successfully(self):
        """Test that data loads without error."""
        df = load_users_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_has_expected_columns(self):
        """Test that all expected columns are present."""
        df = load_users_data()
        for col in EXPECTED_COLUMNS:
            assert col in df.columns, f"Missing column: {col}"

    def test_returns_dataframe(self):
        """Test that the return type is a DataFrame."""
        result = load_users_data()
        assert isinstance(result, pd.DataFrame)

    def test_nonexistent_file_raises(self):
        """Test that a missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_users_data(Path("nonexistent/file.xlsx"))

    def test_data_not_empty(self):
        """Test that loaded data is not empty."""
        df = load_users_data()
        assert len(df) > 0
        assert len(df.columns) > 0


class TestGetDataSummary:
    """Tests for the get_data_summary function."""

    def test_returns_dict(self):
        """Test that summary returns a dictionary."""
        df = load_users_data()
        summary = get_data_summary(df)
        assert isinstance(summary, dict)

    def test_summary_keys(self):
        """Test that summary contains expected keys."""
        df = load_users_data()
        summary = get_data_summary(df)
        expected_keys = [
            "total_rows", "total_columns", "columns",
            "dtypes", "null_counts", "null_percentages",
            "unique_counts", "memory_usage_mb",
        ]
        for key in expected_keys:
            assert key in summary, f"Missing summary key: {key}"

    def test_total_rows_matches(self):
        """Test that total_rows matches DataFrame length."""
        df = load_users_data()
        summary = get_data_summary(df)
        assert summary["total_rows"] == len(df)


class TestValidateColumns:
    """Tests for column validation."""

    def test_valid_dataframe_passes(self):
        """Test that a valid DataFrame passes validation."""
        df = pd.DataFrame({
            "UserID": ["U001"],
            "UserName": ["test"],
            "Age": [25],
            "Gender": ["Male"],
            "Email": ["test@example.com"],
        })
        # Should not raise
        _validate_columns(df)

    def test_missing_column_raises(self):
        """Test that a missing column raises ValueError."""
        df = pd.DataFrame({"UserID": ["U001"], "UserName": ["test"]})
        with pytest.raises(ValueError):
            _validate_columns(df)
