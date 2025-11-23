import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB

# --- Helper to fetch orders from DB ---
def fetch_orders():
    sql = """
        SELECT 
            o.order_id,
            cl.client_name,
            p.product_name,
            c.quantity_ordered,
            o.order_date,
            os.status_name
        FROM "order" o
        JOIN client cl ON o.client_id = cl.client_id
        JOIN composition c ON o.order_id = c.order_id
        JOIN product p ON c.product_id = p.product_id
        JOIN "order-status" os ON o.status_id = os.status_id
        ORDER BY o.order_date DESC
    """
    colnames = ["order_id", "client_name", "product_name", "quantity_ordered", "order_date", "status_name"]
    df = getDataFromDB(sql, [], colnames)
    return df

# === Layout ===
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
                                id="order-search-input",
                                type="text",
                                placeholder="Can filter by order status, order ID, product name, etc",
                                className="supplier-search-input mb-4",
                            ),
                        ],
                        className="search-container",
                    ),

                    # --- Table Container (dynamic) ---
                    html.Div(id="order-table-container"),
                ]
            ),
            className="inventory-card",
        ),
    ],
    fluid=True,
    style={"padding": "2rem"},
)

# === Callback to update order table dynamically ===
@app.callback(
    Output("order-table-container", "children"),
    Input("order-search-input", "value")
)
def update_order_table(search_value):
    df_orders = fetch_orders()

    if search_value:
        search_value_lower = search_value.lower()
        # Filter by multiple columns
        df_orders = df_orders[
            df_orders["client_name"].str.lower().str.contains(search_value_lower, na=False) |
            df_orders["product_name"].str.lower().str.contains(search_value_lower, na=False) |
            df_orders["status_name"].str.lower().str.contains(search_value_lower, na=False) |
            df_orders["order_id"].astype(str).str.contains(search_value_lower, na=False) |
            df_orders["quantity_ordered"].astype(str).str.contains(search_value_lower, na=False) |
            df_orders["order_date"].astype(str).str.contains(search_value_lower, na=False)
        ]

    if df_orders.empty:
        return dbc.Alert("No orders found.", color="warning")

    table_rows = []
    for row in df_orders.to_dict("records"):
        table_rows.append(
            html.Tr(
                [
                    html.Td(f"ORD-{row['order_id']}"),
                    html.Td(row["client_name"]),
                    html.Td(row["product_name"]),
                    html.Td(f"{row['quantity_ordered']} pcs"),
                    html.Td(row["order_date"].strftime("%Y-%m-%d")),
                    html.Td(row["status_name"]),
                    html.Td(
                        dbc.Button(
                            "Edit",
                            href=f"/accounting/order/edit?id={row['order_id']}",
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

    return dbc.Table(
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
                        html.Th("Action"),
                    ]
                )
            ),
            html.Tbody(table_rows),
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
    )
