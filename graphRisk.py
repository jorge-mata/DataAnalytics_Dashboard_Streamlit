import pandas as pd
import calendar
import numpy as np
import plotly.graph_objects as go

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

def get_risk_plotly_figure(csv_path, year="All", height=500, width=900):
    df = pd.read_csv(csv_path)

    # Only filter if year is not None and not "All"
    if 'year' in df.columns and year not in (None, "All"):
        df = df[df['year'] == int(year)]

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

    months_str = grouped['months'].tolist()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=months_str,
        y=grouped['risk_0'],
        name="Risk Client = 0",
        marker_color=color_palette["nx2"],
        hovertemplate='Month: %{x}<br>Risk Client: 0<br>Count: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=months_str,
        y=grouped['risk_1'],
        name="Risk Client = 1",
        marker_color=color_palette["nx3"],
        hovertemplate='Month: %{x}<br>Risk Client: 1<br>Count: %{y}<extra></extra>'
    ))

    # Add line for percentage of risk 1
    fig.add_trace(go.Scatter(
        x=months_str,
        y=grouped['risk_1_pct'],
        name="Risk Client = 1 (%)",
        mode='lines+markers',
        yaxis='y2',
        line=dict(color=color_palette["nx4"], width=3),
        marker=dict(size=10, color=color_palette["nx4"]),
        hovertemplate='Month: %{x}<br>Risk Client = 1 (%): %{y:.2f}%<extra></extra>'
    ))

    fig.update_layout(
        title=f"Risk Client Counts and Percentage by Month ({year if year not in (None, 'All') else 'All'})",
        xaxis=dict(title="Month"),
        yaxis=dict(title="Count"),
        yaxis2=dict(
            title="Risk Client Percentage (%)",
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        barmode='group',
        height=height,
        width=width,
        plot_bgcolor="#fafafa",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def get_account_age_plotly_figure_by_affiliation(csv_path, year_range=None, height=400, width=600):
    df = pd.read_csv(csv_path)

    # Ensure fecha_afiliacion exists and parse year
    if 'fecha_afiliacion' not in df.columns:
        raise ValueError("Column 'fecha_afiliacion' not found in data.")
    df['afiliacion_year'] = pd.to_datetime(df['fecha_afiliacion']).dt.year

    # Filter by year range if provided
    if year_range:
        df = df[(df['afiliacion_year'] >= year_range[0]) & (df['afiliacion_year'] <= year_range[1])]
    
    # Create a new column for account age in years
    if 'account_age_years' not in df.columns:
        if 'fecha_afiliacion' in df.columns:
            df['fecha_afiliacion'] = pd.to_datetime(df['fecha_afiliacion'], errors='coerce')
            df['account_age_years'] = (pd.Timestamp.now() - df['fecha_afiliacion']).dt.days / 365.25
        else:
            raise ValueError("Column 'account_age_years' or 'fecha_afiliacion' not found in data.")

    # Assume 'account_age_years' column exists
    if 'account_age_years' not in df.columns:
        raise ValueError("Column 'account_age_years' not found in data.")

    # Bin account ages
    bins = [0, 1, 3, np.inf]
    labels = ['< 1 year', '1-3 years', '> 3 years']
    df['age_group'] = pd.cut(df['account_age_years'], bins=bins, labels=labels, right=False)

    # Count unique accounts per group
    grouped = df.groupby('age_group')['external_account_id'].nunique().reset_index()
    grouped = grouped.rename(columns={'external_account_id': 'account_count'})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped['age_group'],
        y=grouped['account_count'],
        marker_color=color_palette["nx3"],
        name="Unique Accounts",
        hovertemplate='Age Group: %{x}<br>Unique Accounts: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title="Unique Accounts by Account Age Group (Filtered by Affiliation Year)",
        xaxis_title="Account Age",
        yaxis_title="Unique Accounts",
        height=height,
        width=width,
        plot_bgcolor="#fafafa"
    )

    return fig
