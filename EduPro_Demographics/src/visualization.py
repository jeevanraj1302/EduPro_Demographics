"""
EduPro Demographics — Visualization Module
============================================
Generates all Plotly charts for the dashboard.
Every chart includes professional titles, axis labels,
hover tooltips, and responsive layout.
"""

from typing import Optional

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from loguru import logger

from src.config import (
    CHART_COLORS, GENDER_COLORS, PLOTLY_LAYOUT, COLORS,
)


def _apply_layout(fig: go.Figure, title: str, height: int = 450) -> go.Figure:
    """Apply the standard professional layout to any Plotly figure."""
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title={"text": title, "x": 0.5, "xanchor": "center"},
        height=height,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=COLORS["border"],
            borderwidth=1,
            font=dict(size=12),
        ),
    )
    return fig


# ══════════════════════════════════════════════
# AGE CHARTS
# ══════════════════════════════════════════════
def plot_age_histogram(df: pd.DataFrame) -> go.Figure:
    """Create an interactive histogram of learner ages."""
    fig = px.histogram(
        df, x="Age", nbins=30,
        color_discrete_sequence=[COLORS["primary"]],
        labels={"Age": "Age (Years)", "count": "Number of Learners"},
    )
    fig.update_traces(
        marker_line_color=COLORS["primary_dark"],
        marker_line_width=1,
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>",
    )
    return _apply_layout(fig, "📊 Age Distribution of Learners")


def plot_age_boxplot(df: pd.DataFrame) -> go.Figure:
    """Create a box plot of age distribution."""
    fig = px.box(
        df, y="Age",
        color_discrete_sequence=[COLORS["primary"]],
        labels={"Age": "Age (Years)"},
    )
    fig.update_traces(
        marker_color=COLORS["accent"],
        line_color=COLORS["primary"],
    )
    return _apply_layout(fig, "📦 Age Distribution — Box Plot", height=400)


def plot_age_violin(df: pd.DataFrame) -> go.Figure:
    """Create a violin plot of age distribution, optionally by gender."""
    if "Gender" in df.columns and df["Gender"].nunique() <= 5:
        fig = px.violin(
            df, y="Age", x="Gender", color="Gender",
            box=True, points="outliers",
            color_discrete_map=GENDER_COLORS,
            labels={"Age": "Age (Years)", "Gender": "Gender"},
        )
    else:
        fig = px.violin(
            df, y="Age",
            color_discrete_sequence=[COLORS["primary"]],
            box=True, points="outliers",
            labels={"Age": "Age (Years)"},
        )
    return _apply_layout(fig, "🎻 Age Distribution — Violin Plot")


