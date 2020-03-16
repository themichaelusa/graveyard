NOT_SET = None

SELL_MARKER = 0
BUY_MARKER = 1

SELL = 'SELL'
BUY = 'BUY'

STOP_LOSS_UBAND = 1.25
STOP_LOSS_LBAND = .25
OPTIMAL_BBANDS_MA = 1
OPTIMAL_MA = 1

PROTOCOL = 'https://'
BITFENIX_URL = PROTOCOL + 'api.bitfinex.com/v1/'
BFX_REALTIME_TICKER = 'pubticker/{}'
POLONIEX_PUBLIC_URL = PROTOCOL + 'poloniex.com/public'
POLONIEX_HISTORICAL_DATA = '?command=returnChartData&currencyPair={}&start={}&end={}&period={}'

AV_URL = 'www.alphavantage.co/query'
AV_REALTIME_API = '?function=TIME_SERIES_INTRADAY&symbol={}&interval={}min&outputsize=full&apikey=7128'

EQUITY_PL = ('S', AV_URL, AV_REALTIME_API, 5)
CRYPTO_PL = ('C', POLONIEX_PUBLIC_URL, POLONIEX_HISTORICAL_DATA, 3)