import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import urllib.parse
from credentials import email, password
url = "https://www.screener.in/login/"


def login():
    driver = uc.Chrome(headless=True,use_subprocess=False)
    driver.get(url)
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="id_username"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="id_password"]').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="id_password"]').send_keys(Keys.RETURN)

    time.sleep(5)
    return driver
def find_company_codes(query):
    url = f"https://www.screener.in/api/company/search/?q={query}"
    response = requests.get(url)
    print(response.json())
    return response
def get_charts(driver, company_url):
    url = f"https://www.screener.in/{company_url}#chart"
    driver.get(url)
    time.sleep(3)
    canvas = driver.find_element(By.XPATH, '//*[@id="canvas-chart-holder"]/canvas')
    canvas.screenshot("chart.png")
def get_pe_charts(driver, company_url):
    url = f"https://www.screener.in/{company_url}#chart"
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="company-chart-metrics"]/button[2]').click()
    canvas = driver.find_element(By.XPATH, '//*[@id="canvas-chart-holder"]/canvas')
    canvas.screenshot("chart.png")

def get_peers(driver, company_url):
    url = f"https://www.screener.in/{company_url}"
    driver.get(url)
    time.sleep(3)
    peers_table = driver.find_element(By.XPATH, '//*[@id="peers-table-placeholder"]')
    return peers_table.text

def get_quarterly_results(driver, company_url):
    url = f"https://www.screener.in/{company_url}/#quarters"
    driver.get(url)
    time.sleep(5)
    quarterly_results = driver.find_element(By.XPATH, '//*[@id="quarters"]')
    print(quarterly_results.text)
    return quarterly_results.text

def get_profit_loss(driver, company_url):
    url = f"https://www.screener.in/{company_url}"
    driver.get(url)
    time.sleep(3)
    profit_loss = driver.find_element(By.XPATH, '//*[@id="profit-loss"]')
    print(profit_loss.text)
    return profit_loss.text

def get_announcements(driver, company_url):
    url = f"https://www.screener.in/{company_url}"
    driver.get(url)
    time.sleep(3)
    announcements = driver.find_element(By.XPATH, '//*[@id="company-announcements-tab"]/ul')
    print(announcements.text)
    return announcements.text

def get_concalls(driver, company_url):
    url = f"https://www.screener.in/{company_url}"
    driver.get(url)
    time.sleep(3)
    concalls = driver.find_element(By.XPATH, '//*[@id="documents"]/div[2]/div[4]')
    links = concalls.find_elements(By.TAG_NAME, 'a')
    download_links = []
    for link in links:
        href = link.get_attribute('href')
        if href:
            download_links.append(href)
    return download_links

def run_custom_query(driver, query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.screener.in/screen/raw/?query={encoded_query}&limit=100"
    driver.get(url)
    time.sleep(5)
    
    try:
        table = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[4]/table')
    except Exception:
        print(f"Specific XPath failed. Current URL: {driver.current_url}")
        try:
            # Fallback to finding the first table
            table = driver.find_element(By.TAG_NAME, 'table')
        except Exception as e:
            print(f"Could not find any table. Page source snippet: {driver.page_source[:200]}")
            raise e

    print(table.text)
    return table.text

if __name__ == "__main__":
    # find_company_codes("Tata")
    driver = uc.Chrome()
    out = find_company_codes("Tata")
    company_url = out.json()[0]['url']

    # print(get_quarterly_results(driver, company_url))
    
    query = "Market capitalization > 500 AND\nPrice to earning < 15 AND\nReturn on capital employed > 22%"
    run_custom_query(login(), query)
    