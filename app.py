import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

df = pd.read_csv("formatted_data.csv", parse_dates=["date"])
df = df.sort_values("date")

PRICE_INCREASE_DATE = "2021-01-15"

regions = ["north", "south", "east", "west", "all"]

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1(
            "Soul Foods – Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "color": "#2c3e50"},
        ),
        html.Div(
            [
                html.Label("Filter by Region:", style={"fontWeight": "bold", "marginRight": "8px"}),
                dcc.RadioItems(
                    id="region-filter",
                    options=[{"label": r.capitalize(), "value": r} for r in regions],
                    value="all",
                    inline=True,
                    inputStyle={"marginRight": "4px"},
                    labelStyle={"marginRight": "16px"},
                ),
            ],
            style={"margin": "16px 0"},
        ),
        dcc.Graph(id="sales-chart"),
    ],
)


from dash import Input, Output

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
        line=dict(color="#2980b9", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=after["date"], y=after["sales"],
        mode="lines", name="After price increase",
        line=dict(color="#e74c3c", width=2),
    ))

    fig.add_vline(
        x=PRICE_INCREASE_DATE,
        line_dash="dash", line_color="#7f8c8d",
        annotation_text="Price increase (15 Jan 2021)",
        annotation_position="top right",
    )

    fig.update_layout(
        title="Daily Pink Morsel Sales" + ("" if region == "all" else f" – {region.capitalize()} Region"),
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="white",
        hovermode="x unified",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
