import streamlit as st
import streamlit_option_menu
import pandas as pd
import numpy as np 
import os
import json
# Remove Bokeh imports
# from bokeh.models import FactorRange, HoverTool, ColumnDataSource
# from bokeh.palettes import Category10  
# from bokeh.plotting import figure

import plotly.express as px
import plotly.graph_objects as go

from streamlit_option_menu import option_menu
from graphImporte import get_importe_plotly_figure   # <-- Update to Plotly version
from graphRisk import get_risk_plotly_figure, get_account_age_plotly_figure_by_affiliation  # <-- Update to Plotly version

st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)

# Add file uploader to sidebar
with st.sidebar:
    uploaded_file = st.file_uploader(
        "Upload CSV file (optional)",
        type=["csv"],
        help="Upload a CSV file to override the default data"
    )

DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), "Data", "aggregated_df.csv")

if uploaded_file is not None:
    csv_path = uploaded_file
else:
    csv_path = DEFAULT_CSV_PATH

# Require file upload before showing dashboard
if csv_path is None:
    st.warning("Please upload a CSV file to continue.")
    st.stop()

with st.sidebar:
  selected = option_menu(
    menu_title = "Main Menu",
    options = ["Dashboard.py","App.py"],
    icons = ["house","book"],
    menu_icon = "cast",
    default_index = 0,
    styles={
        "container": {"background-color": "#483349"},
        "nav-link-selected": {"background-color": "#be7b72"}
    }
  )

st.markdown("## KPIs Principales")

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
    years = df['year'].unique().tolist() if 'year' in df.columns else [2024]
    years = ["All"] + [str(y) for y in sorted(years)]
    selected_year_str_importe = st.session_state.get("selected_year_str_importe", years[0])
    selected_year_importe = "All" if selected_year_str_importe == "All" else int(selected_year_str_importe)
    st.markdown(f"## Importe total por mes y promedio mensual por trimestre ({selected_year_importe})")
    # Use Plotly chart
    importe_fig = get_importe_plotly_figure(csv_path, year=selected_year_importe, height=500, width=900)
    st.plotly_chart(importe_fig, use_container_width=True)

    selected_year_str_importe = st.selectbox(
        "Select Year", years, index=years.index(str(selected_year_importe)), key="importe_year"
    )
    st.session_state["selected_year_str_importe"] = selected_year_str_importe

with chart_col2:
    df = pd.read_csv(csv_path)
    years = df['year'].unique().tolist() if 'year' in df.columns else [2024]
    years = ["All"] + [str(y) for y in sorted(years)] 
    selected_year_str = st.session_state.get("selected_year_str", years[0])
    selected_year = "All" if selected_year_str == "All" else int(selected_year_str)

    st.markdown(f"## Risk Client Counts and Percentage by Month ({selected_year})")
    risk_fig = get_risk_plotly_figure(csv_path, year=selected_year, height=500, width=900)
    st.plotly_chart(risk_fig, use_container_width=True)

    selected_year_str = st.selectbox(
        "Select Year", years, index=years.index(str(selected_year)), key="risk_year"
    )
    st.session_state["selected_year_str"] = selected_year_str

st.markdown("---")

st.markdown("## Unique Accounts by Account Age Group (Affiliation Year Filter)")

df = pd.read_csv(csv_path)
af_years = pd.to_datetime(df['fecha_afiliacion']).dt.year
min_af_year, max_af_year = int(af_years.min()), int(af_years.max())

af_year_range = st.session_state.get("af_year_range", (min_af_year, max_af_year))

account_age_aff_fig = get_account_age_plotly_figure_by_affiliation(csv_path, year_range=af_year_range)
st.plotly_chart(account_age_aff_fig, use_container_width=True)

af_year_range = st.slider(
    "Select Affiliation Year Range",
    min_af_year,
    max_af_year,
    af_year_range,
    key="af_year_range"
)

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