import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, MATCH, ctx
from app import app
from apps.commonmodules import makeNavbar, create_pagination_controls
from apps.dbconnect import getDataFromDB, modifyDB
import math

# === Function to fetch products from DB ===
def fetch_products():
    sql = """
        SELECT 
            p.product_id,
            p.product_name,
            p.brand,
            p.selling_price,
            p.weight,
            p.description,
            p.size,
            (
                p.beginning_inventory
                + COALESCE(pur.total_purchased, 0)
                - COALESCE(ord.total_ordered, 0)
            ) AS current_stock
        FROM product p

        -- PURCHASES
        LEFT JOIN (
            SELECT
                co.product_id,
                SUM(co.quantity_purchased) AS total_purchased
            FROM components co
            JOIN purchase pu ON co.purchase_id = pu.purchase_id
            GROUP BY co.product_id
        ) pur ON p.product_id = pur.product_id

        -- ORDERS (excluding returns)
        LEFT JOIN (
            SELECT 
                c.product_id,
                SUM(c.quantity_ordered) AS total_ordered
            FROM composition c
            JOIN "order" o ON c.order_id = o.order_id
            JOIN "order-status" os ON o.status_id = os.status_id
            WHERE os.status_name != 'Returned'
            GROUP BY c.product_id
        ) ord ON p.product_id = ord.product_id
        
        WHERE p.product_delete_ind = FALSE
        ORDER BY p.product_name ASC;
    """
    colnames = ["product_id", "product_name", "brand", "selling_price", "weight", "description", "size", "current_stock"]
    df = getDataFromDB(sql, [], colnames)
    return df

# === Layout ===
def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            dcc.Store(id="product-page-store", data=1),
            dcc.Store(id="stock-update-trigger", data=0),
            makeNavbar(user_role=user_role, pathname=pathname),

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
                className="mb-4 justify-content-start",
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
                                html.Label("Filter Products", className="mb-2 search-label"),
                                html.Div(
                                    [
                                        html.Div(dbc.Input(id="product-name-filter", placeholder="Product Name", type="text"), style={"width": "15%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="brand-filter", placeholder="Brand", type="text"), style={"width": "12.5%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="selling-price-filter", placeholder="Price", type="text"), style={"width": "10%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="weight-filter", placeholder="Weight in kg", type="text"), style={"width": "10%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="description-filter", placeholder="Description", type="text"), style={"width": "15%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="size-filter", placeholder="Size (L x W x H)", type="text"), style={"width": "12.5%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="stock-level-filter", placeholder="Stock", type="text"), style={"width": "10%", "padding": "5px"}),
                                        html.Div(style={"width": "15%", "padding": "5px"}), # Placeholder for Action column
                                    ],
                                    className="d-flex mb-4",
                                ),
                            ],
                            className="search-container",
                        ),

                        # --- Table Container (dynamic) ---
                        html.Div(id="product-table-container"),

                        # --- Pagination Controls ---
                        html.Div(
                            create_pagination_controls(1, 1, "product"),
                            id="product-pagination-container"
                        )
                    ]
                ),
                className="inventory-card",
            ),

            # === Add Stock Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Edit Stock")),
                    dbc.ModalBody(
                        [
                            dcc.Store(id="add-stock-product-id"),
                            html.Label("Quantity to Add/Reduce:", className="form-label"),
                            dbc.Input(id="add-stock-qty", type="number", placeholder="Enter quantity", className="mb-3"),
                            html.Div(id="add-stock-feedback", className="text-danger"),
                        ]
                    ),
                    dbc.ModalFooter(
                        [
                            dbc.Button("Cancel", id="add-stock-cancel-btn", className="ms-auto", n_clicks=0),
                            dbc.Button("Add/Reduce Stock", id="add-stock-confirm-btn", className="ms-2", n_clicks=0, style={"backgroundColor": "#7a5d60", "border": "none"}),
                        ]
                    ),
                ],
                id="add-stock-modal",
                is_open=False,
                centered=True,
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )

