# Screener.in Web Scraper & API

This project is a comprehensive web scraping tool designed to extract financial data from [Screener.in](https://www.screener.in/). It uses Selenium (specifically `undetected-chromedriver`) to navigate the site and handle authentication, and exposes the scraped data through a RESTful API built with FastAPI.

## Features

- **Automated Login**: Handles user authentication securely.
- **Company Search**: Search for companies by name.
- **Financial Data**: Extract Quarterly Results, Profit & Loss statements, and Peer comparisons.
- **Charts**: Capture screenshots of Price and PE charts.
- **Documents**: Retrieve links for Conference Calls and Announcements.
- **Custom Queries**: Run complex screener queries (e.g., "Market Cap > 500 AND PE < 15").
- **API Access**: All features are available via HTTP endpoints.

## Prerequisites

- Python 3.8+
- Google Chrome browser installed

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory.

2.  **Install Dependencies**:
    ```bash
    pip install -r scraper/requirements.txt
    ```

3.  **Configure Credentials**:
    Open `scraper/src/credentials.py` and update it with your Screener.in login details:
    ```python
    email = "your_email@example.com"
    password = "your_password"
    ```

## Usage

### 1. Start the API Server

Run the FastAPI server using `uvicorn` from the project root:

```bash
uvicorn scraper.src.server:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 2. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | Log in to Screener.in (happens automatically on first request if needed). |
| `GET` | `/search/{query}` | Search for a company by name (e.g., "Tata") then get the company url from the list. |
| `GET` | `/charts/{company_url}` | Get a screenshot of the price chart. |
| `GET` | `/pe_charts/{company_url}` | Get a screenshot of the PE chart. |
| `GET` | `/peers/{company_url}` | Get the peer comparison table text. |
| `GET` | `/quarterly_results/{company_url}` | Get quarterly results data. |
| `GET` | `/profit_loss/{company_url}` | Get profit and loss data. |
| `GET` | `/announcements/{company_url}` | Get recent announcements. |
| `GET` | `/concalls/{company_url}` | Get download links for conference calls. |
| `POST` | `/custom_query` | Run a custom screener query. Body: `{"query": "..."}` |

**Note**: `{company_url}` is usually the slug found in the URL or you can get it from /search/{query} (e.g., `Tata-Steel` for Tata Steel).

### 3. Run Automated Checks

To verify that all endpoints are working correctly, run the check script:

```bash
python scraper/src/check.py
```

## Project Structure

```
scraper/
├── requirements.txt    # Python dependencies
└── src/
    ├── check.py        # Script to test API endpoints
    ├── credentials.py  # User credentials configuration
    ├── server.py       # FastAPI server implementation
    └── utils.py        # Core scraping logic with Selenium
```

## Troubleshooting

- **Connection Errors**: If you see `urllib.error.URLError: <urlopen error [Errno 11001] getaddrinfo failed>`, check your internet connection. This often happens when `undetected-chromedriver` tries to download a patch.
- **Element Not Found**: Screener.in may change their layout. If XPaths fail, check `utils.py` and update the selectors.
