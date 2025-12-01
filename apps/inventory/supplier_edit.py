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
            dcc.Location(id='url_supplier_edit', refresh=False),
            dcc.Store(id='supplier_id_store', storage_type='session'),
            dcc.Store(id='product_id_store', storage_type='session'),
            
            # === Page Title ===
            html.H1("Edit Supplier Details", className="supplier-details-title mb-5"),

            # === Card ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Supplier Name ---
                        html.Label("Supplier Name:", className="form-label"),
                        dbc.Input(
                            id="edit_supplier_name",
                            type="text",
                            placeholder="ex. Juan Dela Cruz",
                            className="form-input mb-4",
                        ),

                        # --- Contact Number ---
                        html.Label("Contact Number:", className="form-label"),
                        dbc.Input(
                            id="edit_supplier_contact",
                            type="text",
                            placeholder="ex. 09xxxxxxxxx",
                            className="form-input mb-4",
                        ),

                        # --- Address ---
                        html.Label("Address:", className="form-label"),
                        dbc.Input(
                            id="edit_supplier_address",
                            type="text",
                            placeholder="ex. 22 Cornelia Street, Quezon City",
                            className="form-input mb-4",
                        ),

                        # --- Supplier Product ---
                        html.Label("Supplier Product:", className="form-label"),
                        dbc.Input(
                            id="edit_supplier_product",
                            type="text",
                            placeholder="Product Name",
                            className="form-input mb-4",
                        ),

                        # --- Price ---
                        html.Label("Price (in PHP):", className="form-label"),
                        dbc.Input(
                            id="edit_supplier_price",
                            type="number",
                            placeholder="2200",
                            className="form-input mb-4",
                        ),

                        # --- Centered Submit + Delete Row ---
                        dbc.Row(
                            [
                                dbc.Col(width=3),  # Spacer (left)
                                dbc.Col(
                                    dbc.Button(
                                        "Submit",
                                        id="edit_supplier_submit_btn",
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
                                        id="edit_supplier_delete_checkbox",
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
                        html.Div(id="edit_supplier_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("Supplier details updated successfully."),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Go to Inventory", 
                            href="/inventory", 
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
                id="edit_supplier_success_modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )

# === Callback to Load Data ===
@app.callback(
    [Output('edit_supplier_name', 'value'),
     Output('edit_supplier_address', 'value'),
     Output('edit_supplier_contact', 'value'),
     Output('edit_supplier_product', 'value'),
     Output('edit_supplier_price', 'value'),
     Output('edit_supplier_delete_checkbox', 'value'),
     Output('supplier_id_store', 'data'),
     Output('product_id_store', 'data')],
    [Input('url_supplier_edit', 'search')]
)
def load_supplier_details(search):
    if not search:
        raise PreventUpdate
    
    parsed = urllib.parse.urlparse(search)
    query_params = urllib.parse.parse_qs(parsed.query)
    supplier_id = query_params.get('id', [None])[0]
    product_id = query_params.get('product_id', [None])[0]

    if not supplier_id:
        raise PreventUpdate

    sql = """
        SELECT s.supplier_name, s.address, s.supplier_contact_number,
               p.product_id, p.product_name, p.supplied_price,
               s.supplier_delete_ind
        FROM supplier s
        LEFT JOIN product p ON s.supplier_id = p.supplier_id
        WHERE s.supplier_id = %s
    """
    params = [supplier_id]
    if product_id:
        sql += " AND p.product_id = %s"
        params.append(product_id)

    df = getDataFromDB(sql, params, [
        "supplier_name", "address", "supplier_contact_number",
        "product_id", "product_name", "supplied_price",
        "supplier_delete_ind"
    ])

    if not df.empty:
        row = df.iloc[0]
        return (
            row['supplier_name'],
            row['address'],
            row['supplier_contact_number'],
            row['product_name'],
            row['supplied_price'],
            row['supplier_delete_ind'],
            supplier_id,
            row['product_id']  # store actual product_id from DB
        )

    return None, None, None, None, None, False, None, None

# === Callback to Save Changes ===
@app.callback(
    [Output('edit_supplier_success_modal', 'is_open'),
     Output('edit_supplier_feedback', 'children')],
    [Input('edit_supplier_submit_btn', 'n_clicks')],
    [State('supplier_id_store', 'data'),
     State('product_id_store', 'data'),
     State('edit_supplier_name', 'value'),
     State('edit_supplier_address', 'value'),
     State('edit_supplier_contact', 'value'),
     State('edit_supplier_product', 'value'),
     State('edit_supplier_price', 'value'),
     State('edit_supplier_delete_checkbox', 'value')]
)
def save_supplier_changes(n_clicks, supplier_id, product_id, name, address, contact, product_name, price, delete_ind):
    if not n_clicks or not supplier_id:
        raise PreventUpdate

    try:
        # Update supplier
        sql_supplier = """
            UPDATE supplier
            SET supplier_name=%s,
                address=%s,
                supplier_contact_number=%s,
                supplier_delete_ind=%s
            WHERE supplier_id=%s
        """
        modifyDB(sql_supplier, [name, address, contact, delete_ind, supplier_id])

        # Update product
        if product_id:  # ensure we have product_id
            sql_product = """
                UPDATE product
                SET product_name=%s,
                    supplied_price=%s
                WHERE product_id=%s
            """
            modifyDB(sql_product, [product_name, price, product_id])

        return True, ""

    except Exception as e:
        return False, dbc.Alert(f"Error updating supplier: {str(e)}", color="danger")
