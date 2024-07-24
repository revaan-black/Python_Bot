import ccxt
import pandas as pd
import pandas_ta as ta

def detect_trend(df, n=5):
    """
    Detect the trend based on the last n candles' Stochastic RSI values.
    """
    last_n_k = df['Stoch_RSI_K'].tail(n).values
    last_n_d = df['Stoch_RSI_D'].tail(n).values
    last_n_k_new = df['Stoch_RSI_K'].iloc[-2]
    last_n_d_new = df['Stoch_RSI_D'].iloc[-2]

    average_value = (last_n_d_new + last_n_k_new) / 2

    if all(x < y for x, y in zip(last_n_k, last_n_k[1:])) and all(x < y for x, y in zip(last_n_d, last_n_d[1:])):
        signal = "uptrend"
        if 45 <= average_value <= 55:
            trend = "neutral"
        elif 55 < average_value <= 80:
            trend = "sell"
        elif 80 < average_value:
            trend = "strongSell"
        elif 45 >= average_value >= 20:
            trend = "buy"
        elif 20 > average_value:
            trend = "strongBuy"
        else:
            trend = "error"
    elif all(x > y for x, y in zip(last_n_k, last_n_k[1:])) and all(x > y for x, y in zip(last_n_d, last_n_d[1:])):
        signal = "downtrend"
        if 45 <= average_value <= 55:
            trend = "neutral"
        elif 55 < average_value <= 80:
            trend = "sell"
        elif 80 < average_value:
            trend = "strongSell"
        elif 45 >= average_value >= 20:
            trend = "buy"
        elif 20 > average_value:
            trend = "strongBuy"
        else:
            trend = "error"
    elif all(abs(x - y) < 5 for x, y in zip(last_n_k, last_n_k[1:])) and all(abs(x - y) < 5 for x, y in zip(last_n_d, last_n_d[1:])):
        signal = "sidewaystrend"
        if 45 <= average_value <= 55:
            trend = "neutral"
        elif 55 < average_value <= 80:
            trend = "sell"
        elif 80 < average_value:
            trend = "strongSell"
        elif 45 >= average_value >= 20:
            trend = "buy"
        elif 20 > average_value:
            trend = "strongBuy"
        else:
            trend = "error"
    else:
        signal = "mixed"
        if 45 <= average_value <= 55:
            trend = "neutral"
        elif 55 < average_value <= 80:
            trend = "sell"
        elif 80 < average_value:
            trend = "strongSell"
        elif 45 >= average_value >= 20:
            trend = "buy"
        elif 20 > average_value:
            trend = "strongBuy"
        else:
            trend = "error"

    return {"signal": signal, "trend": trend}

def stochastic(symbol, timeframe):
    # Initialize the Binance exchange
    exchange = ccxt.binance()

    # Fetch historical OHLCV (Open, High, Low, Close, Volume) data
    ohlcvs = exchange.fetch_ohlcv(symbol, timeframe)

    # Convert the OHLCV data into a DataFrame
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(ohlcvs, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime format
    df.set_index('timestamp', inplace=True)

    # Fetch the current ticker price
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker['last']

    # Add the current price as the latest data point
    last_row = df.iloc[-1].copy()
    last_row.name = pd.Timestamp.now()
    last_row['close'] = current_price

    # Concatenate the new row to the DataFrame
    df = pd.concat([df, pd.DataFrame([last_row])])

    # Calculate Stochastic RSI with specified parameters
    stoch_rsi = ta.stochrsi(df['close'], length=14, rsi_length=14, k=3, d=3)

    # Add Stochastic RSI columns to the DataFrame
    df['Stoch_RSI_K'] = stoch_rsi['STOCHRSIk_14_14_3_3']
    df['Stoch_RSI_D'] = stoch_rsi['STOCHRSId_14_14_3_3']

    # Ensure no NaN values are present
    df.dropna(inplace=True)

    # Determine the trend based on the last 5 and 3 candles' Stochastic RSI values
    trend_5 = detect_trend(df, n=5)
    trend_4 = detect_trend(df, n=4)

    # Use the signal in if-statements
    signal_5 = trend_5['signal']
    trend_value_5 = trend_5['trend']
    signal_4 = trend_4['signal']
    trend_value_4 = trend_4['trend']

   

    if signal_4 == "uptrend":
        trend = "uptrend"
        if trend_value_4 == "strongSell":
            signal = "strongSell"
            return "sell"
        elif trend_value_4 == "sell":
            signal = "sell"
            return "buy"
        elif trend_value_4 == "neutral":
            signal = "neutral"
            return "buy"
        elif trend_value_4 == "buy":
            signal = "buy"
            return "buy"
        elif trend_value_4 == "strongBuy":
            signal = "strongbuy"
            return "strongBuy"
        else:
            print("error1")
    elif signal_4 == "downtrend":
        trend = "downtrend"
        if trend_value_4 == "strongBuy":
            signal = "strongBuy"
            return "buy"
        elif trend_value_4 == "buy":
            signal = "buy"
            return "sell"
        elif trend_value_4 == "neutral":
            signal = "neutral"
            return "sell"
        elif trend_value_4 == "sell":
            signal = "sell"
            return "sell"
            
        elif trend_value_4 == "strongSell":
            signal = "strongSell"
            return "strongSell"
            
        else:
            print("error2")
    elif signal_4 == "sidewaystrend":
        trend = "sidewaystrend"
        if trend_value_4 == "strongBuy":
            signal = "strongBuy"
            return "stronBuy"
            
        elif trend_value_4 == "buy":
            signal = "buy"
            return "buy"
            
        elif trend_value_4 == "neutral":
            signal = "neutral"
            return "neutral"
            
        elif trend_value_4 == "sell":
            signal = "sell"
            return "sell"
            
        elif trend_value_4 == "strongSell":
            signal = "strongSell"
            return "strongSell"
            
        else:
            print("error3")
    else:
        trend = "mixed"
        if trend_value_4 == "strongSell":
            signal = "strongSell"
            return "strongSell"
            
        elif trend_value_4 == "sell":
            signal = "sell"
            return "sell"
            
        elif trend_value_4 == "neutral":
            signal = "neutral"
            return "neutral"
            
        elif trend_value_4 == "buy":
            signal = "buy"
            return "buy"
            
        elif trend_value_4 == "strongBuy":
            signal = "strongBuy"
            return "strongBuy"
        
        else:
            print("error4")
