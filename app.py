import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

df = pd.read_csv("formatted_data.csv", parse_dates=["date"])
df = df.sort_values("date")

PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

REGIONS = ["north", "south", "east", "west", "all"]

app = Dash(__name__)

app.layout = html.Div(
    id="page-wrapper",
    children=[
        html.Div(
            id="app-header",
            children=[
                html.H1("Soul Foods – Pink Morsel Sales Visualiser"),
                html.P("Daily sales revenue, split by the 15 Jan 2021 price increase"),
            ],
        ),
        html.Div(
            className="card",
            id="filter-card",
            children=[
                html.Span("Filter by region", id="filter-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": r.capitalize(), "value": r} for r in REGIONS],
                    value="all",
                    inline=True,
                    inputStyle={"display": "none"},
                ),
            ],
        ),
        html.Div(
            className="card",
            id="chart-card",
            children=[dcc.Graph(id="sales-chart", config={"displayModeBar": False})],
        ),
    ],
)


@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    daily = filtered.groupby("date", as_index=False)["sales"].sum()

    before = daily[daily["date"] < PRICE_INCREASE_DATE]
    after = daily[daily["date"] >= PRICE_INCREASE_DATE]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=before["date"], y=before["sales"],
        mode="lines", name="Before price increase",
        line=dict(color="#ad1457", width=2.5),
        fill="tozeroy", fillcolor="rgba(173,20,87,0.07)",
    ))
    fig.add_trace(go.Scatter(
        x=after["date"], y=after["sales"],
        mode="lines", name="After price increase",
        line=dict(color="#6a1b9a", width=2.5),
        fill="tozeroy", fillcolor="rgba(106,27,154,0.07)",
    ))

    fig.add_vline(
        x=PRICE_INCREASE_DATE.timestamp() * 1000,
        line_dash="dot",
        line_color="#78586f",
        line_width=1.5,
        annotation_text="Price increase – 15 Jan 2021",
        annotation_position="top right",
        annotation_font=dict(color="#6a1b9a", size=12),
    )

    region_label = "All Regions" if region == "all" else region.capitalize() + " Region"
    fig.update_layout(
        title=dict(
            text=f"Daily Pink Morsel Sales – {region_label}",
            font=dict(size=17, color="#37003c", family="Segoe UI, Arial, sans-serif"),
            x=0.01,
        ),
        xaxis=dict(title="Date", showgrid=True, gridcolor="#f3e5f5", tickfont=dict(size=11)),
        yaxis=dict(title="Total Sales ($)", showgrid=True, gridcolor="#f3e5f5", tickfont=dict(size=11)),
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1,
                    font=dict(size=12)),
        plot_bgcolor="#fff",
        paper_bgcolor="#fff",
        hovermode="x unified",
        margin=dict(l=60, r=20, t=60, b=50),
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
