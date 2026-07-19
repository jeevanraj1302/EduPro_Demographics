"""
EduPro Demographics — PDF Report Module
=========================================
Generates professional PDF reports with embedded charts and KPI summaries.
Uses fpdf2 for PDF generation and matplotlib for chart rendering.
"""

import io
from datetime import datetime
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from fpdf import FPDF
from loguru import logger

from src.config import COLORS, REPORTS_DIR


class EduProPDF(FPDF):
    """Custom PDF class with EduPro branding."""

    def header(self):
        """Render page header with branding."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(108, 99, 255)
        self.cell(0, 8, "EduPro Demographics Analytics", align="R")
        self.ln(10)
        self.set_draw_color(108, 99, 255)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        """Render page footer with page number."""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(160, 163, 177)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}} | Generated {datetime.now().strftime('%Y-%m-%d')}", align="C")

    def chapter_title(self, title: str):
        """Add a styled chapter title."""
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(108, 99, 255)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(108, 99, 255)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(6)

    def section_title(self, title: str):
        """Add a styled section title."""
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text: str):
        """Add body text."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def kpi_row(self, label: str, value: str):
        """Add a KPI label-value row."""
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(80, 80, 80)
        self.cell(80, 7, f"  {label}:", new_x="END")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(108, 99, 255)
        self.cell(0, 7, str(value), new_x="LMARGIN", new_y="NEXT")


