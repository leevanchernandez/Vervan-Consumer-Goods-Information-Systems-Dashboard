import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar
layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),
        # === Page Title ===
        html.H1("Supplier Details", className="supplier-details-title mb-5"),

        # === Card ===
        dbc.Card(
            dbc.CardBody(
                [
                    # --- Supplier Name ---
                    html.Label("Supplier Name:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Juan Dela Cruz",
                        className="form-input mb-4",
                    ),

                    # --- Contact Number ---
                    html.Label("Contact Number:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. 09xxxxxxxxx",
                        className="form-input mb-4",
                    ),

                    # --- Address ---
                    html.Label("Address:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. 22 Cornelia Street, Quezon City",
                        className="form-input mb-4",
                    ),

                    # --- Supplier Product ---
                    html.Label("Supplier Product:", className="form-label"),
                    dbc.Select(
                        options=[
                            {"label": "Fabric", "value": "fabric"},
                            {"label": "Packaging Material", "value": "packaging"},
                            {"label": "Polymer Tubes", "value": "polymer_tubes"},
                            {"label": "Screws and Rivets", "value": "screws_rivets"},
                        ],
                        placeholder="Select a product...",
                        className="form-input mb-4",
                    ),

                    # --- Price ---
                    html.Label("Price (in PHP):", className="form-label"),
                    dbc.Input(
                        type="number",
                        placeholder="2200",
                        className="form-input mb-4",
                    ),
                                        dbc.Row(
                        [
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