# === Callback to populate table dynamically ===
@app.callback(
    [Output("product-table-container", "children"),
     Output("product-pagination-container", "children"),
     Output("product-page-store", "data")],
    [Input("product-name-filter", "value"),
     Input("brand-filter", "value"),
     Input("selling-price-filter", "value"),
     Input("weight-filter", "value"),
     Input("description-filter", "value"),
     Input("size-filter", "value"),
     Input("stock-level-filter", "value"),
     Input("product-prev-btn", "n_clicks"),
     Input("product-next-btn", "n_clicks"),
     Input("stock-update-trigger", "data")],
    [State("product-page-store", "data")]
)
def update_product_table(product_name, brand, selling_price, weight, description, size, stock_level, prev_clicks, next_clicks, stock_update, current_page):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    df_products = fetch_products()

    # Filter if search value provided
    # Filter by individual columns
    if product_name:
        df_products = df_products[df_products["product_name"].str.contains(product_name, case=False, na=False)]
    if brand:
        df_products = df_products[df_products["brand"].str.contains(brand, case=False, na=False)]
    if selling_price:
        df_products = df_products[df_products["selling_price"].astype(str).str.contains(selling_price, case=False, na=False)]
    if weight:
        df_products = df_products[df_products["weight"].str.contains(weight, case=False, na=False)]
    if description:
        df_products = df_products[df_products["description"].str.contains(description, case=False, na=False)]
    if size:
        df_products = df_products[df_products["size"].str.contains(size, case=False, na=False)]
    if stock_level:
        df_products = df_products[df_products["current_stock"].astype(str).str.contains(stock_level, case=False, na=False)]

    if df_products.empty:
        return dbc.Alert("No products found.", color="warning"), create_pagination_controls(1, 1, "product"), 1

    # Pagination Logic
    rows_per_page = 12
    total_rows = len(df_products)
    total_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1

    # Handle page changes
    if any(triggered_id == filter_id for filter_id in ["product-name-filter", "brand-filter", "selling-price-filter", "weight-filter", "description-filter", "size-filter", "stock-level-filter"]):
        current_page = 1
    elif triggered_id == "product-prev-btn":
        current_page = max(1, current_page - 1)
    elif triggered_id == "product-next-btn":
        current_page = min(total_pages, current_page + 1)
    
    # Ensure current_page is valid
    current_page = max(1, min(current_page, total_pages))

    # Slice Data
    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    df_sliced = df_products.iloc[start_idx:end_idx]

    # Generate table rows
    table_rows = []
    for _, row in df_sliced.iterrows():
        table_rows.append(
            html.Tr(
                [
                    html.Td(row["product_name"]),
                    html.Td(row["brand"]),
                    html.Td(f"₱{row['selling_price']}"),
                    html.Td(row["weight"]),
                    html.Td(row["description"]),
                    html.Td(row["size"]),
                    html.Td(row["current_stock"]),
                    html.Td(
                        [
                            dbc.Button(
                                "Edit Details",
                                href=f"/inventory/products/edit?id={row['product_id']}",
                                color="secondary",
                                size="sm",
                                className="me-2",
                                style={
                                    "background-color": "#977b61",
                                    "color": "#fffaf3",
                                    "border": "none",
                                    "border-radius": "999px",
                                    "padding": "6px 18px",
                                    "font-weight": "500",
                                    "transition": "all 0.2s ease-in-out",
                                    "marginRight": "10px",
                                    "marginBottom": "5px",
                                },
                            ),
                            dbc.Button(
                                "Edit Stock",
                                id={'type': 'add-stock-btn', 'index': row['product_id']},
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
                            ),
                        ]
                    ),
                ]
            )
        )

    table = dbc.Table(
        [html.Thead(
            html.Tr([
                html.Th("Product Name", style={"width": "15%"}),
                html.Th("Brand", style={"width": "12.5%"}),
                html.Th("Selling Price", style={"width": "10%"}),
                html.Th("Weight (in kg)", style={"width": "10%"}),
                html.Th("Description", style={"width": "15%"}),
                html.Th("Size (L x W x H)", style={"width": "12.5%"}),
                html.Th("Current Stock", style={"width": "10%"}),
                html.Th("Actions", style={"width": "15%"}),
            ])
        ),
        html.Tbody(table_rows)],
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

    pagination = create_pagination_controls(current_page, total_pages, "product")

    return table, pagination, current_page

# === Callback to Open/Close Modal and Submit Stock ===
@app.callback(
    [Output("add-stock-modal", "is_open"),
     Output("add-stock-product-id", "data"),
     Output("add-stock-qty", "value"),
     Output("add-stock-feedback", "children"),
     Output("stock-update-trigger", "data")],
    [Input({'type': 'add-stock-btn', 'index': ALL}, 'n_clicks'),
     Input("add-stock-cancel-btn", "n_clicks"),
     Input("add-stock-confirm-btn", "n_clicks")],
    [State("add-stock-modal", "is_open"),
     State("add-stock-product-id", "data"),
     State("add-stock-qty", "value"),
     State("current_user_id", "data"),
     State("stock-update-trigger", "data")]
)
def manage_stock_modal(add_clicks, cancel_clicks, confirm_clicks, is_open, product_id, qty, staff_id, current_trigger):
    triggered = ctx.triggered_id
    
    # Open Modal
    if isinstance(triggered, dict) and triggered['type'] == 'add-stock-btn':
        return True, triggered['index'], None, "", current_trigger
    
    # Close Modal (Cancel)
    if triggered == "add-stock-cancel-btn":
        return False, None, None, "", current_trigger
    
    # Submit Stock
    if triggered == "add-stock-confirm-btn":
        if not qty or qty == 0:
            return True, product_id, qty, "Please enter a valid quantity (positive to add, negative to reduce).", current_trigger
        
        if not staff_id:
             return True, product_id, qty, "Error: User not identified. Please log in.", current_trigger

        try:

            sql_purchase = """
                INSERT INTO purchase (arrival_date, staff_id)
                VALUES (CURRENT_DATE, %s)
                RETURNING purchase_id;
            """
            purchase_id = modifyDB(sql_purchase, [staff_id], return_id=True)
            
            if not purchase_id:
                 return True, product_id, qty, "Error creating purchase record.", current_trigger

            sql_components = """
                INSERT INTO components (purchase_id, product_id, quantity_purchased)
                VALUES (%s, %s, %s);
            """
            modifyDB(sql_components, [int(purchase_id), int(product_id), int(qty)])
            
            return False, None, None, "", current_trigger + 1
            
        except Exception as e:
            return True, product_id, qty, f"Error: {str(e)}", current_trigger

    return is_open, product_id, qty, "", current_trigger

