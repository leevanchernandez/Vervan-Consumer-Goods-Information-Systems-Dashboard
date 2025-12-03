import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from app import app
from apps.commonmodules import makeNavbar, create_pagination_controls
from apps.dbconnect import getDataFromDB  # Make sure you have a function to fetch data
import math

# === Function to fetch products from DB ===
def fetch_products():
    sql = """
        SELECT product_id, product_name, brand, selling_price, weight, description, size, beginning_inventory
        FROM product
        WHERE product_delete_ind = FALSE
        ORDER BY product_name
    """
    colnames = ["product_id", "product_name", "brand", "selling_price", "weight", "description", "size", "stock_level"]
    df = getDataFromDB(sql, [], colnames)
    return df

# === Layout ===
def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            dcc.Store(id="product-page-store", data=1),
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
                                html.Label("Search Product", className="mb-2 search-label"),
                                dbc.Input(
                                    id="product-search-input",
                                    type="text",
                                    placeholder="Enter product name...",
                                    className="supplier-search-input mb-4",
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
        ],
        fluid=True,
        style={"padding": "2rem"},
    )

# === Callback to populate table dynamically ===
@app.callback(
    [Output("product-table-container", "children"),
     Output("product-pagination-container", "children"),
     Output("product-page-store", "data")],
    [Input("product-search-input", "value"),
     Input("product-prev-btn", "n_clicks"),
     Input("product-next-btn", "n_clicks")],
    [State("product-page-store", "data")]
)
def update_product_table(search_value, prev_clicks, next_clicks, current_page):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    df_products = fetch_products()

    # Filter if search value provided
    if search_value:
        search_value_lower = search_value.lower()
        df_products = df_products[df_products["product_name"].str.lower().str.contains(search_value_lower)]

    if df_products.empty:
        return dbc.Alert("No products found.", color="warning"), create_pagination_controls(1, 1, "product"), 1

    # Pagination Logic
    rows_per_page = 12
    total_rows = len(df_products)
    total_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1

    # Handle page changes
    if triggered_id == "product-search-input":
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
                    html.Td(row["stock_level"]),
                    html.Td(
                        dbc.Button(
                            "Edit",
                            href=f"/inventory/products/edit?id={row['product_id']}",
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
        )

    table = dbc.Table(
        [html.Thead(
            html.Tr([
                html.Th("Product Name"),
                html.Th("Brand"),
                html.Th("Selling Price"),
                html.Th("Weight"),
                html.Th("Description"),
                html.Th("Size"),
                html.Th("Stock Level"),
                html.Th("Action"),
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

