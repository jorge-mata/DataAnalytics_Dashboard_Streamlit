import pandas as pd
import calendar
import numpy as np
from bokeh.models import ColumnDataSource, HoverTool, LinearAxis, Range1d, FactorRange
from bokeh.plotting import figure
from bokeh.transform import dodge

color_palette = {
    "nx1" : "#401f71",
    "nx2" : "#824d74",
    "nx3" : "#be7b72",
    "nx4" : "#fdaf7b",
    "nx5" : "#ffffff",
    "nx6" : "#5e3992",
    "nx7" : "#986384",
    "nx8" : "#d88876",
    "nx9" : "#fbcda0",
    "nx10": "#d9ccef"
}

def get_risk_bokeh_figure(csv_path=None, year="All", height=500, width=900, df=None):
    if df is None:
        if csv_path is None:
            raise ValueError("Either df or csv_path must be provided")
        df = pd.read_csv(csv_path)

    # Only filter if year is not None and not "All"
    if 'year' in df.columns and year not in (None, "All"):
        df = df[df['year'] == year]

    grouped = df.groupby(['month', 'riskclient']).size().unstack(fill_value=0).reset_index()
    grouped.columns.name = None

    if 0 not in grouped.columns:
        grouped[0] = 0
    if 1 not in grouped.columns:
        grouped[1] = 0

    grouped = grouped.rename(columns={0: 'risk_0', 1: 'risk_1'})
    grouped['total'] = grouped['risk_0'] + grouped['risk_1']
    grouped['risk_1_pct'] = (grouped['risk_1'] / grouped['total']) * 100
    grouped['months'] = grouped['month'].apply(lambda x: calendar.month_abbr[x])
    grouped = grouped.sort_values('month')
    source = ColumnDataSource(grouped)
    months_str = grouped['months'].tolist()
    y_max = grouped[['risk_0', 'risk_1']].values.max() * 1.1 if not grouped.empty else 1

    # Use color_palette for graph colors
    color_0 = color_palette["nx2"]   # e.g. for Risk Client = 0
    color_1 = color_palette["nx3"]   # e.g. for Risk Client = 1
    color_line = color_palette["nx4"]  # e.g. for percentage line
    color_circle = color_palette["nx4"]

    x_factors = months_str  # Use months_str directly as x_factors

    p = figure(
        x_range=FactorRange(*x_factors),
        height=height,
        width=width,
        title=f"Risk Client Counts and Percentage by Month ({year if year not in (None, 'All') else 'All'})",
        toolbar_location="above",
        tools=["pan", "wheel_zoom", "box_zoom", "reset"]
    )

    bar_0 = p.vbar(x=dodge('months', -0.2, range=p.x_range), top='risk_0', source=source,
                   width=0.35, color=color_0, legend_label="Risk Client = 0",
                   name="risk_0")
    hover_bar_0 = HoverTool(
        tooltips=[
            ("Month", "@months"),
            ("Risk Client", "0"),
            ("Count", "@risk_0"),
            ("Total Clients", "@total"),
            ("Percentage Risk=1", "@risk_1_pct%")
        ],
        renderers=[bar_0]
    )
    bar_1 = p.vbar(x=dodge('months', 0.2, range=p.x_range), top='risk_1', source=source,
                   width=0.35, color=color_1, legend_label="Risk Client = 1",
                   name="risk_1")
    hover_bar_1 = HoverTool(
        tooltips=[
            ("Month", "@months"),
            ("Risk Client", "1"),
            ("Count", "@risk_1"),
            ("Total Clients", "@total"),
            ("Percentage Risk=1", "@risk_1_pct%")
        ],
        renderers=[bar_1]
    )
    p.extra_y_ranges = {"percent": Range1d(start=0, end=100)}
    p.add_layout(LinearAxis(y_range_name="percent", axis_label="Risk Client Percentage (%)"), 'right')
    line = p.line('months', 'risk_1_pct', source=source, line_width=3, color=color_line,
                  y_range_name="percent", legend_label="Risk Client = 1 (%)",
                  name="percentage_line")
    circles = p.circle('months', 'risk_1_pct', source=source, size=10, color=color_circle,
                       y_range_name="percent", name="percentage_line")
    hover_line = HoverTool(
        tooltips=[
            ("Month", "@months"),
            ("Risk Client = 1", "@risk_1_pct%"),
            ("Count (Risk=1)", "@risk_1"),
            ("Count (Risk=0)", "@risk_0"),
            ("Total Clients", "@total")
        ],
        renderers=[line, circles]
    )
    p.add_tools(hover_bar_0, hover_bar_1, hover_line)
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    p.xaxis.axis_label = "Month"
    p.yaxis[0].axis_label = "Count"
    return p

