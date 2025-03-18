import ccxt
import pandas as pd
import time


def get_binance_symbols():
	"""
	Fetch all available trading pairs (symbols) from Binance.

	:return: A list of trading pairs (e.g., ['BTC/USDT', 'ETH/USDT', ...])
	"""
	exchange = ccxt.binance()  # Initialize Binance API
	markets = exchange.load_markets()
	symbols = list(markets.keys())
	return symbols

def fetch_historical_data(client, symbol, interval, start_date, end_date=None):
	"""
	Fetch historical candlestick data for a specific ticker.

	:param symbol: Trading pair symbol (e.g., "BTCUSDT").
	:param interval: Time interval (e.g., "1d", "1h", "15m").
	:param start_date: Start date in "YYYY-MM-DD" format.
	:param end_date: End date in "YYYY-MM-DD" format (optional).
	:return: Pandas DataFrame with historical data.
	"""
	klines = client.get_historical_klines(symbol, interval, start_date, end_date)

	# Create a DataFrame
	df = pd.DataFrame(klines, columns=[
		"Open time", "Open", "High", "Low", "Close", "Volume",
		"Close time", "Quote asset volume", "Number of trades",
		"Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
	])

	df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
	df["Close time"] = pd.to_datetime(df["Close time"], unit="ms")

	numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
	df[numeric_columns] = df[numeric_columns].astype(float)
	df.set_index("Open time", inplace=True)
	return df


def calculate_yearly_liquidity_score(client, symbol, interval, start_date):
	ohlcv_data = fetch_historical_data(client, symbol, interval, start_date)
	liquidity_score = ohlcv_data["Volume"].sum() / (ohlcv_data["Close"].max() - ohlcv_data["Close"].min())
	return liquidity_score