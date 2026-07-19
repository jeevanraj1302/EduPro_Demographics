"""
EduPro Demographics — A/B Testing Analysis Module
===================================================
Statistical comparison of learner cohorts for A/B testing.
Uses scipy.stats for hypothesis testing and effect size calculations.
"""

from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from loguru import logger


# ══════════════════════════════════════════════
# Cohort Splitting
# ══════════════════════════════════════════════
def split_cohorts(
    df: pd.DataFrame,
    split_column: str,
    group_a_values: list,
    group_b_values: list,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into two cohorts based on column values.

    Parameters
    ----------
    df : pd.DataFrame
        Source data.
    split_column : str
        Column to split on.
    group_a_values : list
        Values for Group A.
    group_b_values : list
        Values for Group B.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (group_a_df, group_b_df)
    """
    group_a = df[df[split_column].isin(group_a_values)]
    group_b = df[df[split_column].isin(group_b_values)]
    logger.info(
        f"Split cohorts on '{split_column}': "
        f"Group A = {len(group_a):,}, Group B = {len(group_b):,}"
    )
    return group_a, group_b


def split_by_time(
    df: pd.DataFrame,
    date_column: str = "EnrollmentDate",
    split_date: str = "2025-01-01",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data into before/after cohorts based on a date."""
    split_ts = pd.Timestamp(split_date)
    before = df[df[date_column] < split_ts]
    after = df[df[date_column] >= split_ts]
    logger.info(
        f"Time split at {split_date}: Before = {len(before):,}, After = {len(after):,}"
    )
    return before, after


# ══════════════════════════════════════════════
# Statistical Tests
# ══════════════════════════════════════════════
def compare_means(
    group_a: pd.Series,
    group_b: pd.Series,
    metric_name: str = "metric",
) -> dict[str, Any]:
    """
    Perform independent t-test to compare means of two groups.

    Returns
    -------
    dict
        Statistical comparison results.
    """
    a_clean = group_a.dropna()
    b_clean = group_b.dropna()

    t_stat, p_value = stats.ttest_ind(a_clean, b_clean, equal_var=False)

    # Cohen's d effect size
    pooled_std = np.sqrt(
        (a_clean.std() ** 2 + b_clean.std() ** 2) / 2
    )
    cohens_d = (a_clean.mean() - b_clean.mean()) / pooled_std if pooled_std > 0 else 0

    # Effect size interpretation
    if abs(cohens_d) < 0.2:
        effect_label = "Negligible"
    elif abs(cohens_d) < 0.5:
        effect_label = "Small"
    elif abs(cohens_d) < 0.8:
        effect_label = "Medium"
    else:
        effect_label = "Large"

    result = {
        "metric": metric_name,
        "group_a_mean": round(a_clean.mean(), 2),
        "group_b_mean": round(b_clean.mean(), 2),
        "group_a_std": round(a_clean.std(), 2),
        "group_b_std": round(b_clean.std(), 2),
        "group_a_n": len(a_clean),
        "group_b_n": len(b_clean),
        "difference": round(a_clean.mean() - b_clean.mean(), 2),
        "pct_change": round(
            ((b_clean.mean() - a_clean.mean()) / a_clean.mean() * 100), 2
        ) if a_clean.mean() != 0 else 0,
        "t_statistic": round(t_stat, 4),
        "p_value": round(p_value, 6),
        "significant": p_value < 0.05,
        "cohens_d": round(cohens_d, 4),
        "effect_size": effect_label,
    }

    logger.info(
        f"T-test on '{metric_name}': t={t_stat:.4f}, p={p_value:.6f}, "
        f"d={cohens_d:.4f} ({effect_label})"
    )
    return result


def compare_proportions(
    group_a: pd.Series,
    group_b: pd.Series,
    category_column: str = "category",
) -> dict[str, Any]:
    """
    Perform chi-squared test to compare categorical distributions.

    Returns
    -------
    dict
        Statistical comparison results.
    """
    # Create contingency table
    all_categories = sorted(
        set(group_a.dropna().unique()) | set(group_b.dropna().unique())
    )
    a_counts = group_a.value_counts().reindex(all_categories, fill_value=0)
    b_counts = group_b.value_counts().reindex(all_categories, fill_value=0)

    contingency = pd.DataFrame({
        "Group A": a_counts,
        "Group B": b_counts,
    })

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency.T)

    # Cramer's V
    n = contingency.values.sum()
    min_dim = min(contingency.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0

    result = {
        "category": category_column,
        "chi2_statistic": round(chi2, 4),
        "p_value": round(p_value, 6),
        "degrees_of_freedom": dof,
        "significant": p_value < 0.05,
        "cramers_v": round(cramers_v, 4),
        "contingency_table": contingency.to_dict(),
        "group_a_distribution": (a_counts / a_counts.sum() * 100).round(1).to_dict(),
        "group_b_distribution": (b_counts / b_counts.sum() * 100).round(1).to_dict(),
    }

    logger.info(
        f"Chi-squared on '{category_column}': χ²={chi2:.4f}, p={p_value:.6f}, V={cramers_v:.4f}"
    )
    return result


# ══════════════════════════════════════════════
# Cohort Summary
# ══════════════════════════════════════════════
def cohort_summary(group_a: pd.DataFrame, group_b: pd.DataFrame) -> pd.DataFrame:
    """
    Generate a comparative summary of two cohorts.

    Returns
    -------
    pd.DataFrame
        Summary statistics for both cohorts.
    """
    metrics = []

    metrics.append({
        "Metric": "Total Learners",
        "Group A": f"{len(group_a):,}",
        "Group B": f"{len(group_b):,}",
        "Difference": f"{len(group_b) - len(group_a):+,}",
    })

    if "Age" in group_a.columns:
        metrics.append({
            "Metric": "Average Age",
            "Group A": f"{group_a['Age'].mean():.1f}",
            "Group B": f"{group_b['Age'].mean():.1f}",
            "Difference": f"{group_b['Age'].mean() - group_a['Age'].mean():+.1f}",
        })
        metrics.append({
            "Metric": "Median Age",
            "Group A": f"{group_a['Age'].median():.0f}",
            "Group B": f"{group_b['Age'].median():.0f}",
            "Difference": f"{group_b['Age'].median() - group_a['Age'].median():+.0f}",
        })

    if "Gender" in group_a.columns:
        a_male_pct = round((group_a["Gender"] == "Male").mean() * 100, 1)
        b_male_pct = round((group_b["Gender"] == "Male").mean() * 100, 1)
        metrics.append({
            "Metric": "Male %",
            "Group A": f"{a_male_pct}%",
            "Group B": f"{b_male_pct}%",
            "Difference": f"{b_male_pct - a_male_pct:+.1f}%",
        })

    if "AgeCategory" in group_a.columns:
        a_minor = round((group_a["AgeCategory"] == "Minor").mean() * 100, 1)
        b_minor = round((group_b["AgeCategory"] == "Minor").mean() * 100, 1)
        metrics.append({
            "Metric": "Minor %",
            "Group A": f"{a_minor}%",
            "Group B": f"{b_minor}%",
            "Difference": f"{b_minor - a_minor:+.1f}%",
        })

    return pd.DataFrame(metrics)
