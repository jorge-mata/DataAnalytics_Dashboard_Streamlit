import streamlit as st
import os

def main():
    st.title("About Ximple")
    st.markdown(" ")  # Line break after title

    # Row 1: Image on the right, intro on the left (less margin)
    row1_col1, row1_col2 = st.columns([3, 2], gap="small")
    with row1_col1:
        st.header("Business Understanding")
        st.markdown("---")
        st.write("""
        During this course, we had the opportunity to work with Ximple, a fintech that is facing various challenges, specially when it comes to risk management. 
        The company is looking to improve its risk management processes, particularly in identifying potential clients who may not repay their loans, thus posing a risk to the business.""")
    with row1_col2:
        img_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "img", "Ximple-Card-2048x1072.webp")
        )
        st.image(img_path, use_container_width=True)

    # Row 2: Header left, text right (less margin)
    st.markdown("---")
    row2_col1, row2_col2 = st.columns([1, 3], gap="small")
    with row2_col1:
        st.header("Problem Statement")
    with row2_col2:
        st.write("""
            One of the main challenges is improving its credit risk assessment models. The main problem is to assess the creditworthiness of small business owners to predict loan repayment likelihood.
            The goal is to develop a machine learning model that can accurately predict which clients are likely to default on their loans, allowing Ximple to make informed decisions about loan approvals and risk management.
        """)

    # Row 3: Header left, text right (less margin)
    st.markdown("---")
    row3_col1, row3_col2 = st.columns([1, 3], gap="small")
    with row3_col1:
        st.header("Strategic Insights")
    with row3_col2:
        st.write("""
            The strategic insights derived from the data analysis and machine learning models will help Ximple in the following ways:
        """)

    # --- Strategic Insights Cards ---
    st.markdown("""
    <style>
    .nx-card-header {
        background-color: #401f71;
        color: white;
        text-align: center;
        padding: 0.6em 0.2em;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        font-size: 1.05em;
        letter-spacing: 0.5px;
        margin-bottom: 0;
    }
    .nx-card-body {
        border: 1.5px solid #401f71;
        border-top: none;
        border-radius: 0 0 8px 8px;
        background: transparent;
        padding: 1em 0.7em;
        min-height: 120px;
        font-size: 1em;
        margin-bottom: 1.2em;
        color: #401f71;
    }
    @media (prefers-color-scheme: dark) {
        .nx-card-body {
            color: #fff;
            border-color: #a58fff;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    card_titles = [
        "FINANCIAL INCLUSION FOR UNBANKED ENTREPRENEURS",
        "RISK MANAGEMENT & CREDIT ASSESSMENT",
        "TECH-ENABLED CREDIT & SALES GROWTH",
        "SCALABILITY & MARKET PENETRATION"
    ]
    card_bodies = [
        "Ximple, gives entrepreneurs the opportunity to have a loan to achieve their business goals, providing a safe banking service.",
        "However, it is important to analyze the risk management the company may encounter if the clients don’t repay their loans and credits.",
        "With this, it is also crucial for the company to analyze the risk and keep growing with a well founded base for their customers and sales to keep growing.",
        "Once this is well-established, scalability in the market is important for the penetration of the same and be able to keep innovating and stay competitive."
    ]

    card_cols = st.columns(4, gap="large")
    for i in range(4):
        with card_cols[i]:
            st.markdown(f'<div class="nx-card-header">{card_titles[i]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="nx-card-body">{card_bodies[i]}</div>', unsafe_allow_html=True)
    # --- End Strategic Insights Cards ---

    st.markdown("---")

if __name__ == "__main__":
    main()

# This code is for the "Acerca de" page in a Streamlit application.