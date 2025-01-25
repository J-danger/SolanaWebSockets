import asyncio
import json
import websockets


async def query_account_info(address):
    url = "wss://api.mainnet-beta.solana.com/"  # Solana WebSocket endpoint

    async with websockets.connect(url) as websocket:
        # Prepare the JSON-RPC message for getting account info
        query_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getAccountInfo",
            "params": [
                address,  # The contract or account address you want to query
                {"encoding": "jsonParsed"}  # Encoding for easy parsing of data
            ]
        }

        # Send the query message
        await websocket.send(json.dumps(query_message))
        print(f"Query sent for address: {address}")

        # Receive the response
        response = await websocket.recv()
        print(f"Received response: {response}")

        # Here you might want to parse the JSON response to extract useful information
        parsed_response = json.loads(response)
        if 'result' in parsed_response and parsed_response['result']:
            account_info = parsed_response['result']['value']
            print(f"Account info: {json.dumps(account_info, indent=2)}")
        else:
            print("No result found for this address.")


async def main():
    # Example address - replace with actual address you want to query
    address = "So11111111111111111111111111111111111111112"  # This is the SOL token mint address
    await query_account_info(address)


if __name__ == "__main__":
    asyncio.run(main())