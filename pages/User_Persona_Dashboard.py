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
        col1, col3 = st.columns([1, 2])  # Adjust column widths after removing col2
        with col1:
            # Map 0 and 1 to "No Risk" and "Risk" for display purposes
            riskclient_map = {0: "No Risk", 1: "Risk"}
            risk_levels = sorted(df['riskclient'].unique())  # Ensure risk_levels contains the original values (0 and 1)
            risk_levels_display = [riskclient_map[risk] for risk in risk_levels]
            selected_risk_display = st.multiselect("Risk Level", risk_levels_display, default=risk_levels_display)

            # Reverse map the selected display values back to 0 and 1 for filtering
            selected_risk = [key for key, value in riskclient_map.items() if value in selected_risk_display]

        with col3:
            # Remove the "item_" prefix from the 'most_purchased_category' column for display purposes
            category_display = df['most_purchased_category'].str.replace('item_', '', regex=False).unique()
            category_mapping = dict(zip(category_display, df['most_purchased_category'].unique()))  # Map cleaned names back to original

            # Display the cleaned category names in the multiselect
            selected_category_display = st.multiselect(
                "Most Purchased Category",
                options=category_display,
                default=category_display
            )

            # Reverse map the selected display values back to the original values for filtering
            category_filter = [category_mapping[display] for display in selected_category_display]

    # Apply filters to the DataFrame
    filtered_df = df[df['riskclient'].isin(selected_risk)]
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

    # Update the labels for the graphs to display "No Risk" and "Risk"
    riskclient_map = {0: "No Risk", 1: "Risk"}

    # First row of charts
    with st.expander("Risk Profile Overview", expanded=True):
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            colors = ["#824d74", "#be7b72"]
            st.markdown("<div style='text-align: center;'><b>Number of Loans by Risk Level</b></div>", unsafe_allow_html=True)
            fig = go.Figure(go.Pie(
                labels=risk_summary['riskclient'].map(riskclient_map),  # Map 0/1 to "No Risk"/"Risk"
                values=risk_summary['num_loans'],
                marker=dict(colors=colors),
                textinfo='label+percent',
                textfont=dict(color='white', size=22),
                insidetextfont=dict(color='white', size=22),
                hole=0,
            ))
            fig.update_layout(
                height=400,
                width=400,
                margin=dict(l=0, r=0, t=40, b=0),
                showlegend=True,
                legend=dict(font=dict(size=16), orientation="h", y=-0.1, x=0.5, xanchor="center"),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            risk1_df = risk_summary[risk_summary['riskclient'] == 1]
            if not risk1_df.empty:
                risk1_rate = risk1_df['ever_delinquent_rate'].iloc[0] * 100  # as percentage
                st.markdown("#### Ever Delinquent Rate")
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=risk1_rate,
                    number={'suffix': "%"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#be7b72"},
                        'steps': [
                            {'range': [0, 50], 'color': "#f0e6e6"},
                            {'range': [50, 100], 'color': "#f5cccc"}
                        ],
                    },
                    title={'text': "Percentage of Payments not Paid"}
                ))
                st.plotly_chart(fig_gauge, use_container_width=True)
            else:
                st.info("No data for Risk Level 1 in current filter.")

    # Second row of charts
    with st.expander("Category and Payment Analysis", expanded=False):
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("#### Most Purchased Category by Risk Level")
            category_by_risk = filtered_df.groupby(['riskclient', 'most_purchased_category']).size().reset_index(name='count')

            # Remove the "item_" prefix from the 'most_purchased_category' column for display purposes
            category_by_risk['most_purchased_category_clean'] = category_by_risk['most_purchased_category'].str.replace('item_', '', regex=False)

            # Group categories with counts < 10 for both "Risk" and "No Risk" into "otros"
            grouped_data = []
            for category in category_by_risk['most_purchased_category_clean'].unique():
                category_data = category_by_risk[category_by_risk['most_purchased_category_clean'] == category]
                risk_counts = category_data.groupby('riskclient')['count'].sum()
                if all(risk_counts < 10):  # Check if counts for both "Risk" and "No Risk" are < 10
                    for risk in risk_counts.index:
                        grouped_data.append({'riskclient': risk, 'most_purchased_category_clean': 'otros', 'count': risk_counts[risk]})
                else:
                    grouped_data.extend(category_data.to_dict('records'))

            # Convert grouped data back to a DataFrame
            category_by_risk_grouped = pd.DataFrame(grouped_data)

            # Aggregate counts for "otros" to ensure it is summed up properly
            category_by_risk_grouped = category_by_risk_grouped.groupby(['riskclient', 'most_purchased_category_clean'], as_index=False).agg({'count': 'sum'})

            fig3 = go.Figure()
            for i, risk in enumerate(risk_levels):
                df_risk = category_by_risk_grouped[category_by_risk_grouped['riskclient'] == risk]
                fig3.add_trace(go.Bar(
                    x=df_risk['most_purchased_category_clean'],  # Use the cleaned category names
                    y=df_risk['count'],
                    name=riskclient_map[risk],  # Map 0/1 to "No Risk"/"Risk"
                    marker_color=colors[i % len(colors)]
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
            
            fig4 = go.Figure()
            for i, risk in enumerate(risk_levels):
                df_risk = payment_method_by_risk[payment_method_by_risk['riskclient'] == risk]
                fig4.add_trace(go.Bar(
                    x=df_risk['medio_pago'],
                    y=df_risk['count'],
                    name=riskclient_map[risk],  # Map 0/1 to "No Risk"/"Risk"
                    marker_color=colors[i % len(colors)]
                ))
            
            fig4.update_layout(
                title='Payment Method by Risk Level',
                xaxis_title='Payment Method',
                yaxis_title='Count',
                barmode='stack'
            )
            st.plotly_chart(fig4, use_container_width=True)

    # Third row of charts
    with st.expander("Tenure and Seasonality", expanded=False):
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("#### Client Tenure vs. Risk")
            tenure_by_risk = filtered_df.groupby('riskclient')['days_since_affiliation'].mean().reset_index()
            
            fig5 = go.Figure()
            for i, risk in enumerate(risk_levels):
                df_risk = tenure_by_risk[tenure_by_risk['riskclient'] == risk]
                fig5.add_trace(go.Bar(
                    x=[riskclient_map[risk]],  # Map 0/1 to "No Risk"/"Risk"
                    y=df_risk['days_since_affiliation'],
                    name=riskclient_map[risk],  # Map 0/1 to "No Risk"/"Risk"
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
            # Group by 'riskclient' and 'es_temporada_alta_real' to calculate the required metrics
            seasonality = filtered_df.groupby(['riskclient', 'es_temporada_alta_real']).agg(
                num_loans=('loan_request_id', 'count'),
                avg_importe=('total_importe', 'mean'),
                avg_delinquencies=('num_delinquencies', 'mean')
            ).reset_index()
            seasonality['seasonality_label'] = seasonality['es_temporada_alta_real'].map({1: 'High', 0: 'Low'})
            
            fig6 = go.Figure()
            for i, season in enumerate(['High', 'Low']):
                df_season = seasonality[seasonality['seasonality_label'] == season]
                fig6.add_trace(go.Bar(
                    x=df_season['riskclient'].map(riskclient_map),  # Map 0/1 to "No Risk"/"Risk"
                    y=df_season['num_loans'],
                    name=season,  # Use "High" and "Low" as the legend labels
                    marker_color=colors[i % len(colors)],
                    hovertemplate="<b>Risk Level:</b> %{x}<br><b>Seasonality:</b> %{name}<br><b>Number of Loans:</b> %{y}<extra></extra>"  # Custom hover text
                ))
            
            fig6.update_layout(
                title='Loans by Risk Level and Seasonality',
                xaxis_title='Risk Level',
                yaxis_title='Number of Loans',
                barmode='group',
                legend_title_text='Seasonality'
            )
            st.plotly_chart(fig6, use_container_width=True)

    # Show filtered raw data in a collapsed expander
    with st.expander("Raw Data (Filtered)", expanded=False):
        st.dataframe(filtered_df)

if __name__ == "__main__":
    main()

