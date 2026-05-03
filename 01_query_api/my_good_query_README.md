# my_good_query.py

> This script fetches U.S. Economic Census data from the Census Bureau API (Application Programming Interface). It helps you retrieve establishment counts, total receipts, and employment figures by NAICS (North American Industry Classification System) industry code. Run the script to see the first 10 rows of 2022 Economic Census data for the United States.

---

## 📋 Overview

`my_good_query.py` calls the U.S. Census Bureau’s Economic Census API and prints a small sample of data. It uses your Census API key from a `.env` file so the key never appears in the code.

---

## 📦 Prerequisites

Before running the script, ensure you have:

- **Python 3** installed
- **Required packages**: `requests`, `python-dotenv`
- A **Census API key** from [api.census.gov](https://api.census.gov/data/key_signup.html)

---

## 🔧 Configuration

1. Create a `.env` file in the same folder as `my_good_query.py`.
2. Add your Census API key:

   ```
   CENSUS_API_KEY=your_api_key_here
   ```

3. Replace `your_api_key_here` with the key you received from the Census Bureau.

> ⚠️ **Important:** Never commit your `.env` file to version control. Add `.env` to your `.gitignore`.

---

## 🚀 Getting Started

1. Install dependencies:

   ```bash
   pip install requests python-dotenv
   ```

2. Add your Census API key to `.env` (see [Configuration](#-configuration) above).
3. Run the script:

   ```bash
   python my_good_query.py
   ```

---

## 📖 Usage

Run the script from the `01_query_api` directory:

```bash
python my_good_query.py
```

No command-line arguments are required. The script loads your API key from `.env`, requests data from the Census API, and prints the first 10 rows.

---

## 💡 Example Output

If the request succeeds, you’ll see something like:

```
Status code: 200
{'NAICS2022': '11', 'NAICS2022_LABEL': 'Agriculture, Forestry, Fishing and Hunting', 'NAME': 'United States', 'GEO_ID': '0100000US', 'ESTAB': '...', 'RCPTOT': '...', 'EMP': '...'}
{'NAICS2022': '21', 'NAICS2022_LABEL': 'Mining, Quarrying, and Oil and Gas Extraction', ...}
...
```

If there is an error (for example, an invalid or missing API key), the script will raise an exception and print details.

---

## 📖 Data Fields

| Field        | Description                                              |
|-------------|----------------------------------------------------------|
| `NAICS2022` | Industry code (NAICS 2022)                               |
| `NAICS2022_LABEL` | Human-readable industry name                       |
| `NAME`      | Geographic area (here: United States)                    |
| `GEO_ID`    | Census geographic identifier                            |
| `ESTAB`     | Number of establishments                                 |
| `RCPTOT`    | Total receipts ($1,000)                                  |
| `EMP`       | Employment (mid-March pay period)                        |

---

## 💡 Tips

- To change how many rows are printed, edit the slice `data[1:11]` in the script (for example, `data[1:51]` for 50 rows).
- The script uses the 2022 Economic Census Basic (`ecnbasic`) dataset. See [Census API documentation](https://www.census.gov/data/developers/data-sets/economic-census.html) for other datasets and parameters.
