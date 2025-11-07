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
        makeNavbar(user_role="inventory"),
        # Greeting
        html.H1(
            f"Hello, {ownerName}!",
            style={"color": "#7a5d60", "font-weight": "bold"}
        ),
        html.H6(
            "Here are the recent product updates.",
            style={"color": "#7a5d60"},
        ),

        # Dashboard Cards
        dbc.Row(
            [
                # Left Card (Table)
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Inventory Summary", className="card-title mb-3"),
                                dbc.Table(
                                    # Placeholder data: 3 columns, 5 rows
                                    [
                                        html.Thead(
                                            html.Tr(
                                                [
                                                    html.Th("Product"),
                                                    html.Th("Stock"),
                                                    html.Th("Status"),
                                                ]
                                            )
                                        ),
                                        html.Tbody(
                                            [
                                                html.Tr(
                                                    [html.Td(f"Item {i+1}"), html.Td("50"), html.Td("Normal")]
                                                )
                                                for i in range(5)
                                            ]
                                        ),
                                    ],
                                    bordered=True,
                                    striped=True,
                                    hover=True,
                                    responsive=True,
                                    style={"background-color": "#fffaf3", "color": "#3d2f25"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "center",
                                "height": "100%",
                            },
                        ),
                        style={
                            "background-color": "#3d2f25",
                            "color": "#fffaf3",
                            "border-radius": "2rem",
                            "min-height": "180px",
                            "padding": "1rem",
                        },
                    ),
                    width=9,
                ),

                # Right Card (Low Stock Alert)
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Low Stock Alert!", className="card-title mb-3"),
                                html.Ul(
                                    [
                                        html.Li("*Item A (placeholder)"),
                                        html.Li("*Item B (placeholder)"),
                                        html.Li("*Item C (placeholder)"),
                                    ],
                                    style={"margin-left": "1rem"},
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flex-direction": "column",
                                "justify-content": "flex-start",
                                "height": "100%",
                            },
                        ),
                        style={
                            "background-color": "#564e6d",
                            "color": "#fffaf3",
                            "border-radius": "2rem",
                            "min-height": "180px",
                            "padding": "1rem",
                        },
                    ),
                    width=3,
                ),
            ],
            className="mt-4",
        ),
    ],
    style={"padding": "2rem"},
)
