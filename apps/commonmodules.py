import dash_bootstrap_components as dbc
from dash import html, dcc

def makeNavbar(user_role="public", pathname=None):
    # Determine active state for Inventory
    inventory_active = False
    if pathname:
        if pathname == "/inventory" or pathname.startswith("/inventory/"):
            inventory_active = True

    # Helper to check active state
    def is_active(href):
        return pathname == href

    # === Define nav items by role ===
    if user_role == "public":
        nav_items = [
            dbc.NavLink("Home", href="/home", active=is_active("/home"), className="nav-pill"),
            dbc.NavLink("Login", href="/login", active=is_active("/login"), className="nav-pill"),
        ]
    elif user_role == "owner":
        nav_items = [
            dbc.NavLink("Dashboard", href="/ownerdashboard", active=is_active("/ownerdashboard"), className="nav-pill"),
            dbc.NavLink("Reports", href="/reports", active=is_active("/reports"), className="nav-pill"),
            dbc.NavLink("Inventory", href="/inventory", active=inventory_active, className="nav-pill"),
            dbc.NavLink("Accounting", href="/accounting", active=is_active("/accounting"), className="nav-pill"),
            dbc.NavLink("Transactions", href="/transactions", active=is_active("/transactions"), className="nav-pill"),
            dbc.NavLink("Add User", href="/adduser", active=is_active("/adduser"), className="nav-pill"),
        ]
    elif user_role == "inventory":
        nav_items = [
            dbc.NavLink("Dashboard", href="/inventorydashboard", active=is_active("/inventorydashboard"), className="nav-pill"),
            dbc.NavLink("Inventory", href="/inventory", active=inventory_active, className="nav-pill"),
        ]
    elif user_role == "accounting":
        nav_items = [
            dbc.NavLink("Dashboard", href="/accountingdashboard", active=is_active("/accountingdashboard"), className="nav-pill"),
            dbc.NavLink("Accounting", href="/accounting", active=is_active("/accounting"), className="nav-pill"),
            dbc.NavLink("Transactions", href="/transactions", active=is_active("/transactions"), className="nav-pill"),
        ]
    else:
        nav_items = []

    # === Conditionally include logo and logout ===
    logo_element = None
    logout_btn = None
    logout_modal = None
    
    if user_role != "public":
        # Logout Button (triggers modal)
        logout_btn = dbc.Button("Logout", id="logout_btn", n_clicks=0, className="nav-pill me-3")
        
        # Logout Confirmation Modal
        logout_modal = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Confirm Logout")),
                dbc.ModalBody("Are you sure you want to log out?"),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancel", id="logout_cancel", className="ms-auto", n_clicks=0),
                        dbc.Button("Logout", id="logout_confirm", href="/login", className="ms-2", n_clicks=0, style={"backgroundColor": "#7a5d60", "border": "none"}),
                    ]
                ),
            ],
            id="logout_modal",
            is_open=False,
            centered=True,
        )
        
        # Determine dashboard link based on role
        dashboard_href = "/home"
        if user_role == "owner":
            dashboard_href = "/ownerdashboard"
        elif user_role == "inventory":
            dashboard_href = "/inventorydashboard"
        elif user_role == "accounting":
            dashboard_href = "/accountingdashboard"

        logo_element = html.Div(
            dcc.Link(
                html.Img(
                    src="/assets/Vervan Logo Small.svg",
                    height="90px",
                    style={
                        "display": "block",
                        "paddingTop": "5px",
                        "paddingBottom": "5px",
                        "cursor": "pointer",
                    },
                ),
                href=dashboard_href,
            ),
            style={"display": "flex", "alignItems": "center"},
        )

    # === Navbar layout ===
    navbar = dbc.Navbar(
        dbc.Container(
            [
                # Left side: navigation links
                dbc.Nav(nav_items, className="me-auto", navbar=True),

                # Right side: Logout + Logo
                html.Div(
                    [
                        logout_btn if logout_btn else None,
                        logo_element if logo_element else None,
                    ],
                    className="d-flex align-items-center",
                ),
            ],
            fluid=True,
        ),
        className="navbar-custom",
    )
    
    if logout_modal:
        return html.Div([navbar, logout_modal])
    else:
        return navbar

def create_pagination_controls(current_page, total_pages, id_prefix):
    return dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Previous", 
                    id=f"{id_prefix}-prev-btn", 
                    n_clicks=0, 
                    disabled=(current_page <= 1),
                    color="secondary",
                    outline=True,
                    className="me-2"
                ),
                width="auto"
            ),
            dbc.Col(
                html.Span(
                    f"Page {current_page} of {total_pages}", 
                    className="align-middle fw-bold",
                    style={"color": "#7a5d60"}
                ),
                width="auto",
                className="d-flex align-items-center"
            ),
            dbc.Col(
                dbc.Button(
                    "Next", 
                    id=f"{id_prefix}-next-btn", 
                    n_clicks=0, 
                    disabled=(current_page >= total_pages),
                    color="secondary",
                    outline=True,
                    className="ms-2"
                ),
                width="auto"
            ),
        ],
        className="mt-3 justify-content-center align-items-center"
    )
