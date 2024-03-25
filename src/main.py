from api import Api
from api.tradestation import TradeStation

def main():
    api = Api(TradeStation())
    args = {
        "symbol": "QQQ",
        "interval": 1,
        "unit": "Minute",
        "start_date": "2024-03-01T08:00:00Z",
        "end_date": "2024-03-01T20:00:00Z"
    }
    data = api.get_symbol_data(args)
    print(data)

if __name__ == "__main__":
    main()
