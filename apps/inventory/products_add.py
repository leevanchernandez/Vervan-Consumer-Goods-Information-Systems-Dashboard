import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB, modifyDB

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),
            # === Page Title ===
            html.H1("Product Details", className="supplier-details-title mb-5"),

            # === Card ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Product Name ---
                        html.Label("Product Name:", className="form-label"),
                        dbc.Input(
                            id="add_product_name",
                            type="text",
                            placeholder="ex. Foam A",
                            className="form-input mb-4",
                        ),

                        # --- Brand ---
                        html.Label("Brand:", className="form-label"),
                        dbc.Input(
                            id="add_product_brand",
                            type="text",
                            placeholder="ex. Brand B",
                            className="form-input mb-4",
                        ),

                        # --- Selling Price (in Pesos) ---
                        html.Label("Selling Price (in Pesos):", className="form-label"),
                        dbc.Input(
                            id="add_product_price",
                            type="number",
                            placeholder="ex. 2200",
                            className="form-input mb-4",
                        ),

                        # --- Description ---
                        html.Label("Description:", className="form-label"),
                        dbc.Input(
                            id="add_product_description",
                            type="text",
                            placeholder="ex. Lorem Ipsum",
                            className="form-input mb-4",
                        ),

                        # --- Weight, Volumetric Weight, Stock Level ---
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label("Weight (in kg)"),
                                        dbc.Input(
                                            id="add_product_weight",
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
                                            id="add_product_size",
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
                                            id="add_product_stock",
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
                            id="add_product_supplier",
                            options=[], # Populated by callback
                            placeholder="Select a supplier...",
                            className="form-input mb-4",
                        ),

                        # --- Supplied Price ---
                        html.Label("Supplied Price (in Pesos):", className="form-label"),
                        dbc.Input(
                            id="add_product_supplied_price",
                            type="number",
                            placeholder="ex. 1500",
                            className="form-input mb-4",
                        ),

                        # --- Centered Submit Row ---
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Submit",
                                        id="add_product_submit_btn",
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
                            ],
                            justify="center",
                            align="center",
                            className="g-2",
                        ),
                        html.Div(id="add_product_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("Product added successfully."),
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
                id="add_product_success_modal",
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
    Output('add_product_supplier', 'options'),
    Input('add_product_name', 'id') # Dummy input to trigger on load
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

# === Callback to Submit Form ===
@app.callback(
    [Output('add_product_success_modal', 'is_open'),
     Output('add_product_feedback', 'children')],
    [Input('add_product_submit_btn', 'n_clicks')],
    [State('add_product_name', 'value'),
     State('add_product_brand', 'value'),
     State('add_product_price', 'value'),
     State('add_product_description', 'value'),
     State('add_product_weight', 'value'),
     State('add_product_size', 'value'),
     State('add_product_stock', 'value'),
     State('add_product_supplier', 'value'),
     State('add_product_supplied_price', 'value')]
)
def submit_new_product(n_clicks, name, brand, price, description, weight, size, stock, supplier_id, supplied_price):
    if not n_clicks:
        raise PreventUpdate
    
    # Basic Validation
    if not all([name, price, supplier_id]): # Minimal required fields
        return False, dbc.Alert("Please fill in at least Product Name, Price, and Supplier.", color="danger")
    
    try:
        sql = """
            INSERT INTO product (
                product_name,
                brand,
                selling_price,
                description,
                weight,
                size,
                beginning_inventory,
                supplier_id,
                supplied_price
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Handle optional fields being None/Empty
        # Ensure numeric fields are numbers or None
        
        modifyDB(sql, [name, brand, price, description, weight, size, stock, supplier_id, supplied_price])
        return True, ""
        
    except Exception as e:
        return False, dbc.Alert(f"Error adding product: {str(e)}", color="danger")
