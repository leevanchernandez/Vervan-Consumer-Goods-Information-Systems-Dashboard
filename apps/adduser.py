import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.exceptions import PreventUpdate
from apps.commonmodules import makeNavbar
from app import app

# Coloring
bg_color = "#1e0f00"
card_color = "#faf3e7"
accent_color = "#7a5d60"
text_color = "#c69a9a"

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),
            html.H1(
                "Add User",
                style={
                    "color": text_color,
                    "fontWeight": "800",
                    "textAlign": "center",
                    "marginBottom": "30px",
                    "fontSize": "2.5rem",
                },
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Label(
                            "Name",
                            style={
                                "fontWeight": "600",
                                "fontSize": "1.1rem",
                            },
                        ),
                        dbc.Input(
                            type="text",
                            placeholder="ex. Juan Dela Cruz",
                            style={
                                "borderRadius": "30px",
                                "padding": "14px 24px",
                                "marginBottom": "25px",
                                "backgroundColor": "white",
                                "fontSize": "1rem",
                            },
                        ),

                        dbc.Label(
                            "Username",
                            style={
                                "fontWeight": "600",
                                "fontSize": "1.1rem",
                            },
                        ),
                        dbc.Input(
                            type="text",
                            placeholder="ex. vervan1223",
                            style={
                                "borderRadius": "30px",
                                "padding": "14px 24px",
                                "marginBottom": "25px",
                                "backgroundColor": "white",
                                "fontSize": "1rem",
                            },
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Password",
                                            style={
                                                "fontWeight": "600",
                                                "fontSize": "1.1rem",
                                            },
                                        ),
                                        dbc.Input(
                                            type="password",
                                            placeholder="ex. 12345678",
                                            style={
                                                "borderRadius": "30px",
                                                "padding": "14px 24px",
                                                "marginBottom": "25px",
                                                "backgroundColor": "white",
                                                "fontSize": "1rem",
                                            },
                                        ),
                                    ],
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Confirm Password",
                                            style={
                                                "fontWeight": "600",
                                                "fontSize": "1.1rem",
                                            },
                                        ),
                                        dbc.Input(
                                            type="password",
                                            placeholder="ex. 12345678",
                                            style={
                                                "borderRadius": "30px",
                                                "padding": "14px 24px",
                                                "marginBottom": "25px",
                                                "backgroundColor": "white",
                                                "fontSize": "1rem",
                                            },
                                        ),
                                    ],
                                ),
                            ],
                        ),

                        dbc.Label(
                            "Role",
                            style={
                                "fontWeight": "600",
                                "fontSize": "1.1rem",
                            },
                        ),
                        dbc.Select(
                            options=[
                                {"label": "Inventory Staff", "value": "inventory"},
                                {"label": "Accounting Staff", "value": "Accounting Staff"},
                                {"label": "Owner", "value": "Owner"},
                            ],
                            style={
                                "borderRadius": "30px",
                                "padding": "14px 24px",
                                "marginBottom": "25px",
                                "backgroundColor": "white",
                                "fontSize": "1rem",
                            },
                        ),

                        dbc.Button(
                            "Submit",
                            href="/ownerdashboard",
                            id="signup-button",
                            n_clicks=0,
                            style={
                                "backgroundColor": accent_color,
                                "border": "none",
                                "borderRadius": "30px",
                                "padding": "14px 0",
                                "fontWeight": "600",
                                "fontSize": "1.1rem",
                                "width": "100%",
                                "boxShadow": "0px 3px 8px rgba(0, 0, 0, 0.2)",
                            },
                        ),
                    ]
                ),
                className="supplier-details-card",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )
