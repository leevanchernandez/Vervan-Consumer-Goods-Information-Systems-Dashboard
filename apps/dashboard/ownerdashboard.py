import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB

def layout(user_role="owner", pathname=None):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role, pathname=pathname),
            # Greeting
            html.H1(
                "Hello!", 
                id="owner_greeting",
                style={"color": "#7a5d60", "fontWeight":"bold"}
            ),
            html.H6(
                "This is what's happening in your store this month.",
                style={"color": "#7a5d60"},
            ),
            
            # Dashboard Cards
            dbc.Row(
                [
                    # Card 1: Total Revenue (formerly Total Sales)
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Total Revenue", style={"textAlign": "center"}),
                                    html.H1("₱0.00", id="total_revenue_card", style={"textAlign": "center"}),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "center",
                                    "height": "100%",
                                },
                            ),
                            style={
                                "backgroundColor": "#564e6d",
                                "color": "#fffaf3",
                                "borderRadius": "2rem",
                                "minHeight": "180px",
                            },
                        ),
                        width=4,
                    ),
                    # Card 2: Net Income (formerly Total Revenue)
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Net Income", style={"textAlign": "center"}),
                                    html.H1("₱0.00", id="net_income_card", style={"textAlign": "center"}),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "center",
                                    "height": "100%",
                                },
                            ),
                            style={
                                "backgroundColor": "#c69a9a",
                                "color": "#fffaf3",
                                "borderRadius": "2rem",
                                "minHeight": "180px",
                            },
                        ),
                        width=4,
                    ),
                    # Card 3: Total Orders
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Total Orders", style={"textAlign": "center"}),
                                    html.H1("0", id="total_orders_card", style={"textAlign": "center"}),
                                ],
                                style={
                                    "display": "flex",
                                    "flexDirection": "column",
                                    "justifyContent": "center",
                                    "height": "100%",
                                },
                            ),
                            style={
                                "backgroundColor": "#977b61",
                                "color": "#fffaf3",
                                "borderRadius": "2rem",
                                "minHeight": "180px",
                            },
                        ),
                        width=4,
                    ),
                ],
                className="mt-4",
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )

@app.callback(
    [Output("owner_greeting", "children"),
     Output("total_revenue_card", "children"),
     Output("net_income_card", "children"),
     Output("total_orders_card", "children")],
    [Input("current_user_id", "data")]
)
def update_owner_dashboard(user_id):
    # Default values
    greeting = "Hello!"
    revenue_text = "₱0.00"
    net_income_text = "₱0.00"
    orders_text = "0"
    
    import datetime
    today = datetime.date.today()
    current_month = today.month
    current_year = today.year

    # 1. Update Greeting
    if user_id:
        sql_user = "SELECT staff_name FROM staff WHERE staff_id = %s"
        df_user = getDataFromDB(sql_user, [user_id], ["staff_name"])
        if not df_user.empty:
            greeting = f"Hello, {df_user.iloc[0]['staff_name']}!"

    # 2. Calculate Total Revenue (This Month)
    sql_revenue = """
        SELECT SUM(c.quantity_ordered * p.selling_price) AS total_revenue
        FROM composition c
        JOIN product p ON c.product_id = p.product_id
        JOIN "order" o ON c.order_id = o.order_id
        WHERE o.status_id != COALESCE((SELECT status_id FROM "order-status" WHERE status_name = 'Returned'), -1)
          AND EXTRACT(MONTH FROM o.order_date) = %s 
          AND EXTRACT(YEAR FROM o.order_date) = %s;
    """
    df_rev = getDataFromDB(sql_revenue, [current_month, current_year], ["total_revenue"])
    total_revenue = 0.0
    if not df_rev.empty and df_rev.iloc[0]["total_revenue"] is not None:
        total_revenue = float(df_rev.iloc[0]["total_revenue"])
    
    revenue_text = f"₱{total_revenue:,.2f}"

    # 3. Calculate Total Expenses (This Month)
    # Need to join with purchase table to get date
    sql_expenses = """
        SELECT SUM(c.quantity_purchased * p.supplied_price) AS total_expenses
        FROM components c
        JOIN product p ON c.product_id = p.product_id
        JOIN purchase pu ON c.purchase_id = pu.purchase_id
        WHERE EXTRACT(MONTH FROM pu.arrival_date) = %s 
          AND EXTRACT(YEAR FROM pu.arrival_date) = %s;
    """
    df_exp = getDataFromDB(sql_expenses, [current_month, current_year], ["total_expenses"])
    total_expenses = 0.0
    if not df_exp.empty and df_exp.iloc[0]["total_expenses"] is not None:
        total_expenses = float(df_exp.iloc[0]["total_expenses"])

    # 4. Calculate Net Income
    net_income = total_revenue - total_expenses
    net_income_text = f"₱{net_income:,.2f}"

    # 5. Calculate Total Orders (This Month)
    sql_orders = """
        SELECT COUNT(*) as order_count 
        FROM "order" 
        WHERE status_id != COALESCE((SELECT status_id FROM "order-status" WHERE status_name = 'Cancelled'), -1)
          AND EXTRACT(MONTH FROM order_date) = %s 
          AND EXTRACT(YEAR FROM order_date) = %s;
    """
    df_orders = getDataFromDB(sql_orders, [current_month, current_year], ["order_count"])
    if not df_orders.empty:
        orders_text = str(df_orders.iloc[0]["order_count"])

    return greeting, revenue_text, net_income_text, orders_text

