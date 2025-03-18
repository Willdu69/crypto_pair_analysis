import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, kpss, grangercausalitytests, coint
from statsmodels.tsa.vector_ar.vecm import coint_johansen
from crypto_constant import crypto_list


def init_df():
	df = pd.DataFrame(columns=[
		# 1. Returns and Basic Statistics
		"Pair",
		"Correlation",

		# 2. Spread Analysis
		"Mean_Spread",
		"Standard_Deviation_Spread",
		"Z-Score_Spread",
		"Half-Life_Spread",
		"Stationarity_ADF",
		"Stationarity_KPSS",

		# 3. Cointegration and Dynamic Relationships
		"Engle_Granger_Test",
		"Johansen_Test",
		"Optimal_Hedge_Ratio",
		"Granger_Causality",
	])

	return df


def calc_correlation(series1: pd.Series, series2: pd.Series) -> float:
	"""
	Calculate the Pearson correlation coefficient between two series.
	"""
	return series1.corr(series2)


def calc_mean_spread(spread: pd.Series) -> float:
	"""
	Calculate the mean of the spread.
	"""
	return spread.mean()


def calc_std_spread(spread: pd.Series) -> float:
	"""
	Calculate the standard deviation of the spread.
	"""
	return spread.std()


def calc_zscore_spread(spread: pd.Series) -> pd.Series:
	"""
	Calculate the z-score of the spread.
	"""
	return (spread - spread.mean()) / spread.std()


def calc_half_life_spread(spread: pd.Series) -> float:
	"""
	Calculate the half-life of mean reversion for a spread.
	Uses the method of regressing the change in spread on its lagged value.
	"""
	spread = spread.dropna()
	spread_lag = spread.shift(1).dropna()
	delta_spread = spread.diff().dropna()

	# Align indices for regression
	spread_lag = spread_lag[delta_spread.index]

	# Run OLS regression: delta_spread = alpha + beta * spread_lag
	reg = sm.OLS(delta_spread, sm.add_constant(spread_lag)).fit()
	beta = reg.params[1]
	if beta >= 0:
		# If beta is not negative, the concept of half-life is not applicable (non mean-reverting)
		return np.nan
	half_life = -np.log(2) / beta
	return half_life


def test_stationarity_adf(spread: pd.Series) -> dict:
	"""
	Perform the Augmented Dickey-Fuller (ADF) test for stationarity.
	Returns a dictionary with the test statistic, p-value, lags used, number of observations, and critical values.
	"""
	spread = spread.dropna()
	result = adfuller(spread)
	return result[0]


def test_stationarity_kpss(spread: pd.Series, regression: str = 'c') -> float:
	"""
	Perform the KPSS test for stationarity.
	Returns a dictionary with the test statistic, p-value, lags used, and critical values.
	The 'regression' parameter defines the type of regression ('c' for constant, 'ct' for constant and trend).
	"""
	spread = spread.dropna()
	statistic, p_value, lags, critical_values = kpss(spread, regression=regression, nlags="auto")
	return statistic


def engle_granger_test(series1: pd.Series, series2: pd.Series) -> dict:
	"""
	Perform the Engle-Granger cointegration test between two series.
	Returns the cointegration test statistic and p-value.
	"""
	series1 = series1.dropna()
	series2 = series2.dropna()
	test_stat, p_value, _ = coint(series1, series2)
	return test_stat


def johansen_test(df: pd.DataFrame, det_order: int = 0, k_ar_diff: int = 1) -> dict:
	"""
	Perform the Johansen cointegration test.
	df should be a DataFrame with two or more time series.
	'det_order' is the deterministic term (-1, 0, 1, 2) and 'k_ar_diff' is the lag order for differencing.
	Returns the eigenvalue statistics and their critical values.
	"""
	df = df.dropna()
	result = coint_johansen(df, det_order, k_ar_diff)
	return result.lr1


def calc_optimal_hedge_ratio(series1: pd.Series, series2: pd.Series) -> float:
	"""
	Calculate the optimal hedge ratio by regressing series1 on series2.
	The hedge ratio is the slope coefficient from the OLS regression.
	"""
	# Align series by concatenating and dropping missing values
	df = pd.concat([series1, series2], axis=1).dropna()
	y = df.iloc[:, 0]
	X = sm.add_constant(df.iloc[:, 1])
	model = sm.OLS(y, X).fit()
	# The hedge ratio is the coefficient on series2 (ignoring the constant)
	return model.params[1]


def test_granger_causality(series1: pd.Series, series2: pd.Series, maxlag: int = 5) -> dict:
	"""
	Perform the Granger causality test to see if past values of series1 help predict series2.
	Returns a dictionary where keys are the lag and values are the corresponding p-values for the test.
	"""
	# Arrange data: first column is the dependent variable (series2), second is the potential cause (series1)
	data = pd.concat([series2, series1], axis=1).dropna()
	test_result = grangercausalitytests(data, maxlag=maxlag, verbose=False)
	p_value = 0
	for lag in range(1, maxlag + 1):
		p_value = max(p_value, test_result[lag][0]['ssr_ftest'][1])
	return p_value
