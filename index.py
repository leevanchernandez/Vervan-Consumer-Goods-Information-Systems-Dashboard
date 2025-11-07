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

# Test comment
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='navbar-container'),
        html.Div(id='page-content'),
    ]
)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)

def displaypage(pathname):
    if pathname == '/home' or pathname == "/":
        return home.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/adduser':
        return adduser.layout
    elif pathname == '/ownerdashboard':
        return ownerdashboard.layout
    elif pathname == '/reports':
        return reports.layout
    elif pathname == '/inventory':
        return inventory.layout
    elif pathname == '/inventory/supplier':
        return inventory_supplier.layout
    elif pathname == '/inventory/supplier/edit':
        return supplier_edit.layout
    elif pathname == '/inventory/products':
        return inventory_products.layout
    elif pathname == '/inventory/products/add':
        return products_add.layout
    elif pathname == '/inventory/products/edit':
        return products_edit.layout
    elif pathname == '/inventorydashboard':
        return inventorydashboard.layout
    elif pathname == '/accountingdashboard':
        return accountingdashboard.layout
    elif pathname == '/accounting':
        return accounting.layout
    elif pathname == '/accounting/order':
        return accounting_order.layout
    elif pathname == '/accounting/order/edit':
        return order_edit.layout
    elif pathname == '/transactions':
        return transactions.layout
    else:
        return html.H1("404: Page not found", className="text-center text-danger")
"""
@app.callback(
   Output('navbar-container', 'children'),
   Input('url', 'pathname') 
)

# [todo] For now just set user_role to owner
def displayNavbar(pathname):
    user_role = "owner"
    
    return cm.makeNavbar(user_role=user_role)
"""

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run(debug=True)

