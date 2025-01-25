import requests
import json

# Your transaction signature
transaction_signature = "HDD48CmFYabTuirq9Ljtu3RXghPmPHVqMCgYjC1AE7rZSt6v4d7nPiLCJRqMukq8qWn7ayq9pBxDqNjDytNfbzx"

# URL for the Solana mainnet-beta RPC
url = "https://api.mainnet-beta.solana.com"

# Prepare the body of the request
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTransaction",
    "params": [
        transaction_signature,
        {
            "encoding": "json",
            "maxSupportedTransactionVersion": 0
        }
    ]
}

# Send the request
response = requests.post(url, json=payload)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    if 'result' in result:
        print(json.dumps(result['result'], indent=2))
    else:
        print("Transaction not found or some error occurred.")
        print(json.dumps(result, indent=2))
else:
    print(f"An error occurred: {response.status_code}")
    print(response.text)