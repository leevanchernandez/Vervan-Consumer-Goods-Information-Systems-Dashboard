import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, ctx
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB
import pandas as pd

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
            dcc.Store(id='selected-report-type', data='inventory'),
            dbc.Row(
                [
                    # ==== LEFT COLUMN ====
                    dbc.Col(
                        [
                            html.H5("Report Type:", className="mb-2"),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Button(
                                            "Inventory Report",
                                            id="inventory-report-btn",
                                            color="link",
                                            className="report-link mb-2 text-start w-100",
                                            style={'textDecoration': 'none', 'color': '#faf3e7'}
                                        ),
                                        dbc.Button(
                                            "Sales Report",
                                            id="sales-report-btn",
                                            color="link",
                                            className="report-link mb-2 text-start w-100",
                                            style={'textDecoration': 'none', 'color': '#faf3e7'}
                                        ),
                                        dbc.Button(
                                            "Financial Report",
                                            id="financial-report-btn",
                                            color="link",
                                            className="report-link text-start w-100",
                                            style={'textDecoration': 'none', 'color': '#faf3e7'}
                                        ),
                                    ]
                                ),
                                className="mb-3 report-card",
                                style={"backgroundColor": "#3d2f25"}
                            ),

                            html.H5("Parameters:", className="mb-2"),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.Label("Start Date", className="m-0", style={"color": "#faf3e7"}),
                                                html.Div(
                                                    dcc.DatePickerSingle(
                                                        id="start-date",
                                                        placeholder="Start Date",
                                                        display_format="YYYY-MM-DD",
                                                        className="pill-date-picker mb-4",
                                                    ),
                                                    style={"width": "100%"},
                                                ),
                                                html.Label("End Date", className="m-0", style={"color": "#faf3e7"}),
                                                html.Div(
                                                    dcc.DatePickerSingle(
                                                        id="end-date",
                                                        placeholder="End Date",
                                                        display_format="YYYY-MM-DD",
                                                        className="pill-date-picker",
                                                    ),
                                                    style={"width": "100%"},
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                                className="report-card",
                                style={"backgroundColor": "#3d2f25"},
                            ),
                        ],
                        width=3,
                    ),

                    # ==== RIGHT COLUMN ====
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(id='report-table-container')
                                ),
                                style={
                                    "borderRadius": "2rem",
                                    "backgroundColor": "#faf3e7",
                                    "padding": "2rem",
                                    "minHeight": "500px"
                                },
                            ),
                        ],
                        width=9,
                    ),
                ],
                className="g-3 mt-4",
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )

@app.callback(
    [
        Output('selected-report-type', 'data'),
        Output('inventory-report-btn', 'style'),
        Output('sales-report-btn', 'style'),
        Output('financial-report-btn', 'style')
    ],
    [
        Input('inventory-report-btn', 'n_clicks'),
        Input('sales-report-btn', 'n_clicks'),
        Input('financial-report-btn', 'n_clicks')
    ],
    [State('selected-report-type', 'data')]
)
def update_selected_report(inv_clicks, sales_clicks, fin_clicks, current_selection):
    ctx_msg = ctx.triggered_id
    
    selected = current_selection
    if ctx_msg == 'inventory-report-btn':
        selected = 'inventory'
    elif ctx_msg == 'sales-report-btn':
        selected = 'sales'
    elif ctx_msg == 'financial-report-btn':
        selected = 'financial'
    
    default_style = {
        'textDecoration': 'none',
        'color': '#faf3e7',
        'fontWeight': 'normal',
        'backgroundColor': '#3d2f25',
        'cursor': 'pointer'
    }

    active_style = {
        'textDecoration': 'none',
        'color': '#3d2f25',
        'fontWeight': 'bold',
        'backgroundColor': '#faf3e7',
        'cursor': 'pointer',
        'borderLeft': '4px solid #3d2f25'
    }

    inv_style = active_style if selected == 'inventory' else default_style
    sales_style = active_style if selected == 'sales' else default_style
    fin_style = active_style if selected == 'financial' else default_style
    
    return selected, inv_style, sales_style, fin_style


