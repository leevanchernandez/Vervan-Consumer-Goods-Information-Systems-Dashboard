import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

from app import app
from apps.commonmodules import makeNavbar
from dash.dependencies import Input, Output

# [todo] ownerName is Vanessa for now, should be dynamic based on login
ownerName = "Vanessa"


layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),
        # Greeting
        html.H1(f"Hello, {ownerName}!", style={"color": "#7a5d60", "font-weight":"bold"}),
        html.H6(
            "This is what's happening in your store this month.",
            style={"color": "#7a5d60"},
        ),
        
        # Dashboard Cards
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Total Sales", style={"text-align": "center"}),
                                html.H1("₱60,245.00", style={"text-align": "center"}),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "height": "100%",  # ensures flex takes full card height
                            },
                        ),
                        style={
                            "background-color": "#564e6d",
                            "color": "#fffaf3",
                            "border-radius": "2rem",
                            "min-height": "180px",
                        },
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Total Revenue", style={"text-align": "center"}),
                                html.H1("₱12,365.00", style={"text-align": "center"}),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "height": "100%",
                            },
                        ),
                        style={
                            "background-color": "#c69a9a",
                            "color": "#fffaf3",
                            "border-radius": "2rem",
                            "min-height": "180px",
                        },
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Total Orders", style={"text-align": "center"}),
                                html.H1("52", style={"text-align": "center"}),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "height": "100%",
                            },
                        ),
                        style={
                            "background-color": "#977b61",
                            "color": "#fffaf3",
                            "border-radius": "2rem",
                            "min-height": "180px",
                        },
                    ),
                    width=4,
                ),
            ],
            className="mt-4",
        ),
    ],
    fluid=True,
    style={"padding": "2rem"},
)

