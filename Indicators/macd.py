import ccxt
import pandas as pd
import pandas_ta as ta
def macd(symbol, timeframe):
    # Initialize the Binance exchange
    exchange = ccxt.binance()

    # Fetch historical OHLCV (Open, High, Low, Close, Volume) data
    ohlcvs = exchange.fetch_ohlcv(symbol, timeframe)

    # Convert the OHLCV data into a DataFrame
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(ohlcvs, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime format
    df.set_index('timestamp', inplace=True)

    # Calculate the MACD indicator
    try:
        macd = ta.macd(df['close'])
        
        # Add MACD values to the DataFrame
        df['MACD'] = macd['MACD_12_26_9']
        df['MACD_signal'] = macd['MACDs_12_26_9']
        df['MACD_hist'] = macd['MACDh_12_26_9']

        # Normalize MACD, MACD_signal, and MACD_hist by the closing price
        df['Normalized_MACD'] = df['MACD'] / df['close']
        df['Normalized_MACD_signal'] = df['MACD_signal'] / df['close']
        df['Normalized_MACD_hist'] = df['MACD_hist'] / df['close']

        # Print the DataFrame with both real and normalized values
        # print(df[['MACD', 'MACD_signal', 'MACD_hist', 'Normalized_MACD', 'Normalized_MACD_signal', 'Normalized_MACD_hist']])

        # Assign the last value of Normalized_MACD to least
        Normalized_MACD_Least_blueMA = df['Normalized_MACD'].iloc[-1]
        Normalized_MACD_second_least_blueMA = df['Normalized_MACD'].iloc[-2]
        Normalized_MACD_third_least_blueMA = df['Normalized_MACD'].iloc[-3]
        Normalized_MACD_fourth_least_blueMA = df['Normalized_MACD'].iloc[-4]
        Normalized_MACD_fift_least_blueMA = df['Normalized_MACD'].iloc[-5]

        # Assign the last value of Normalized_MACD_signal to least
        Normalized_MACD_signal_Least_redMA = df['Normalized_MACD_signal'].iloc[-1]
        Normalized_MACD_signal_second_least_redMA = df['Normalized_MACD_signal'].iloc[-2]
        Normalized_MACD_signal_third_least_redMA = df['Normalized_MACD_signal'].iloc[-3]
        Normalized_MACD_signal_fourth_least_redMA = df['Normalized_MACD_signal'].iloc[-4]
        Normalized_MACD_signal_fift_least_redMA = df['Normalized_MACD_signal'].iloc[-5]
        
        # Assign the last value of Normalized_MACD_signal to least
        Normalized_MACD_hist_Least_candles = df['Normalized_MACD_hist'].iloc[-1]
        Normalized_MACD_hist_second_least_candles = df['Normalized_MACD_hist'].iloc[-2]
        Normalized_MACD_hist_third_least_candles = df['Normalized_MACD_hist'].iloc[-3]
        Normalized_MACD_hist_fourth_least_candles = df['Normalized_MACD_hist'].iloc[-4]
        Normalized_MACD_hist_fift_least_candles = df['Normalized_MACD_hist'].iloc[-5]

    except Exception as e:
        print("Error:", e)

    Normalized_MACD_Average_Value = (Normalized_MACD_Least_blueMA + Normalized_MACD_signal_Least_redMA) / 2  

    if 0.012 < Normalized_MACD_Average_Value:
        return "strongSell"
    elif 0.005 < Normalized_MACD_Average_Value <= 0.012:
        return "sell"
    elif 0.006 > Normalized_MACD_Average_Value >= -0.006:
        return "neutral"
    elif -0.006 > Normalized_MACD_Average_Value >= -0.012:
        return "buy"
    elif -0.012 > Normalized_MACD_Average_Value :
        return "strongBuy"
    else:
        return "error"
    
    
# macd("BTC/USDT", "4h")
    


