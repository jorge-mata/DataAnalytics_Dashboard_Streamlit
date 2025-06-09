import streamlit as st
import pandas as pd
import numpy as np 
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from graphImporte import get_importe_plotly_figure
from graphRisk import get_risk_plotly_figure, get_account_age_plotly_figure_by_affiliation

# Import your page modules
from pages import Acerca_de, Key_Findings, User_Persona_Dashboard, Meet_Nexus, ML_Models

# Then, use them as:
page1 = Acerca_de
page2 = Key_Findings
page3 = User_Persona_Dashboard
page4 = Meet_Nexus
page5 = ML_Models

st.set_page_config(
    page_title='NEXUS Dashboard',
    initial_sidebar_state='collapsed',
    page_icon='NEXUS.png',
    layout='wide'
)

# Custom CSS to hide sidebar and other elements
st.markdown(
    """
    <style>
        /* Hide sidebar, collapsed control, and hamburger/arrow */
        [data-testid="stSidebar"] {display: none !important;}
        [data-testid="collapsedControl"] {display: none !important;}
        .css-1d391kg {display: none !important;} /* Older versions */
        .stDeployButton {display:none;}
        header[data-testid="stHeader"] {z-index: 2;}
        /* Hide the new sidebar toggle button if Streamlit changes its selector */
        [data-testid="stSidebarNav"] {display: none !important;}
        /* Hide the menu button in the header (three dots) */
        button[title="Main menu"] {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# HEADER NAVIGATION BAR
selected = option_menu(
    menu_title=None,
    options=["Dashboard", "About Ximple", "Machine Learning", "Risk Management", "Key Findings", "Meet Nexus"],
    icons=["house", "info-circle", "robot", "person", "book", "people"],
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#483349"},
        "icon": {"color": "white", "font-size": "18px"},
        "nav-link": {"color": "white", "font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#be7b72"},
        "nav-link-selected": {"background-color": "#be7b72"},
    }
)

DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), "Data", "aggregated_df.csv")
csv_path = DEFAULT_CSV_PATH

if csv_path is None:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

if selected == "Dashboard":
    st.markdown("## Main KPIs")

    kpi_json_path = os.path.join(os.path.dirname(__file__), "kpis.json")
    with open(kpi_json_path, "r") as f:
        kpis = json.load(f)

    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric("Loan Approval Rate", f"{kpis['Loan Approval Rate']:.2%}")
    with kpi2:
        st.metric("Delinquency Rate", f"{kpis['Delinquency Rate']:.2%}")

    st.markdown("---")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        df = pd.read_csv(csv_path)
        years_importe = df['year'].unique().tolist() if 'year' in df.columns else [2024]
        years_importe = ["All"] + [str(y) for y in sorted(years_importe)]
        selected_year_str_importe = st.selectbox(
            "Select Year for Importe", years_importe, key="importe_year"
        )
        selected_year_importe = "All" if selected_year_str_importe == "All" else int(selected_year_str_importe)
        importe_fig = get_importe_plotly_figure(csv_path, year=selected_year_importe, height=500)
        importe_fig.update_layout(title_text=f"Total amount per month and monthly average per quarter ({selected_year_importe})")
        st.plotly_chart(importe_fig, use_container_width=True)

    with chart_col2:
        df = pd.read_csv(csv_path)
        years_risk = df['year'].unique().tolist() if 'year' in df.columns else [2024]
        years_risk = ["All"] + [str(y) for y in sorted(years_risk)]
        selected_year_str_risk = st.selectbox(
            "Select Year for Risk", years_risk, key="risk_year"
        )
        selected_year_risk = "All" if selected_year_str_risk == "All" else int(selected_year_str_risk)
        risk_fig = get_risk_plotly_figure(csv_path, year=selected_year_risk, height=500)
        risk_fig.update_layout(title_text=f"Risk Client Counts and Percentage by Month ({selected_year_risk})")
        st.plotly_chart(risk_fig, use_container_width=True)

    st.markdown("---")

    df = pd.read_csv(csv_path)
    af_years = pd.to_datetime(df['fecha_afiliacion']).dt.year
    min_af_year, max_af_year = int(af_years.min()), int(af_years.max())

    af_year_range = st.session_state.get("af_year_range", (min_af_year, max_af_year))

    account_age_aff_fig = get_account_age_plotly_figure_by_affiliation(csv_path, year_range=af_year_range)
    account_age_aff_fig.update_layout(
        title_text="Unique Accounts by Account Age Group (Affiliation Year Filter)"
    )
    st.plotly_chart(account_age_aff_fig, use_container_width=True)

    st.markdown("---")

    table1, table2, table3 = st.columns(3)

    with table1:
        st.markdown("#### Loan Requests per Quarter")
        st.table(pd.DataFrame(list(kpis["Loan Requests per Quarter"].items()), columns=["Quarter", "Requests"]))

    with table2:
        st.markdown("#### Repayment Rate per Quarter")
        repayment_df = pd.DataFrame(
            [(k, f"{v:.2%}") for k, v in kpis["Loan Repayment Rate per Quarter"].items()],
            columns=["Quarter", "Repayment Rate"]
        )
        st.table(repayment_df)

    with table3:
        st.markdown("#### Avg Purchase Value by Payment Type")
        avg_purchase_df = pd.DataFrame(
            [(k, f"${v:,.2f}") for k, v in kpis["Average Purchase Value by Payment Type"].items()],
            columns=["Payment Type", "Average Value"]
        )
        st.table(avg_purchase_df)

elif selected == "About Ximple":
    page1.main()

elif selected == "Key Findings":
    page2.main()

elif selected == "Risk Management":
    page3.main()

elif selected == "Meet Nexus":
    page4.main()

elif selected == "Machine Learning":
    page5.main()