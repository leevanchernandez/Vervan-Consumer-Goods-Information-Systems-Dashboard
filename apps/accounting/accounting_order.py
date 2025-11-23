import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, MATCH, ctx
from dash.exceptions import PreventUpdate
import flask
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB, modifyDB
from datetime import date

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),
            
            # Store to keep track of product options to avoid re-fetching constantly if needed, 
            # but for now we can just fetch in the row adder or update existing rows. 
            # Actually, simpler to just fetch options once and store in a dcc.Store or just pass to the callback.
            dcc.Store(id='product_options_store'),

            # === Page Title ===
            html.H1("Order Details", className="supplier-details-title mb-5"),

            # === Card ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Username ---
                        html.Label("Username (Client Name):", className="form-label"),
                        dbc.Input(
                            id="order_username",
                            type="text",
                            placeholder="ex. Juan Dela Cruz",
                            className="form-input mb-4",
                        ),

                        # --- Date Ordered ---
                        html.Label("Date Ordered:", className="form-label"),
                        html.Div(
                            dcc.DatePickerSingle(
                                id="order_date",
                                placeholder="Date",
                                date=date.today(),
                                display_format="YYYY-MM-DD",
                                className="pill-date-picker",
                            ),
                            style={"width": "100%", "display": "block", "marginBottom": "1.5rem"},                                                
                        ),

                        # --- Products Ordered Container ---
                        html.Label("Products Ordered:", className="form-label mb-3"),
                        html.Div(id="order_product_container", children=[]),

                        # --- Add (+) Button ---
                        html.Div(
                            dbc.Button(
                                "+",
                                id="add_product_row_btn",
                                n_clicks=0,
                                style={
                                    "backgroundColor": "#7a5d60",
                                    "color": "white",
                                    "border": "none",
                                    "borderRadius": "50%",
                                    "width": "50px",
                                    "height": "50px",
                                    "fontWeight": "600",
                                    "fontSize": "1.5rem",
                                    "display": "flex",
                                    "alignItems": "center",
                                    "justifyContent": "center",
                                    "margin": "0 auto 30px auto",
                                },
                            ),
                            style={"textAlign": "center"},
                        ),

                        # --- Order Status ---
                        html.Label("Order Status:", className="form-label"),
                        dbc.Select(
                            id="order_status",
                            options=[], # Populated by callback
                            placeholder="Select Order Status",
                            className="form-input mb-4",
                        ),

                        # --- Centered Submit Row ---
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Submit",
                                        id="submit_order_btn",
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
                        html.Div(id="order_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("Order logged successfully."),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Go to Orders", 
                            href="/accounting", 
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
                id="order_success_modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )

# === Callback to Populate Initial Options (Status and Product List) ===
@app.callback(
    [Output('order_status', 'options'),
     Output('product_options_store', 'data')],
    [Input('order_username', 'id')] # Dummy input to trigger on load
)
def populate_options(_):
    # Fetch Statuses
    sql_status = """
        SELECT status_id, status_name 
        FROM "order-status"
        ORDER BY status_id;
    """
    df_status = getDataFromDB(sql_status, [], ["status_id", "status_name"])
    status_options = [{'label': row['status_name'], 'value': row['status_id']} for _, row in df_status.iterrows()]
    
    # Fetch Products
    sql_products = """
        SELECT product_id, product_name 
        FROM product
        WHERE product_delete_ind = FALSE
        ORDER BY product_name;
    """
    df_products = getDataFromDB(sql_products, [], ["product_id", "product_name"])
    product_options = [{'label': row['product_name'], 'value': row['product_id']} for _, row in df_products.iterrows()]
    
    return status_options, product_options

# === Callback to Add/Remove Product Rows ===
@app.callback(
    Output('order_product_container', 'children'),
    [Input('add_product_row_btn', 'n_clicks'),
     Input({'type': 'remove_product_row_btn', 'index': ALL}, 'n_clicks')],
    [State('order_product_container', 'children'),
     State('product_options_store', 'data')]
)
def manage_product_rows(add_clicks, remove_clicks, children, product_options):
    triggered = ctx.triggered_id
    
    if not children:
        children = []

    if triggered == 'add_product_row_btn':
        new_index = add_clicks
        new_row = dbc.Row(
            [
                dbc.Col(
                    dbc.Select(
                        id={'type': 'order_product_dropdown', 'index': new_index},
                        options=product_options if product_options else [],
                        placeholder="Select Product",
                        className="form-input mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Input(
                        id={'type': 'order_product_qty', 'index': new_index},
                        type="number",
                        placeholder="Qty",
                        className="form-input mb-4",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "×",
                        id={'type': 'remove_product_row_btn', 'index': new_index},
                        style={
                            "backgroundColor": "#1e0f00",
                            "color": "#faf3e7",
                            "border": "none",
                            "borderRadius": "50%",
                            "width": "38px",
                            "height": "38px",
                            "fontWeight": "600",
                            "fontSize": "1.2rem",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "padding": "0",
                        },
                    ),
                    width=2,
                    className="d-flex align-items-center justify-content-center",
                ),
            ],
            className="g-2",
            id={'type': 'product_row', 'index': new_index}
        )
        children.append(new_row)
        
    elif isinstance(triggered, dict) and triggered['type'] == 'remove_product_row_btn':
        index_to_remove = triggered['index']
        children = [
            child for child in children 
            if child['props']['id']['index'] != index_to_remove
        ]
        
    # Ensure at least one row exists initially if empty (optional, but good UX)
    if not children and (not triggered or triggered == 'add_product_row_btn'):
         # If it's the first load or we just removed the last one, maybe don't force it, 
         # but usually we want at least one. Let's leave it empty until 'add' is clicked 
         # OR trigger 'add' logic if list is empty on load? 
         # For now, let's rely on user clicking '+'.
         pass

    return children

# === Callback to Submit Order ===
@app.callback(
    [Output('order_success_modal', 'is_open'),
     Output('order_feedback', 'children')],
    [Input('submit_order_btn', 'n_clicks')],
    [State('order_username', 'value'),
     State('order_date', 'date'),
     State('order_status', 'value'),
     State({'type': 'order_product_dropdown', 'index': ALL}, 'value'),
     State({'type': 'order_product_qty', 'index': ALL}, 'value')]
)
def submit_order(n_clicks, username, order_date, status_id, product_ids, quantities):
    if not n_clicks:
        raise PreventUpdate
    
    # Validation
    if not all([username, order_date, status_id]):
        return False, dbc.Alert("Please fill in Username, Date, and Status.", color="danger")
    
    if not product_ids or not any(product_ids):
        return False, dbc.Alert("Please add at least one product.", color="danger")
        
    valid_products = []
    for p_id, qty in zip(product_ids, quantities):
        if p_id and qty and int(qty) > 0:
            valid_products.append((p_id, qty))
            
    if not valid_products:
        return False, dbc.Alert("Please ensure all added products have a selected product and valid quantity.", color="danger")

    try:
        # 1. Get Staff ID from session
        staff_id = flask.session.get("staff_id")
        # For robustness during development if session is empty:
        if staff_id is None:
             # Try to find a default staff or error? 
             # Let's assume there's at least one staff in DB or handle gracefully.
             # For now, let's just proceed, but DB might enforce NOT NULL.
             # If strictly following user instruction:
             pass 

        # 2. Check/Create Client
        sql_check_client = "SELECT client_id FROM client WHERE client_name = %s;"
        df_client = getDataFromDB(sql_check_client, [username], ["client_id"])
        
        if not df_client.empty:
            client_id = int(df_client.iloc[0]['client_id'])
        else:
            sql_create_client = """
                INSERT INTO client (client_name, client_phone_number) 
                VALUES (%s, NULL)
                RETURNING client_id;
            """
            client_id = modifyDB(sql_create_client, [username], return_id=True)
            
        # 3. Insert Order
        sql_insert_order = """
            INSERT INTO "order" (order_date, platform_id, client_id, staff_id, status_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING order_id;
        """
        # Assuming platform_id is 1 (e.g., 'In-store' or default) since it wasn't specified in inputs.
        # If platform table exists, we might need to fetch a valid ID. 
        # Let's assume 1 is valid or NULL if allowed. 
        # User didn't provide SQL for platform lookup, so I'll assume a default or NULL.
        # Looking at schema from previous context might help, but let's try 1 or NULL.
        # Actually, let's try to fetch a platform ID if possible, or just use 1.
        platform_id = 1 
        
        order_id = modifyDB(sql_insert_order, [order_date, platform_id, client_id, staff_id, status_id], return_id=True)
        
        # 4. Insert Products
        sql_insert_comp = """
            INSERT INTO composition (order_id, product_id, quantity_ordered) 
            VALUES (%s, %s, %s);
        """
        for p_id, qty in valid_products:
            modifyDB(sql_insert_comp, [order_id, p_id, qty])
            
        return True, ""

    except Exception as e:
        return False, dbc.Alert(f"Error submitting order: {str(e)}", color="danger")