# --- New graph for external_account_id by account age group and year range ---

def get_account_age_bokeh_figure(csv_path=None, year_range=None, df=None):
    if df is None:
        if csv_path is None:
            raise ValueError("Either df or csv_path must be provided")
        df = pd.read_csv(csv_path)
    if year_range and 'year' in df.columns:
        df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    if 'account_age_years' not in df.columns:
        raise ValueError("Column 'account_age_years' not found in data.")
    bins = [0, 1, 3, np.inf]
    labels = ['< 1 year', '1-3 years', '> 3 years']
    df['age_group'] = pd.cut(df['account_age_years'], bins=bins, labels=labels, right=False)
    grouped = df.groupby('age_group')['external_account_id'].nunique().reset_index()
    grouped = grouped.rename(columns={'external_account_id': 'account_count'})
    source = ColumnDataSource(grouped)
    p = figure(x_range=labels, height=400, width=600,
               title="Unique Accounts by Account Age Group",
               toolbar_location=None, tools="")
    bars = p.vbar(x='age_group', top='account_count', width=0.6, source=source,
                  fill_color=color_palette["nx3"], line_color=color_palette["nx2"])
    hover = HoverTool(tooltips=[
        ("Age Group", "@age_group"),
        ("Unique Accounts", "@account_count")
    ], renderers=[bars])
    p.add_tools(hover)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Account Age"
    p.yaxis.axis_label = "Unique Accounts"
    return p

def get_account_age_bokeh_figure_by_affiliation(csv_path=None, year_range=None, df=None):
    if df is None:
        if csv_path is None:
            raise ValueError("Either df or csv_path must be provided")
        df = pd.read_csv(csv_path)
    if 'fecha_afiliacion' not in df.columns:
        raise ValueError("Column 'fecha_afiliacion' not found in data.")
    df['afiliacion_year'] = pd.to_datetime(df['fecha_afiliacion']).dt.year
    if year_range:
        df = df[(df['afiliacion_year'] >= year_range[0]) & (df['afiliacion_year'] <= year_range[1])]
    if 'account_age_years' not in df.columns:
        if 'fecha_afiliacion' in df.columns:
            df['fecha_afiliacion'] = pd.to_datetime(df['fecha_afiliacion'], errors='coerce')
            df['account_age_years'] = (pd.Timestamp.now() - df['fecha_afiliacion']).dt.days / 365.25
        else:
            raise ValueError("Column 'account_age_years' or 'fecha_afiliacion' not found in data.")
    if 'account_age_years' not in df.columns:
        raise ValueError("Column 'account_age_years' not found in data.")
    bins = [0, 1, 3, np.inf]
    labels = ['< 1 year', '1-3 years', '> 3 years']
    df['age_group'] = pd.cut(df['account_age_years'], bins=bins, labels=labels, right=False)
    grouped = df.groupby('age_group')['external_account_id'].nunique().reset_index()
    grouped = grouped.rename(columns={'external_account_id': 'account_count'})
    source = ColumnDataSource(grouped)
    p = figure(
        x_range=labels,
        height=400,
        width=600,
        title="Unique Accounts by Account Age Group (Filtered by Affiliation Year)",
        toolbar_location=None,
        tools=""
    )
    bars = p.vbar(
        x='age_group',
        top='account_count',
        width=0.6,
        source=source,
        fill_color=color_palette["nx3"],
        line_color=color_palette["nx2"]
    )
    hover = HoverTool(tooltips=[
        ("Age Group", "@age_group"),
        ("Unique Accounts", "@account_count")
    ], renderers=[bars])
    p.add_tools(hover)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.axis_label = "Account Age"
    p.yaxis.axis_label = "Unique Accounts"
    return p
