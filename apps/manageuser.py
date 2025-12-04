import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB

# === Fetch users from DB ===
def fetch_users():
    sql = """
        SELECT staff_id, staff_name, staff_username, staff_role
        FROM staff
        WHERE staff_delete_ind = FALSE
        ORDER BY staff_name;
    """
    colnames = ["staff_id", "staff_name", "staff_username", "staff_role"]
    df = getDataFromDB(sql, [], colnames)
    return df

# =====================================
#            PAGE LAYOUT
# =====================================
def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),

            # === TOP TAB PILL ===
            dbc.Row(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Manage Staff",
                            href="/users",
                            id="staff-tab",
                            className="tab-pill-left active-tab",
                        ),
                        dbc.Button(
                            "Manage Users",
                            href="/users/manage",
                            id="manage-users-tab",
                            className="tab-pill-right",
                        ),
                    ],
                    className="tab-pill-group",
                ),
                className="mb-4 justify-content-start",
            ),

            # === MAIN CARD ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Header Row ---
                        dbc.Row(
                            [
                                dbc.Col(html.H2("Manage Users", className="m-0"), width="auto"),
                                dbc.Col(
                                    dbc.Button(
                                        "Add User",
                                        href="/users/add",
                                        id="add-user-btn",
                                        className="add-edit-btn",
                                    ),
                                    width="auto",
                                    className="ms-auto text-end",
                                ),
                            ],
                            align="center",
                            className="mb-4",
                        ),

                        # --- Search Input ---
                        html.Div(
                            [
                                html.Label("Search User", className="mb-2 search-label"),
                                dbc.Input(
                                    id="user-search-input",
                                    type="text",
                                    placeholder="Enter name or username...",
                                    className="supplier-search-input mb-4",
                                ),
                            ],
                            className="search-container",
                        ),

                        # --- Table Container ---
                        html.Div(id="users-table-container"),
                    ]
                ),
                className="inventory-card",
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )


# =====================================
#        CALLBACK: UPDATE TABLE
# =====================================
@app.callback(
    Output("users-table-container", "children"),
    Input("user-search-input", "value")
)
def update_users_table(search_value):
    df_users = fetch_users()

    # Filter by search input
    if search_value:
        search = search_value.lower()
        df_users = df_users[
            df_users["staff_name"].str.lower().str.contains(search) |
            df_users["staff_username"].str.lower().str.contains(search)
        ]

    # No results
    if df_users.empty:
        return dbc.Alert("No users found.", color="warning")

    # Build table rows
    table_rows = []
    for _, row in df_users.iterrows():
        table_rows.append(
            html.Tr(
                [
                    html.Td(row["staff_name"]),
                    html.Td(row["staff_username"]),
                    html.Td(row["staff_role"]),
                    html.Td(
                        dbc.Button(
                            "Edit",
                            href=f"/users/edit?id={row['staff_id']}",
                            color="secondary",
                            size="sm",
                            style={
                                "backgroundColor": "#977b61",
                                "color": "#fffaf3",
                                "border": "none",
                                "borderRadius": "999px",
                                "padding": "6px 18px",
                                "fontWeight": "500",
                                "transition": "all 0.2s ease-in-out",
                            },
                        )
                    ),
                ]
            )
        )

    # Render table
    return dbc.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Name"),
                    html.Th("Username"),
                    html.Th("Role"),
                    html.Th("Action"),
                ])
            ),
            html.Tbody(table_rows),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        style={
            "borderCollapse": "separate",
            "borderSpacing": "0",
            "borderRadius": "1rem",
            "overflow": "hidden",
            "backgroundColor": "#faf3e7",
        }
    )
