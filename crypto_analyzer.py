import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
import json

def get_crypto_data(coin='bitcoin', days='30', currency='usd'):
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart'

    params = {
        'vs_currency': currency,
        'days': days
        }

    response = requests.get(url, params=params)

    if (response.status_code != 200):
        raise Exception('API request failed')

    data = response.json()

    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit = 'ms')

    return df
     
def detect_sampling_rate(df):
    df = df.sort_values('timestamp')
    diffs = df['timestamp'].diff().dropna()
    median_diff = diffs.median()

    print('Detected sampling rate:', median_diff)
    return median_diff

def resample_data(df):
    df = df.set_index("timestamp")

    diffs = df.index.to_series().diff().dropna()
    median_diff = diffs.median()
    
    if median_diff < pd.Timedelta(minutes = 10):
        freq = '5min'
    elif median_diff < pd.Timedelta(hours = 2):
        freq = '1H'
    else:
        freq = '1D'

    print('Resampling to:', freq)
    
    resampled = df.resample(freq).mean()
    resampled = resampled.interpolate()

    return resampled

def daily_income(df):
    df = df.set_index("timestamp")
    daily  = df.resample('1D').mean().interpolate()
    
    daily["returns"] = daily["price"].pct_change()
    daily = daily.dropna(subset=["returns"])

    daily["cum_return"] = (1 + daily["returns"]).cumprod()
    

    print('Mean daily income: ', daily["returns"].mean()) 
    
    return daily

def calculate_metrics(df):
    return {
        'mean': df['price'].mean(),
        'std': df['price'].std(),
        'max': df['price'].max(),
        'min': df['price'].min()
        }

def get_output_path(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

def plot_data(df, coin, days, currency):
    path = get_output_path(f"{coin}_{currency}_data.png")
    
    plt.figure()
    plt.xticks(rotation=45)
    plt.plot(df.index, df['price'])
    plt.title(f'{coin} price, {days} days, currency {currency}')
    plt.tight_layout()
    plt.savefig(path)
    print("Plot saved to:", path)

def plot_returns(daily, coin, days, currency):
    path = get_output_path(f"{coin}_{currency}_data_daily_income.png")
    
    plt.figure()
    plt.xticks(rotation=45)
    plt.plot(daily.index, daily["returns"])
    plt.title(f'{coin} price, {days} days, currency {currency}, daily income')
    plt.tight_layout()
    plt.savefig(path)
    print("Second plot saved to:", path)

def plot_cumulative(daily, coin, days, currency):
    path = get_output_path(f"{coin}_{currency}_data_cumulative_return.png")
    
    plt.figure()
    plt.xticks(rotation=45)
    plt.plot(daily.index, daily["cum_return"])
    plt.title(f'{coin} price, {days} days, currency {currency}, Cumulative Return')
    plt.tight_layout()
    plt.savefig(path)
    print("Third plot saved to:", path)

##def plot_data_daily_income(daily, coin, days, currency):
##    path = get_output_path(f"{coin}_{currency}_data_daily_income.png")
##    
##    plt.figure()
##    plt.xticks(rotation=45)
##    plt.plot(daily.index, daily["returns"])
##    plt.title(f'{coin} price, {days} days, currency {currency}, daily income')
##    plt.tight_layout()
##    plt.savefig(path)
##    print("Second plot saved to:", path)
##
##    path = get_output_path(f"{coin}_{currency}_data_cumulative_return.png")
##    
##    plt.figure()
##    plt.xticks(rotation=45)
##    plt.plot(daily.index, daily["cum_return"])
##    plt.title(f'{coin} price, {days} days, currency {currency}, Cumulative Return')
##    plt.tight_layout()
##    plt.savefig(path)
##    print("Third plot saved to:", path)

    
    

def save_csv(df, coin, currency):
    path = get_output_path(f"{coin}_{currency}_data.csv")
    df.to_csv(path)
    print("CSV saved to:", path)

def save_json(metrics, coin, currency, days):
    path = get_output_path(f"{coin}_{currency}_{days}_days_data.json")
    f = open(path, 'w', encoding='utf-8')
    json.dump(metrics, f, indent=2, ensure_ascii=False)
    print("json saved to:", path)
    

def main():
    coin = sys.argv[1] if len(sys.argv) > 1 else 'bitcoin'
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    currency = sys.argv[3] if len(sys.argv) > 3 else 'usd'
        
    df = get_crypto_data(coin, days, currency)
    detect_sampling_rate(df)
    df_resampled = resample_data(df)
    df_daily_income = daily_income(df)
    metrics = calculate_metrics(df_resampled)
        
    print(metrics)

    plot_data(df_resampled, coin, days, currency)
    plot_returns(df_daily_income, coin, days, currency)
    plot_cumulative(df_daily_income, coin, days, currency)
##    plot_data_daily_income(df_daily_income, coin, days, currency)
    save_csv(df_resampled, coin, currency)
    save_json(metrics, coin, currency, days)

if __name__ == '__main__': 
    main()

