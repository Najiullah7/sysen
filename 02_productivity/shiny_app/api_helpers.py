# api_helpers.py
# Census API helper for Shiny app
# Fetches U.S. Economic Census data; used by app.py
# Tim Fraser

# Centralizes API request and error handling. Does not load .env or resolve keys;
# the app passes the resolved API key when calling fetch_census_ecn.

from typing import Optional

import requests

# Default Census Economic Census (ECN Basic) endpoint and variables
CENSUS_BASE_URL = "https://api.census.gov/data/2022/ecnbasic"
DEFAULT_VARS = "NAICS2022,NAICS2022_LABEL,NAME,GEO_ID,ESTAB,RCPTOT,EMP"
DEFAULT_GEO = "us:*"


def fetch_census_ecn(
    api_key: Optional[str] = None,
    row_limit: int = 10,
    variables: str = DEFAULT_VARS,
    geography: str = DEFAULT_GEO,
) -> tuple[Optional[list[dict]], Optional[str]]:
    """
    Fetch Economic Census data from the Census Bureau API.

    Parameters
    ----------
    api_key : str or None
        Census API key. Must be provided by the caller (e.g. from user input or .env).
    row_limit : int
        Maximum number of data rows to return (1–500).
    variables : str
        Comma-separated variable names to request.
    geography : str
        Geography clause, e.g. "us:*" for United States.

    Returns
    -------
    (data, error_message) : tuple
        data: list of dicts (one per row) or None on failure.
        error_message: str with user-friendly error, or None if no error.
    """
    key = (api_key or "").strip()
    if not key:
        return None, "No API key found. Set CENSUS_API_KEY in the .env file in the shiny_app folder."

    # Clamp row limit to a reasonable range (API returns many rows; we slice)
    limit = max(1, min(500, int(row_limit)))

    params = {
        "get": variables,
        "for": geography,
        "key": key,
    }

    try:
        response = requests.get(CENSUS_BASE_URL, params=params, timeout=30)
    except requests.exceptions.Timeout:
        return None, "Request timed out. Check your connection and try again."
    except requests.exceptions.ConnectionError:
        return None, "Network error. Check your internet connection."
    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {str(e)}"

    if response.status_code != 200:
        try:
            body = response.json()
            msg = body.get("message", body.get("error", response.text[:200]))
        except Exception:
            msg = response.text[:200] if response.text else f"HTTP {response.status_code}"
        return None, f"API error (HTTP {response.status_code}): {msg}"

    try:
        raw = response.json()
    except ValueError:
        return None, "Invalid response: API did not return valid JSON."

    if not raw or not isinstance(raw, list):
        return None, "Unexpected response: empty or invalid format."

    # First row is headers, rest is data
    if len(raw) < 2:
        return [], None  # No data rows; show empty table

    headers = raw[0]
    if not all(isinstance(h, str) for h in headers):
        return None, "Unexpected response: invalid header row."

    rows = raw[1 : limit + 1]
    data = [dict(zip(headers, row)) for row in rows]
    return data, None
