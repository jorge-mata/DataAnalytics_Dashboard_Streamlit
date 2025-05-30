import os
import pandas as pd
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

def get_importe_plotly_figure(csv_path, year="All", height=500, width=900):
    aggregated_df = pd.read_csv(csv_path)

    # Filter by year if not "All"
    if year != "All":
        aggregated_df = aggregated_df[aggregated_df['year'] == int(year)].copy()

    # If no data for selected year, return empty plot
    if aggregated_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title=f"No data for year {year}",
            height=height,
            width=width
        )
        return fig

    # Prepare labels and groupings
    aggregated_df['quarter_label'] = 'Q' + aggregated_df['quarter'].astype(str)
    aggregated_df['month_str'] = aggregated_df['month'].astype(str)
    aggregated_df['x'] = aggregated_df['quarter_label'] + '-' + aggregated_df['month_str']

    # Group by (quarter, month) and sum importe
    monthly_group = aggregated_df.groupby(['quarter_label', 'month']).agg({
        'total_importe': 'sum'
    }).reset_index()
    monthly_group['x'] = monthly_group['quarter_label'] + '-' + monthly_group['month'].astype(str)
    monthly_group = monthly_group.sort_values(['quarter_label', 'month'])

    # Group monthly and then average monthly by quarter
    quarterly_avg = monthly_group.groupby('quarter_label')['total_importe'].mean().reset_index()

    # Bar chart for monthly totals
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=monthly_group['x'],
        y=monthly_group['total_importe'],
        name='Importe mensual',
        marker_color=color_palette["nx3"],
        hovertemplate='Trimestre: %{x}<br>Importe: %{y:,.2f}<extra></extra>'
    ))

    # Line for quarterly average
    # Place the line in the middle of each quarter group
    quarter_positions = []
    for q in quarterly_avg['quarter_label']:
        quarter_months = monthly_group[monthly_group['quarter_label'] == q]['x']
        if not quarter_months.empty:
            idx = len(quarter_months) // 2
            quarter_positions.append(quarter_months.iloc[idx])
        else:
            quarter_positions.append(q + '-2')  # fallback

    fig.add_trace(go.Scatter(
        x=quarter_positions,
        y=quarterly_avg['total_importe'],
        mode='lines+markers',
        name='Promedio mensual por trimestre',
        line=dict(color=color_palette["nx2"], width=3),
        marker=dict(size=10, color=color_palette["nx5"], line=dict(width=2, color=color_palette["nx2"])),
        hovertemplate='Trimestre: %{x}<br>Promedio: %{y:,.2f}<extra></extra>'
    ))

    fig.update_layout(
        title=f"Importe total por mes y promedio mensual por trimestre ({year})" if year != "All" else "Importe total por mes y promedio mensual por trimestre (Todos los años)",
        xaxis_title="Trimestre-Mes",
        yaxis_title="Importe total",
        barmode='group',
        height=height,
        width=width,
        plot_bgcolor="#fafafa",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig