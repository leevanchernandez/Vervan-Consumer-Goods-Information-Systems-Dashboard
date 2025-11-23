import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB, modifyDB

# --- Helper function to fetch product names ---
def fetch_product_names():
    sql = "SELECT DISTINCT product_name FROM product ORDER BY product_name"
    colnames = ["Product Name"]
    df = getDataFromDB(sql, [], colnames)
    return [{"label": name, "value": name} for name in df["Product Name"].tolist()]

# === Layout ===
layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),
        html.H1("Supplier Details", className="supplier-details-title mb-5"),

        dbc.Card(
            dbc.CardBody(
                [
                    html.Label("Supplier Name:", className="form-label"),
                    dbc.Input(id="supplier-name-input", type="text", placeholder="ex. Juan Dela Cruz", className="form-input mb-4"),

                    html.Label("Contact Number:", className="form-label"),
                    dbc.Input(id="supplier-contact-input", type="text", placeholder="ex. 09xxxxxxxxx", className="form-input mb-4"),

                    html.Label("Address:", className="form-label"),
                    dbc.Input(id="supplier-address-input", type="text", placeholder="ex. 22 Cornelia Street, Quezon City", className="form-input mb-4"),

                    html.Label("Supplier Product:", className="form-label"),
                    dbc.Select(id="supplier-product-select", placeholder="Select an existing product...", className="form-input mb-2"),

                    dbc.Input(id="new-product-input", type="text", placeholder="Or type a new product...", className="form-input mb-4"),

                    html.Label("Price (in PHP):", className="form-label"),
                    dbc.Input(id="supplier-price-input", type="number", placeholder="2200", className="form-input mb-4"),

                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button(
                                    "Submit",
                                    id="submit-supplier-btn",
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
                    html.Div(id="supplier-feedback", className="mt-3"),
                ]
            ),
            className="supplier-details-card",
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Success")),
                dbc.ModalBody(id="supplier-modal-body"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Go to Inventory", 
                        href="/inventory", 
                        style={
                            "backgroundColor": "#7a5d60",
                            "color": "#fff",         # text color
                            "border": "none",
                            "borderRadius": "30px",
                            "padding": "10px 30px",
                            "fontWeight": "600",
                        }
                    )
                ),
            ],
            id="supplier-modal",
            is_open=False,
            centered=True,
            backdrop="static",
        ),
    ],
    fluid=True,
    className="supplier-details-container",
)

# --- Callback to populate product dropdown dynamically ---
@app.callback(
    Output("supplier-product-select", "options"),
    Input("submit-supplier-btn", "n_clicks")
)
def update_product_dropdown(n_clicks):
    return fetch_product_names()

# --- Callback to insert new supplier and product ---
@app.callback(
    Output("supplier-modal", "is_open"),        # Open modal on success
    Output("supplier-modal-body", "children"), # Message inside modal
    Output("supplier-feedback", "children"),
    Input("submit-supplier-btn", "n_clicks"),
    State("supplier-name-input", "value"),
    State("supplier-contact-input", "value"),
    State("supplier-address-input", "value"),
    State("supplier-product-select", "value"),
    State("new-product-input", "value"),
    State("supplier-price-input", "value"),
)
def submit_supplier(n_clicks, name, contact, address, selected_product, new_product, price):
    if n_clicks == 0:
        raise PreventUpdate

    # Validate required fields
    if not all([name, contact, address, price]) or (not selected_product and not new_product):
        return False, None, dbc.Alert("Please fill in all required fields.", color="danger")

    product_name = new_product if new_product else selected_product

    try:
        # Insert supplier
        sql_supplier = """
            INSERT INTO supplier (supplier_name, address, supplier_contact_number)
            VALUES (%s, %s, %s)
            RETURNING supplier_id
        """
        supplier_id = modifyDB(sql_supplier, [name, address, contact], return_id=True)

        # Insert product
        sql_product = """
            INSERT INTO product (product_name, supplied_price, supplier_id)
            VALUES (%s, %s, %s)
        """
        modifyDB(sql_product, [product_name, price, supplier_id])

        # Success: show modal, no error
        return True, f"Supplier and product '{product_name}' added successfully!", None

    except Exception as e:
        print(e)
        return False, None, dbc.Alert("An error occurred. Please try again.", color="danger")

