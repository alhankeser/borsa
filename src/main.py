from api import Api
from api.tradestation import TradeStation
from stock import Stock
from database import Database
from utils import get_minute, get_day, as_datetime
import time


ENV = "dev"

def main():

    db = Database(ENV)
    api = Api(TradeStation, ENV)
    stock = Stock("QQQ", api)

    # db.query("select * from _trades").to_csv("trades.csv")

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
