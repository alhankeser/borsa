import time
import subprocess
from api import Api
from api.tradestation import TradeStation
from stock import Stock
from database import Database
from backtest import Backtest
from analyze import Analyze
from visualize import Visualize
from utils import get_minute, get_day, as_datetime, upload_to_cloud

import pandas as pd

ENV = "dev"

def main():
    
    # subprocess.call(["dbt", "run", "--target", ENV])
    db = Database(ENV)
    model_input_path = db.export("int__model_input")
    # model_input_path = "./storage/export/int__model_input.parquet"
    # df = pd.read_parquet(model_input_path)
    # print(df.columns)
    # print(model_input_path)

    

if __name__ == "__main__":
    main()