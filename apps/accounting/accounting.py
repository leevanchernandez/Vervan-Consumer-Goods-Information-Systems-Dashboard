import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar

layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),
        # === MAIN CARD ===
        dbc.Card(
            dbc.CardBody(
                [
                    # --- Header Row ---
                    dbc.Row(
                        [
                            dbc.Col(html.H2("Manage Orders", className="m-0"), width="auto"),
                            dbc.Col(
                                dbc.Button(
                                    "Log New Order",
                                    href="/accounting/order",
                                    id="log-order-btn",
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
                            html.Label("Filter Orders", className="mb-2 search-label"),
                            dbc.Input(
                                type="text",
                                placeholder="Can filter by order status, order ID, product name, etc",
                                className="supplier-search-input mb-4",
                            ),
                        ],
                        className="search-container",
                    ),

                    # --- Table ---
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Order ID"),
                                        html.Th("Username"),
                                        html.Th("Product"),
                                        html.Th("Product Quantity"),
                                        html.Th("Date Ordered"),
                                        html.Th("Order Status"),
                                        html.Th("Action"),  # column for Edit buttons
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(f"ORD-{1000 + i}"),
                                            html.Td(f"user_{i}"),
                                            html.Td(f"Product {i}"),
                                            html.Td(f"{2 * i} pcs"),
                                            html.Td(f"2025-10-{20 + i}"),
                                            html.Td("Delivered" if i % 2 == 0 else "Pending"),
                                            html.Td(
                                                dbc.Button(
                                                    "Edit",
                                                    href="/accounting/order/edit",
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
                            "borderCollapse": "separate",  # allow rounded corners
                            "borderSpacing": "0",
                            "borderRadius": "1rem",        # 1rem corner radius
                            "overflow": "hidden",          # clip cell backgrounds
                            "backgroundColor": "#faf3e7",  # soft table background
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
