import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar, create_pagination_controls
from dash.dependencies import Input, Output, State
from apps.dbconnect import getDataFromDB
import pandas as pd
import math

# === Function to fetch supplier data from the database ===
def fetch_suppliers():
    """
    Fetch supplier details along with one product and its price.
    """
    sql = """
        SELECT s.supplier_id,
               s.supplier_name,
               s.supplier_contact_number,
               s.address,
               p.product_id,
               p.product_name,
               p.supplied_price
        FROM supplier s
        LEFT JOIN product p ON p.supplier_id = s.supplier_id
        WHERE s.supplier_delete_ind = FALSE
        ORDER BY s.supplier_name
    """
    colnames = ["supplier_id", "Supplier Name", "Contact Number", "Address", "product_id", "Product Name", "Price"]
    df = getDataFromDB(sql, [], colnames)
    return df

# === Layout ===
def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            dcc.Store(id="supplier-page-store", data=1),
            makeNavbar(user_role=user_role, pathname=pathname),

            # === Top tab pill navigation ===
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

            # === Main card ===
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

                        # --- Search Inputs ---
                        html.Div(
                            [
                                html.Label("Filter Suppliers", className="mb-2 search-label"),
                                html.Div(
                                    [
                                        html.Div(dbc.Input(id="supplier-name-filter", placeholder="Supplier Name", type="text"), style={"width": "20%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="contact-number-filter", placeholder="Contact Number", type="text"), style={"width": "15%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="address-filter", placeholder="Address", type="text"), style={"width": "25%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="product-name-filter", placeholder="Product Name", type="text"), style={"width": "15%", "padding": "5px"}),
                                        html.Div(dbc.Input(id="price-filter", placeholder="Price", type="text"), style={"width": "10%", "padding": "5px"}),
                                        html.Div(style={"width": "15%", "padding": "5px"}), # Placeholder for Action column
                                    ],
                                    className="d-flex mb-4",
                                ),
                            ],
                            className="search-container",
                        ),

                        # --- Table Container (dynamic) ---
                        html.Div(id="supplier-table-container"),

                        # --- Pagination Controls ---
                        html.Div(
                            create_pagination_controls(1, 1, "supplier"),
                            id="supplier-pagination-container"
                        )
                    ]
                ),
                className="inventory-card",
                style={"backgroundColor": "#3d2f25", "borderRadius": "2rem"},
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )

# === Callback to update supplier table dynamically based on search input ===
@app.callback(
    [Output("supplier-table-container", "children"),
     Output("supplier-pagination-container", "children"),
     Output("supplier-page-store", "data")],
    [Input("supplier-name-filter", "value"),
     Input("contact-number-filter", "value"),
     Input("address-filter", "value"),
     Input("product-name-filter", "value"),
     Input("price-filter", "value"),
     Input("supplier-prev-btn", "n_clicks"),
     Input("supplier-next-btn", "n_clicks")],
    [State("supplier-page-store", "data")]
)
def update_supplier_table(supplier_name, contact_number, address, product_name, price, prev_clicks, next_clicks, current_page):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    # Fetch supplier data
    df_suppliers = fetch_suppliers()

    # Filter by individual columns
    if supplier_name:
        df_suppliers = df_suppliers[df_suppliers["Supplier Name"].str.contains(supplier_name, case=False, na=False)]
    if contact_number:
        df_suppliers = df_suppliers[df_suppliers["Contact Number"].str.contains(contact_number, case=False, na=False)]
    if address:
        df_suppliers = df_suppliers[df_suppliers["Address"].str.contains(address, case=False, na=False)]
    if product_name:
        df_suppliers = df_suppliers[df_suppliers["Product Name"].str.contains(product_name, case=False, na=False)]
    if price:
        df_suppliers = df_suppliers[df_suppliers["Price"].astype(str).str.contains(price, case=False, na=False)]

    if df_suppliers.empty:
        return dbc.Alert("No suppliers found.", color="warning"), create_pagination_controls(1, 1, "supplier"), 1

    # Pagination Logic
    rows_per_page = 12
    total_rows = len(df_suppliers)
    total_pages = math.ceil(total_rows / rows_per_page) if total_rows > 0 else 1

    # Handle page changes
    if any(triggered_id == filter_id for filter_id in ["supplier-name-filter", "contact-number-filter", "address-filter", "product-name-filter", "price-filter"]):
        current_page = 1
    elif triggered_id == "supplier-prev-btn":
        current_page = max(1, current_page - 1)
    elif triggered_id == "supplier-next-btn":
        current_page = min(total_pages, current_page + 1)
    
    # Ensure current_page is valid
    current_page = max(1, min(current_page, total_pages))

    # Slice Data
    start_idx = (current_page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    df_sliced = df_suppliers.iloc[start_idx:end_idx]

    # Generate table rows
    table_rows = []
    for _, row in df_sliced.iterrows():
        product_id_param = f"&product_id={int(row['product_id'])}" if pd.notna(row['product_id']) else ""
        table_rows.append(
            html.Tr(
                [
                    html.Td(row["Supplier Name"]),
                    html.Td(row["Contact Number"]),
                    html.Td(row["Address"]),
                    html.Td(row["Product Name"] if row["Product Name"] else "-"),
                    html.Td(f"₱{row['Price']}" if row["Price"] else "-"),
                    html.Td(
                        dbc.Button(
                            "Edit",
                            href=f"/inventory/supplier/edit?id={row['supplier_id']}{product_id_param}",
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

    # Return the table
    table = dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Supplier Name", style={"width": "20%"}),
                        html.Th("Contact Number", style={"width": "15%"}),
                        html.Th("Address", style={"width": "25%"}),
                        html.Th("Product Name", style={"width": "15%"}),
                        html.Th("Price", style={"width": "10%"}),
                        html.Th("Action", style={"width": "15%"}),
                    ]
                )
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
        },
    )

    pagination = create_pagination_controls(current_page, total_pages, "supplier")

    return table, pagination, current_page