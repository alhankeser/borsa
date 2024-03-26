from api import Api
from api.tradestation import TradeStation
from stock import Stock
from strategy import Strategy
import timeit
from time import time


def main():

    api = Api(TradeStation)
    stock = Stock("QQQ", api)
    price = stock.price()
    print(price)
    
    strategy = Strategy([
        {
            "close:1__cross:above__ewm:40",
            "ewm:20__comp:>__ewm:40",
        },
        {
            "close:1__comp:>__ewm:5",
            "ewm:5__comp:>__ewm:10",
            "ewm:10__comp:>__ewm:20",
            "ewm:20__move:continuation__dir:up",
        }
    ])

    print(strategy.trigger_groups[0].triggers[0].indicators[0])
    
    # stock.reset_history(start_date="2007-01-01T00:00:00Z", end_date="2024-03-25T20:00:00Z")

    # args = {
    #     "symbol": "QQQ",
    #     "interval": 1,
    #     "unit": "Minute",
    #     "barsback": 10000,
    #     # "end_date": "2024-03-01T20:00:00Z"
    # }
    # # data = 
    # result = timeit.timeit(lambda:api.get_symbol_data(args), number=5)
    # print(result/10)
    # print(data["TimeStamp"])

if __name__ == "__main__":
    main()