@app.callback(
    Output('report-table-container', 'children'),
    [
        Input('selected-report-type', 'data'),
        Input('start-date', 'date'),
        Input('end-date', 'date')
    ]
)
def update_report_table(report_type, start_date, end_date):
    if not start_date or not end_date:
        return html.Div(
            "Please select a start and end date to generate the report.",
            className="text-center text-muted mt-5"
        )

    columns = []
    values = ()
    sql = ""
    
    try:
        if report_type == 'inventory':
            sql = """
                SELECT 
                    p.product_id,
                    p.product_name,
                    p.beginning_inventory
                        + COALESCE(purchase.total_purchased, 0)
                        - COALESCE("order".total_ordered, 0) AS current_stock
                FROM product p
                LEFT JOIN (
                    SELECT
                        product_id,
                        SUM(quantity_purchased) AS total_purchased
                    FROM components co
                    JOIN purchase pu ON co.purchase_id = pu.purchase_id
                    WHERE pu.arrival_date BETWEEN %s AND %s
                    GROUP BY product_id
                ) purchase ON p.product_id = purchase.product_id
                LEFT JOIN (
                    SELECT 
                        product_id,
                        SUM(quantity_ordered) AS total_ordered
                    FROM composition c
                    JOIN "order" o ON c.order_id = o.order_id
                    WHERE o.order_date BETWEEN %s AND %s
                    GROUP BY product_id
                ) "order" ON p.product_id = "order".product_id;
            """
            values = (start_date, end_date, start_date, end_date)
            columns = ["Product ID", "Product Name", "Current Stock"]
            
        elif report_type == 'sales':
            sql = """
                SELECT 
                    p.product_name,
                    SUM(c.quantity_ordered) AS total_units_sold
                FROM composition c
                JOIN product p ON c.product_id = p.product_id
                JOIN "order" o ON c.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s
                GROUP BY p.product_name
                ORDER BY total_units_sold DESC;
            """
            values = (start_date, end_date)
            columns = ["Product Name", "Total Units Sold"]
            
        elif report_type == 'financial':
            sql = """
                SELECT
                    COALESCE(SUM(c.quantity_ordered * p.selling_price), 0) as total_revenue,
                    COALESCE(SUM(c.quantity_ordered * p.supplied_price), 0) as total_expense,
                    COALESCE(SUM(c.quantity_ordered * p.selling_price) - SUM(c.quantity_ordered * p.supplied_price), 0) as net_profit
                FROM composition c
                JOIN product p ON c.product_id = p.product_id
                JOIN "order" o ON c.order_id = o.order_id
                JOIN "order-status" os ON o.status_id = os.status_id
                WHERE o.order_date BETWEEN %s AND %s
                  AND os.status_name = 'Delivered';
            """
            values = (start_date, end_date)
            columns = ["Total Revenue", "Total Expense", "Net Profit"]
        
        else:
            return html.Div("Invalid report type selected.")

        df = getDataFromDB(sql, values, columns)
        
        if df.empty:
            return html.Div(
                "No data found for the selected date range.",
                className="text-center text-muted mt-5"
            )

        if report_type == 'financial':
            df['Total Revenue'] = df['Total Revenue'].apply(lambda x: f"₱{x:,.2f}")
            df['Total Expense'] = df['Total Expense'].apply(lambda x: f"₱{x:,.2f}")
            df['Net Profit'] = df['Net Profit'].apply(lambda x: f"₱{x:,.2f}")

        return dbc.Table.from_dataframe(
            df,
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            style={
                "borderCollapse": "separate",
                "borderSpacing": "0",
                "borderRadius": "1rem",
                "overflow": "hidden",
            }
        )

    except Exception as e:
        return html.Div(f"Error generating report: {str(e)}", className="text-danger")
