import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),
            # === TOP TAB PILL ===
            dbc.Row(
                dbc.ButtonGroup(
                    [
                        dbc.Button(
                            "Suppliers Tab",
                            href="/inventory",
                            id="suppliers-tab",
                            className="tab-pill-left active-tab",
                        ),
                        dbc.Button(
                            "Products Tab",
                            href="/inventory/products",
                            id="products-tab",
                            className="tab-pill-right",
                        ),
                    ],
                    className="tab-pill-group",
                ),
                className="mb-3 justify-content-start",
            ),

            # === MAIN CARD ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Header Row ---
                        dbc.Row(
                            [
                                dbc.Col(html.H2("Manage Suppliers", className="m-0"), width="auto"),
                                dbc.Col(
                                    dbc.Button(
                                        "Add Supplier Details",
                                        href="/inventory/supplier",
                                        id="add-edit-btn",
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
                                html.Label("Search Suppliers", className="mb-2 search-label"),
                                dbc.Input(
                                    type="text",
                                    placeholder="Enter supplier name...",
                                    className="supplier-search-input mb-4",
                                ),
                            ],
                            className="search-container",
                        ),

                        # --- Rounded Table with Sample Data ---
                        dbc.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [
                                            html.Th("Supplier Name"),
                                            html.Th("Contact Number"),
                                            html.Th("Address"),
                                            html.Th("Product Name"),
                                            html.Th("Price"),
                                            html.Th("Action"),  # New column for edit buttons
                                        ]
                                    )
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td("ABC Supplies Co."),
                                                html.Td("0917-123-4567"),
                                                html.Td("123 Main Street, Quezon City"),
                                                html.Td("Ceramic Tile 30x30"),
                                                html.Td("₱250"),
                                                html.Td(
                                                    dbc.Button(
                                                        "Edit",
                                                        href="/inventory/supplier/edit",
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
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("BuildSmart Trading"),
                                                html.Td("0998-765-4321"),
                                                html.Td("Makati Business Center"),
                                                html.Td("Marble Tile 60x60"),
                                                html.Td("₱720"),
                                                html.Td(
                                                    dbc.Button(
                                                        "Edit",
                                                        href="/inventory/supplier",
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
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("StonePro Manufacturing"),
                                                html.Td("0928-555-8899"),
                                                html.Td("San Fernando, Pampanga"),
                                                html.Td("Granite Tile 40x40"),
                                                html.Td("₱480"),
                                                html.Td(
                                                    dbc.Button(
                                                        "Edit",
                                                        href="/inventory/supplier",
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
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("TileWorks Depot"),
                                                html.Td("0933-222-1111"),
                                                html.Td("Cebu City"),
                                                html.Td("Vinyl Tile 50x50"),
                                                html.Td("₱300"),
                                                html.Td(
                                                    dbc.Button(
                                                        "Edit",
                                                        href="/inventory/supplier",
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
                                        ),
                                        html.Tr(
                                            [
                                                html.Td("Elite Builders Supply"),
                                                html.Td("0945-333-7777"),
                                                html.Td("Davao City"),
                                                html.Td("Porcelain Tile 60x60"),
                                                html.Td("₱650"),
                                                html.Td(
                                                    dbc.Button(
                                                        "Edit",
                                                        href="/inventory/supplier",
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
                                        ),
                                    ]
                                ),
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
                            },
                        ),
                    ]
                ),
                className="inventory-card",
                style={"backgroundColor": "#3d2f25", "borderRadius": "2rem"},
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )
