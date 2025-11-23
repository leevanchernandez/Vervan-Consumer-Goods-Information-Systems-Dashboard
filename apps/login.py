import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB

# Coloring
bg_color = "#1e0f00",
card_color = "#faf3e7",
accent_color = "#7a5d60",
text_color = "#c69a9a"

layout = html.Div(
    [
        # Navbar
        makeNavbar(user_role="public"),

        # Main Container
        dbc.Container(
            [
                dcc.Location(id='url_login', refresh=True),
                html.H1(
                    "Good to see you again!",
                    style={
                        "color": text_color,
                        "fontWeight": "800",
                        "textAlign": "center",
                        "marginBottom": "30px",
                        "fontSize": "2.5rem",
                    },
                ),
                # Login Card
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Alert(id='login_alert', is_open=False, color="danger"),
                            dbc.Label(
                                "Enter your username:",
                                style={
                                    "fontWeight": "600",
                                    "fontSize": "1.1rem",
                                },
                            ),
                            dbc.Input(
                                id="login_username",
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

                            dbc.Label(
                                "Enter your password:",
                                style={
                                    "fontWeight": "600",
                                    "fontSize": "1.1rem",
                                },
                            ),
                            dbc.Input(
                                id="login_password",
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
                            dbc.Button(
                                "Log In",
                                # href = "/ownerdashboard",
                                color="secondary",
                                id="login-button",
                                n_clicks = 0,
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
                    style={
                        "backgroundColor": card_color,
                        "borderRadius": "40px",
                        "padding": "50px 60px",
                        "width": "600px",
                        "maxWidth": "90vw",
                        "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.15)",
                    },
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "justifyContent": "center",
                "height": "90vh",
            },
        ),
    ],
    style={
        "backgroundColor": bg_color,
        "padding": "2rem",
    },
)

@app.callback(
    [
        Output('url_login', 'pathname'),
        Output('login_alert', 'is_open'),
        Output('login_alert', 'children')
    ],
    [
        Input('login-button', 'n_clicks')
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value')
    ]
)
def login_process(n_clicks, username, password):
    if n_clicks > 0:
        if username is None or password is None or username == "" or password == "":
            return [dash.no_update, True, "Please enter both username and password."]
        
        sql = """
            SELECT staff_id, staff_name, staff_username, staff_password, staff_role
            FROM staff
            WHERE staff_username = %s AND staff_delete_ind = FALSE
        """

        df = getDataFromDB(sql, (username,), ["staff_id", "staff_name", "staff_username", "staff_password", "staff_role"])
        
        if not df.empty:
            stored_password = df.iloc[0]['staff_password']
            
            if stored_password == password:
                # For now, we redirect to ownerdashboard as per the original href
                return ["/ownerdashboard", False, ""]
            else:
                return [dash.no_update, True, "Incorrect password."]
        else:
            return [dash.no_update, True, "User not found."]
            
    raise PreventUpdate
