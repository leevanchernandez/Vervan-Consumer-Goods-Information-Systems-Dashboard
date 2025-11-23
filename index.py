import webbrowser

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Apps
from app import app
from apps import adduser, home, commonmodules as cm, login
from apps.dashboard import ownerdashboard, accountingdashboard, inventorydashboard
from apps.reports import reports
from apps.inventory import inventory, inventory_supplier, inventory_products, products_add, products_edit, supplier_edit
from apps.accounting import accounting, accounting_order, order_edit
from apps.transactions import transactions


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='current_role', storage_type='session', data='public'),
        # html.Div(id='navbar-container'), # Removed global navbar
        html.Div(id='page-content'),
    ]
)

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'),
     Input('current_role', 'data')]
)

def displaypage(pathname, user_role):
    if user_role is None:
        user_role = "public"

    layout = None
    
    if pathname == '/home' or pathname == "/":
        layout = home.layout
    elif pathname == '/login':
        layout = login.layout
    elif pathname == '/adduser':
        layout = adduser.layout
    elif pathname == '/ownerdashboard':
        layout = ownerdashboard.layout
    elif pathname == '/reports':
        layout = reports.layout
    elif pathname == '/inventory':
        layout = inventory.layout
    elif pathname == '/inventory/supplier':
        layout = inventory_supplier.layout
    elif pathname == '/inventory/supplier/edit':
        layout = supplier_edit.layout
    elif pathname == '/inventory/products':
        layout = inventory_products.layout
    elif pathname == '/inventory/products/add':
        layout = products_add.layout
    elif pathname == '/inventory/products/edit':
        layout = products_edit.layout
    elif pathname == '/inventorydashboard':
        layout = inventorydashboard.layout
    elif pathname == '/accountingdashboard':
        layout = accountingdashboard.layout
    elif pathname == '/accounting':
        layout = accounting.layout
    elif pathname == '/accounting/order':
        layout = accounting_order.layout
    elif pathname == '/accounting/order/edit':
        layout = order_edit.layout
    elif pathname == '/transactions':
        layout = transactions.layout
    else:
        return html.H1("404: Page not found", className="text-center text-danger")
    
    if callable(layout):
        return layout(user_role=user_role)
    else:
        return layout

# Navbar callback removed as it is now handled per page


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run(debug=True)
