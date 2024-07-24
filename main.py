from Indicators.macd import macd
from Indicators.stochasticRSI import stochastic
from Indicators.ATR import ATR
from Indicators.Coins_That_AvailableIn_Binance_Futures import fetch_usdt_pairs

coins = ['ACE/USDT', 'ACH/USDT', 'AEVO/USDT', 'AGIX/USDT', 'AGLD/USDT', 'AI/USDT', 'ALT/USDT', 'AMB/USDT', 'APT/USDT', 'ARB/USDT', 'ARK/USDT', 'ARKM/USDT', 'ASTR/USDT', 'AUCTION/USDT', 'AVAX/USDT', 'AXL/USDT', 'BADGER/USDT', 'BB/USDT', 'BCH/USDT', 'BEAMX/USDT', 'BICO/USDT', 'BIGTIME/USDT', 'BLUR/USDT', 'BNB/USDT', 'BNT/USDT', 'BNX/USDT', 'BOME/USDT', 'BOND/USDT', 'BSV/USDT', 'BTC/USDT', 'CAKE/USDT', 'CFX/USDT', 'CKB/USDT', 'COMBO/USDT', 'CYBER/USDT', 'DODOX/USDT', 'DOGE/USDT', 'DYM/USDT', 'EDU/USDT', 'ENA/USDT', 'ETH/USDT', 'ETHFI/USDT', 'ETHW/USDT', 'FET/USDT', 'FIL/USDT', 'FRONT/USDT', 'FXS/USDT', 'GAS/USDT', 'GLM/USDT', 'GLMR/USDT', 'GMX/USDT'] 

# coins = ['HFT/USDT', 'HIFI/USDT', 'HIGH/USDT', 'HOOK/USDT', 'ICP/USDT', 'ID/USDT', 'IDEX/USDT', 'ILV/USDT', 'JOE/USDT', 'JTO/USDT', 'JUP/USDT', 'KAS/USDT', 'KEY/USDT', 'LDO/USDT', 'LEVER/USDT', 'LINK/USDT', 'LOOM/USDT', 'LQTY/USDT', 'LSK/USDT', 'LTC/USDT', 'MAGIC/USDT', 'MANTA/USDT', 'MATIC/USDT', 'MAV/USDT', 'MAVIA/USDT', 'MBL/USDT', 'MEME/USDT', 'METIS/USDT', 'MINA/USDT', 'MOVR/USDT', 'MYRO/USDT']

# coins = [ 'NMR/USDT', 'NOT/USDT', 'STEEM/USDT', 'STPT/USDT', 'STRK/USDT', 'STX/USDT', 'SUI/USDT', 'SUPER/USDT', 'T/USDT', 'TAO/USDT', 'TIA/USDT', 'TLM/USDT', 'TNSR/USDT', 'TOKEN/USDT', 'TON/USDT', 'TRU/USDT', 'TWT/USDT', 'UMA/USDT', 'USTC/USDT', 'VANRY/USDT', 'W/USDT', 'WAXP/USDT', 'WIF/USDT', 'WLD/USDT', 'XAI/USDT', 'XRP/USDT', 'XVG/USDT', 'XVS/USDT', 'YGG/USDT', 'ZETA/USDT']

# coins = ['1000BONK/USDT', '1000FLOKI/USDT', '1000PEPE/USDT', '1000RATS/USDT', '1000SATS/USDT', '1000SHIB/USDT',]

# coins = fetch_usdt_pairs()

timeframe = "4h"
def indicators_decision(symbol, timeframe):
    macdValue = macd(symbol, timeframe)
    stochValue = stochastic(symbol, timeframe)
    ATRValue = ATR(symbol, timeframe)
    if stochValue in ["sell", "strongSell"]:
        if macdValue == "strongSell" and ATRValue in ["sell", "neutral"]:
            return "short"
            result = "short"
        elif macdValue == "sell" and ATRValue in ["sell", "neutral"]:
            return "short"
            result = "short"
        elif macdValue == "neutral" and ATRValue in ["sell", "neutral"]:
            return "short"
            result = "short"
        else:
            return "no"
            result = "no"
    elif stochValue in ["buy", "strongBuy"]:
        if macdValue == "strongBuy" and ATRValue in ["buy", "neutral"]:
            return "long"
            result = "long"
        elif macdValue == "buy" and ATRValue in ["buy", "neutral"]:
            return "long"
            result = "long"
        elif macdValue == "neutral" and ATRValue in ["buy", "neutral"]:
            return "long"
            result = "long"
        else:
            return "no"
            result = "no"
    else:
        return "no"

def decision_maker(symbol, timeframe):
    def if_statemant(own, up, down):
        if not down:
            down = 0
            second = up
        else:
            up = 0
            second = down

        if own == "long" and second == "long" :
            print(f"Long : {symbol} on {timeframe}")
            return "long"
            result = "long"
        elif own == "short" and second == "short":
            print(f"Short: {symbol} on {timeframe}")
            return "short"
            result = "short"
        else:
            print(f"No: {symbol} on {timeframe}")
            return "no"
            result = "no"
        
    if timeframe == "4h":
        timeframeup = "1h"
        timeframedown = "1h"
        own = indicators_decision(symbol, timeframe)
        up = indicators_decision(symbol, timeframeup)
        down = ""
        if_statemant(own, up, down)
    elif timeframe == "30m":
        timeframeup = "1h"
        timeframedown = "15m"
        own = indicators_decision(symbol, timeframe)
        up = indicators_decision(symbol, timeframeup)
        down = ""
        if_statemant(own, up, down)
    elif timeframe == "4h":
        timeframeup = "1d"
        timeframedown = "1h"
        own = indicators_decision(symbol, timeframe)
        up = ""
        down = indicators_decision(symbol, timeframedown)
        if_statemant(own, up, down)
    else:
        print("error of decision")

for coin in coins:
    decision_maker(coin, timeframe)



