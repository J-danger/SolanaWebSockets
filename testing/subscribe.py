import asyncio
import json
import websockets

async def subscribe_to_slots():
    url = "wss://api.mainnet-beta.solana.com/"  # Solana WebSocket endpoint

    async with websockets.connect(url) as websocket:
        # Prepare the JSON-RPC message for slot subscription
        subscription_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "slotSubscribe"
        }

        # Send the subscription message
        await websocket.send(json.dumps(subscription_message))
        print("Subscribed to slots.")

        while True:
            # Wait for messages from the WebSocket
            response = await websocket.recv()
            print(f"Received response: {response}")

async def main():
    await subscribe_to_slots()

if __name__ == "__main__":
    asyncio.run(main())
