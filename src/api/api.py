import os
import sys
import json
import logging
import pandas as pd

logger = logging.getLogger("api")

class Token:
    def __init__(self, token_subdir):
        self.token_parent_dir = os.path.join(".tokens")
        self.token_subdir = os.path.join(token_subdir)
        self.token_dir = os.path.join(self.token_parent_dir, self.token_subdir)

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


class Api:
    def __init__(self, config, env):
        self.env = env
        self.config = config()
        self.token = Token(self.config.token_subdir)
        self.response = self.config.response

    def _get_first_access_token(self):
        auth_code = self.config.get_auth_code()
        res = self.config.get_first_access_token(auth_code)
        if not res.is_authorized():
            return 1
        self.token.save("access", res.text["access_token"])
        self.token.save("refresh", res.text["refresh_token"])

    def _is_response_authorized(self, res):
        response = self.response(res.status_code, res.text)
        if not response.is_authorized():
            logger.warning(response.text)
            return False
        return True

    def _refresh_access_token(self):
        refresh_token = self.token.refresh()
        res = self.config.get_access_token(refresh_token)
        if not res.is_authorized():
            return 1
        self.token.save("access", res.text["access_token"])
    
    def get_token(self):
        return self.token.access()
    
    def try_endpoint(self, token, endpoint, args):
        res = endpoint(token, args)
        if not self._is_response_authorized(res):
            logger.info("Refreshing token...")
            self._refresh_access_token()
            token = self.get_token()
            res = endpoint(token, args)
        if not self._is_response_authorized(res):
            logger.info("Getting first token...")
            self._get_first_access_token()
            token = self.get_token()
            res = endpoint(token, args)
        if not self._is_response_authorized(res):
            logger.error("Cannot authorize api.")
            sys.exit(1)
        return res

    def get_symbol_data(self, args):
        token = self.get_token()
        endpoint = self.config.get_symbol_data
        res = self.try_endpoint(token, endpoint, args)
        data = self.config.parse_symbol_data(res.text)
        return data

