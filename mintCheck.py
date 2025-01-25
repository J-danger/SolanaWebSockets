import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed, Finalized
from solana.rpc.api import Client, Pubkey, Signature
import json
import requests

# Solana address to monitor
ADDRESS = Pubkey.from_string('6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P')

# Free Solana RPC nodes
RPC_URLS = [
    'https://api.mainnet-beta.solana.com',
    'https://solana-mainnet.rpc.extrnode.com',
    'https://rpc.ankr.com/solana'
]

async def listen_to_address():
    for rpc_url in RPC_URLS:
        try:
            async with AsyncClient(rpc_url) as client:
                print(f"Connected to RPC: {rpc_url}")
                last_signature = None

                while True:
                    try:
                        # Fetch recent transactions for the address
                        response = await client.get_signatures_for_address(
                            ADDRESS, 
                            limit=1, 
                            commitment=Finalized
                        )

                        # Print the response to inspect its structure
                        print("response type", type(response.value[0].signature))
                        print("transaction ID", response.value[0].signature)
                        print("txid type", type(response.value[0].signature))
                        
                    except Exception as e:
                        print(f"Error fetching transactions: {e}")
                    try:
                        transaction_signature = str(response.value[0].signature)
                        
                        # Prepare the body of the request
                        payload = {
                            "jsonrpc": "2.0",
                            "id": 1,
                            "method": "getTransaction",
                            "params": [
                                transaction_signature,
                                {
                                    "encoding": "jsonParsed",
                                    "maxSupportedTransactionVersion": 0
                                }
                            ]
                        }

                        # Send the request 
                        response = await asyncio.to_thread(requests.post, rpc_url, json=payload)
                                                
                        if response.status_code == 200:
                            result = response.json()
                           
                            if 'result' in result:
                                if result['result'] is not None:
                                    transaction = result['result']
                                    # Parse transaction for create operations
                                    logs = transaction.get('meta', {}).get('logMessages', [])
                                    for log in logs:
                                        if "CreateIdempotent" in log or "InitializeMint" in log:
                                            print("Detected a CREATE operation.")
                                            print(json.dumps(transaction, indent=4, sort_keys=True, ensure_ascii=False))
                                            break                                  
                                else:
                                    print(f"Transaction with signature {transaction_signature} not found.")
                            elif 'error' in result:
                                print(f"RPC Error: {json.dumps(result['error'], indent=2)}")
                            else:
                                print("Unexpected response structure.")
                                print(json.dumps(result, indent=2))
                        else:
                            print(f"HTTP Error {response.status_code}: {response.text}")
                    except Exception as e:
                        print(f"An error occurred: {e}")    

                    await asyncio.sleep(10)

        except Exception as connection_error:
            print(f"Connection error with {rpc_url}: {connection_error}")
            continue

async def main():
    await listen_to_address()

if __name__ == '__main__':
    asyncio.run(main())