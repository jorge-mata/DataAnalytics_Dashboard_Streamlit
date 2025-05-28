import pandas as pd
import calendar
from bokeh.models import ColumnDataSource, HoverTool, LinearAxis, Range1d
from bokeh.plotting import figure
from bokeh.transform import dodge

def get_risk_bokeh_figure(csv_path="aggregated_df.csv"):
    aggregated_df = pd.read_csv(csv_path)

    grouped = aggregated_df.groupby(['month', 'riskclient']).size().unstack(fill_value=0).reset_index()
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
    y_max = grouped[['risk_0', 'risk_1']].values.max() * 1.1

    p = figure(x_range=months_str, y_range=(0, y_max),
               title="Risk Client Counts and Percentage by Month (2024)",
               height=400, width=800, toolbar_location="above",
               tools=["pan", "wheel_zoom", "box_zoom", "reset"])

    bar_0 = p.vbar(x=dodge('months', -0.2, range=p.x_range), top='risk_0', source=source,
                   width=0.35, color="#718dbf", legend_label="Risk Client = 0",
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
                   width=0.35, color="#e84d60", legend_label="Risk Client = 1",
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
    line = p.line('months', 'risk_1_pct', source=source, line_width=3, color='#2ca02c',
                  y_range_name="percent", legend_label="Risk Client = 1 (%)",
                  name="percentage_line")
    circles = p.circle('months', 'risk_1_pct', source=source, size=10, color='#2ca02c',
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
