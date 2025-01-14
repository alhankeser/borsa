import time
import subprocess
from api import Api
from api.schwab import Schwab
from stock import Stock
from database import Database
from backtest import Backtest
from analyze import Analyze
from visualize import Visualize
# from utils import get_minute, get_day, as_datetime, upload_to_cloud
import utils
import requests
import urllib
import os

os.environ['TZ'] = 'UTC'

ENV = "dev"
START_DATE = "2020-01-01"
END_DATE = utils.get_tomorrow_date_as_str()
WATCHLIST = ["AAPL", "NVDA", "SPY", "GOOGL", "SHOP", "TTD"]
WEEKLY_INVESTMENT = 1000

def main():

    ##############
    ### SETUP ####
    ##############

    db = Database(ENV)
    db.health_check()

    api = Api(Schwab, ENV)
    api.health_check()

    if ENV == "prod":
        utils.wait_until_market_is_open(api)

    ##############
    ### BUILD ####
    ##############

    # stocks = [Stock(symbol, api, db) for symbol in WATCHLIST]
    # for stock in stocks:
    #     stock.get_history(start_date=START_DATE, end_date=END_DATE)
    
    db.build()

    ##############
    #### BUY #####
    ##############



    ##############
    ### REPORT ###
    ##############
    

    # subprocess.call(["dbt", "build", "--target", ENV])
    # stock = Stock("NVDA", api, db)
    # stock.reset_history(start_date=START_DATE, end_date=END_DATE)
    # print(db.query("select ts_day from rpt__backtest_by_day order by profit limit 1"))

# b = Backtest(db)  
    # b.run()

    # a = Analyze(db)
    # best_days = a.get_best_days(3).df()
    # worst_days = a.get_worst_days(3).df()

    # print(worst_days)

    # viz = Visualize(db)
    # viz.profit(['2000-01-01', '2024-04-01'], symbol="QQQ")
    # viz.profit_by_day(['2001-01-01', '2024-04-01'])
    # viz.days(['2024-03-21', '2024-03-22'], strategy_id='optimal', symbol="QQQ")
    # 2009-07-01
    # plot.show()

    

    # table = "rpt__backtest"
    # filepath = db.export(table)

    # upload_to_cloud(filepath, table)

    # print(db.query("select * from rpt__backtest_by_day"))

    # # Simulate or trade on a single day
    # last_minute = None
    # t = get_day(days_ago=1)
    # while True:
    #     if get_minute(on_date=t) != last_minute:
    #         t1 = time.time()
    #         last_minute = get_minute(on_date=t)
    #         print("Getting latest")
    #         print(last_minute)
    #         stock.get_latest(start_date=t, end_date=last_minute)
    #         date = db.query("select ts, sma40dwn5rvsup4ago from _indicators order by ts desc limit 1")
    #         print(date)
    #         t2 = time.time()
    #         print(t2-t1)
    #     time.sleep(1)

    # count = db.query("select count(*) from _indicators")
    # print(count)
    # t1 = time.time()
    # result = db.query("select * from _indicators where ts = '2024-03-25T15:59:00Z'")
    # t2 = time.time()
    # print(t2-t1)

    # t1 = time.time()
    # result = db.query("select price from _indicators where ts = '2024-03-25T15:59:00Z'")
    # t2 = time.time()
    # print(t2-t1)
    
    # api = Api(TradeStation, "prod")
    # stock = Stock("QQQ", api)

    # t1 = time.time()
    # price = stock.price()
    # t2 = time.time()
    # print(t2-t1)


    # t1 = time.time()
    # price = stock.price(date='2024-03-25T15:59:00Z')
    # t2 = time.time()
    # print(t2-t1)

    # t1 = time.time()
    # stock.get_latest(start_date="2024-03-27T00:00:00Z", end_date="2024-03-27T15:30:00Z")
    # date = db.query("select ts, sma40dwn5rvsup4ago from _indicators order by ts desc limit 1")
    # print(date)
    # t2 = time.time()
    # print(t2-t1)

    # t1 = time.time()
    # stock.get_latest(start_date="2024-03-28T00:00:00Z")
    # date = db.query("select ts, sma40dwn5rvsup4ago from _indicators order by ts desc limit 1")
    # print(date)
    # t2 = time.time()
    # print(t2-t1)
    
    # timestamps = [
    #     "2024-03-25T19:59:00Z",
    #     "2024-03-25T19:58:00Z",
    #     "2024-03-25T19:57:00Z",
    #     "2024-03-25T19:56:00Z",
    #     "2024-03-25T19:55:00Z",
    #     "2024-03-25T19:54:00Z",
    #     "2024-03-25T19:53:00Z",
    #     "2024-03-25T19:52:00Z",
    #     "2024-03-25T19:51:00Z",
    #     "2024-03-25T19:50:00Z"
    # ]
    # for ts in timestamps:
    #     t1 = time.time()
    #     args = {
    #         "symbol": "QQQ",
    #         "interval": 1,
    #         "unit": "Minute",
    #         "start_date": "2024-03-25T19:50:00Z",
    #         "end_date": ts
    #     }
    #     api.get_symbol_data(args)
    #     t2 = time.time()
    #     print(ts, t2-t1)

if __name__ == "__main__":
    main()