def plot_age_group_bar(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart of age group distribution."""
    age_dist = df["AgeGroup"].value_counts().sort_index().reset_index()
    age_dist.columns = ["AgeGroup", "Count"]

    fig = px.bar(
        age_dist, x="AgeGroup", y="Count",
        color="Count",
        color_continuous_scale=["#4A42D4", "#6C63FF", "#8B83FF", "#FF6584"],
        labels={"AgeGroup": "Age Group", "Count": "Number of Learners"},
        text="Count",
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=13,
        hovertemplate="Age Group: %{x}<br>Learners: %{y:,}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_layout(fig, "📊 Learner Distribution by Age Group")


def plot_age_group_pie(df: pd.DataFrame) -> go.Figure:
    """Create a pie chart of age group proportions."""
    age_dist = df["AgeGroup"].value_counts().sort_index().reset_index()
    age_dist.columns = ["AgeGroup", "Count"]

    fig = px.pie(
        age_dist, values="Count", names="AgeGroup",
        color_discrete_sequence=CHART_COLORS,
        hole=0,
        labels={"AgeGroup": "Age Group", "Count": "Learners"},
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="Age Group: %{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    return _apply_layout(fig, "🥧 Age Group Proportions")


def plot_age_group_donut(df: pd.DataFrame) -> go.Figure:
    """Create a donut chart of age group proportions."""
    age_dist = df["AgeGroup"].value_counts().sort_index().reset_index()
    age_dist.columns = ["AgeGroup", "Count"]

    fig = px.pie(
        age_dist, values="Count", names="AgeGroup",
        color_discrete_sequence=CHART_COLORS,
        hole=0.5,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="Age Group: %{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.add_annotation(
        text=f"<b>{len(df):,}</b><br>Learners",
        showarrow=False,
        font=dict(size=18, color=COLORS["text_primary"]),
    )
    return _apply_layout(fig, "🍩 Age Group Distribution — Donut")


def plot_age_line(df: pd.DataFrame) -> go.Figure:
    """Create a line chart of age frequency distribution."""
    age_freq = df["Age"].value_counts().sort_index().reset_index()
    age_freq.columns = ["Age", "Count"]

    fig = px.line(
        age_freq, x="Age", y="Count",
        markers=True,
        color_discrete_sequence=[COLORS["primary"]],
        labels={"Age": "Age (Years)", "Count": "Number of Learners"},
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6, color=COLORS["accent"]),
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>",
    )
    return _apply_layout(fig, "📈 Age Frequency Trend")


def plot_age_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of Age vs UserNameLength colored by Gender."""
    if "UserNameLength" not in df.columns:
        return go.Figure()

    fig = px.scatter(
        df, x="Age", y="UserNameLength", color="Gender",
        color_discrete_map=GENDER_COLORS,
        opacity=0.6,
        labels={
            "Age": "Age (Years)",
            "UserNameLength": "Username Length",
            "Gender": "Gender",
        },
    )
    fig.update_traces(
        marker=dict(size=5, line=dict(width=0.5, color="white")),
        hovertemplate="Age: %{x}<br>Username Length: %{y}<extra></extra>",
    )
    return _apply_layout(fig, "🔬 Age vs Username Length")


def plot_minor_adult_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of Minor vs Adult counts."""
    if "AgeCategory" not in df.columns:
        return go.Figure()

    dist = df["AgeCategory"].value_counts().reset_index()
    dist.columns = ["Category", "Count"]

    fig = px.bar(
        dist, x="Category", y="Count",
        color="Category",
        color_discrete_map={"Minor": COLORS["warning"], "Adult": COLORS["success"]},
        text="Count",
        labels={"Category": "Age Category", "Count": "Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=14,
        hovertemplate="Category: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    fig.update_layout(showlegend=False)
    return _apply_layout(fig, "👥 Minor vs Adult Learners", height=400)


# ══════════════════════════════════════════════
# GENDER CHARTS
# ══════════════════════════════════════════════
def plot_gender_bar(df: pd.DataFrame) -> go.Figure:
    """Create a bar chart of gender distribution."""
    dist = df["Gender"].value_counts().reset_index()
    dist.columns = ["Gender", "Count"]

    fig = px.bar(
        dist, x="Gender", y="Count",
        color="Gender",
        color_discrete_map=GENDER_COLORS,
        text="Count",
        labels={"Gender": "Gender", "Count": "Number of Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=14,
        hovertemplate="Gender: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    fig.update_layout(showlegend=False)
    return _apply_layout(fig, "👤 Gender Distribution")


def plot_gender_pie(df: pd.DataFrame) -> go.Figure:
    """Create a pie chart of gender distribution."""
    dist = df["Gender"].value_counts().reset_index()
    dist.columns = ["Gender", "Count"]

    fig = px.pie(
        dist, values="Count", names="Gender",
        color="Gender",
        color_discrete_map=GENDER_COLORS,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="Gender: %{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    return _apply_layout(fig, "🥧 Gender Proportions")


def plot_gender_donut(df: pd.DataFrame) -> go.Figure:
    """Create a donut chart of gender distribution."""
    dist = df["Gender"].value_counts().reset_index()
    dist.columns = ["Gender", "Count"]

    fig = px.pie(
        dist, values="Count", names="Gender",
        color="Gender",
        color_discrete_map=GENDER_COLORS,
        hole=0.55,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="Gender: %{label}<br>Count: %{value:,}<extra></extra>",
    )
    fig.add_annotation(
        text=f"<b>{len(df):,}</b><br>Total",
        showarrow=False,
        font=dict(size=18, color=COLORS["text_primary"]),
    )
    return _apply_layout(fig, "🍩 Gender Breakdown")


def plot_gender_horizontal_bar(df: pd.DataFrame) -> go.Figure:
    """Create a horizontal bar chart of gender distribution."""
    dist = df["Gender"].value_counts().reset_index()
    dist.columns = ["Gender", "Count"]

    fig = px.bar(
        dist, y="Gender", x="Count", orientation="h",
        color="Gender",
        color_discrete_map=GENDER_COLORS,
        text="Count",
        labels={"Gender": "", "Count": "Number of Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=14,
        hovertemplate="Gender: %{y}<br>Count: %{x:,}<extra></extra>",
    )
    fig.update_layout(showlegend=False)
    return _apply_layout(fig, "📊 Gender Distribution — Horizontal")


def plot_age_by_gender_box(df: pd.DataFrame) -> go.Figure:
    """Box plot of age grouped by gender."""
    fig = px.box(
        df, x="Gender", y="Age",
        color="Gender",
        color_discrete_map=GENDER_COLORS,
        labels={"Gender": "Gender", "Age": "Age (Years)"},
    )
    return _apply_layout(fig, "📦 Age Distribution by Gender")


def plot_age_group_by_gender_grouped(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart: age groups by gender."""
    if "AgeGroup" not in df.columns or "Gender" not in df.columns:
        return go.Figure()

    cross = df.groupby(["AgeGroup", "Gender"]).size().reset_index(name="Count")

    fig = px.bar(
        cross, x="AgeGroup", y="Count", color="Gender",
        barmode="group",
        color_discrete_map=GENDER_COLORS,
        text="Count",
        labels={"AgeGroup": "Age Group", "Count": "Learners", "Gender": "Gender"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=11,
        hovertemplate="Age Group: %{x}<br>Gender: %{data.name}<br>Count: %{y:,}<extra></extra>",
    )
    return _apply_layout(fig, "📊 Age Group × Gender — Grouped")


def plot_age_group_by_gender_stacked(df: pd.DataFrame) -> go.Figure:
    """Stacked bar chart: age groups by gender."""
    if "AgeGroup" not in df.columns or "Gender" not in df.columns:
        return go.Figure()

    cross = df.groupby(["AgeGroup", "Gender"]).size().reset_index(name="Count")

    fig = px.bar(
        cross, x="AgeGroup", y="Count", color="Gender",
        barmode="stack",
        color_discrete_map=GENDER_COLORS,
        labels={"AgeGroup": "Age Group", "Count": "Learners"},
    )
    fig.update_traces(
        hovertemplate="Age Group: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    return _apply_layout(fig, "📊 Age Group × Gender — Stacked")


# ══════════════════════════════════════════════
# EMAIL CHARTS
# ══════════════════════════════════════════════
def plot_email_provider_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of email provider distribution."""
    if "EmailProvider" not in df.columns:
        return go.Figure()

    dist = df["EmailProvider"].value_counts().reset_index()
    dist.columns = ["Provider", "Count"]

    fig = px.bar(
        dist, x="Provider", y="Count",
        color="Count",
        color_continuous_scale=["#4A42D4", "#6C63FF", "#FF6584"],
        text="Count",
        labels={"Provider": "Email Provider", "Count": "Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=12,
        hovertemplate="Provider: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_layout(fig, "📧 Email Provider Distribution")


def plot_email_provider_pie(df: pd.DataFrame) -> go.Figure:
    """Pie chart of email providers."""
    if "EmailProvider" not in df.columns:
        return go.Figure()

    dist = df["EmailProvider"].value_counts().reset_index()
    dist.columns = ["Provider", "Count"]

    fig = px.pie(
        dist, values="Count", names="Provider",
        color_discrete_sequence=CHART_COLORS,
        hole=0,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="Provider: %{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    return _apply_layout(fig, "📧 Email Provider Proportions")


def plot_email_provider_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart of email providers."""
    if "EmailProvider" not in df.columns:
        return go.Figure()

    dist = df["EmailProvider"].value_counts().reset_index()
    dist.columns = ["Provider", "Count"]

    fig = px.pie(
        dist, values="Count", names="Provider",
        color_discrete_sequence=CHART_COLORS,
        hole=0.5,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="Provider: %{label}<br>Count: %{value:,}<extra></extra>",
    )
    return _apply_layout(fig, "🍩 Email Provider Breakdown")


def plot_email_domain_horizontal_bar(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart of top email domains."""
    if "EmailDomain" not in df.columns:
        return go.Figure()

    dist = df["EmailDomain"].value_counts().head(top_n).sort_values().reset_index()
    dist.columns = ["Domain", "Count"]

    fig = px.bar(
        dist, y="Domain", x="Count", orientation="h",
        color="Count",
        color_continuous_scale=["#4A42D4", "#6C63FF", "#FF6584"],
        text="Count",
        labels={"Domain": "Email Domain", "Count": "Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=12,
        hovertemplate="Domain: %{y}<br>Count: %{x:,}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_layout(fig, f"🌐 Top {top_n} Email Domains")


def plot_email_provider_by_gender(df: pd.DataFrame) -> go.Figure:
    """Grouped bar chart: email provider by gender."""
    if "EmailProvider" not in df.columns or "Gender" not in df.columns:
        return go.Figure()

    cross = df.groupby(["EmailProvider", "Gender"]).size().reset_index(name="Count")

    fig = px.bar(
        cross, x="EmailProvider", y="Count", color="Gender",
        barmode="group",
        color_discrete_map=GENDER_COLORS,
        labels={"EmailProvider": "Email Provider", "Count": "Learners"},
    )
    fig.update_traces(
        hovertemplate="Provider: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    return _apply_layout(fig, "📧 Email Provider by Gender")


# ══════════════════════════════════════════════
# USERNAME CHARTS
# ══════════════════════════════════════════════
def plot_username_length_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram of username lengths."""
    if "UserNameLength" not in df.columns:
        return go.Figure()

    fig = px.histogram(
        df, x="UserNameLength", nbins=25,
        color_discrete_sequence=[COLORS["accent"]],
        labels={"UserNameLength": "Username Length (characters)", "count": "Frequency"},
    )
    fig.update_traces(
        marker_line_color=COLORS["primary_dark"],
        marker_line_width=1,
        hovertemplate="Length: %{x}<br>Count: %{y}<extra></extra>",
    )
    return _apply_layout(fig, "📝 Username Length Distribution")


# ══════════════════════════════════════════════
# ADVANCED CHARTS
# ══════════════════════════════════════════════
def plot_sunburst(df: pd.DataFrame) -> go.Figure:
    """Sunburst chart: Gender → AgeGroup → AgeCategory."""
    if not all(c in df.columns for c in ["Gender", "AgeGroup", "AgeCategory"]):
        return go.Figure()

    fig = px.sunburst(
        df,
        path=["Gender", "AgeGroup", "AgeCategory"],
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percentRoot:.1%}<extra></extra>",
    )
    return _apply_layout(fig, "☀️ Demographic Sunburst — Gender → Age Group → Category", height=550)


def plot_treemap(df: pd.DataFrame) -> go.Figure:
    """Treemap chart: Gender → AgeGroup."""
    if not all(c in df.columns for c in ["Gender", "AgeGroup"]):
        return go.Figure()

    fig = px.treemap(
        df,
        path=["Gender", "AgeGroup"],
        color_discrete_sequence=CHART_COLORS,
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share of Parent: %{percentParent:.1%}<extra></extra>",
    )
    return _apply_layout(fig, "🗺️ Demographic Treemap — Gender → Age Group", height=550)


def plot_age_area(df: pd.DataFrame) -> go.Figure:
    """Area chart of age frequency distribution."""
    age_freq = df["Age"].value_counts().sort_index().reset_index()
    age_freq.columns = ["Age", "Count"]

    fig = px.area(
        age_freq, x="Age", y="Count",
        color_discrete_sequence=[COLORS["primary"]],
        labels={"Age": "Age (Years)", "Count": "Number of Learners"},
    )
    fig.update_traces(
        line=dict(width=2, color=COLORS["primary"]),
        fillcolor="rgba(108,99,255,0.2)",
        hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>",
    )
    return _apply_layout(fig, "📈 Age Frequency — Area Chart")


def plot_heatmap_age_gender(df: pd.DataFrame) -> go.Figure:
    """Heatmap of age group × gender counts."""
    if "AgeGroup" not in df.columns or "Gender" not in df.columns:
        return go.Figure()

    ct = pd.crosstab(df["AgeGroup"], df["Gender"])

    fig = go.Figure(data=go.Heatmap(
        z=ct.values,
        x=ct.columns.tolist(),
        y=ct.index.astype(str).tolist(),
        colorscale=[[0, "#1A1D29"], [0.5, "#6C63FF"], [1, "#FF6584"]],
        text=ct.values,
        texttemplate="%{text}",
        textfont={"size": 14},
        hovertemplate="Gender: %{x}<br>Age Group: %{y}<br>Count: %{z:,}<extra></extra>",
    ))
    fig.update_layout(
        xaxis_title="Gender",
        yaxis_title="Age Group",
    )
    return _apply_layout(fig, "🔥 Heatmap — Age Group × Gender", height=400)


# ══════════════════════════════════════════════
# ENROLLMENT / TIME-SERIES CHARTS
# ══════════════════════════════════════════════
def plot_enrollment_timeline(df: pd.DataFrame) -> go.Figure:
    """Line chart of monthly enrollment trends."""
    if "EnrollmentDate" not in df.columns:
        return go.Figure()

    monthly = (
        df.groupby(df["EnrollmentDate"].dt.to_period("M"))
        .size()
        .reset_index(name="Count")
    )
    monthly.columns = ["Month", "Count"]
    monthly["Month"] = monthly["Month"].astype(str)

    fig = px.line(
        monthly, x="Month", y="Count",
        markers=True,
        color_discrete_sequence=[COLORS["primary"]],
        labels={"Month": "Month", "Count": "New Enrollments"},
    )
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6, color=COLORS["accent"]),
        hovertemplate="Month: %{x}<br>Enrollments: %{y:,}<extra></extra>",
    )
    return _apply_layout(fig, "📈 Monthly Enrollment Trend")


def plot_monthly_enrollment_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of monthly enrollment counts."""
    if "EnrollmentDate" not in df.columns:
        return go.Figure()

    monthly = (
        df.groupby(df["EnrollmentDate"].dt.to_period("M"))
        .size()
        .reset_index(name="Count")
    )
    monthly.columns = ["Month", "Count"]
    monthly["Month"] = monthly["Month"].astype(str)

    fig = px.bar(
        monthly, x="Month", y="Count",
        color="Count",
        color_continuous_scale=["#4A42D4", "#6C63FF", "#FF6584"],
        text="Count",
        labels={"Month": "Month", "Count": "New Enrollments"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=10,
        hovertemplate="Month: %{x}<br>Enrollments: %{y:,}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-45)
    return _apply_layout(fig, "📊 Monthly Enrollment Count", height=500)


def plot_cumulative_enrollment(df: pd.DataFrame) -> go.Figure:
    """Area chart of cumulative enrollment growth."""
    if "EnrollmentDate" not in df.columns:
        return go.Figure()

    monthly = (
        df.groupby(df["EnrollmentDate"].dt.to_period("M"))
        .size()
        .cumsum()
        .reset_index(name="Cumulative")
    )
    monthly.columns = ["Month", "Cumulative"]
    monthly["Month"] = monthly["Month"].astype(str)

    fig = px.area(
        monthly, x="Month", y="Cumulative",
        color_discrete_sequence=[COLORS["primary"]],
        labels={"Month": "Month", "Cumulative": "Total Learners"},
    )
    fig.update_traces(
        line=dict(width=2, color=COLORS["primary"]),
        fillcolor="rgba(108,99,255,0.2)",
        hovertemplate="Month: %{x}<br>Total: %{y:,}<extra></extra>",
    )
    return _apply_layout(fig, "📈 Cumulative Enrollment Growth")


def plot_enrollment_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap of enrollments by month × day-of-week."""
    if "EnrollmentDate" not in df.columns:
        return go.Figure()

    from src.analysis import get_enrollment_seasonality
    seasonality = get_enrollment_seasonality(df)
    if seasonality.empty:
        return go.Figure()

    fig = go.Figure(data=go.Heatmap(
        z=seasonality.values,
        x=seasonality.columns.tolist(),
        y=seasonality.index.tolist(),
        colorscale=[[0, "#1A1D29"], [0.5, "#6C63FF"], [1, "#FF6584"]],
        text=seasonality.values,
        texttemplate="%{text}",
        textfont={"size": 11},
        hovertemplate="Day: %{x}<br>Month: %{y}<br>Count: %{z}<extra></extra>",
    ))
    return _apply_layout(fig, "🗓️ Enrollment Heatmap — Month × Day of Week", height=500)


def plot_quarterly_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart of quarterly enrollment counts."""
    if "EnrollmentQuarter" not in df.columns:
        return go.Figure()

    quarterly = df["EnrollmentQuarter"].value_counts().sort_index().reset_index()
    quarterly.columns = ["Quarter", "Count"]

    fig = px.bar(
        quarterly, x="Quarter", y="Count",
        color="Count",
        color_continuous_scale=["#4A42D4", "#6C63FF", "#FF6584"],
        text="Count",
        labels={"Quarter": "Quarter", "Count": "Enrollments"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=12,
        hovertemplate="Quarter: %{x}<br>Enrollments: %{y:,}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_layout(fig, "📊 Quarterly Enrollment", height=400)


# ══════════════════════════════════════════════
# GEOGRAPHIC CHARTS
# ══════════════════════════════════════════════
def plot_world_map(df: pd.DataFrame) -> go.Figure:
    """Choropleth world map of learner distribution."""
    if "Country" not in df.columns:
        return go.Figure()

    from src.geo_analysis import get_choropleth_data
    geo_data = get_choropleth_data(df)
    if geo_data.empty:
        return go.Figure()

    fig = px.choropleth(
        geo_data,
        locations="ISO",
        color="Count",
        hover_name="Country",
        hover_data={"Percentage": True, "Count": True, "ISO": False},
        color_continuous_scale=["#1A1D29", "#4A42D4", "#6C63FF", "#FF6584"],
        labels={"Count": "Learners"},
    )
    fig.update_layout(
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#2D3142",
            landcolor="#1A1D29",
            showocean=True,
            oceancolor="#0E1117",
            projection_type="natural earth",
        ),
    )
    return _apply_layout(fig, "🌍 Global Learner Distribution", height=550)


def plot_top_countries_bar(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Horizontal bar chart of top countries."""
    if "Country" not in df.columns:
        return go.Figure()

    dist = df["Country"].value_counts().head(top_n).sort_values().reset_index()
    dist.columns = ["Country", "Count"]

    fig = px.bar(
        dist, y="Country", x="Count", orientation="h",
        color="Count",
        color_continuous_scale=["#4A42D4", "#6C63FF", "#FF6584"],
        text="Count",
        labels={"Country": "", "Count": "Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=12,
        hovertemplate="Country: %{y}<br>Learners: %{x:,}<extra></extra>",
    )
    fig.update_layout(coloraxis_showscale=False)
    return _apply_layout(fig, f"🏆 Top {top_n} Countries by Learners")


def plot_region_pie(df: pd.DataFrame) -> go.Figure:
    """Pie chart of regional distribution."""
    if "Region" not in df.columns:
        return go.Figure()

    dist = df["Region"].value_counts().reset_index()
    dist.columns = ["Region", "Count"]

    fig = px.pie(
        dist, values="Count", names="Region",
        color_discrete_sequence=CHART_COLORS,
        hole=0.45,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="Region: %{label}<br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.add_annotation(
        text=f"<b>{df['Region'].nunique()}</b><br>Regions",
        showarrow=False,
        font=dict(size=16, color=COLORS["text_primary"]),
    )
    return _apply_layout(fig, "🌐 Learners by Region")


def plot_country_gender_bar(df: pd.DataFrame, top_n: int = 8) -> go.Figure:
    """Grouped bar chart of top countries by gender."""
    if "Country" not in df.columns or "Gender" not in df.columns:
        return go.Figure()

    top_countries = df["Country"].value_counts().head(top_n).index
    filtered = df[df["Country"].isin(top_countries)]
    cross = filtered.groupby(["Country", "Gender"]).size().reset_index(name="Count")

    fig = px.bar(
        cross, x="Country", y="Count", color="Gender",
        barmode="group",
        color_discrete_map=GENDER_COLORS,
        text="Count",
        labels={"Country": "Country", "Count": "Learners"},
    )
    fig.update_traces(
        textposition="outside",
        textfont_size=10,
        hovertemplate="Country: %{x}<br>Count: %{y:,}<extra></extra>",
    )
    return _apply_layout(fig, f"🌍 Top {top_n} Countries by Gender")


# ══════════════════════════════════════════════
# PERIOD COMPARISON CHARTS
# ══════════════════════════════════════════════
def plot_period_comparison_bar(metrics: list[dict], label_a: str, label_b: str) -> go.Figure:
    """Side-by-side comparison bar chart of two periods."""
    if not metrics:
        return go.Figure()

    metric_names = [m["metric"] for m in metrics]
    values_a = [float(str(m["period_a"]).replace(",", "").replace("%", "")) for m in metrics]
    values_b = [float(str(m["period_b"]).replace(",", "").replace("%", "")) for m in metrics]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=label_a,
        x=metric_names, y=values_a,
        marker_color=COLORS["primary"],
        text=[m["period_a"] for m in metrics],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name=label_b,
        x=metric_names, y=values_b,
        marker_color=COLORS["secondary"],
        text=[m["period_b"] for m in metrics],
        textposition="outside",
    ))
    fig.update_layout(barmode="group")
    return _apply_layout(fig, f"📊 Period Comparison: {label_a} vs {label_b}")


