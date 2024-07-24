import ccxt
import pandas as pd
import pandas_ta as ta

def fetch_ohlcv(exchange, symbol, timeframe):
    """
    Fetch historical OHLCV data from the exchange.
    """
    ohlcvs = exchange.fetch_ohlcv(symbol, timeframe)
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(ohlcvs, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime format
    df.set_index('timestamp', inplace=True)
    return df

def calculate_normalized_atr(df):
    """
    Calculate the normalized ATR.
    """
    atr = ta.atr(df['high'], df['low'], df['close'])
    df['ATR'] = atr

    # Calculate mean and standard deviation of ATR
    mean_atr = df['ATR'].mean()
    std_atr = df['ATR'].std()

    # Calculate normalized ATR (Z-score normalization)
    df['Normalized_ATR'] = (df['ATR'] - mean_atr) / std_atr

    return df

def generate_signals(df, buy_threshold=-0.5, sell_threshold=0.5):
    """
    Generate buy and sell signals based on the normalized ATR.
    """
    buy_signal = (df['Normalized_ATR'] < buy_threshold)
    sell_signal = (df['Normalized_ATR'] > sell_threshold)

    df['Signal'] = 0
    df.loc[buy_signal, 'Signal'] = 1
    df.loc[sell_signal, 'Signal'] = -1
    

    return df

def ATR(symbol, timeframe):
    # Initialize the Binance exchange
    exchange = ccxt.binance()

    # Fetch historical OHLCV data
    df = fetch_ohlcv(exchange, symbol, timeframe)

    # Calculate normalized ATR
    df = calculate_normalized_atr(df)

    # Generate buy and sell signals with adjusted thresholds
    df = generate_signals(df, buy_threshold=-0.5, sell_threshold=0.5)

    # The script will store "1" for a buy signal, "-1" for a sell signal, and "0" for no signal.

    signal = df['Signal'].iloc[-1]
    if signal == 1:
        signal = "buy"
    elif signal == -1:
        signal = "sell"
    else:
        signal = "neutral"
    # print(signal)
    return signal
