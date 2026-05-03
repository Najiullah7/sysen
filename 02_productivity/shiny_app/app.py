# app.py
# Census Economic Data Shiny App
# Runs the Census API query on button click; part of SYSEN5381 productivity lab
# Tim Fraser

# UI and server are separated; the API runs only when the user clicks "Run query".
# API key is read only from the .env file in the shiny_app folder.

import os
from pathlib import Path
from typing import Optional

import pandas as pd
from dotenv import load_dotenv
from shiny import App, reactive, render, run_app, ui

from api_helpers import fetch_census_ecn

# .env lives in the same folder as this file (shiny_app).
_ENV_PATH = Path(__file__).resolve().parent / ".env"


def _get_api_key_from_env() -> Optional[str]:
    """Load .env from the shiny_app folder and return CENSUS_API_KEY."""
    if _ENV_PATH.is_file():
        load_dotenv(_ENV_PATH)
    return os.getenv("CENSUS_API_KEY") or None

# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
        ui.tags.style(
            """
            .content-wrapper { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }
            .title-block { margin-bottom: 1.5rem; }
            .title-block h1 { font-size: 1.75rem; font-weight: 600; color: #1a1a2e; margin-bottom: 0.35rem; }
            .title-block p { color: #4a4a68; font-size: 0.95rem; line-height: 1.5; margin: 0; }
            .card-like { background: #f8f9fa; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.25rem; }
            .status-ok { color: #0d6efd; }
            .status-err { color: #dc3545; }
            .btn-run { font-weight: 600; }
            """
        ),
    ),
    ui.div(
        ui.div(
            ui.div(
                ui.tags.h1("U.S. Economic Census Data"),
                ui.tags.p(
                    "Fetch establishment counts, total receipts, and employment by NAICS industry "
                    "from the Census Bureau API. The API key is read from the .env file in this folder. "
                    "Choose how many rows to load, then click Run query."
                ),
                class_="title-block",
            ),
            ui.div(
                ui.tags.h4("Inputs", style="margin-top: 0; margin-bottom: 0.75rem; font-size: 1rem;"),
                ui.input_numeric(
                    "row_limit",
                    "Number of rows",
                    value=10,
                    min=1,
                    max=500,
                    step=1,
                    width="120px",
                ),
                ui.input_action_button("run_button", "Run query", class_="btn-run"),
                class_="card-like",
            ),
            ui.div(
                ui.tags.h4("Status", style="margin-top: 0; margin-bottom: 0.5rem; font-size: 1rem;"),
                ui.output_ui("status"),
                class_="card-like",
            ),
            ui.div(
                ui.tags.h4("Results", style="margin-top: 0; margin-bottom: 0.5rem; font-size: 1rem;"),
                ui.output_data_frame("table"),
                class_="card-like",
            ),
            class_="content-wrapper",
        ),
        style="font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;",
    ),
    title="Census Economic Data",
)


# -----------------------------------------------------------------------------
# Server
# -----------------------------------------------------------------------------

def server(input, output, session):
    # Store (data, error_message) or None before any query has run.
    query_result = reactive.Value(None)

    # Run the API only when the user clicks the button.
    @reactive.Effect
    @reactive.event(input.run_button)
    def run_query():
        key = _get_api_key_from_env()
        limit = input.row_limit()
        if limit is None or limit < 1:
            limit = 10
        data, err = fetch_census_ecn(api_key=key, row_limit=int(limit))
        query_result.set((data, err))

    @render.ui
    def status():
        r = query_result.get()
        if r is None:
            return "Click “Run query” to fetch data."
        data, err = r
        if err:
            return ui.tags.span(err, class_="status-err")
        n = len(data) if data else 0
        return ui.tags.span(f"Loaded {n} row(s).", class_="status-ok")

    @render.data_frame
    def table():
        r = query_result.get()
        if r is None:
            return render.DataGrid(pd.DataFrame(), height="200px")
        data, err = r
        if err or not data:
            return render.DataGrid(pd.DataFrame(), height="200px")
        df = pd.DataFrame(data)
        return render.DataGrid(df, height="350px")


# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------

app = App(app_ui, server)

if __name__ == "__main__":
    run_app(app)
