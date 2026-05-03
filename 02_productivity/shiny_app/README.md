# Census Economic Data Shiny App

> This Shiny for Python app runs your Census API query on demand. It reads the API key from a `.env` file in the `shiny_app` folder, lets you choose how many rows to fetch, and displays U.S. Economic Census data in a table. Errors and status messages are shown clearly so you can fix missing keys or network issues.

---

## 📋 Overview

The app calls the U.S. Census Bureau’s Economic Census API (ECN Basic) and displays NAICS industry data: establishment counts, total receipts, and employment. The query runs **only when you click “Run query”**. The API key is read **only from the `.env` file** in the `shiny_app` folder (no manual entry in the app).

---

## 📦 Prerequisites

- **Python 3.9+**
- A **Census API key** from [api.census.gov](https://api.census.gov/data/key_signup.html)

---

## 🚀 Getting Started

### 1. Install dependencies

From the `shiny_app` folder:

```bash
pip install -r requirements.txt
```

### 2. Configure API key

Create a `.env` file **in the `shiny_app` folder** (same folder as `app.py`) with:

```
CENSUS_API_KEY=your_census_api_key_here
```

Replace `your_census_api_key_here` with the key from the Census Bureau.

> ⚠️ **Important:** Do not commit `.env` to version control. Add `.env` to your `.gitignore`.

### 3. Run the app

```bash
python app.py
```

Then open the URL shown in the terminal (e.g. `http://127.0.0.1:8000`) in your browser.

---

## 📖 Usage

1. **Number of rows:** Choose 1–500 (default 10).
2. Click **Run query** to fetch data.
3. Check **Status** for success or error messages; view **Results** in the table below.

---

## 🔧 Configuration

| Item        | Description |
|------------|-------------|
| API key    | Set in the `.env` file in the `shiny_app` folder as `CENSUS_API_KEY`. |
| Row limit  | Controlled by the “Number of rows” input (1–500). |

---

## ⚠️ Error handling

The app handles:

- **Missing or invalid API key:** Message asking you to set `CENSUS_API_KEY` in the `.env` file in the `shiny_app` folder.
- **Network/API errors:** Timeouts and connection errors with clear messages.
- **Empty or unexpected results:** Shows an empty table and a status message where applicable.

---

## 📁 Files

| File               | Purpose |
|--------------------|--------|
| `app.py`           | Shiny UI and server; runs the app and renders the table/status. |
| `api_helpers.py`   | Census API request and error handling (used by `app.py`). |
| `requirements.txt` | Python dependencies (Shiny, requests, python-dotenv, pandas). |

---

## 💡 Example

After clicking **Run query** with a valid key and 10 rows:

- **Status:** “Loaded 10 row(s).”
- **Results:** A table with columns such as `NAICS2022`, `NAICS2022_LABEL`, `NAME`, `GEO_ID`, `ESTAB`, `RCPTOT`, `EMP`.

If the key is missing, **Status** will show: “No API key found. Set CENSUS_API_KEY in the .env file in the shiny_app folder.”