def plot_growth_rate_line(growth_data: pd.DataFrame) -> go.Figure:
    """Line chart of monthly growth rates."""
    if growth_data.empty or "Growth_Rate" not in growth_data.columns:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=growth_data["Month"],
        y=growth_data["Growth_Rate"],
        mode="lines+markers",
        name="Growth Rate",
        line=dict(width=3, color=COLORS["primary"]),
        marker=dict(size=7, color=COLORS["accent"]),
        hovertemplate="Month: %{x}<br>Growth: %{y:.1f}%<extra></extra>",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["text_muted"])
    fig.update_layout(yaxis_title="Growth Rate (%)")
    return _apply_layout(fig, "📈 Monthly Enrollment Growth Rate")


def plot_demographic_trends(trends_data: pd.DataFrame) -> go.Figure:
    """Multi-line chart showing demographic trends over time."""
    if trends_data.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trends_data["Month"], y=trends_data["Avg_Age"],
        mode="lines+markers", name="Avg Age",
        line=dict(width=2, color=COLORS["primary"]),
        yaxis="y",
    ))
    fig.add_trace(go.Scatter(
        x=trends_data["Month"], y=trends_data["Male_Pct"],
        mode="lines+markers", name="Male %",
        line=dict(width=2, color="#00D2FF"),
        yaxis="y2",
    ))
    fig.add_trace(go.Scatter(
        x=trends_data["Month"], y=trends_data["Minor_Pct"],
        mode="lines+markers", name="Minor %",
        line=dict(width=2, color="#FFB547"),
        yaxis="y2",
    ))
    fig.update_layout(
        yaxis=dict(title="Average Age", side="left"),
        yaxis2=dict(title="Percentage (%)", side="right", overlaying="y"),
    )
    return _apply_layout(fig, "📊 Demographic Trends Over Time", height=500)


