# Usual dash imports
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.exceptions import PreventUpdate

# Import app config 
from app import app
from apps.commonmodules import makeNavbar

# Homepage layout
def layout(user_role="public"):
    return html.Div(
        [
            makeNavbar(user_role=user_role),

            # Page Content
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H1(
                                        "Welcome, Vervan Consumer Goods Trading!",
                                        style={
                                            "fontWeight": "900",
                                            "fontSize": "3rem",
                                            "color": "#3d2f25",
                                            "marginTop": "50px",
                                            "marginBottom": "20px",
                                        },
                                    ),
                                    html.P(
                                        "This web-based information system will help you manage product inventory, supplier information, orders, and financial reports.",
                                        style={
                                            "color": "#977b61",
                                            "fontStyle": "italic",
                                            "fontSize": "1.1rem",
                                            "maxWidth": "600px",
                                        },
                                    ),
                                    html.P(
                                        "Log in using your account to acess your assigned dashboard!",
                                        style={
                                            "color": "#977b61",
                                            "fontStyle": "italic",
                                            "fontSize": "1.1rem",
                                            "marginBottom": "40px",
                                        },
                                    ),
                                    dbc.Button(
                                        "Log In",
                                        href = "/login",
                                        color = "secondary",
                                        style={
                                            "backgroundColor": "#7a5d60",
                                            "border": "none",
                                            "borderRadius": "25px",
                                            "fontWeight": "600",
                                            "padding": "10px 25px",
                                        },
                                    ),
                                ],
                                width = 7,
                            ),
                            dbc.Col(
                                html.Img(
                                    src="/assets/Vervan Logo Big.svg",
                                    style={
                                        "width": "300px",
                                        "height": "300px",
                                        "borderRadius": "50%",
                                        "backgroundColor": "#fffaf3",
                                        "objectFit": "contain",
                                        "padding": "20px",
                                    },
                                ),
                                style={
                                    "display": "flex",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "paddingLeft": "100px", 
                                },
                            ),
                        ],
                        align = "center",
                        className="mt-5",
                    ),
                ],
                style={
                    "backgroundColor": "#fffaf3",
                    "height": "100vh",
                    "padding": "50px 80px",
                    "fontFamily": "Arial, sans-serif",
                },
            ),
        ],
        style={"padding": "2rem"}  
    )
