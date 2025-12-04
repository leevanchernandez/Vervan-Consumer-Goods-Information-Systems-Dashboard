import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, MATCH, ctx
from dash.exceptions import PreventUpdate
import flask
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB, modifyDB
from datetime import date
import urllib.parse

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
            dcc.Location(id='url_order_edit', refresh=False),
            dcc.Store(id='order_id_store', storage_type='session'),
            dcc.Store(id='edit_product_options_store'),

            # === Page Title ===
            html.H1("Edit Order Details", className="supplier-details-title mb-5"),

            # === Card ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Username ---
                        html.Label("Username (Client Name):", className="form-label"),
                        dbc.Input(
                            id="edit_order_username",
                            type="text",
                            placeholder="ex. Juan Dela Cruz",
                            className="form-input mb-4",
                        ),

                        # --- Date Ordered ---
                        html.Label("Date Ordered:", className="form-label"),
                        html.Div(
                            dcc.DatePickerSingle(
                                id="edit_order_date",
                                placeholder="Date",
                                display_format="YYYY-MM-DD",
                                className="pill-date-picker",
                            ),
                            style={"width": "100%", "display": "block", "marginBottom": "1.5rem"},                                                
                        ),

                        # --- Platform ---
                        html.Label("Platform:", className="form-label"),
                        dbc.Select(
                            id="edit_order_platform",
                            options=[], # Populated by callback
                            placeholder="Select Platform",
                            className="form-input mb-4",
                        ),

                        # --- Products Ordered Container ---
                        html.Label("Products Ordered:", className="form-label mb-3"),
                        html.Div(id="edit_order_product_container", children=[]),

                        # --- Add (+) Button ---
                        html.Div(
                            dbc.Button(
                                "+",
                                id="edit_add_product_row_btn",
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
                            id="edit_order_status",
                            options=[], # Populated by callback
                            placeholder="Select Order Status",
                            className="form-input mb-4",
                        ),

                        # --- Centered Submit + Delete Row ---
                        dbc.Row(
                            [
                                dbc.Col(width=3),
                                dbc.Col(
                                    dbc.Button(
                                        "Submit",
                                        id="edit_order_submit_btn",
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
                                        id="edit_order_delete_checkbox",
                                        label="Returned?",
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
                        html.Div(id="edit_order_feedback", className="mt-3 text-center"),
                    ]
                ),
                className="supplier-details-card",
            ),
            
            # === Success Modal ===
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Success")),
                    dbc.ModalBody("Order details updated successfully."),
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
                id="edit_order_success_modal",
                is_open=False,
                centered=True,
                backdrop="static",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )

# === Callback to Populate Initial Options ===
@app.callback(
    [Output('edit_order_status', 'options'),
     Output('edit_order_platform', 'options'),
     Output('edit_product_options_store', 'data')],
    [Input('url_order_edit', 'pathname')]
)
def populate_edit_options(_):
    # Fetch Statuses
    sql_status = """
        SELECT status_id, status_name 
        FROM "order-status"
        ORDER BY status_id;
    """
    df_status = getDataFromDB(sql_status, [], ["status_id", "status_name"])
    status_options = [{'label': row['status_name'], 'value': row['status_name']} for _, row in df_status.iterrows()] 
    
    # Fetch Platforms
    sql_platform = """
        SELECT platform_id, platform_name
        FROM platform
        ORDER BY platform_name;
    """
    df_platform = getDataFromDB(sql_platform, [], ["platform_id", "platform_name"])
    platform_options = [{'label': row['platform_name'], 'value': row['platform_id']} for _, row in df_platform.iterrows()]
    
    # Fetch Products
    sql_products = """
        SELECT product_id, product_name 
        FROM product
        WHERE product_delete_ind = FALSE
        ORDER BY product_name;
    """
    df_products = getDataFromDB(sql_products, [], ["product_id", "product_name"])
    product_options = [{'label': row['product_name'], 'value': row['product_id']} for _, row in df_products.iterrows()]
    
    return status_options, platform_options, product_options

# === Callback to Load Order Details ===
@app.callback(
    [Output('edit_order_username', 'value'),
     Output('edit_order_date', 'date'),
     Output('edit_order_status', 'value'),
     Output('edit_order_platform', 'value'),
     Output('edit_order_product_container', 'children'),
     Output('order_id_store', 'data')],
    [Input('url_order_edit', 'search')],
    [State('edit_product_options_store', 'data')]
)
def load_order_details(search, product_options):
    if not search:
        raise PreventUpdate
    
    parsed = urllib.parse.urlparse(search)
    query_params = urllib.parse.parse_qs(parsed.query)
    order_id = query_params.get('id', [None])[0]
    
    if not order_id:
        raise PreventUpdate
        
    try:
        order_id = int(float(order_id))
    except (ValueError, TypeError):
        raise PreventUpdate

    # 1. Get Main Order Info
    sql_order = """
        SELECT 
            o.order_id,
            o.order_date,
            cl.client_name,
            os.status_name,
            p.platform_id
        FROM "order" o
        JOIN "order-status" os ON o.status_id = os.status_id
        JOIN client cl ON o.client_id = cl.client_id
        LEFT JOIN platform p ON o.platform_id = p.platform_id
        WHERE o.order_id = %s;
    """
    
    df_order = getDataFromDB(sql_order, [order_id], ["order_id", "order_date", "client_name", "status_name", "platform_id"])
    
    if df_order.empty:
        return None, None, None, None, [], None
        
    row = df_order.iloc[0]
    client_name = row['client_name']
    order_date = row['order_date']
    status_name = row['status_name']
    platform_id = row['platform_id']
    
    # 2. Get Products
    sql_products = """
        SELECT c.product_id, p.product_name, c.quantity_ordered
        FROM composition c
        JOIN product p ON c.product_id = p.product_id
        WHERE c.order_id = %s;
    """
    df_prods = getDataFromDB(sql_products, [order_id], ["product_id", "product_name", "quantity_ordered"])
    
    product_rows = []
    for i, prod in df_prods.iterrows():
        new_row = dbc.Row(
            [
                dbc.Col(
                    dbc.Select(
                        id={'type': 'edit_order_product_dropdown', 'index': i},
                        options=product_options if product_options else [],
                        value=prod['product_id'],
                        placeholder="Select Product",
                        className="form-input mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Input(
                        id={'type': 'edit_order_product_qty', 'index': i},
                        type="number",
                        value=prod['quantity_ordered'],
                        placeholder="Qty",
                        className="form-input mb-4",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "×",
                        id={'type': 'edit_remove_product_row_btn', 'index': i},
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
            id={'type': 'edit_product_row', 'index': i}
        )
        product_rows.append(new_row)

    return client_name, order_date, status_name, platform_id, product_rows, order_id

# === Callback to Add/Remove Product Rows ===
@app.callback(
    Output('edit_order_product_container', 'children', allow_duplicate=True),
    [Input('edit_add_product_row_btn', 'n_clicks'),
     Input({'type': 'edit_remove_product_row_btn', 'index': ALL}, 'n_clicks')],
    [State('edit_order_product_container', 'children'),
     State('edit_product_options_store', 'data')],
    prevent_initial_call=True
)
def manage_edit_product_rows(add_clicks, remove_clicks, children, product_options):
    triggered = ctx.triggered_id
    
    if not children:
        children = []

    if triggered == 'edit_add_product_row_btn':
        # Generate a unique index based on existing children count + timestamp or just random
        # Simple count might conflict if we remove middle ones, so let's use max index + 1
        import time
        new_index = int(time.time() * 1000) 
        
        new_row = dbc.Row(
            [
                dbc.Col(
                    dbc.Select(
                        id={'type': 'edit_order_product_dropdown', 'index': new_index},
                        options=product_options if product_options else [],
                        placeholder="Select Product",
                        className="form-input mb-4",
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.Input(
                        id={'type': 'edit_order_product_qty', 'index': new_index},
                        type="number",
                        placeholder="Qty",
                        className="form-input mb-4",
                    ),
                    width=4,
                ),
                dbc.Col(
                    dbc.Button(
                        "×",
                        id={'type': 'edit_remove_product_row_btn', 'index': new_index},
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
            id={'type': 'edit_product_row', 'index': new_index}
        )
        children.append(new_row)
        
    elif isinstance(triggered, dict) and triggered['type'] == 'edit_remove_product_row_btn':
        index_to_remove = triggered['index']
        children = [
            child for child in children 
            if child['props']['id']['index'] != index_to_remove
        ]

    return children

# === Callback to Save Changes ===
@app.callback(
    [Output('edit_order_success_modal', 'is_open'),
     Output('edit_order_feedback', 'children')],
    [Input('edit_order_submit_btn', 'n_clicks')],
    [State('order_id_store', 'data'),
     State('edit_order_date', 'date'),
     State('edit_order_status', 'value'),
     State('edit_order_platform', 'value'),
     State('edit_order_delete_checkbox', 'value'),
     State({'type': 'edit_order_product_dropdown', 'index': ALL}, 'value'),
     State({'type': 'edit_order_product_qty', 'index': ALL}, 'value')]
)
def save_order_changes(n_clicks, order_id, order_date, status_name, platform_id, delete_ind, product_ids, quantities):
    if not n_clicks or not order_id:
        raise PreventUpdate
        
    try:
        if delete_ind:
            sql = """
                UPDATE "order"
                SET status_id = (SELECT status_id FROM "order-status" WHERE status_name = 'Returned')
                WHERE order_id = %s;
            """
            modifyDB(sql, [order_id])
        else:
            # Update Order Details
            if not order_date or not status_name or not platform_id:
                 return False, dbc.Alert("Please ensure Date, Status, and Platform are filled.", color="danger")
            
            sql_update = """
                UPDATE "order"
                SET 
                    order_date = %s,
                    platform_id = %s,
                    status_id = (
                        SELECT status_id 
                        FROM "order-status"
                        WHERE status_name = %s
                    )
                WHERE order_id = %s;
            """
            modifyDB(sql_update, [order_date, platform_id, status_name, order_id])
            
            # Update Products (Delete old, Insert new)
            # 1. Delete existing composition
            sql_delete_comp = 'DELETE FROM composition WHERE order_id = %s'
            modifyDB(sql_delete_comp, [order_id])
            
            # 2. Insert new composition
            valid_products = []
            for p_id, qty in zip(product_ids, quantities):
                if p_id and qty and int(qty) > 0:
                    valid_products.append((p_id, qty))
            
            if not valid_products:
                 return False, dbc.Alert("Please ensure at least one valid product is added.", color="danger")

            sql_insert_comp = """
                INSERT INTO composition (order_id, product_id, quantity_ordered)
                VALUES (%s, %s, %s);
            """
            for p_id, qty in valid_products:
                modifyDB(sql_insert_comp, [order_id, p_id, qty])
            
        return True, ""
        
    except Exception as e:
        return False, dbc.Alert(f"Error updating order: {str(e)}", color="danger")
