import asyncio
import websockets
import json
from asyncio import TimeoutError

# Solana WebSocket endpoint
SOLANA_WS_URL = "wss://api.mainnet-beta.solana.com"

# Address to monitor
WALLET_ADDRESS = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"

subscription_id = None

async def subscribe_to_account():
    global subscription_id
    while True:
        try:
            print(f"Attempting to connect to {SOLANA_WS_URL}")
            async with websockets.connect(SOLANA_WS_URL) as websocket:
                print(f"Successfully connected to {SOLANA_WS_URL}")
                
                # Unsubscribe if there's an existing subscription
                if subscription_id is not None:
                    print(f"Attempting to unsubscribe with Subscription ID: {subscription_id}")
                    unsubscribe_request = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "accountUnsubscribe",
                        "params": [subscription_id]
                    }
                    try:
                        await websocket.send(json.dumps(unsubscribe_request))
                        response = await asyncio.wait_for(websocket.recv(), timeout=10)
                        print(f"Unsubscription response: {response}")
                        result = json.loads(response)
                        if result['result']:
                            print("Successfully unsubscribed")
                            subscription_id = None
                        else:
                            print("Failed to unsubscribe")
                    except Exception as e:
                        print(f"Error during unsubscription: {e}")
                
                # Subscription request
                subscription_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "accountSubscribe",
                    "params": [
                        WALLET_ADDRESS,
                        {
                            "encoding": "jsonParsed",
                            "commitment": "finalized"
                        }
                    ]
                }
                
                print(f"Sending subscription request for address {WALLET_ADDRESS}")
                # Send the subscription request
                await websocket.send(json.dumps(subscription_request))
                print(f"Subscription request sent. Waiting for response...")
                
                # Increased timeout to 30 seconds
                response = await asyncio.wait_for(websocket.recv(), timeout=30)
                print(f"Received subscription response: {response}")
                result = json.loads(response)
                subscription_id = result['result']
                print(f"Subscribed to address {WALLET_ADDRESS} with Subscription ID: {subscription_id}")

                while True:
                    print("Waiting for account updates...")
                    # Wait for updates
                    message = await websocket.recv()
                    print(f"Received message: {message}")
                    update = json.loads(message)
                    
                    # Check if it's an update notification
                    if 'method' in update and update['method'] == 'accountNotification':
                        params = update['params']
                        result = params['result']
                        
                        # Print every time there is a change to the address
                        print(f"Change detected for address {WALLET_ADDRESS}:")
                        print(json.dumps(result, indent=2))
                        print("---")  # Separator for readability

        except TimeoutError:
            print("Timeout occurred while waiting for subscription response. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"WebSocket connection closed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    print("Starting the script...")
    asyncio.run(subscribe_to_account())