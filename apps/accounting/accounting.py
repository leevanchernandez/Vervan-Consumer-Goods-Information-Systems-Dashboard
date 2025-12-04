import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from app import app
from apps.commonmodules import makeNavbar, create_pagination_controls
from apps.dbconnect import getDataFromDB
import math

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

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            dcc.Store(id="order-page-store", data=1),
            makeNavbar(user_role=user_role, pathname=pathname),

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
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Input(id="order-id-filter", placeholder="Order ID", type="text"), width=2),
                                        dbc.Col(dbc.Input(id="client-name-filter", placeholder="Client Name", type="text"), width=2),
                                        dbc.Col(dbc.Input(id="product-name-filter", placeholder="Product", type="text"), width=2),
                                        dbc.Col(dbc.Input(id="quantity-filter", placeholder="Qty", type="text"), width=1),
                                        dbc.Col(dbc.Input(id="order-date-filter", placeholder="Date (YYYY-MM-DD)", type="text"), width=2),
                                        dbc.Col(dbc.Input(id="order-status-filter", placeholder="Status", type="text"), width=2),
                                    ],
                                    className="mb-4",
                                ),
                            ],
                            className="search-container",
                        ),

                        # --- Table Container (dynamic) ---
                        html.Div(id="order-table-container"),

                        # --- Pagination Controls ---
                        html.Div(
                            create_pagination_controls(1, 1, "order"),
                            id="order-pagination-container"
                        )
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
    [Output("order-table-container", "children"),
     Output("order-pagination-container", "children"),
     Output("order-page-store", "data")],
    [Input("order-id-filter", "value"),
     Input("client-name-filter", "value"),
     Input("product-name-filter", "value"),
     Input("quantity-filter", "value"),
     Input("order-date-filter", "value"),
     Input("order-status-filter", "value"),
     Input("order-prev-btn", "n_clicks"),
     Input("order-next-btn", "n_clicks")],
    [State("order-page-store", "data")]
)
def update_order_table(order_id, client_name, product_name, quantity, order_date, order_status, prev_clicks, next_clicks, current_page):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    df_orders = fetch_orders()

    # Filter by individual columns
    if order_id:
        df_orders = df_orders[df_orders["order_id"].astype(str).str.contains(order_id, case=False, na=False)]
    if client_name:
        df_orders = df_orders[df_orders["client_name"].str.contains(client_name, case=False, na=False)]
    if product_name:
        df_orders = df_orders[df_orders["product_name"].str.contains(product_name, case=False, na=False)]
    if quantity:
        df_orders = df_orders[df_orders["quantity_ordered"].astype(str).str.contains(quantity, case=False, na=False)]
    if order_date:
        df_orders = df_orders[df_orders["order_date"].astype(str).str.contains(order_date, case=False, na=False)]
    if order_status:
        df_orders = df_orders[df_orders["status_name"].str.contains(order_status, case=False, na=False)]

    if df_orders.empty:
        return dbc.Alert("No orders found.", color="warning"), create_pagination_controls(1, 1, "order"), 1

    # Pagination Logic
    rows_per_page = 12
    total_rows = len(df_orders)
    total_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1

    # Handle page changes
    # Handle page changes
    if any(triggered_id == filter_id for filter_id in ["order-id-filter", "client-name-filter", "product-name-filter", "quantity-filter", "order-date-filter", "order-status-filter"]):
        current_page = 1
    elif triggered_id == "order-prev-btn":
        current_page = max(1, current_page - 1)
    elif triggered_id == "order-next-btn":
        current_page = min(total_pages, current_page + 1)
    
    # Ensure current_page is valid
    current_page = max(1, min(current_page, total_pages))

    # Slice Data
    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    df_sliced = df_orders.iloc[start_idx:end_idx]

    table_rows = []
    for row in df_sliced.to_dict("records"):
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

    table = dbc.Table(
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

    pagination = create_pagination_controls(current_page, total_pages, "order")

    return table, pagination, current_page
