import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from apps.commonmodules import makeNavbar
from apps.dbconnect import getDataFromDB
from datetime import date

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),
            html.H1("Transaction History", className="mb-4"),
            
            dbc.Row(
                [
                    # ==== LEFT COLUMN ====
                    dbc.Col(
                        [
                            # Report Type header
                            html.H5(
                                "Report Type:",
                                className="mb-2",
                                style={"color": "#3d2f25"}
                            ),

                            # Report Type card
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.RadioItems(
                                            id="report-type-selector",
                                            options=[
                                                {"label": "Total Revenues", "value": "revenues"},
                                                {"label": "Total Expenses", "value": "expenses"},
                                                {"label": "Net Income", "value": "net_income"},
                                            ],
                                            value="revenues",
                                            labelStyle={
                                                "display": "block",
                                                "marginBottom": "10px",
                                                "cursor": "pointer",
                                            },
                                            inputStyle={"marginRight": "10px"},
                                            style={"fontSize": "1.1rem"}
                                        ),
                                    ],
                                    style={"color": "#faf3e7"},  # ← off-white text
                                ),
                                className="mb-3 report-card",
                            ),

                            # Parameters header
                            html.H5(
                                "Parameters:",
                                className="mb-2",
                                style={"color": "#3d2f25"}
                            ),

                            # Parameters card
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Label("Start Date", className="mb-1"),
                                        html.Div(
                                            dcc.DatePickerSingle(
                                                id="start-date",
                                                placeholder="Start Date",
                                                display_format="YYYY-MM-DD",
                                                className="pill-date-picker mb-3",
                                                date=date(date.today().year, 1, 1),
                                            ),
                                            style={"width": "100%"},
                                        ),

                                        html.Label("End Date", className="mb-1"),
                                        html.Div(
                                            dcc.DatePickerSingle(
                                                id="end-date",
                                                placeholder="End Date",
                                                display_format="YYYY-MM-DD",
                                                className="pill-date-picker",
                                                date=date.today(),
                                            ),
                                            style={"width": "100%"},
                                        ),
                                    ],
                                    style={"color": "#faf3e7"},  # ← off-white text
                                ),
                                className="report-card",
                            ),
                        ],
                        width=3,
                    ),

                    # ==== RIGHT COLUMN ====
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        id="transaction-result-container",
                                        className="d-flex flex-column align-items-center justify-content-center",
                                        style={"height": "100%", "minHeight": "200px"},
                                    )
                                ),
                                style={
                                    "borderRadius": "2rem",
                                    "backgroundColor": "#faf3e7",
                                    "padding": "2rem",
                                    "minHeight": "300px",
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
    Output("transaction-result-container", "children"),
    [
        Input("report-type-selector", "value"),
        Input("start-date", "date"),
        Input("end-date", "date"),
    ]
)
def update_transaction_report(report_type, start_date, end_date):
    if not start_date or not end_date:
        return html.H3("Please select a date range.", className="text-muted")

    result_value = 0.0
    title = ""

    try:
        if report_type == "revenues":
            title = "Total Revenues"
            sql = """
                SELECT 
                    SUM(c.quantity_ordered * p.selling_price) AS total_revenue
                FROM composition c
                JOIN product p ON c.product_id = p.product_id
                JOIN "order" o ON c.order_id = o.order_id
                WHERE o.order_date BETWEEN %s AND %s;
            """
            df = getDataFromDB(sql, [start_date, end_date], ["total_revenue"])
            if not df.empty and df.iloc[0]["total_revenue"] is not None:
                result_value = float(df.iloc[0]["total_revenue"])

        elif report_type == "expenses":
            title = "Total Expenses"
            sql = """
                SELECT 
                    SUM(c.quantity_purchased * p.supplied_price) AS total_expenses
                FROM components c
                JOIN product p ON c.product_id = p.product_id
                JOIN purchase pu ON c.purchase_id = pu.purchase_id
                WHERE pu.arrival_date BETWEEN %s AND %s;
            """
            df = getDataFromDB(sql, [start_date, end_date], ["total_expenses"])
            if not df.empty and df.iloc[0]["total_expenses"] is not None:
                result_value = float(df.iloc[0]["total_expenses"])

        elif report_type == "net_income":
            title = "Net Income"
            sql = """
                SELECT 
                    COALESCE(revenue.total_revenue, 0) - COALESCE(expense.total_expenses, 0) AS net_income
                FROM
                    (SELECT SUM(c.quantity_ordered * p.selling_price) AS total_revenue
                     FROM composition c
                     JOIN product p ON c.product_id = p.product_id
                     JOIN "order" o ON c.order_id = o.order_id
                     WHERE o.order_date BETWEEN %s AND %s) AS revenue,
                    (SELECT SUM(c.quantity_purchased * p.supplied_price) AS total_expenses
                     FROM components c
                     JOIN product p ON c.product_id = p.product_id
                     JOIN purchase pu ON c.purchase_id = pu.purchase_id
                     WHERE pu.arrival_date BETWEEN %s AND %s) AS expense;
            """
            df = getDataFromDB(
                sql,
                [start_date, end_date, start_date, end_date],
                ["net_income"]
            )
            if not df.empty and df.iloc[0]["net_income"] is not None:
                result_value = float(df.iloc[0]["net_income"])

        formatted_value = f"₱ {result_value:,.2f}"

        color = "#28a745" if result_value >= 0 else "#dc3545"
        if report_type == "expenses":
            color = "#3d2f25"
        if report_type == "net_income":
            color = "#28a745" if result_value >= 0 else "#dc3545"

        return [
            html.H2(title, className="mb-4", style={"color": "#7a5d60"}),
            html.H1(
                formatted_value,
                style={
                    "fontSize": "4rem",
                    "fontWeight": "bold",
                    "color": color,
                },
            ),
            html.P(
                f"Period: {start_date} to {end_date}",
                className="mt-3 text-muted",
            )
        ]

    except Exception as e:
        return dbc.Alert(f"Error calculating report: {str(e)}", color="danger")
