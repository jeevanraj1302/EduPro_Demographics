"""
EduPro Demographics — Real-Time Streaming Module
==================================================
Simulates real-time data streaming by generating new learner records.
When connected to a real database, polls for new records instead.
"""

import random
import string
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from loguru import logger

# ── Ensure project root is on sys.path ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import (
    STREAM_BATCH_SIZE, COUNTRIES_DISTRIBUTION, COUNTRY_REGION_MAP,
    AGE_BINS, AGE_LABELS,
)



# ══════════════════════════════════════════════
# Simulated Data Generator
# ══════════════════════════════════════════════
_FIRST_NAMES_MALE = [
    "james", "john", "robert", "michael", "david", "william", "richard",
    "joseph", "thomas", "charles", "daniel", "matthew", "anthony", "mark",
    "donald", "steven", "paul", "andrew", "joshua", "kevin", "brian",
    "rahul", "amit", "vikram", "arjun", "pradeep", "rajesh", "sanjay",
]

_FIRST_NAMES_FEMALE = [
    "mary", "patricia", "jennifer", "linda", "elizabeth", "barbara",
    "susan", "jessica", "sarah", "karen", "nancy", "lisa", "betty",
    "emily", "ashley", "amanda", "michelle", "kimberly", "laura", "megan",
    "priya", "anita", "deepa", "sunita", "kavita", "neha", "pooja",
]

_DOMAINS = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "protonmail.com"]


def generate_random_learner(base_id: int) -> dict:
    """
    Generate a single random learner record.

    Parameters
    ----------
    base_id : int
        Base number for generating the UserID.

    Returns
    -------
    dict
        A learner record dictionary.
    """
    gender = random.choice(["Male", "Female"])
    if gender == "Male":
        name = random.choice(_FIRST_NAMES_MALE) + random.choice(string.digits * 3)
    else:
        name = random.choice(_FIRST_NAMES_FEMALE) + random.choice(string.digits * 3)

    age = random.randint(14, 65)
    domain = random.choice(_DOMAINS)
    email = f"{name}@{domain}"

    countries = list(COUNTRIES_DISTRIBUTION.keys())
    weights = list(COUNTRIES_DISTRIBUTION.values())
    total_w = sum(weights)
    weights = [w / total_w for w in weights]
    country = np.random.choice(countries, p=weights)
    region = COUNTRY_REGION_MAP.get(country, "Other")

    # Determine age group
    age_group = "60+"
    for i, (low, high) in enumerate(zip(AGE_BINS[:-1], AGE_BINS[1:])):
        if low <= age <= high:
            age_group = AGE_LABELS[i]
            break

    provider_map = {
        "gmail.com": "Gmail", "yahoo.com": "Yahoo",
        "hotmail.com": "Hotmail", "outlook.com": "Outlook",
        "protonmail.com": "ProtonMail",
    }

    return {
        "UserID": f"U{base_id:05d}",
        "UserName": name,
        "Age": age,
        "Gender": gender,
        "Email": email,
        "AgeGroup": age_group,
        "AgeCategory": "Minor" if age < 18 else "Adult",
        "EmailDomain": domain,
        "EmailProvider": provider_map.get(domain, "Other"),
        "UserNameLength": len(name),
        "EnrollmentDate": datetime.now(),
        "EnrollmentMonth": datetime.now().strftime("%Y-%m"),
        "EnrollmentYear": datetime.now().year,
        "EnrollmentQuarter": f"{datetime.now().year}-Q{(datetime.now().month - 1) // 3 + 1}",
        "Country": country,
        "Region": region,
    }


def generate_batch(existing_count: int, batch_size: Optional[int] = None) -> pd.DataFrame:
    """
    Generate a batch of random learner records.

    Parameters
    ----------
    existing_count : int
        Current number of learners (for ID generation).
    batch_size : int, optional
        Number of records to generate. Defaults to config STREAM_BATCH_SIZE.

    Returns
    -------
    pd.DataFrame
        DataFrame with new learner records.
    """
    batch_size = batch_size or STREAM_BATCH_SIZE
    records = []
    for i in range(batch_size):
        record = generate_random_learner(existing_count + i + 1)
        records.append(record)

    df = pd.DataFrame(records)
    logger.info(f"Generated {batch_size} new learner records.")
    return df


def get_stream_stats(df: pd.DataFrame) -> dict:
    """
    Compute live streaming statistics.

    Parameters
    ----------
    df : pd.DataFrame
        Current full dataset.

    Returns
    -------
    dict
        Live metrics.
    """
    now = datetime.now()
    return {
        "total_records": len(df),
        "last_updated": now.strftime("%H:%M:%S"),
        "latest_enrollment": df["EnrollmentDate"].max().strftime("%Y-%m-%d %H:%M")
        if "EnrollmentDate" in df.columns else "N/A",
        "avg_age": round(df["Age"].mean(), 1) if "Age" in df.columns else 0,
        "male_pct": round(
            (df["Gender"] == "Male").sum() / len(df) * 100, 1
        ) if "Gender" in df.columns else 0,
        "female_pct": round(
            (df["Gender"] == "Female").sum() / len(df) * 100, 1
        ) if "Gender" in df.columns else 0,
    }
