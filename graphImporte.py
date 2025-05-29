import os
import pandas as pd
from bokeh.models import FactorRange, HoverTool, ColumnDataSource
from bokeh.palettes import Category10
from bokeh.plotting import figure

def get_importe_bokeh_figure(csv_path):
    aggregated_df = pd.read_csv(csv_path)

    # 1. Filter year 2024
    df_2024 = aggregated_df[aggregated_df['year'] == 2024].copy()

    # 2. Create labels like ("Q1", "1"), ("Q1", "2"), ...
    df_2024['quarter_label'] = 'Q' + df_2024['quarter'].astype(str)
    df_2024['month_str'] = df_2024['month'].astype(str)
    df_2024['x'] = list(zip(df_2024['quarter_label'], df_2024['month_str']))

    # 3. Group by (quarter, month) and sum importe
    monthly_group = df_2024.groupby('x')['total_importe'].sum().reset_index()
    monthly_group = monthly_group.sort_values('x')
    x_factors = list(monthly_group['x'])

    # 4. Group monthly and then average monthly by quarter
    monthly_by_q = df_2024.groupby(['quarter_label', 'month'])['total_importe'].sum().reset_index()
    quarterly_avg = monthly_by_q.groupby('quarter_label')['total_importe'].mean()

    # 5. Calculate centered positions for each quarter using month groups
    quarter_groups = {}
    for i, (q, m) in enumerate(x_factors):
        quarter_groups.setdefault(q, []).append(i)
    quarter_x_positions = {}
    for quarter, positions in quarter_groups.items():
        quarter_x_positions[quarter] = (min(positions) + max(positions)) / 2

    # 6. Prepare line coordinates
    quarters_sorted = ['Q1', 'Q2', 'Q3', 'Q4']
    x_quarter_coords = [quarter_x_positions[q] for q in quarters_sorted if q in quarter_x_positions and q in quarterly_avg]
    y_quarter_values = [quarterly_avg[q] for q in quarters_sorted if q in quarter_x_positions and q in quarterly_avg]

    # 7. Colors (usando Category10)
    fill_color, line_color = Category10[4][2], Category10[4][3]

    # 8. Create figure with hover tools
    bar_hover = HoverTool(tooltips=[
        ("Trimestre", "@quarter"),
        ("Mes", "@month_name (@month)"),
        ("Importe", "@top{0,0.00}")
    ], renderers=[])

    line_hover = HoverTool(tooltips=[
        ("Trimestre", "@quarter"),
        ("Promedio", "@y{0,0.00}")
    ], renderers=[])

    p = figure(x_range=FactorRange(*x_factors), height=500, tools=[bar_hover, line_hover],
               background_fill_color="#fafafa", toolbar_location=None,
               title="Total amount per month and monthly average per quarter (2024)")

    # 9. ColumnDataSource for bars with hover info
    bar_data = {
        'x': x_factors,
        'top': monthly_group['total_importe'],
        'quarter': [f[0] for f in x_factors],
        'month': [f[1] for f in x_factors],
        'month_name': [
            ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
             'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'][int(f[1])-1]
            for f in x_factors
        ]
    }
    source = ColumnDataSource(bar_data)

    bars = p.vbar(x='x', top='top', width=0.8, source=source,
           fill_color=fill_color, fill_alpha=0.8,
           line_color=line_color, line_width=1.2)
    bar_hover.renderers = [bars]

    # 10. Line for quarterly average
    quarter_coords = []
    for quarter in quarters_sorted:
        if quarter in quarterly_avg:
            quarter_factors = [f for f in x_factors if f[0] == quarter]
            if quarter_factors:
                middle_idx = len(quarter_factors) // 2
                quarter_coords.append(quarter_factors[middle_idx])

    line_data = {
        'x': quarter_coords,
        'y': y_quarter_values,
        'quarter': quarters_sorted[:len(y_quarter_values)]
    }
    line_source = ColumnDataSource(line_data)

    line_renderer = p.line(x='x', y='y', source=line_source, color=line_color, line_width=3)
    scatter_renderer = p.scatter(x='x', y='y', source=line_source, size=10,
              line_color=line_color, fill_color="white", line_width=3)
    line_hover.renderers = [line_renderer, scatter_renderer]

    # 11. Final aesthetics
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    return p