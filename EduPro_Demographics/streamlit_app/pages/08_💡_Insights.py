"""
EduPro Demographics — Business Insights Page
==============================================
Professional business insights and strategic recommendations.
"""

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.dashboard import (
    inject_custom_css, render_page_header, render_section_header,
    render_sidebar_filters, render_insight_card,
)
from src.data_loader import load_users_data
from src.preprocessing import preprocess_data
from src.analysis import compute_kpis
from src.utils import generate_insights_text

st.set_page_config(page_title="Insights | EduPro", page_icon="💡", layout="wide")


@st.cache_data(show_spinner=False)
def get_data():
    raw = load_users_data()
    return preprocess_data(raw, save=False)


def main():
    inject_custom_css()
    df = get_data()
    filtered = render_sidebar_filters(df)
    kpis = compute_kpis(filtered)

    render_page_header("💡 Business Insights", "Data-driven insights and strategic recommendations")

    # ── Auto-Generated Insights ──
    render_section_header(
        "🔍 Key Findings",
        "Automatically generated insights from the learner demographics data",
    )

    insights = generate_insights_text(filtered, kpis)
    for insight in insights:
        render_insight_card(insight["title"], insight["content"], insight["style"])

    # ── Executive Summary ──
    render_section_header("📋 Executive Summary")

    st.markdown(f"""
    <div class="insight-card info">
        <h4>📊 Platform Overview</h4>
        <p>
        EduPro currently serves <b>{kpis['total_learners']:,}</b> registered learners.
        The platform's user base spans ages <b>{kpis['min_age']}</b> to <b>{kpis['max_age']}</b>,
        with an average age of <b>{kpis['average_age']}</b> years (median: {kpis['median_age']}).
        The gender distribution shows a <b>{kpis['gender_ratio']}</b> male-to-female ratio,
        with <b>{kpis['male_count']:,}</b> male and <b>{kpis['female_count']:,}</b> female learners.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Detailed Analysis Sections ──
    col1, col2 = st.columns(2)

    with col1:
        render_section_header("📅 Age Demographics Insights")

        minor_pct = round(kpis["minor_count"] / kpis["total_learners"] * 100, 1)
        adult_pct = round(kpis["adult_count"] / kpis["total_learners"] * 100, 1)

        st.markdown(f"""
        **Key Observations:**

        - 📊 The age distribution is concentrated between **{kpis['min_age']}–{kpis['max_age']}** years
        - 📈 Average age is **{kpis['average_age']}** years, indicating a young user base
        - 🔞 **{kpis['minor_count']:,}** learners (**{minor_pct}%**) are minors (under 18)
        - 🧑 **{kpis['adult_count']:,}** learners (**{adult_pct}%**) are adults
        - 📋 The most common age indicates peak enrollment timing

        **Recommendations:**
        - Develop age-appropriate learning pathways
        - Implement parental consent for minor learners
        - Create targeted content for the dominant age group
        """)

    with col2:
        render_section_header("👥 Gender Balance Insights")

        male_pct = round(kpis["male_count"] / kpis["total_learners"] * 100, 1)
        female_pct = round(kpis["female_count"] / kpis["total_learners"] * 100, 1)
        balance = "balanced" if abs(male_pct - female_pct) < 10 else "shows disparity"

        st.markdown(f"""
        **Key Observations:**

        - ♂️ Male learners: **{kpis['male_count']:,}** (**{male_pct}%**)
        - ♀️ Female learners: **{kpis['female_count']:,}** (**{female_pct}%**)
        - ⚖️ The gender distribution is **{balance}**
        - 📊 Gender ratio: **{kpis['gender_ratio']}** (Male:Female)

        **Recommendations:**
        - {'Maintain current inclusive strategies' if balance == 'balanced' else 'Implement targeted outreach to underrepresented gender'}
        - Monitor gender distribution trends over time
        - Ensure course content appeals to all demographics
        - Consider gender-specific marketing campaigns
        """)

    # ── Email & Communication ──
    render_section_header("📧 Communication Channel Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        **Email Provider Analysis:**

        - 📧 Most popular provider: **{kpis['most_common_provider']}**
        - 🌐 Total unique providers: **{kpis['unique_email_providers']}**
        - 📝 Average username length: **{kpis['avg_username_length']}** characters

        **Action Items:**
        - Optimize email templates for {kpis['most_common_provider']}
        - Test deliverability across all major providers
        - Consider provider-specific formatting requirements
        """)

    with col2:
        st.markdown("""
        **Data Quality Recommendations:**

        - ✅ Implement real-time email validation at registration
        - ✅ Add email verification step for new accounts
        - ✅ Monitor for disposable email addresses
        - ✅ Maintain email hygiene with periodic bounced-email cleanup
        - ✅ Consider double opt-in for marketing communications
        """)

    # ── Strategic Recommendations ──
    render_section_header("🚀 Strategic Recommendations", "Actionable strategies based on data analysis")

    strategies = [
        {
            "title": "📚 Content Strategy",
            "content": (
                f"Design learning content tailored to the {kpis['min_age']}–{kpis['max_age']} age demographic. "
                f"Prioritize topics and teaching styles that resonate with learners averaging "
                f"{kpis['average_age']} years old. Consider gamification for younger learners."
            ),
            "style": "info",
        },
        {
            "title": "📈 Growth Strategy",
            "content": (
                "Expand the user base by targeting underrepresented age groups and demographics. "
                "Implement referral programs leveraging the existing active user community. "
                "Partner with educational institutions for bulk enrollments."
            ),
            "style": "default",
        },
        {
            "title": "🔒 Compliance & Safety",
            "content": (
                f"With {kpis['minor_count']:,} minor learners on the platform, ensure compliance with "
                "COPPA (Children's Online Privacy Protection Act) and GDPR regulations. "
                "Implement age verification, parental consent workflows, and data protection measures."
            ),
            "style": "warning",
        },
        {
            "title": "📊 Data Quality Improvement",
            "content": (
                "Enhance the learner database quality by implementing mandatory field validation, "
                "email verification, and periodic data audits. Add optional fields like location, "
                "education level, and interests for richer demographic analysis."
            ),
            "style": "info",
        },
    ]

    for strategy in strategies:
        render_insight_card(strategy["title"], strategy["content"], strategy["style"])


main()
