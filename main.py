import pandas as pd
from itertools import combinations
import warnings
from tqdm import tqdm
from binance_usage import get_binance_symbols, fetch_historical_data
from metric_calculator import *
from crypto_constant import crypto_list
from binance_usage import fetch_historical_data, calculate_yearly_liquidity_score
from binance.client import Client
import concurrent.futures

def get_unique_pairs(strings):
    return list(combinations(strings, 2))

def process_pair(permutation, client, start_date):
    """Processes a single pair and returns a dictionary of results."""
    asset_1_close = fetch_historical_data(client, permutation[0], '1d', start_date)['Close'].dropna()
    asset_2_close = fetch_historical_data(client, permutation[1], '1d', start_date)['Close'].dropna()

    min_length = min(len(asset_1_close), len(asset_2_close))

    asset_1_close = asset_1_close[len(asset_1_close) - min_length:]
    asset_2_close = asset_2_close[len(asset_2_close) - min_length:]

    spread = (asset_1_close - asset_2_close)
    cor = calc_correlation(asset_1_close, asset_2_close)
    mean_spread = calc_mean_spread(spread)
    std_spread = calc_std_spread(spread)
    half_life = calc_half_life_spread(spread)
    adf = test_stationarity_adf(spread)
    kpss = test_stationarity_kpss(spread)
    granger = engle_granger_test(asset_1_close, asset_2_close)
    ratio = calc_optimal_hedge_ratio(asset_1_close, asset_2_close)
    granger_caus = test_granger_causality(asset_1_close, asset_2_close)
    z_score = (spread - mean_spread) / std_spread if std_spread != 0 else 0

    return {
        "Pair": f"{permutation[0]}-{permutation[1]}",
        "Correlation": cor,
        "Mean_Spread": mean_spread,
        "Standard_Deviation_Spread": std_spread,
        "Z-Score_Spread": z_score.iloc[-1] if isinstance(z_score, pd.Series) else z_score,
        "Half-Life_Spread": half_life,
        "Stationarity_ADF": adf,
        "Stationarity_KPSS": kpss,
        "Engle_Granger_Test": granger,
        "Johansen_Test": "Not Implemented",
        "Optimal_Hedge_Ratio": ratio,
        "Granger_Causality": granger_caus,
    }

if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    API_KEY = "8FBVQV0BXPml3EK9OoQwrjDwBSSgg1bgAP9dp92EGUUpxmfeWpBfXYIND8admXL5"
    API_SECRET = "CkPE5A6NkVLZnThHJmZFDIN84erSuF2RwLG6abUYCNrGcNfdypCHAN08dQD5RtcO"

    client = Client(API_KEY, API_SECRET)
    start_date = "2020-01-01"

    permutations = get_unique_pairs(crypto_list)
    df = init_df()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_pair, permutations, [client] * len(permutations), [start_date] * len(permutations)), total=len(permutations)))

    for result in results:
        df = pd.concat([df, pd.DataFrame([result])], ignore_index=True)

    df.to_csv("data/corr_test.csv", index=False)