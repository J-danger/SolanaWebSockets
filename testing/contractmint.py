import asyncio
import json
import base64
import websockets
import time
from typing import List, Tuple

# Function to decode instruction data from base64
def decode_instruction_data(data: str) -> str:
    try:
        return base64.b64decode(data).hex()
    except Exception as e:
        print(f"Error decoding instruction data: {e}")
        return None

# Function to check if a minting activity is detected in an instruction
def is_minting_instruction(instruction: dict) -> bool:
    spl_token_program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
    if instruction.get("programId") == spl_token_program_id:
        decoded_data = decode_instruction_data(instruction.get("data", ""))
        if decoded_data and decoded_data.startswith('01'):
            return True
    return False

# Function to process transactions and detect minting activity
def process_transactions(transactions: List[dict]) -> Tuple[bool, List[str]]:
    mint_found = False
    contract_addresses = []
    for tx in transactions:
        for instruction in tx.get("transaction", {}).get("message", {}).get("instructions", []):
            if is_minting_instruction(instruction):
                mint_found = True
                mint_account = instruction.get("accounts", [])[0]
                contract_addresses.append(mint_account)
    return mint_found, contract_addresses

# Alert function
def alert_minting_activity(slot: int, contract_addresses: List[str]):
    print(f"Minting activity detected in slot {slot}:")
    for address in contract_addresses:
        print(f"- Minted contract: {address}")

# Main WebSocket subscription function with rate limiting
async def subscribe_to_slots():
    url = "wss://api.mainnet-beta.solana.com/"  # Solana WebSocket endpoint for mainnet-beta

    async with websockets.connect(url) as websocket:
        subscription_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "slotSubscribe"
        }

        await websocket.send(json.dumps(subscription_message))
        print("Subscribed to slots.")

        last_slot_checked = 0
        while True:
            try:
                response = await websocket.recv()
                response_data = json.loads(response)

                if "params" in response_data and "result" in response_data["params"]:
                    slot = response_data["params"]["result"]["slot"]
                    
                    # Only process every nth slot to reduce load (rate limiting)
                    if slot - last_slot_checked >= 5:  # Check every 5 slots
                        block_request = {
                            "jsonrpc": "2.0",
                            "id": 2,
                            "method": "getBlock",
                            "params": [slot, {"encoding": "json", "transactionDetails": "full", "rewards": False}]
                        }
                        await websocket.send(json.dumps(block_request))
                        block_response = await websocket.recv()
                        block_data = json.loads(block_response)
                        
                        if 'result' in block_data and 'transactions' in block_data['result']:
                            transactions = block_data['result']['transactions']
                            mint_found, contract_addresses = process_transactions(transactions)
                            if mint_found:
                                alert_minting_activity(slot, contract_addresses)
                        
                        last_slot_checked = slot
                    
                    # Small delay to prevent excessive polling
                    await asyncio.sleep(1)  # Sleep for 1 second

            except Exception as e:
                print(f"Error in WebSocket subscription: {e}")
                # Small delay before attempting to reconnect
                await asyncio.sleep(5)

# Main entry point
async def main():
    while True:
        try:
            await subscribe_to_slots()
        except Exception as e:
            print(f"WebSocket connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())