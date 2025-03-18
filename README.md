# Crypto Pair Analysis

This project analyzes cryptocurrency pairs to identify potential opportunities for pair trading strategies. It calculates various statistical and econometric metrics to evaluate the relationships between different cryptocurrency price series.

## Overall Goal

The primary goal of this project is to provide quantitative data and analysis that can inform the development or evaluation of cryptocurrency pair trading strategies. Pair trading is a market-neutral strategy that capitalizes on temporary divergences in the prices of two correlated assets. This project aims to quantify the relationships between cryptocurrency pairs by calculating key metrics related to:

* **Correlation and Cointegration:** Identifying pairs that exhibit statistical relationships, suggesting they move together in the short or long term.
* **Spread Dynamics:** Analyzing the price difference (spread) between pairs to understand its statistical properties like mean, volatility, and mean-reversion.
* **Stationarity:** Assessing if the price relationships or spreads are statistically stable over time, a crucial requirement for many time-series-based trading strategies.
* **Causality and Hedge Ratios:** Determining if one asset's price movements can help predict another's and calculating optimal hedge ratios to minimize risk in a pair trade.

By calculating these metrics, the project intends to help users:

* **Screen Potential Pairs:** Identify cryptocurrency pairs that warrant further investigation for pair trading.
* **Quantify Relationships:** Understand the statistical characteristics of cryptocurrency pairs.
* **Provide Data for Strategy Development:** Generate data that can be used as input for building and testing pair trading strategies.

## Files Description

* `binance_usage.py`: This file contains functions for interacting with the Binance API.
    * `get_binance_symbols()`: Fetches all available trading pairs from Binance.
    * `fetch_historical_data()`: Retrieves historical candlestick data for a given symbol and time interval.
    * `calculate_yearly_liquidity_score()`: Calculates a liquidity score for a given symbol.
* `crypto_constant.py`: Defines a list (`crypto_list`) of cryptocurrency symbols used for analysis.
* `main.py`: The main script that orchestrates the analysis.
    * It gets all unique pairs from `crypto_list`.
    * Uses `concurrent.futures.ThreadPoolExecutor` to process pairs in parallel.
    * For each pair, it calculates metrics (using functions from `metric_calculator.py`) such as correlation, spread statistics, stationarity tests, cointegration tests, hedge ratios, and Granger causality.
    * Stores the results in a pandas DataFrame and saves it to a CSV file (`data/corr_test.csv`).
* `metric_calculator.py`: This file contains functions for calculating various statistical and econometric metrics on cryptocurrency price series.
    * `init_df()`: Initializes an empty pandas DataFrame with the required columns.
    * `calc_correlation()`: Calculates the Pearson correlation coefficient.
    * `calc_mean_spread()`: Calculates the mean of the spread.
    * `calc_std_spread()`: Calculates the standard deviation of the spread.
    * `calc_zscore_spread()`: Calculates the z-score of the spread.
    * `calc_half_life_spread()`: Calculates the half-life of mean reversion.
    * `test_stationarity_adf()`: Performs the Augmented Dickey-Fuller (ADF) test for stationarity.
    * `test_stationarity_kpss()`: Performs the KPSS test for stationarity.
    * `engle_granger_test()`: Performs the Engle-Granger cointegration test.
    * `johansen_test()`: Performs the Johansen cointegration test.
    * `calc_optimal_hedge_ratio()`: Calculates the optimal hedge ratio.
    * `test_granger_causality()`: Performs the Granger causality test.

## Theoretical Background

This project leverages several key concepts from statistics and econometrics to analyze cryptocurrency pairs, primarily for the purpose of identifying potential pair trading opportunities. Here's an overview of the theoretical underpinnings:

* **Correlation:** Measures the linear relationship between two price series. A high correlation (positive or negative) suggests that the prices tend to move together. However, correlation does not imply causation or a stable relationship for pair trading.
* **Spread Analysis:**
    * **Spread:** The price difference between two assets in a pair. In pair trading, the focus is on the *spread* rather than the individual asset prices.
    * **Mean and Standard Deviation of Spread:** These statistics describe the central tendency and volatility of the spread. Pair trading strategies often capitalize on deviations of the spread from its mean.
    * **Z-Score:** Measures how many standard deviations the current spread is away from its mean. High absolute Z-scores may signal potential trading opportunities (overbought or oversold spread).
    * **Half-Life of Mean Reversion:** If a spread is mean-reverting (tends to return to its average), the half-life is the expected time it takes for the spread to revert halfway back to its mean. This is crucial for timing trades.
* **Stationarity:** A stationary time series has statistical properties (mean, variance) that remain constant over time. Many time series analysis techniques, including pair trading, rely on the assumption of stationarity.
    * **Augmented Dickey-Fuller (ADF) Test:** A statistical test for stationarity. A low p-value suggests that the series is likely stationary.
    * **KPSS Test:** Another stationarity test, but its null hypothesis is that the series *is* stationary. A high p-value suggests stationarity.
* **Cointegration:** A stronger condition than correlation. Cointegrated series have a long-term equilibrium relationship; they tend to move together in the long run, even if they deviate in the short term. This is a key requirement for pair trading.
    * **Engle-Granger Test:** A test for cointegration between two series.
    * **Johansen Test:** A more general test for cointegration that can be used with multiple time series.
* **Hedge Ratio:** In pair trading, the hedge ratio is the relative number of units of each asset to trade. It's often calculated using a linear regression, where it represents the slope of the line that best fits the relationship between the two assets. This ratio aims to neutralize market risk.
* **Granger Causality:** A statistical test to determine if one time series can be used to predict another. It doesn't imply true causality but rather a predictive relationship. In pair trading, it can provide insights into the lead-lag relationship between the assets.

## Usage

1.  The primary usage of this project is to analyze cryptocurrency pairs and generate data for pair trading strategy development or evaluation.
2.  The `main.py` script is the entry point. When executed, it performs the following:
    * Fetches historical data for the cryptocurrency pairs defined in `crypto_constant.py` using the Binance API (via `binance_usage.py`).
    * Calculates statistical and econometric metrics for each pair, including correlation, spread statistics, stationarity tests, cointegration tests, hedge ratios, and Granger causality (using functions from `metric_calculator.py`).
    * Stores the calculated metrics in a pandas DataFrame.
    * Saves the results to a CSV file named `data/corr_test.csv`.
3.  The output CSV file (`data/corr_test.csv`) contains the calculated metrics for each cryptocurrency pair, which can be used for further analysis, visualization, or as input to a pair trading strategy.
4.  Users can modify the `crypto_constant.py` file to change the list of cryptocurrency symbols to be analyzed.
5.  To use this project, you will need a Binance API key and secret to access historical data. These should be set as `API_KEY` and `API_SECRET` variables in the `main.py` file.

## Disclaimer

* This code is for informational and educational purposes only.
* It is not financial advice.
* Trading cryptocurrencies involves substantial risk.
* The user is not responsible for any outcomes resulting from the use of this code.
