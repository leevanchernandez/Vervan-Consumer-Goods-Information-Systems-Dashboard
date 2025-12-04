import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from apps.commonmodules import makeNavbar
from app import app
from apps.dbconnect import modifyDB, getDataFromDB, hash_string
from urllib.parse import parse_qs, urlparse

# Coloring
bg_color = "#1e0f00"
card_color = "#faf3e7"
accent_color = "#7a5d60"
text_color = "#c69a9a"

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
            
            # Store for keeping track of the user ID being edited and original password hash
            dcc.Store(id='edit_user_id_store'),
            dcc.Store(id='original_password_hash_store'),
            html.H1(
                "Edit User",
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
                            id="edit_user_name",
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
                            id="edit_user_username",
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
                                            "Password (Leave blank to keep unchanged)",
                                            style={
                                                "fontWeight": "600",
                                                "fontSize": "1.1rem",
                                            },
                                        ),
                                        dbc.Input(
                                            id="edit_user_password",
                                            type="password",
                                            placeholder="Enter new password",
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
                                            id="edit_user_confirmpass",
                                            type="password",
                                            placeholder="Confirm new password",
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
                            id="edit_user_role",
                            options=[], # Populated by callback
                            style={
                                "borderRadius": "30px",
                                "padding": "14px 24px",
                                "marginBottom": "25px",
                                "backgroundColor": "white",
                                "fontSize": "1rem",
                            },
                        ),
                        
                        dbc.Checkbox(
                            id="edit_user_delete",
                            label="Delete User",
                            style={"marginBottom": "25px"},
                        ),

                        dbc.Button(
                            "Update",
                            id="edit_user_submit_btn",
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
                        html.Div(id="edit_user_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("User updated successfully.", id="edit_user_success_body"),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", 
                            id="edit_user_success_close",
                            href="/users", # Redirect to list on close
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
                id="edit_user_success_modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )

# === Callback to populate form ===
@app.callback(
    [Output("edit_user_name", "value"),
     Output("edit_user_username", "value"),
     Output("edit_user_role", "value"),
     Output("edit_user_role", "options"),
     Output("edit_user_id_store", "data"),
     Output("original_password_hash_store", "data")],
    [Input("url", "search")]
)
def populate_user_form(search):
    if not search:
        raise PreventUpdate
    
    parsed = parse_qs(search.lstrip("?"))
    user_id = parsed.get("id", [None])[0]
    
    if not user_id:
        raise PreventUpdate

    # Fetch user details
    sql_user = """
        SELECT staff_name, staff_username, staff_password, staff_role
        FROM staff
        WHERE staff_id = %s
          AND staff_delete_ind = FALSE;
    """
    df_user = getDataFromDB(sql_user, [user_id], ["staff_name", "staff_username", "staff_password", "staff_role"])
    
    if df_user.empty:
        return "", "", "", [], None, None

    user = df_user.iloc[0]
    
    # Fetch roles
    sql_roles = "SELECT DISTINCT staff_role FROM staff ORDER BY staff_role;"
    df_roles = getDataFromDB(sql_roles, [], ["staff_role"])
    role_options = [{"label": role, "value": role} for role in df_roles["staff_role"]]
    
    # Ensure current role is in options if not present (though it should be)
    if user["staff_role"] not in df_roles["staff_role"].values:
        role_options.append({"label": user["staff_role"], "value": user["staff_role"]})

    return user["staff_name"], user["staff_username"], user["staff_role"], role_options, user_id, user["staff_password"]


# === Callback to handle update ===
@app.callback(
    [Output('edit_user_success_modal', 'is_open'),
     Output('edit_user_success_body', 'children'),
     Output('edit_user_feedback', 'children')],
    [Input('edit_user_submit_btn', 'n_clicks'),
     Input('edit_user_success_close', 'n_clicks')],
    [State('edit_user_name', 'value'),
     State('edit_user_username', 'value'),
     State('edit_user_password', 'value'),
     State('edit_user_confirmpass', 'value'),
     State('edit_user_role', 'value'),
     State('edit_user_delete', 'value'),
     State('edit_user_id_store', 'data'),
     State('original_password_hash_store', 'data'),
     State('edit_user_success_modal', 'is_open')]
)
def update_user(submit_clicks, close_clicks, name, username, password, confirmpass, role, delete_ind, user_id, original_hash, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
        
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'edit_user_success_close':
        return False, "User updated successfully.", ""

    if trigger_id == 'edit_user_submit_btn':
        if not submit_clicks or not user_id:
            raise PreventUpdate
            
        try:
            # Handle Delete
            if delete_ind:
                sql_delete = "UPDATE staff SET staff_delete_ind = TRUE WHERE staff_id = %s;"
                modifyDB(sql_delete, [user_id])
                return True, "User deleted successfully.", ""

            # Validation
            if not all([name, username, role]):
                return False, "", dbc.Alert("Please fill in all required fields.", color="danger")
            
            # Password Logic
            final_password = original_hash
            if password:
                if password != confirmpass:
                    return False, "", dbc.Alert("Passwords do not match.", color="danger")
                final_password = hash_string(password)
            
            # Check username uniqueness (exclude current user)
            sql_check = "SELECT staff_id FROM staff WHERE staff_username = %s AND staff_id != %s AND staff_delete_ind = FALSE"
            df_check = getDataFromDB(sql_check, [username, user_id], ["staff_id"])
            if not df_check.empty:
                return False, "", dbc.Alert("Username already exists.", color="danger")

            # Update User
            sql_update = """
                UPDATE staff
                SET 
                    staff_name = %s,
                    staff_username = %s,
                    staff_password = %s,
                    staff_role = %s
                WHERE staff_id = %s;
            """
            modifyDB(sql_update, [name, username, final_password, role, user_id])
            
            return True, "User updated successfully.", ""
            
        except Exception as e:
            return False, "", dbc.Alert(f"Error updating user: {str(e)}", color="danger")
            
    return is_open, "User updated successfully.", ""