def _create_chart_image(df: pd.DataFrame, chart_type: str) -> bytes:
    """Generate a chart as PNG bytes using matplotlib."""
    fig, ax = plt.subplots(figsize=(7, 3.5))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FAFAFA")

    if chart_type == "age_histogram":
        ax.hist(df["Age"], bins=25, color="#6C63FF", edgecolor="#4A42D4", alpha=0.85)
        ax.set_xlabel("Age (Years)", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)
        ax.set_title("Age Distribution of Learners", fontsize=12, fontweight="bold")

    elif chart_type == "gender_pie":
        counts = df["Gender"].value_counts()
        colors = ["#00D2FF", "#FF6584", "#FFB547"]
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%",
               colors=colors[:len(counts)], startangle=90)
        ax.set_title("Gender Distribution", fontsize=12, fontweight="bold")

    elif chart_type == "age_group_bar":
        if "AgeGroup" in df.columns:
            counts = df["AgeGroup"].value_counts().sort_index()
            bars = ax.bar(counts.index.astype(str), counts.values,
                          color="#6C63FF", edgecolor="#4A42D4")
            ax.set_xlabel("Age Group", fontsize=10)
            ax.set_ylabel("Count", fontsize=10)
            ax.set_title("Learners by Age Group", fontsize=12, fontweight="bold")
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                        str(int(bar.get_height())), ha="center", fontsize=9)

    elif chart_type == "email_bar":
        if "EmailProvider" in df.columns:
            counts = df["EmailProvider"].value_counts().head(8)
            bars = ax.barh(counts.index, counts.values, color="#6C63FF", edgecolor="#4A42D4")
            ax.set_xlabel("Count", fontsize=10)
            ax.set_title("Top Email Providers", fontsize=12, fontweight="bold")
            ax.invert_yaxis()

    elif chart_type == "enrollment_trend":
        if "EnrollmentDate" in df.columns:
            monthly = df.groupby(df["EnrollmentDate"].dt.to_period("M")).size()
            monthly.index = monthly.index.astype(str)
            ax.plot(range(len(monthly)), monthly.values, color="#6C63FF",
                    linewidth=2, marker="o", markersize=4)
            ax.fill_between(range(len(monthly)), monthly.values,
                            alpha=0.15, color="#6C63FF")
            step = max(1, len(monthly) // 8)
            ax.set_xticks(range(0, len(monthly), step))
            ax.set_xticklabels([monthly.index[i] for i in range(0, len(monthly), step)],
                               rotation=45, fontsize=8)
            ax.set_ylabel("New Enrollments", fontsize=10)
            ax.set_title("Monthly Enrollment Trend", fontsize=12, fontweight="bold")

    elif chart_type == "country_bar":
        if "Country" in df.columns:
            counts = df["Country"].value_counts().head(10)
            bars = ax.barh(counts.index, counts.values, color="#6C63FF", edgecolor="#4A42D4")
            ax.set_xlabel("Count", fontsize=10)
            ax.set_title("Top 10 Countries", fontsize=12, fontweight="bold")
            ax.invert_yaxis()

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()


def generate_pdf_report(df: pd.DataFrame, kpis: dict) -> bytes:
    """
    Generate a comprehensive PDF report with KPIs, charts, and insights.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned learner data.
    kpis : dict
        Computed KPI values.

    Returns
    -------
    bytes
        PDF file content as bytes.
    """
    logger.info("Generating PDF report...")
    pdf = EduProPDF()
    pdf.alias_nb_pages()

    # ── Cover Page ──
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 32)
    pdf.set_text_color(108, 99, 255)
    pdf.cell(0, 15, "EduPro Demographics", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(255, 101, 132)
    pdf.cell(0, 12, "Analytics Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Total Learners: {kpis['total_learners']:,}",
             align="C", new_x="LMARGIN", new_y="NEXT")

    # ── Executive Summary ──
    pdf.add_page()
    pdf.chapter_title("1. Executive Summary")
    pdf.body_text(
        f"EduPro currently serves {kpis['total_learners']:,} registered learners. "
        f"The platform's user base spans ages {kpis['min_age']} to {kpis['max_age']}, "
        f"with an average age of {kpis['average_age']} years (median: {kpis['median_age']}). "
        f"The gender distribution shows a {kpis['gender_ratio']} male-to-female ratio."
    )

    # ── KPI Summary ──
    pdf.chapter_title("2. Key Performance Indicators")
    kpi_items = [
        ("Total Learners", f"{kpis['total_learners']:,}"),
        ("Average Age", f"{kpis['average_age']} years"),
        ("Median Age", f"{kpis['median_age']} years"),
        ("Age Range", f"{kpis['min_age']} - {kpis['max_age']} years"),
        ("Male Learners", f"{kpis['male_count']:,}"),
        ("Female Learners", f"{kpis['female_count']:,}"),
        ("Gender Ratio (M:F)", kpis['gender_ratio']),
        ("Minor Learners (< 18)", f"{kpis['minor_count']:,}"),
        ("Adult Learners (>= 18)", f"{kpis['adult_count']:,}"),
        ("Unique Email Providers", str(kpis['unique_email_providers'])),
        ("Most Common Provider", kpis['most_common_provider']),
        ("Avg Username Length", f"{kpis['avg_username_length']} chars"),
    ]
    for label, value in kpi_items:
        pdf.kpi_row(label, value)

    # ── Charts ──
    pdf.add_page()
    pdf.chapter_title("3. Demographic Analysis")

    charts = [
        ("age_histogram", "3.1 Age Distribution"),
        ("gender_pie", "3.2 Gender Distribution"),
        ("age_group_bar", "3.3 Age Group Breakdown"),
        ("email_bar", "3.4 Email Provider Analysis"),
    ]

    if "EnrollmentDate" in df.columns:
        charts.append(("enrollment_trend", "3.5 Enrollment Trend"))
    if "Country" in df.columns:
        charts.append(("country_bar", "3.6 Geographic Distribution"))

    for i, (chart_type, title) in enumerate(charts):
        if i > 0 and i % 2 == 0:
            pdf.add_page()
        pdf.section_title(title)
        try:
            img_bytes = _create_chart_image(df, chart_type)
            pdf.image(io.BytesIO(img_bytes), x=15, w=180)
            pdf.ln(5)
        except Exception as exc:
            logger.warning(f"Could not generate chart '{chart_type}': {exc}")
            pdf.body_text(f"[Chart could not be generated: {exc}]")

    # ── Recommendations ──
    pdf.add_page()
    pdf.chapter_title("4. Strategic Recommendations")

    recommendations = [
        f"Content Strategy: Design learning content tailored to the {kpis['min_age']}-{kpis['max_age']} "
        f"age demographic. Prioritize topics and teaching styles that resonate with learners averaging "
        f"{kpis['average_age']} years old.",
        f"Compliance & Safety: With {kpis['minor_count']:,} minor learners, ensure compliance with "
        "COPPA and GDPR regulations. Implement age verification and parental consent workflows.",
        "Growth Strategy: Expand the user base by targeting underrepresented age groups. "
        "Implement referral programs and partner with educational institutions.",
        f"Communication: Optimize email templates for {kpis['most_common_provider']}, "
        f"the most popular provider among {kpis['unique_email_providers']} providers used.",
    ]

    for i, rec in enumerate(recommendations, 1):
        pdf.body_text(f"{i}. {rec}")

    # ── Output ──
    pdf_bytes = pdf.output()

    # Save to file
    try:
        report_path = REPORTS_DIR / "analytics_report.pdf"
        report_path.write_bytes(pdf_bytes)
        logger.success(f"PDF report saved to: {report_path}")
    except Exception as exc:
        logger.warning(f"Could not save PDF file: {exc}")

    return pdf_bytes
