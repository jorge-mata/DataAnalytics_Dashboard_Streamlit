import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

def main():
    st.title("Risk Management Dashboard")

    # Custom CSS to set selected filter color to #be7b72
    st.markdown(
        """
        <style>
        /* Selected option in selectbox/multiselect dropdown */
        div[data-baseweb="option"]:has([aria-selected="true"]) {
            background-color: #be7b72 !important;
            color: white !important;
        }
        /* Selected tag in multiselect */
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #be7b72 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Load data
    DATA_PATH = os.path.join(os.path.dirname(__file__), '../Data/aggregated_df.csv')
    df = pd.read_csv(DATA_PATH)

    # Preprocessing
    df['fecha_afiliacion'] = pd.to_datetime(df['fecha_afiliacion'])
    df['days_since_affiliation'] = (pd.Timestamp.today() - df['fecha_afiliacion']).dt.days

    # Top filters (not sidebar)
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            risk_levels = sorted(df['riskclient'].unique())
            selected_risk = st.multiselect("Risk Level", risk_levels, default=risk_levels)
        with col2:
            delinquency_filter = st.selectbox("Ever Delinquent", options=["All", True, False], index=0)
        with col3:
            category_filter = st.multiselect("Most Purchased Category", df['most_purchased_category'].unique(), default=list(df['most_purchased_category'].unique()))

    filtered_df = df[df['riskclient'].isin(selected_risk)]
    if delinquency_filter != "All":
        filtered_df = filtered_df[filtered_df['ever_delinquent'] == delinquency_filter]
    if category_filter:
        filtered_df = filtered_df[filtered_df['most_purchased_category'].isin(category_filter)]

    st.markdown("### Risk Profile Overview")
    risk_summary = filtered_df.groupby('riskclient').agg(
        num_loans=('loan_request_id', 'count'),
        approval_rate=('approved', 'mean'),
        avg_importe=('total_importe', 'mean'),
        avg_delinquencies=('num_delinquencies', 'mean'),
        ever_delinquent_rate=('ever_delinquent', 'mean')
    ).reset_index()

    st.dataframe(risk_summary)

    # First row of charts
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            risk_summary,
            x='riskclient',
            y='num_loans',
            color='riskclient',
            title='Number of Loans by Risk Level'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            risk_summary,
            x='riskclient',
            y='ever_delinquent_rate',
            color='riskclient',
            title='Ever Delinquent Rate by Risk Level'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Second row of charts
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Most Purchased Category by Risk Level")
        category_by_risk = filtered_df.groupby(['riskclient', 'most_purchased_category']).size().reset_index(name='count')
        fig3 = px.bar(
            category_by_risk,
            x='riskclient',
            y='count',
            color='most_purchased_category',
            barmode='stack',
            title='Most Purchased Category by Risk Level'
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### Payment Method by Risk Level")
        payment_method_by_risk = filtered_df.groupby(['riskclient', 'medio_pago']).size().reset_index(name='count')
        fig4 = px.bar(
            payment_method_by_risk,
            x='riskclient',
            y='count',
            color='medio_pago',
            barmode='stack',
            title='Payment Method by Risk Level'
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Third row of charts
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### Client Tenure vs. Risk")
        tenure_by_risk = filtered_df.groupby('riskclient')['days_since_affiliation'].mean().reset_index()
        fig5 = px.bar(
            tenure_by_risk,
            x='riskclient',
            y='days_since_affiliation',
            color='riskclient',
            title='Average Days Since Affiliation by Risk Level'
        )
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("#### Seasonality Analysis")
        seasonality = filtered_df.groupby(['riskclient', 'es_temporada_alta_real']).agg(
            num_loans=('loan_request_id', 'count'),
            avg_importe=('total_importe', 'mean'),
            avg_delinquencies=('num_delinquencies', 'mean')
        ).reset_index()
        seasonality['temporada'] = seasonality['es_temporada_alta_real'].map({1: 'Alta', 0: 'Baja'})
        fig6 = px.bar(
            seasonality,
            x='riskclient',
            y='num_loans',
            color='temporada',
            barmode='group',
            title='Loans by Risk Level and Season'
        )
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("### Raw Data (Filtered)")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()

