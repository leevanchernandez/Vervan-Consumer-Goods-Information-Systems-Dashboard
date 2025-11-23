import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from app import app
from apps.commonmodules import makeNavbar

def layout(user_role="owner"):
    return dbc.Container(
        [
            makeNavbar(user_role=user_role),
            dbc.Row(
                [
                    # ==== LEFT COLUMN ====
                    dbc.Col(
                        [
                            html.H5("Report Type:", className="mb-2", style={"color": "#3d2f25"}),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("Inventory Report", id="inventory-report", className="report-link mb-2"),
                                        html.Div("Sales Report", id="sales-report", className="report-link mb-2"),
                                        html.Div("Financial Report", id="financial-report", className="report-link"),
                                    ]
                                ),
                                className="mb-3 report-card",
                            ),

                            html.H5("Parameters:", className="mb-2", style={"color": "#3d2f25"}),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    dcc.DatePickerSingle(
                                                        id="start-date",
                                                        placeholder="Start Date",
                                                        display_format="YYYY-MM-DD",
                                                        className="pill-date-picker mb-4",
                                                    ),
                                                    style={"width": "100%"},                                                
                                                ),
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
                            ),
                        ],
                        width=3,
                    ),

                    # ==== RIGHT COLUMN ====
                    dbc.Col(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    dbc.Table(
                                        [
                                            html.Thead(
                                                html.Tr(
                                                    [
                                                        html.Th("Column 1"),
                                                        html.Th("Column 2"),
                                                        html.Th("Column 3"),
                                                    ]
                                                )
                                            ),
                                            html.Tbody(
                                                [
                                                    html.Tr(
                                                        [
                                                            html.Td("Value 1"),
                                                            html.Td("Value 2"),
                                                            html.Td("Value 3"),
                                                        ]
                                                    ),
                                                    html.Tr(
                                                        [
                                                            html.Td("Value 1"),
                                                            html.Td("Value 2"),
                                                            html.Td("Value 3"),
                                                        ]
                                                    ),
                                                    html.Tr(
                                                        [
                                                            html.Td("Value 1"),
                                                            html.Td("Value 2"),
                                                            html.Td("Value 3"),
                                                        ]
                                                    ),
                                                ]
                                            ),
                                        ],
                                        bordered=True,
                                        hover=True,
                                        responsive=True,
                                        style={
                                            "borderCollapse": "separate",
                                            "borderSpacing": "0",
                                            "borderRadius": "1rem",
                                            "overflow": "hidden",
                                        },
                                    )
                                ),
                                style={
                                    "borderRadius": "2rem",
                                    "backgroundColor": "#faf3e7",
                                    "padding": "2rem",
                                },
                            ),
                        ],
                        width=9,
                        style={"height": "300px"},
                    ),
                ],
                className="g-3 mt-4",
            ),
        ],
        fluid=True,
        style={"padding": "2rem"},
    )
