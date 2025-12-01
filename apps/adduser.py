import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from apps.commonmodules import makeNavbar
from app import app
from apps.dbconnect import modifyDB, getDataFromDB, hash_string

# Coloring
bg_color = "#1e0f00"
card_color = "#faf3e7"
accent_color = "#7a5d60"
text_color = "#c69a9a"

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
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
                            id="add_user_name",
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
                            id="add_user_username",
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
                                            id="add_user_password",
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
                                            id="add_user_confirmpass",
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
                            id="add_user_role",
                            options=[
                                {"label": "Inventory Staff", "value": "inventory"},
                                {"label": "Accounting Staff", "value": "accounting"},
                                {"label": "Owner", "value": "owner"},
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
                            id="add_user_submit_btn",
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
                        html.Div(id="add_user_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("New user added successfully."),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", 
                            id="add_user_success_close",
                            className="ms-auto", 
                            n_clicks=0,
                            style={
                                "backgroundColor": accent_color,
                                "color": "#fff",
                                "border": "none",
                                "borderRadius": "30px",
                                "padding": "10px 30px",
                                "fontWeight": "600",
                            }
                        )
                    ),
                ],
                id="add_user_success_modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )

@app.callback(
    [Output('add_user_success_modal', 'is_open'),
     Output('add_user_feedback', 'children')],
    [Input('add_user_submit_btn', 'n_clicks'),
     Input('add_user_success_close', 'n_clicks')],
    [State('add_user_name', 'value'),
     State('add_user_username', 'value'),
     State('add_user_password', 'value'),
     State('add_user_confirmpass', 'value'),
     State('add_user_role', 'value'),
     State('add_user_success_modal', 'is_open')]
)
def add_new_user(submit_clicks, close_clicks, name, username, password, confirmpass, role, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
        
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'add_user_success_close':
        return False, ""

    if trigger_id == 'add_user_submit_btn':
        if not submit_clicks:
            raise PreventUpdate
            
        # Validation
        if not all([name, username, password, confirmpass, role]):
            return False, dbc.Alert("Please fill in all fields.", color="danger")
        
        if password != confirmpass:
            return False, dbc.Alert("Passwords do not match.", color="danger")
            
        # Check if username exists
        sql_check = "SELECT staff_id FROM staff WHERE staff_username = %s AND staff_delete_ind = FALSE"
        df_check = getDataFromDB(sql_check, [username], ["staff_id"])
        if not df_check.empty:
            return False, dbc.Alert("Username already exists.", color="danger")
            
        try:
            # Hash Password
            hashed_password = hash_string(password)
            
            # Insert User
            sql_insert = """
                INSERT INTO staff (staff_username, staff_name, staff_password, staff_role, staff_delete_ind)
                VALUES (%s, %s, %s, %s, FALSE)
            """
            modifyDB(sql_insert, [username, name, hashed_password, role])
            
            return True, ""
            
        except Exception as e:
            return False, dbc.Alert(f"Error adding user: {str(e)}", color="danger")
            
    return is_open, ""
