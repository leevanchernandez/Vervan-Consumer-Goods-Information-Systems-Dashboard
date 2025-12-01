import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB

def layout(user_role="inventory", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
            # Greeting
            html.H1(
                "Hello!", 
                id="inv_greeting",
                style={"color": "#7a5d60", "fontWeight": "bold"}
            ),
            html.H6(
                "Here are the recent product updates.",
                style={"color": "#7a5d60"},
            ),

            # Dashboard Cards
            dbc.Row(
                [
                    # Left Card (Table)
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Inventory Summary", className="card-title mb-3"),
                                    html.Div(id="inv_summary_table"),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "center",
                                    "height": "100%",
                                },
                            ),
                            style={
                                "backgroundColor": "#3d2f25",
                                "color": "#fffaf3",
                                "borderRadius": "2rem",
                                "minHeight": "180px",
                                "padding": "1rem",
                            },
                        ),
                        width=9,
                    ),

                    # Right Card (Low Stock Alert)
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Low Stock Alert!", className="card-title mb-3"),
                                    html.Div(id="inv_low_stock_list"),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "flexStart",
                                    "height": "100%",
                                },
                            ),
                            style={
                                "backgroundColor": "#564e6d",
                                "color": "#fffaf3",
                                "borderRadius": "2rem",
                                "minHeight": "180px",
                                "padding": "1rem",
                            },
                        ),
                        width=3,
                    ),
                ],
                className="mt-4",
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )

@app.callback(
    [Output("inv_greeting", "children"),
     Output("inv_summary_table", "children"),
     Output("inv_low_stock_list", "children")],
    [Input("current_user_id", "data")]
)
def update_inventory_dashboard(user_id):
    # Default values
    greeting = "Hello!"
    table_content = html.P("No products found.", style={"fontStyle": "italic", "color": "#fffaf3"})
    low_stock_content = html.P("No low stock items.", style={"fontStyle": "italic"})

    # 1. Update Greeting
    if user_id:
        sql_user = "SELECT staff_name FROM staff WHERE staff_id = %s"
        df_user = getDataFromDB(sql_user, [user_id], ["staff_name"])
        if not df_user.empty:
            greeting = f"Hello, {df_user.iloc[0]['staff_name']}!"

    # 2. Fetch Inventory Data
    sql_inv = """
        SELECT product_name, beginning_inventory
        FROM product
        WHERE product_delete_ind = FALSE
        ORDER BY product_name;
    """
    df_inv = getDataFromDB(sql_inv, [], ["product_name", "beginning_inventory"])
    
    if not df_inv.empty:
        # --- Build Summary Table ---
        table_rows = []
        low_stock_items = []
        
        import pandas as pd
        
        for _, row in df_inv.iterrows():
            stock = row['beginning_inventory']
            
            # Handle None/NaN stock
            if stock is None or pd.isna(stock):
                stock_val = 0
                stock_display = "N/A"
            else:
                try:
                    stock_val = int(stock)
                    stock_display = str(stock_val)
                except:
                    stock_val = 0
                    stock_display = "Invalid"
            
            # Determine Status
            if stock_val < 20:
                status = "Low Stock"
                low_stock_items.append(row['product_name'])
                status_style = {"color": "#ff6b6b", "fontWeight": "bold"} # Reddish for alert
            else:
                status = "Normal"
                status_style = {}
                
            table_rows.append(
                html.Tr(
                    [
                        html.Td(row['product_name']),
                        html.Td(stock_display),
                        html.Td(status, style=status_style),
                    ]
                )
            )
            
        table_content = dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Product"),
                            html.Th("Stock"),
                            html.Th("Status"),
                        ]
                    )
                ),
                html.Tbody(table_rows),
            ],
            bordered=True,
            striped=True,
            hover=True,
            responsive=True,
            style={"backgroundColor": "#fffaf3", "color": "#3d2f25"},
        )
        
        # --- Build Low Stock List ---
        if low_stock_items:
            low_stock_content = html.Ul(
                [html.Li(f"{item}") for item in low_stock_items],
                style={"marginLeft": "1rem"}
            )
        else:
            low_stock_content = html.P("All stock levels are healthy!", style={"color": "#a8e6cf"})

    return greeting, table_content, low_stock_content
