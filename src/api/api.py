import os
import sys
import json
import pandas as pd
import logging

logger = logging.getLogger("api")
logging.basicConfig(level=logging.INFO)

class Api:
    def __init__(self, config, env):
        self.env = env
        self.config = config()
        self.token = Token(self.config.token_subdir)

    def health_check(self):
        failed = False
        res = self.get_positions()
        try:
            if not self._is_response_success(res):
                raise Exception
        except Exception as err:
            failed = True
            logger.error("health check failed")
            logger.error(err)
        try:
            if not self.is_market_open():
                logger.warning("market closed")
        except Exception as err:
            logger.error(err)
        if not failed:
            logger.info("health check ok")
            

    def is_market_open(self):
        token = self.get_token()
        return self.config.is_market_open(token)

    def _get_first_access_token(self):
        auth_code = self.config.get_auth_code()
        res = self.config.get_token("authorization_code", auth_code)
        if self._is_response_success(res):
            self.token.save("access", res.json()["access_token"])
            self.token.save("refresh", res.json()["refresh_token"])
            return self.get_token()

    def _refresh_access_token(self):
        refresh_token = self.token.refresh()
        res = self.config.get_token("refresh_token", refresh_token)
        if self._is_response_success(res):
            self.token.save("access", res.json()["access_token"])
            return self.get_token()
    
    def _is_response_success(self, res):
        if res.status_code == 200:
            return True
        else:
            try:
                logger.info(f"status_code: {res.status_code}")
                logger.info(res.json())
            except:
                pass
        return False

    def get_token(self):
        return self.token.access()
    
    def try_endpoint(self, endpoint, args=None):
        token = self.get_token()
        res = endpoint(token, args)
        if not self._is_response_success(res):
            logger.info("Refreshing token...")
            token = self._refresh_access_token()
            res = endpoint(token, args)
        if not self._is_response_success(res):
            logger.info("Getting first token...")
            token = self._get_first_access_token()
            res = endpoint(token, args)
        if not self._is_response_success(res):
            logger.error("Cannot authorize api.")
            sys.exit(1)
        return res 

    def get_positions(self, args=None):
        endpoint = self.config.get_account_positions
        res = self.try_endpoint(endpoint, args)
        return res

    def get_symbol_data(self, args):
        endpoint = self.config.get_price_history
        res = self.try_endpoint(endpoint, args)
        return res
    
    def get_market_hours(self, args=None):
        endpoint = self.config.get_market_hours
        res = self.try_endpoint(endpoint, args)
        return res

class Token:
    def __init__(self, token_subdir):
        self.token_parent_dir = os.path.join(".tokens")
        self.token_subdir = os.path.join(token_subdir)
        self.token_dir = os.path.join(self.token_parent_dir, self.token_subdir)
        self.setup()

    def setup(self):
        if not os.path.exists(self.token_parent_dir):
            os.mkdir(self.token_parent_dir)
        if not os.path.exists(self.token_dir):
            os.mkdir(self.token_dir)
            with open(os.path.join(self.token_dir, "access_token.json"), "w") as file:
                json.dump({"access_token": ""}, file)
            with open(os.path.join(self.token_dir, "refresh_token.json"), "w") as file:
                json.dump({"refresh_token": ""}, file)

    def _get(self, name):
        filepath = os.path.join(self.token_dir, f"{name}_token.json")
        try:
            with open(filepath, "r") as file:
                value = json.load(file)
                return value[f"{name}_token"]
        except FileNotFoundError:
            print(f"File {filepath} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {filepath}.")
            return None

    def access(self):
        return self._get("access")

    def refresh(self):
        return self._get("refresh")

    def save(self, name, value):
        if not os.path.exists(self.token_dir):
            if not os.path.exists(self.token_parent_dir):
                os.mkdir(self.token_parent_dir)
            os.mkdir(self.token_dir)
        filepath = os.path.join(self.token_dir, f"{name}_token.json")
        with open(filepath, "w") as file:
            json.dump({f"{name}_token": value}, file)
