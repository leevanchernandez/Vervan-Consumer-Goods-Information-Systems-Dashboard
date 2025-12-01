import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB, modifyDB
import urllib.parse

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
            dcc.Location(id='url_product_edit', refresh=False),
            dcc.Store(id='products_edit_id_store', storage_type='session'),

            # === Page Title ===
            html.H1("Edit Product Details", className="supplier-details-title mb-5"),

            # === Card ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Product Name ---
                        html.Label("Product Name:", className="form-label"),
                        dbc.Input(
                            id="edit_product_name",
                            type="text",
                            placeholder="ex. Foam A",
                            className="form-input mb-4",
                        ),

                        # --- Brand ---
                        html.Label("Brand:", className="form-label"),
                        dbc.Input(
                            id="edit_product_brand",
                            type="text",
                            placeholder="ex. Brand B",
                            className="form-input mb-4",
                        ),

                        # --- Selling Price (in Pesos) ---
                        html.Label("Selling Price (in Pesos):", className="form-label"),
                        dbc.Input(
                            id="edit_product_price",
                            type="number",
                            placeholder="ex. 2200",
                            className="form-input mb-4",
                        ),

                        # --- Description ---
                        html.Label("Description:", className="form-label"),
                        dbc.Input(
                            id="edit_product_description",
                            type="text",
                            placeholder="ex. Lorem Ipsum",
                            className="form-input mb-4",
                        ),

                        # --- Weight, Size, Stock Level ---
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Weight (in kg)"),
                                        dbc.Input(
                                            id="edit_product_weight",
                                            type="number",
                                            placeholder="ex. 4",
                                            className="form-input mb-4",
                                        ),
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Size"),
                                        dbc.Input(
                                            id="edit_product_size",
                                            type="text",
                                            placeholder="ex. 2x3",
                                            className="form-input mb-4",
                                        ),
                                    ],
                                    width=4,
                                ),
                                dbc.Col(
                                    [
                                        html.Label("Stock Level"),
                                        dbc.Input(
                                            id="edit_product_stock",
                                            type="number",
                                            placeholder="ex. 100",
                                            className="form-input mb-4",
                                        ),
                                    ],
                                    width=4,
                                ),
                            ],
                            className="g-2",
                        ),

                        # --- Supplier ---
                        html.Label("Supplier"),
                        dbc.Select(
                            id="edit_product_supplier",
                            options=[], # Populated by callback
                            placeholder="Select a supplier...",
                            className="form-input mb-4",
                        ),

                        # --- Supplied Price ---
                        html.Label("Supplied Price (in Pesos):", className="form-label"),
                        dbc.Input(
                            id="edit_product_supplied_price",
                            type="number",
                            placeholder="ex. 1500",
                            className="form-input mb-4",
                        ),

                        # --- Centered Submit + Delete Row ---
                        dbc.Row(
                            [
                                dbc.Col(width=3),  # Spacer (left)
                                dbc.Col(
                                    dbc.Button(
                                        "Submit",
                                        id="edit_product_submit_btn",
                                        n_clicks=0,
                                        style={
                                            "backgroundColor": "#7a5d60",
                                            "border": "none",
                                            "borderRadius": "30px",
                                            "padding": "12px 40px",
                                            "fontWeight": "600",
                                            "fontSize": "1.1rem",
                                            "boxShadow": "0px 3px 8px rgba(0, 0, 0, 0.2)",
                                        },
                                    ),
                                    width="auto",
                                    className="d-flex justify-content-center",
                                ),
                                dbc.Col(
                                    dbc.Checkbox(
                                        id="edit_product_delete_checkbox",
                                        label="Delete?",
                                        value=False,
                                        style={
                                            "fontWeight": "500",
                                            "marginTop": "10px",
                                            "marginLeft": "12px",
                                        },
                                    ),
                                    width="auto",
                                ),
                            ],
                            justify="center",
                            align="center",
                            className="g-2",
                        ),
                        html.Div(id="edit_product_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("Product details updated successfully."),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Go to Products", 
                            href="/inventory/products", 
                            style={
                                "backgroundColor": "#7a5d60",
                                "color": "#fff",
                                "border": "none",
                                "borderRadius": "30px",
                                "padding": "10px 30px",
                                "fontWeight": "600",
                            }
                        )
                    ),
                ],
                id="edit_product_success_modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )

