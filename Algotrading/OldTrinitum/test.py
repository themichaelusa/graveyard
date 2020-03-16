
from Trinitum import Backtest

def entry_conditions(tick_data): 

	price, volume, upperband, EMA, lowerband = tick_data
	if (price <= lowerband): return 1
	return 0

def exit_conditions(tick_data): 

	price, volume, upperband, EMA, lowerband = tick_data	
	if (price >= EMA): return 1
	if (price <= lowerband*.99): return 1
	return 0

backtest = Backtest('TEST001', 'BTC-USD', capital=100000, commission=.025)
backtest.add_indicator("BBANDS", 2, 2, 2, 1)
backtest.add_strategy("MA_FUN", entry_conditions, exit_conditions)

backtest.set_trade_params(trade_quantity=1, loss_tolerance=.05, total_positions=5)
backtest.set_advanced_params(hist_period=300, indicator_lag=5)
backtest.run(start_date='20170709', end_date='20170715')
