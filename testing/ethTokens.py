import json
import requests

# Replace with your Alchemy API key:
api_key = "demo"source venv/bin/activate
fetch_url = f"https://eth-mainnet.g.alchemy.com/v2/{api_key}"

def hex_to_decimal(hex_value, decimals=18):
    decimal_value = int(hex_value, 16)
    return decimal_value / (10 ** decimals)

# Define specific wallet-token pairs
wallet_token_pairs = [
    ("0x95222290DD7278Aa3Ddd389Cc1E1d165CC4BAfe5", "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"),
    ("0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be", "0x6B175474E89094C44Da98b954EedeAC495271d0F")
]

# Headers for the request
headers = {
    'Content-Type': 'application/json'
}

# Make individual requests for each wallet-token pair
for i, (wallet, token) in enumerate(wallet_token_pairs):
    data = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [wallet, [token]],
        "id": i + 1
    }

    # Make the request
    response = requests.post(fetch_url, headers=headers, json=data)

    if response.status_code == 200:
        response_json = response.json()
        if 'result' in response_json:
            result = response_json['result']
            for balance in result['tokenBalances']:
                if balance['contractAddress'] == token:  # We check for the specific token we queried
                    token_balance_hex = balance['tokenBalance']
                    token_balance = hex_to_decimal(token_balance_hex)
                    print(f"Wallet Address: {wallet}")
                    print(f"  Token Contract Address: {token}")
                    print(f"    Balance: {token_balance} tokens")
        else:
            print(f"Error for request id {response_json['id']}: {response_json.get('error', 'No error details')}")
    else:
        print(f"Error: {response.status_code}, {response.text}")