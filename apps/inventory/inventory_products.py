import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar

layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),

        # === TOP TAB PILL ===
        dbc.Row(
            dbc.ButtonGroup(
                [
                    dbc.Button(
                        "Suppliers Tab",
                        href="/inventory",
                        id="suppliers-tab",
                        className="tab-pill-left",
                    ),
                    dbc.Button(
                        "Products Tab",
                        href="/inventory/products",
                        id="products-tab",
                        className="tab-pill-right active-tab",
                    ),
                ],
                className="tab-pill-group",
            ),
            className="mb-4 justify-content-start",  # left align
        ),

        # === MAIN CARD ===
        dbc.Card(
            dbc.CardBody(
                [
                    # --- Header Row ---
                    dbc.Row(
                        [
                            dbc.Col(html.H2("Manage Products", className="m-0"), width="auto"),
                            dbc.Col(
                                dbc.Button(
                                    "Add Product Details",
                                    href="/inventory/products/add",
                                    id="add-btn",
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
                            html.Label("Search Product", className="mb-2 search-label"),
                            dbc.Input(
                                type="text",
                                placeholder="Enter product name...",
                                className="supplier-search-input mb-4",
                            ),
                        ],
                        className="search-container",
                    ),

                    # --- Rounded Table ---
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Product Name"),
                                        html.Th("Brand"),
                                        html.Th("Selling Price"),
                                        html.Th("Weight"),
                                        html.Th("Description"),
                                        html.Th("Size"),
                                        html.Th("Stock Level"),
                                        html.Th("Action"),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(f"Product {i}"),
                                            html.Td(f"Brand {i}"),
                                            html.Td(f"{100.00 * i:.2f}"),
                                            html.Td(f"{10 * i}"),
                                            html.Td("Sample description"),
                                            html.Td(f"{2 * i}x{3 * i}"),
                                            html.Td(f"{12 * i}"),
                                            html.Td(
                                                dbc.Button(
                                                    "Edit",
                                                    href="/inventory/products/edit",
                                                    id=f"edit-btn-{i}",
                                                    color="secondary",
                                                    size="sm",
                                                    style={
                                                        "background-color": "#977b61",
                                                        "color": "#fffaf3",
                                                        "border": "none",
                                                        "border-radius": "999px",
                                                        "padding": "6px 18px",
                                                        "font-weight": "500",
                                                        "transition": "all 0.2s ease-in-out",
                                                    },
                                                )
                                            ),
                                        ]
                                    )
                                    for i in range(1, 6)
                                ]
                            ),
                        ],
                        bordered=True,
                        hover=True,
                        responsive=True,
                        className="product-table",
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
        ),
    ],
    fluid=True,
    style={"padding": "2rem"},
)
