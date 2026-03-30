import webbrowser

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Apps
from app import app
from apps import adduser, home, commonmodules as cm, login, manageuser, edituser
from apps.dashboard import ownerdashboard, accountingdashboard, inventorydashboard
from apps.reports import reports
from apps.inventory import inventory, inventory_supplier, inventory_products, products_add, products_edit, supplier_edit
from apps.accounting import accounting, accounting_order, order_edit
from apps.transactions import transactions


app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='current_role', storage_type='session', data='public'),
        dcc.Store(id='current_user_id', storage_type='session'),
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
    
    error_403 = html.Div([
        html.H2("You do not have access to this page, try contacting the owner if this is a mistake", className="text-danger text-center")
    ], className="p-5")

    if pathname == '/home' or pathname == "/":
        layout = home.layout
    elif pathname == '/login':
        layout = login.layout
    elif pathname == '/users' or pathname == '/users/manage':
        if user_role == 'owner':
            layout = manageuser.layout
        else:
            return error_403
    elif pathname == '/users/add' or pathname == '/adduser':
        if user_role == 'owner':
            layout = adduser.layout
        else:
            return error_403
    elif pathname == '/users/edit':
        if user_role == 'owner':
            layout = edituser.layout
        else:
            return error_403
    elif pathname == '/ownerdashboard':
        if user_role == 'owner':
            layout = ownerdashboard.layout
        else:
            return error_403
    elif pathname == '/reports':
        if user_role == 'owner':
            layout = reports.layout
        else:
            return error_403
    elif pathname == '/inventory':
        if user_role in ['owner', 'inventory']:
            layout = inventory.layout
        else:
            return error_403
    elif pathname == '/inventory/supplier':
        if user_role in ['owner', 'inventory']:
            layout = inventory_supplier.layout
        else:
            return error_403
    elif pathname == '/inventory/supplier/edit':
        if user_role in ['owner', 'inventory']:
            layout = supplier_edit.layout
        else:
            return error_403
    elif pathname == '/inventory/products':
        if user_role in ['owner', 'inventory']:
            layout = inventory_products.layout
        else:
            return error_403
    elif pathname == '/inventory/products/add':
        if user_role in ['owner', 'inventory']:
            layout = products_add.layout
        else:
            return error_403
    elif pathname == '/inventory/products/edit':
        if user_role in ['owner', 'inventory']:
            layout = products_edit.layout
        else:
            return error_403
    elif pathname == '/inventorydashboard':
        if user_role in ['owner', 'inventory']:
            layout = inventorydashboard.layout
        else:
            return error_403
    elif pathname == '/accountingdashboard':
        if user_role in ['owner', 'accounting']:
            layout = accountingdashboard.layout
        else:
            return error_403
    elif pathname == '/accounting':
        if user_role in ['owner', 'accounting']:
            layout = accounting.layout
        else:
            return error_403
    elif pathname == '/accounting/order':
        if user_role in ['owner', 'accounting']:
            layout = accounting_order.layout
        else:
            return error_403
    elif pathname == '/accounting/order/edit':
        if user_role in ['owner', 'accounting']:
            layout = order_edit.layout
        else:
            return error_403
    elif pathname == '/transactions':
        if user_role in ['owner', 'accounting']:
            layout = transactions.layout
        else:
            return error_403
    else:
        return html.H1("404: Page not found", className="text-center text-danger")
    
    if callable(layout):
        return layout(user_role=user_role, pathname=pathname)
    else:
        return layout

# Navbar callback removed as it is now handled per page

@app.callback(
    [Output("logout_modal", "is_open"),
     Output("current_role", "data", allow_duplicate=True),
     Output("current_user_id", "data", allow_duplicate=True)],
    [Input("logout_btn", "n_clicks"),
     Input("logout_cancel", "n_clicks"),
     Input("logout_confirm", "n_clicks")],
    [State("logout_modal", "is_open")],
    prevent_initial_call=True
)
def toggle_logout_modal(n_btn, n_cancel, n_confirm, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return is_open, dash.no_update, dash.no_update
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    if button_id == "logout_btn":
        if n_btn and n_btn > 0:
            return True, dash.no_update, dash.no_update
    elif button_id == "logout_cancel":
        if n_cancel and n_cancel > 0:
            return False, dash.no_update, dash.no_update
    elif button_id == "logout_confirm":
        if n_confirm and n_confirm > 0:
            return False, "public", None
    
    return is_open, dash.no_update, dash.no_update


if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run(debug=False)
