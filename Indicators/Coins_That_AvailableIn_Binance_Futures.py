

import requests

def fetch_usdt_pairs():
    # URL for Binance USD-M futures exchange information
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"

    # Send a GET request to the URL
    response = requests.get(url)
    data = response.json()

    # Initialize a set to store unique USDT pairs
    usdt_pairs_set = set()

    found_ldo = False

    # Define the coins to exclude
    exclude_coins = {
        'SRM/USDT', 'TOMO/USDT', 'CVC/USDT', 'BTS/USDT', 'BTCST/USDT', 
        'BTCBOM/USDT', 'AUDIO/USDT', 'RAY/USDT', 'ANT/USDT', 'FTT/USDT', 
        'FOOTBALL/USDT', 'CVX/USDT', 'QNT/USDT', 'BLUEBIRD/USDT', 
        'COCOS/USDT', 'STRAX/USDT'
    }

    # Iterate over symbols and find those with USDT pairs
    for symbol_info in data['symbols']:
        formatted_symbol = f"{symbol_info['baseAsset']}/USDT"
        if found_ldo:
            usdt_pairs_set.add(formatted_symbol)
        elif formatted_symbol == 'LDO/USDT':
            found_ldo = True
            usdt_pairs_set.add(formatted_symbol)

    # Convert the set to a list and sort it
    usdt_pairs_list = sorted(list(usdt_pairs_set))

    # Filter out the excluded coins
    filtered_usdt_pairs = [pair for pair in usdt_pairs_list if pair not in exclude_coins]

    return filtered_usdt_pairs






