import sys
import os
import time
import json
import requests
import subprocess
import pandas as pd
from terminalplot import plot
from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver

# import importlib
# importlib.reload(api)

def main():
    
    # Get Auth code
    login_url = (
        f"https://signin.tradestation.com/authorize?"
        f"response_type=code&client_id={os.getenv('TRADESTATION_API_KEY')}"
        f"&redirect_uri={os.getenv('TRADESTATION_REDIRECT_URL')}"
        f"&audience=https://api.tradestation.com"
        f"&scope=openid offline_access profile MarketData ReadAccount Trade"
    )

    driver = webdriver.Firefox()
    driver.get(login_url)
    driver.find_element("id", "username").send_keys(os.getenv("TRADESTATION_USERNAME"))
    driver.find_element("id", "password").send_keys(os.getenv("TRADESTATION_PASSWORD"))
    driver.find_element("id", "btn-login").click()
    while "?code=" not in driver.current_url:
        time.sleep(0.5)
    auth_code = driver.current_url.split("?code=")[1]
    driver.quit()
    
    # Get token
    curl_command = [
        'curl',
        '--request', 'POST',
        '--url', 'https://signin.tradestation.com/oauth/token',
        '--header', 'content-type: application/x-www-form-urlencoded',
        '--data', 'grant_type=authorization_code',
        '--data', f'client_id={os.getenv("TRADESTATION_API_KEY")}',
        '--data', f'client_secret={os.getenv("TRADESTATION_API_SECRET")}',
        '--data', f'code={auth_code}',
        '--data', 'redirect_uri=http://localhost'
    ]
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
        tokens = json.loads(result.stdout)
        with open("./.tokens/access_token.json", 'w') as file:
            json.dump({"access_token": tokens["access_token"]}, file)
        with open("./.tokens/refresh_token.json", 'w') as file:
            json.dump({"refresh_token": tokens["refresh_token"]}, file)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
    
    # Read Access Token
    def get_token(name):
        try:
            with open(f"./.tokens/{name}_token.json", 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file.")
            return None

    # Get Refresh token
    refresh_token = get_token("refresh")
    curl_command = [
        'curl',
        '--request', 'POST',
        '--url', 'https://signin.tradestation.com/oauth/token',
        '--header', 'content-type: application/x-www-form-urlencoded',
        '--data', 'grant_type=refresh_token',
        '--data', f'client_id={os.getenv("TRADESTATION_API_KEY")}',
        '--data', f'client_secret={os.getenv("TRADESTATION_API_SECRET")}',
        '--data', f'refresh_token={refresh_token}'
    ]
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error executing command:", e)
    with open("./.tokens/access_token.json", 'w') as file:
        json.dump({"access_token": tokens["access_token"]}, file)
    
    access_token = get_token("access")

    # First endpoint
    url = "https://api.tradestation.com/v3/marketdata/barcharts/MSFT?interval=1&unit=Minute&firstdate=2024-03-22T09:00:00Z&lastdate=2024-03-22T20:00:00Z"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("GET", url, headers=headers)
        bars = json.loads(response.text)["Bars"]
        df = pd.DataFrame(bars)
    except:
        # get refresh token
        # try again
        pass

if __name__ == "__main__":
    main()