# ══════════════════════════════════════════════
# A/B TESTING CHARTS
# ══════════════════════════════════════════════
def plot_ab_comparison_bar(result: dict) -> go.Figure:
    """Bar chart comparing two cohort means."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Group A",
        x=[result["metric"]],
        y=[result["group_a_mean"]],
        marker_color=COLORS["primary"],
        text=[f"{result['group_a_mean']:.1f}"],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="Group B",
        x=[result["metric"]],
        y=[result["group_b_mean"]],
        marker_color=COLORS["secondary"],
        text=[f"{result['group_b_mean']:.1f}"],
        textposition="outside",
    ))
    sig_text = "✅ Significant" if result["significant"] else "❌ Not Significant"
    fig.update_layout(barmode="group")
    return _apply_layout(
        fig,
        f"📊 {result['metric']} — {sig_text} (p={result['p_value']:.4f})",
        height=400,
    )


def plot_ab_distribution_overlay(
    group_a_values: pd.Series,
    group_b_values: pd.Series,
    metric_name: str = "Metric",
) -> go.Figure:
    """Overlaid histograms of two cohorts."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=group_a_values, name="Group A",
        marker_color=COLORS["primary"], opacity=0.6,
        nbinsx=30,
    ))
    fig.add_trace(go.Histogram(
        x=group_b_values, name="Group B",
        marker_color=COLORS["secondary"], opacity=0.6,
        nbinsx=30,
    ))
    fig.update_layout(
        barmode="overlay",
        xaxis_title=metric_name,
        yaxis_title="Count",
    )
    return _apply_layout(fig, f"📊 Distribution Comparison — {metric_name}")

