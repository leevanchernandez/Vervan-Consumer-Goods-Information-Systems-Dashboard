import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar

layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),
        # === Page Title ===
        html.H1("Upload Inventory", className="supplier-details-title mb-5"),

        # === Card ===
        dbc.Card(
            dbc.CardBody(
                [
                    # --- Product ID ---
                    html.Label("Product ID", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. 2001",
                        className="form-input mb-4",
                    ),

                    # --- Product Name ---
                    html.Label("Product Name", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Foam A",
                        className="form-input mb-4",
                    ),

                    # --- Date ---
                    html.Label("Date:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Today, October 15, 2002",
                        className="form-input mb-4",
                    ),

                    # --- Quantity Receive ---
                    html.Label("Quantity Receive", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. 2000",
                        className="form-input mb-4",
                    ),

                    # --- Remarks ---
                    html.Label("Remarks", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Lorem Ipsum",
                        className="form-input mb-4",
                    ),

                    # --- Centered Submit + Edit Row ---
                    dbc.Row(
                        [
                            dbc.Col(width=3),  # Spacer (left)
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
                                    id="edit-checkbox",
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
