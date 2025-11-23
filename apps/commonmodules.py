import dash_bootstrap_components as dbc
from dash import html, dcc

def makeNavbar(user_role="public"):
    # === Define nav items by role ===
    if user_role == "public":
        nav_items = [
            dbc.NavLink("Home", href="/home", active="exact", className="nav-pill"),
            dbc.NavLink("Login", href="/login", active="exact", className="nav-pill"),
        ]
    elif user_role == "owner":
        nav_items = [
            dbc.NavLink("Dashboard", href="/ownerdashboard", active="exact", className="nav-pill"),
            dbc.NavLink("Reports", href="/reports", active="exact", className="nav-pill"),
            dbc.NavLink("Inventory", href="/inventory", active="exact", className="nav-pill"),
            dbc.NavLink("Accounting", href="/accounting", active="exact", className="nav-pill"),
            dbc.NavLink("Transactions", href="/transactions", active="exact", className="nav-pill"),
            dbc.NavLink("Add User", href="/adduser", active="exact", className="nav-pill"),
        ]
    elif user_role == "inventory":
        nav_items = [
            dbc.NavLink("Dashboard", href="/inventorydashboard", active="exact", className="nav-pill"),
            dbc.NavLink("Inventory", href="/inventory", active="exact", className="nav-pill"),
        ]
    elif user_role == "accounting":
        nav_items = [
            dbc.NavLink("Dashboard", href="/accountingdashboard", active="exact", className="nav-pill"),
            dbc.NavLink("Accounting", href="/accounting", active="exact", className="nav-pill"),
            dbc.NavLink("Transactions", href="/transactions", active="exact", className="nav-pill"),
        ]
    else:
        nav_items = []

    # === Conditionally include logo ===
    logo_element = None
    logout_btn = None
    if user_role != "public":
        logout_btn = dbc.Button("Logout", href="/home", className="nav-pill me-3")
        
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
                href="/ownerdashboard",
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

    return navbar
