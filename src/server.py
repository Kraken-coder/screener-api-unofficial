from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import utils
import os

app = FastAPI()

# Global driver instance
driver = None

class QueryRequest(BaseModel):
    query: str

def get_driver():
    global driver
    if driver is None:
        # Auto-login if driver is not active
        print("Driver not initialized. Logging in...")
        driver = utils.login()
    return driver

@app.post("/login")
def login_endpoint():
    global driver
    if driver is None:
        driver = utils.login()
    return {"status": "logged in"}

@app.get("/search/{query}")
def search_company(query: str):
    response = utils.find_company_codes(query)
    return response.json()

@app.get("/charts/{company_url:path}")
def get_charts(company_url: str):
    driver = get_driver()
    utils.get_charts(driver, company_url)
    if os.path.exists("chart.png"):
        return FileResponse("chart.png")
    raise HTTPException(status_code=404, detail="Chart not found")

@app.get("/pe_charts/{company_url:path}")
def get_pe_charts(company_url: str):
    driver = get_driver()
    utils.get_pe_charts(driver, company_url)
    if os.path.exists("chart.png"):
        return FileResponse("chart.png")
    raise HTTPException(status_code=404, detail="Chart not found")

@app.get("/peers/{company_url:path}")
def get_peers(company_url: str):
    driver = get_driver()
    data = utils.get_peers(driver, company_url)
    return {"data": data}

@app.get("/quarterly_results/{company_url:path}")
def get_quarterly_results(company_url: str):
    driver = get_driver()
    data = utils.get_quarterly_results(driver, company_url)
    return {"data": data}

@app.get("/profit_loss/{company_url:path}")
def get_profit_loss(company_url: str):
    driver = get_driver()
    data = utils.get_profit_loss(driver, company_url)
    return {"data": data}

@app.get("/announcements/{company_url:path}")
def get_announcements(company_url: str):
    driver = get_driver()
    data = utils.get_announcements(driver, company_url)
    return {"data": data}

@app.get("/concalls/{company_url:path}")
def get_concalls(company_url: str):
    driver = get_driver()
    links = utils.get_concalls(driver, company_url)
    return {"links": links}

@app.post("/custom_query")
def custom_query(request: QueryRequest):
    driver = get_driver()
    data = utils.run_custom_query(driver, request.query)
    return {"data": data}

@app.on_event("shutdown")
def shutdown_event():
    global driver
    if driver:
        driver.quit()
