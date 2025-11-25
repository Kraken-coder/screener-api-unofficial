import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def check_endpoint(method, endpoint, data=None, description=""):
    url = f"{BASE_URL}{endpoint}"
    print(f"Checking {description} ({method} {url})...")
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print(f"SUCCESS: {description}")
            # Print a snippet of the response
            content = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"Response: {content}\n")
            return response
        else:
            print(f"FAILURE: {description} - Status Code: {response.status_code}")
            print(f"Response: {response.text}\n")
            return None
    except Exception as e:
        print(f"ERROR: {description} - {e}\n")
        return None

def main():
    # 1. Login
    check_endpoint("POST", "/login", description="Login")

    # 2. Search for a company
    search_response = check_endpoint("GET", "/search/Tata", description="Search Company")
    
    company_url = "Tata-Steel/" # Default fallback
    if search_response and search_response.json():
        # Assuming the first result is relevant
        results = search_response.json()
        if results and isinstance(results, list) and len(results) > 0:
            company_url = results[0]['url'].strip('/')
            print(f"Using company URL: {company_url}\n")

    # 3. Get Charts
    check_endpoint("GET", f"/charts/{company_url}", description="Get Charts (Image)")

    # 4. Get PE Charts
    check_endpoint("GET", f"/pe_charts/{company_url}", description="Get PE Charts (Image)")

    # 5. Get Peers
    check_endpoint("GET", f"/peers/{company_url}", description="Get Peers")

    # 6. Get Quarterly Results
    check_endpoint("GET", f"/quarterly_results/{company_url}", description="Get Quarterly Results")

    # 7. Get Profit Loss
    check_endpoint("GET", f"/profit_loss/{company_url}", description="Get Profit Loss")

    # 8. Get Announcements
    check_endpoint("GET", f"/announcements/{company_url}", description="Get Announcements")

    # 9. Get Concalls
    check_endpoint("GET", f"/concalls/{company_url}", description="Get Concalls Links")

    # 10. Custom Query
    query_payload = {
        "query": "Market capitalization > 500 AND\nPrice to earning < 15 AND\nReturn on capital employed > 22%"
    }
    check_endpoint("POST", "/custom_query", data=query_payload, description="Run Custom Query")

if __name__ == "__main__":
    print("Starting checks... Ensure the server is running on port 8000.")
    main()
