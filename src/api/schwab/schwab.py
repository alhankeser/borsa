import os
import time
import json
import requests
import logging
import subprocess
import base64
from urllib.parse import unquote
from selenium import webdriver
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth  # Assuming you're using selenium-stealth for anti-bot measures

# Setup options for Chrome in headless mode
load_dotenv()

logger = logging.getLogger("api")

class Schwab:

    def __init__(self) -> None:
        self.domain = "https://api.schwabapi.com"
        self.trader_path = "/trader/v1"
        self.marketdata_path = "/marketdata/v1"
        self.auth_path = "/v1"
        self.token_subdir = "schwab"
        self.client_id = os.getenv("SCHWAB_API_KEY")
        self.client_secret = os.getenv("SCHWAB_API_SECRET")
        self.redirect_url = os.getenv("SCHWAB_REDIRECT_URL")
        self.auth_code_base_url = self.domain + self.auth_path + "/oauth/authorize"
        self.access_token_url = self.domain + self.auth_path + "/oauth/token"
        self.marketdata_url = self.domain + self.marketdata_path
        self.trader_url = self.domain + self.trader_path

    def headers(self, token):
        return {"Authorization": f"Bearer {token}"}

    def get_token(self, grant_type, token=None):
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode('utf-8')
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {encoded_credentials}'
        }
        data = f"grant_type={grant_type}"
        token_key = "refresh_token"
        if grant_type == "authorization_code":
            data += f"&redirect_uri={self.redirect_url}"
            token_key = "code"
        data += f"&{token_key}={token}"
        return requests.request("POST", self.access_token_url, headers=headers, data=data)

    def get_browser(self):
        options = Options()
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        user_data_dir = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        options.add_argument(f"user-data-dir={user_data_dir}")
        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="MacIntel",
            webgl_vendor="Apple Inc.",
            renderer="Apple Hardware",
            fix_hairline=True,
        )
        return driver

    def get_auth_code(self):
        url = (
            f"{self.auth_code_base_url}"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_url}"
        )
        driver = self.get_browser()
        driver.get(url)
        while "?code=" not in driver.current_url:
           time.sleep(0.25)
        auth_code = driver.current_url.split("?code=")[1].split("&")[0]
        driver.quit()
        return auth_code
    
    def _get_price_history_endpoint(self, symbol, start_date_unix=None, end_date_unix=None, period_type="year", period=10, frequency="daily"):
        url = f"{self.marketdata_url}/pricehistory?"
        url += f"symbol={symbol}"
        if period_type:
            url += f"&periodType={period_type}"
        if period:
            url += f"&period={period}"
        if frequency:
            url += f"&frequencyType={frequency}"
        if start_date_unix:
            url += f"&startDate={start_date_unix}"
        if end_date_unix:
            url += f"&endDate={end_date_unix}"
        return url

    def get_price_history(self, token, args):
        url = self._get_price_history_endpoint(**args)
        return  requests.request("GET", url, headers=self.headers(token))

    def get_account_positions(self, token, args=None):
        url = f"{self.domain}{self.trader_path}/accounts?fields=positions"
        return  requests.request("GET", url, headers=self.headers(token))
    
    def get_market_hours(self, token, args=None):
        url = f"{self.marketdata_url}/markets/equity"
        return requests.request("GET", url, headers=self.headers(token))

    def is_market_open(self, token):
        market_hours = self.get_market_hours(token)
        return market_hours.json()["equity"]["EQ"]["isOpen"]
