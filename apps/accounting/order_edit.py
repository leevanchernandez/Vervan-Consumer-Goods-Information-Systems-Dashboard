import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),

            # === Page Title ===
            html.H1("Order Details", className="supplier-details-title mb-5"),

            # === Card ===
            dbc.Card(
                dbc.CardBody(
                    [
                        # --- Username ---
                        html.Label("Username:", className="form-label"),
                        dbc.Input(
                            type="text",
                            placeholder="ex. Juan Dela Cruz",
                            className="form-input mb-4",
                        ),

                        # --- Date Ordered ---
                        html.Label("Date Ordered:", className="form-label"),
                        html.Div(
                            dcc.DatePickerSingle(
                                id="date",
                                placeholder="Date",
                                display_format="YYYY-MM-DD",
                                className="pill-date-picker",
                            ),
                            style={"width": "100%", "display": "block"},                                                
                        ),
                        # --- Products Ordered (2 rows sample) ---
                        html.Label("Products Ordered:", className="form-label mb-3"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Select(
                                        options=[
                                            {"label": "Foam A", "value": "foam_a"},
                                            {"label": "Foam B", "value": "foam_b"},
                                        ],
                                        placeholder="Select Product",
                                        className="form-input mb-4",
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        type="number",
                                        placeholder="ex. 10 pcs",
                                        className="form-input mb-4",
                                    ),
                                    width=4,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "×",
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
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Select(
                                        options=[
                                            {"label": "Foam C", "value": "foam_c"},
                                            {"label": "Foam D", "value": "foam_d"},
                                        ],
                                        placeholder="Select Product",
                                        className="form-input mb-4",
                                    ),
                                    width=6,
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        type="number",
                                        placeholder="ex. 5 pcs",
                                        className="form-input mb-4",
                                    ),
                                    width=4,
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "×",
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
                        ),

                        # --- Add (+) Button ---
                        html.Div(
                            dbc.Button(
                                "+",
                                id="add-product-btn",
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
                            options=[
                                {"label": "Pending", "value": "pending"},
                                {"label": "Processing", "value": "processing"},
                                {"label": "Shipped", "value": "shipped"},
                                {"label": "Delivered", "value": "delivered"},
                                {"label": "Cancelled", "value": "cancelled"},
                            ],
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
                                        id="delete-checkbox",
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
                    ]
                ),
                className="supplier-details-card",
            ),
        ],
        fluid=True,
        className="supplier-details-container",
    )
