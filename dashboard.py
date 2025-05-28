import streamlit as st
import streamlit_option_menu
import pandas as pd
import numpy as np 
import os
import json
from bokeh.models import FactorRange, HoverTool, ColumnDataSource
from bokeh.palettes import Category10  # Cambiado aquí
from bokeh.plotting import figure

from streamlit_option_menu import option_menu
from graphImporte import get_importe_bokeh_figure
from graphRisk import get_risk_bokeh_figure

st.set_page_config(
    page_title = 'Streamlit Sample Dashboard Template',
    page_icon = '✅',
    layout = 'wide'
)


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


# Bokeh chart section
# Load your aggregated_df.csv
csv_path = os.path.join(os.path.dirname(__file__), "aggregated_df.csv")

st.markdown("## Importe total por mes y promedio mensual por trimestre (2024)")
importe_fig = get_importe_bokeh_figure(csv_path)
st.bokeh_chart(importe_fig, use_container_width=True)

st.markdown("## Risk Client Counts and Percentage by Month (2024)")
risk_fig = get_risk_bokeh_figure(csv_path)
st.bokeh_chart(risk_fig, use_container_width=True)

# Leer KPIs desde el archivo JSON
kpi_json_path = os.path.join(os.path.dirname(__file__), "kpis.json")
with open(kpi_json_path, "r") as f:
    kpis = json.load(f)

# Mostrar KPIs principales
st.markdown("## KPIs Principales")
kpi1, kpi2 = st.columns(2)
with kpi1:
    st.metric("Loan Approval Rate", f"{kpis['Loan Approval Rate']:.2%}")
with kpi2:
    st.metric("Delinquency Rate", f"{kpis['Delinquency Rate']:.2%}")

# Mostrar Loan Requests per Quarter
st.markdown("### Loan Requests per Quarter")
st.table(pd.DataFrame(list(kpis["Loan Requests per Quarter"].items()), columns=["Quarter", "Requests"]))

# Mostrar Loan Repayment Rate per Quarter
st.markdown("### Loan Repayment Rate per Quarter")
repayment_df = pd.DataFrame(
    [(k, f"{v:.2%}") for k, v in kpis["Loan Repayment Rate per Quarter"].items()],
    columns=["Quarter", "Repayment Rate"]
)
st.table(repayment_df)

# Mostrar Average Purchase Value by Payment Type
st.markdown("### Average Purchase Value by Payment Type")
avg_purchase_df = pd.DataFrame(
    [(k, f"${v:,.2f}") for k, v in kpis["Average Purchase Value by Payment Type"].items()],
    columns=["Payment Type", "Average Value"]
)
st.table(avg_purchase_df)

