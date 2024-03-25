from api import Api
from api.tradestation import TradeStation
from stock import Stock
import timeit

def main():
    api = Api(TradeStation)
    stock = Stock("QQQ", api, None)
    stock.reset_history(start_date="2007-01-01T00:00:00Z", end_date="2024-03-25T20:00:00Z")
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
