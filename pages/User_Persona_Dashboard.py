import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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

    # First row of charts with go instead of px
    col1, col2 = st.columns(2)
    with col1:
        colors = ["#824d74", "#be7b72"]
        risk_levels = risk_summary['riskclient'].unique()
        
        fig = go.Figure()
        for i, risk in enumerate(risk_levels):
            df_risk = risk_summary[risk_summary['riskclient'] == risk]
            fig.add_trace(go.Bar(
                x=df_risk['riskclient'],
                y=df_risk['num_loans'],
                name=str(risk),
                marker_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            title='Number of Loans by Risk Level',
            xaxis_title='Risk Level',
            yaxis_title='Number of Loans',
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = go.Figure()
        for i, risk in enumerate(risk_levels):
            df_risk = risk_summary[risk_summary['riskclient'] == risk]
            fig2.add_trace(go.Bar(
                x=df_risk['riskclient'],
                y=df_risk['ever_delinquent_rate'],
                name=str(risk),
                marker_color=colors[i % len(colors)]
            ))
        
        fig2.update_layout(
            title='Ever Delinquent Rate by Risk Level',
            xaxis_title='Risk Level',
            yaxis_title='Delinquent Rate',
            barmode='group'
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Second row of charts - only changing the bar colors
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### Most Purchased Category by Risk Level")
        category_by_risk = filtered_df.groupby(['riskclient', 'most_purchased_category']).size().reset_index(name='count')
        
        # Get unique categories
        categories = category_by_risk['most_purchased_category'].unique()
        
        fig3 = go.Figure()
        colors = ["#824d74", "#be7b72"]  # Specified hex colors
        for i, risk in enumerate(risk_levels):
            df_risk = category_by_risk[category_by_risk['riskclient'] == risk]
            fig3.add_trace(go.Bar(
                x=df_risk['most_purchased_category'],
                y=df_risk['count'],
                name=str(risk),
                marker_color=colors[i % len(colors)]  # Alternating colors
            ))
        
        fig3.update_layout(
            title='Most Purchased Category by Risk Level',
            xaxis_title='Category',
            yaxis_title='Count',
            barmode='stack'
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### Payment Method by Risk Level")
        payment_method_by_risk = filtered_df.groupby(['riskclient', 'medio_pago']).size().reset_index(name='count')
        
        # Get unique payment methods
        payment_methods = payment_method_by_risk['medio_pago'].unique()
        
        fig4 = go.Figure()
        for i, risk in enumerate(risk_levels):
            df_risk = payment_method_by_risk[payment_method_by_risk['riskclient'] == risk]
            fig4.add_trace(go.Bar(
                x=df_risk['medio_pago'],
                y=df_risk['count'],
                name=str(risk),
                marker_color=colors[i % len(colors)]  # Alternating colors
            ))
        
        fig4.update_layout(
            title='Payment Method by Risk Level',
            xaxis_title='Payment Method',
            yaxis_title='Count',
            barmode='stack'
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Third row of charts
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("#### Client Tenure vs. Risk")
        tenure_by_risk = filtered_df.groupby('riskclient')['days_since_affiliation'].mean().reset_index()
        
        fig5 = go.Figure()
        for i, risk in enumerate(risk_levels):
            df_risk = tenure_by_risk[tenure_by_risk['riskclient'] == risk]
            fig5.add_trace(go.Bar(
                x=df_risk['riskclient'],
                y=df_risk['days_since_affiliation'],
                name=str(risk),
                marker_color=colors[i % len(colors)]
            ))
        
        fig5.update_layout(
            title='Average Days Since Affiliation by Risk Level',
            xaxis_title='Risk Level',
            yaxis_title='Days Since Affiliation',
            barmode='group'
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
        
        fig6 = go.Figure()
        for i, temp in enumerate(['Alta', 'Baja']):
            df_temp = seasonality[seasonality['temporada'] == temp]
            fig6.add_trace(go.Bar(
                x=df_temp['riskclient'],
                y=df_temp['num_loans'],
                name=temp,
                marker_color=colors[i % len(colors)]
            ))
        
        fig6.update_layout(
            title='Loans by Risk Level and Season',
            xaxis_title='Risk Level',
            yaxis_title='Number of Loans',
            barmode='group'
        )
        st.plotly_chart(fig6, use_container_width=True)

    st.markdown("### Raw Data (Filtered)")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main()

