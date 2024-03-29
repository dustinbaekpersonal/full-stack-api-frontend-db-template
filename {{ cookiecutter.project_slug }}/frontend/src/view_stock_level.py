"""View stock level."""
import pandas as pd
import plotly.express as px
import requests
from dash import dcc, html
from dash.dependencies import Input, Output
from loguru import logger

from src.app import app

config = {
    "products": ["milk", "bread", "fruit"],
    "stores": [
        "Waitrose",
        "Sainsbury's",
        "Aldi",
    ],
}

colors = {"background": "#111111", "text": "#7FDBFF"}

layout = dcc.Tab(
    label="View local stock levels",
    children=[
        html.Br(),
        html.H2("View local stock levels"),
        html.Label("Store name"),
        dcc.Dropdown(
            id="store_name_dropdown",
            options=[{"label": p.title(), "value": p} for p in config["stores"]],
            value=config["stores"][0],
            searchable=False,
        ),
        html.Br(),
        html.Div(
            [dcc.Graph(id="bar_chart")],
        ),
    ],
)


@app.callback(
    Output("bar_chart", "figure"),
    [
        Input("store_name_dropdown", "value"),
    ],
)
def draw_graph(store_name: str) -> px.bar:
    """Draw a bar chart of the stock level of all products in given store.

    Parameters
    ----------
    store_name : str
        store name

    Returns:
    -------
    Plotly Figure
        bar chart of the stock level of a product in each store

    Raises:
    ------
    PreventUpdate
        When the API call fails
    """
    url = f"http://backend:8000/inventory/{store_name}"
    logger.info(f"Calling {url} with store name ={store_name}")
    response = requests.get(url)
    if response.status_code == 200:
        data_df = pd.DataFrame(response.json())
        data_df = data_df[["product_name", "stock_level"]].set_index("product_name")
        fig = px.bar(
            data_df,
            x=data_df.index,
            y="stock_level",
            title=f"Stock Level of {store_name.title()} by product",
            labels={"stock_level": "Stock Level", "index": "Product"},
        )
        return fig
    else:
        logger.error(f"Error calling {url}: {response.status_code} {response.text}")
        df = pd.DataFrame({})
        fig = px.bar(
            df,
            title=f"Stock Level of {store_name.title()} by product",
            labels={"stock_level": "Stock Level", "index": "Product"},
        )
        return fig
