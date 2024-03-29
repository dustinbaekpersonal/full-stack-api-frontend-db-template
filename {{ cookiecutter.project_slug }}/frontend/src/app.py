"""App for frontend using dash."""
import dash

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width,initial-scale=1,shrink-to-fit=no",
        }
    ],
)

app.title = "Inventory Management System"

app.config.suppress_callback_exceptions = True