# === Callback to Populate Supplier Dropdown ===
@app.callback(
    Output('edit_product_supplier', 'options'),
    Input('edit_product_name', 'id') # Dummy input to trigger on load
)
def populate_supplier_dropdown(_):
    sql = """
        SELECT supplier_id, supplier_name
        FROM supplier
        WHERE supplier_delete_ind = FALSE
        ORDER BY supplier_name;
    """
    df = getDataFromDB(sql, [], ["supplier_id", "supplier_name"])
    
    options = [
        {'label': row['supplier_name'], 'value': row['supplier_id']}
        for _, row in df.iterrows()
    ]
    return options

# === Callback to Load Product Details ===
@app.callback(
    [Output('edit_product_name', 'value'),
     Output('edit_product_brand', 'value'),
     Output('edit_product_price', 'value'),
     Output('edit_product_description', 'value'),
     Output('edit_product_weight', 'value'),
     Output('edit_product_size', 'value'),
     Output('edit_product_stock', 'value'),
     Output('edit_product_supplier', 'value'),
     Output('edit_product_supplied_price', 'value'),
     Output('products_edit_id_store', 'data')],
    [Input('url_product_edit', 'search')]
)
def load_product_details(search):
    if not search:
        raise PreventUpdate
    
    parsed = urllib.parse.urlparse(search)
    query_params = urllib.parse.parse_qs(parsed.query)
    product_id = query_params.get('id', [None])[0]
    
    if not product_id:
        raise PreventUpdate
        
    # Ensure product_id is an integer (handle cases like "1.0" or "1")
    try:
        product_id = int(float(product_id))
    except (ValueError, TypeError):
        raise PreventUpdate

    sql = """
        SELECT product_name, brand, selling_price, description, weight, size, beginning_inventory, supplier_id, supplied_price
        FROM product
        WHERE product_id = %s
    """
    df = getDataFromDB(sql, [product_id], ["product_name", "brand", "selling_price", "description", "weight", "size", "beginning_inventory", "supplier_id", "supplied_price"])
    
    if not df.empty:
        row = df.iloc[0]
        return (
            row['product_name'],
            row['brand'],
            row['selling_price'],
            row['description'],
            row['weight'],
            row['size'],
            row['beginning_inventory'],
            row['supplier_id'],
            row['supplied_price'],
            product_id
        )
    return None, None, None, None, None, None, None, None, None, None

# === Callback to Save Changes ===
@app.callback(
    [Output('edit_product_success_modal', 'is_open'),
     Output('edit_product_feedback', 'children')],
    [Input('edit_product_submit_btn', 'n_clicks')],
    [State('products_edit_id_store', 'data'),
     State('edit_product_name', 'value'),
     State('edit_product_brand', 'value'),
     State('edit_product_price', 'value'),
     State('edit_product_description', 'value'),
     State('edit_product_weight', 'value'),
     State('edit_product_size', 'value'),
     State('edit_product_stock', 'value'),
     State('edit_product_supplier', 'value'),
     State('edit_product_supplied_price', 'value'),
     State('edit_product_delete_checkbox', 'value')]
)
def save_product_changes(n_clicks, product_id, name, brand, price, description, weight, size, stock, supplier_id, supplied_price, delete_ind):
    if not n_clicks or not product_id:
        raise PreventUpdate
        
    try:
        if delete_ind:
            sql = "UPDATE product SET product_delete_ind = TRUE WHERE product_id = %s"
            modifyDB(sql, [product_id])
        else:
            sql = """
                UPDATE product
                SET 
                product_name=%s,
                brand=%s,
                selling_price=%s,
                description=%s,
                weight=%s,
                size=%s,
                beginning_inventory=%s,
                supplier_id=%s,
                supplied_price=%s
                WHERE product_id=%s
            """
            modifyDB(sql, [name, brand, price, description, weight, size, stock, supplier_id, supplied_price, product_id])
            
        return True, ""
        
    except Exception as e:
        return False, dbc.Alert(f"Error updating product: {str(e)}", color="danger")
