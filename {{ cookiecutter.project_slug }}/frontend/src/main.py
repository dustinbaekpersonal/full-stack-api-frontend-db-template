"""Main script."""
from dash import dcc, html

from src import submit_stock_level, view_stock_level
from src.app import app

app.layout = html.Div(
    children=[
        html.Div(
            [
                html.Div(
                    children=[
                        html.H1(children="Inventory Management System"),
                        html.H4(children="""Find, Report, Update, Delete Inventories"""),
                        html.Div(id="dummy", children=None),
                        html.Br(),
                        dcc.Tabs(
                            [
                                submit_stock_level.layout,
                                view_stock_level.layout,
                            ]
                        ),
                        html.Div(style={"height": "50%"}),
                    ],
                    className="col-12",
                )
            ],
            className="row justify-content-md-center",
        ),
    ],
    className="container",
)


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
