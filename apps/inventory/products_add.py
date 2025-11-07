import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from app import app
from apps.commonmodules import makeNavbar

layout = dbc.Container(
    [
        makeNavbar(user_role="owner"),
        # === Page Title ===
        html.H1("Product Details", className="supplier-details-title mb-5"),

        # === Card ===
        dbc.Card(
            dbc.CardBody(
                [
                    # --- Product Name ---
                    html.Label("Product Name:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Foam A",
                        className="form-input mb-4",
                    ),

                    # --- Brand ---
                    html.Label("Brand:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Brand B",
                        className="form-input mb-4",
                    ),

                    # --- Selling Price (in Pesos) ---
                    html.Label("Selling Price (in Pesos):", className="form-label"),
                    dbc.Input(
                        type="number",
                        placeholder="ex. 2200",
                        className="form-input mb-4",
                    ),

                    # --- Description ---
                    html.Label("Description:", className="form-label"),
                    dbc.Input(
                        type="text",
                        placeholder="ex. Lorem Ipsum",
                        className="form-input mb-4",
                    ),

                    # --- Weight, Volumetric Weight, Stock Level ---
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Weight (in kg)"),
                                    dbc.Input(
                                        type="number",
                                        placeholder="ex. 4",
                                        className="form-input mb-4",
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Volumetric Weight"),
                                    dbc.Input(
                                        type="number",
                                        placeholder="ex. 2",
                                        className="form-input mb-4",
                                    ),
                                ],
                                width=4,
                            ),
                            dbc.Col(
                                [
                                    html.Label("Stock Level"),
                                    dbc.Input(
                                        type="number",
                                        placeholder="ex. 2200",
                                        className="form-input mb-4",
                                    ),
                                ],
                                width=4,
                            ),
                        ],
                        className="g-2",
                    ),

                    # --- Supplier ---
                    html.Label("Supplier"),
                    dbc.Select(
                        options=[
                            {"label": "Uratex", "value": "uratex"},
                            {"label": "Slumberland", "value": "slumberland"},
                            {"label": "King Koil", "value": "king_koil"},
                            {"label": "Magniflex", "value": "magniflex"},
                            {"label": "Tempur", "value": "tempur"},
                        ],
                        className="form-input mb-4",
                    ),

                    # --- Centered Submit + Delete Row ---
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
