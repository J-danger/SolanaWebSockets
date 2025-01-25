from web3 import Web3

# Public node URL - these can change or become less reliable over time
public_node_url = 'https://cloudflare-eth.com'
web3 = Web3(Web3.HTTPProvider(public_node_url))

if web3.is_connected():
    ethereum_address = '0x5be9a4959308a0d0c7bc0870e319314d8d957dbb'
    balance_wei = web3.eth.get_balance(ethereum_address)
    balance_ether = web3.from_wei(balance_wei, 'ether')
    print(f"The balance of Ethereum address {ethereum_address} is {balance_ether} ETH.")
else:
    print("Failed to connect to the public Ethereum node.")
