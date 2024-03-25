import os
import time
import json
import requests
import logging
import subprocess
from selenium import webdriver
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger("api")

class Response:
    def __init__(self, status_code, text):
        self._status_code = status_code
        self._text = text

    @property
    def text(self):
        return self._text

    @property
    def status_code(self):
        return self._status_code
    
    def is_authorized(self):
        return False == (self._status_code != 200 and self._status_code >= 400 and self._status_code <= 500)

class TradeStation:

    def __init__(self) -> None:
        self.base_url = "https://api.tradestation.com/v3"
        self.max_bars = 57_600
        self.token_subdir = "tradestation"
        self.client_id = os.getenv("TRADESTATION_API_KEY")
        self.client_secret = os.getenv("TRADESTATION_API_SECRET")
        self.redirect_url = os.getenv("TRADESTATION_REDIRECT_URL")
        self.auth_code_base_url = "https://signin.tradestation.com/authorize"
        self.auth_code_extra_params = "&audience=https://api.tradestation.com&scope=openid offline_access profile MarketData ReadAccount Trade"
        self.access_token_url = "https://signin.tradestation.com/oauth/token" 
        self.response = Response

    def _token_command(self, grant_type):
        command = [
            'curl',
            '--request', 'POST',
            '--url', self.access_token_url,
            '--header', 'content-type: application/x-www-form-urlencoded',
            '--data', f'grant_type={grant_type}',
            '--data', f'client_id={self.client_id}',
            '--data', f'client_secret={self.client_secret}',
            '--data', f'redirect_uri={os.getenv('TRADESTATION_REDIRECT_URL')}'
        ]
        return command

    def get_auth_code(self):
        url = (
            f"{self.auth_code_base_url}"
            f"?response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_url}"
            f"{self.auth_code_extra_params}"
        )
        driver = webdriver.Firefox()
        driver.get(url)
        driver.find_element("id", "username").send_keys(os.getenv("TRADESTATION_USERNAME"))
        driver.find_element("id", "password").send_keys(os.getenv("TRADESTATION_PASSWORD"))
        driver.find_element("id", "btn-login").click()
        while "?code=" not in driver.current_url:
            time.sleep(0.25)
        auth_code = driver.current_url.split("?code=")[1]
        driver.quit()
        return auth_code
    
    def get_first_access_token(self, auth_code):
        command = self._token_command("authorization_code")
        command = command + ['--data', f'code={auth_code}']
        response = subprocess.run(command, capture_output=True, text=True, check=True)
        if "error" in response.stdout:
            return Response(401, None)
        return Response(200, json.loads(response.stdout))

    def get_access_token(self, refresh_token):
        command = self._token_command("refresh_token") + ["--data", f"refresh_token={refresh_token}"]
        response = subprocess.run(command, capture_output=True, text=True, check=True)
        if "error" in response.stdout:
            return Response(401, None)
        return Response(200, json.loads(response.stdout))

    def _get_bars_endpoint(self, symbol, interval=None, unit=None, barsback=None, start_date=None, end_date=None):
        url = f"{self.base_url}/marketdata/barcharts/{symbol}?sessiontemplate=Default"
        if interval is not None:
            url += f"&interval={interval}"
        if unit is not None:
            url += f"&unit={unit}"
        if barsback is not None:
            url += f"&barsback={barsback}"
        if start_date is not None:
            url += f"&firstdate={start_date}"
        if end_date is not None:
            url += f"&lastdate={end_date}"
        return url

    def get_symbol_data(self, token, args):
        url = self._get_bars_endpoint(**args)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.request("GET", url, headers=headers)
        return response
    
    def parse_symbol_data(self, data):
        return json.loads(data)["Bars"]