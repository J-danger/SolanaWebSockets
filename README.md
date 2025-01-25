# Solana Transaction Listener

## Overview
A Python script that monitors transactions for a specific Solana address using asynchronous RPC calls. (Default is pump.fun)

## Features
- Monitors a specific Solana wallet address
- Supports multiple RPC endpoints
- Detects and logs CREATE operations (CreateIdempotent, InitializeMint)
- Asynchronous transaction fetching

## Prerequisites
- Python 3.8+
- `solana` library
- `requests` library
- `asyncio`

## Installation
```bash
pip install solana-python-sdk requests
```

## Configuration
Modify the following variables in the script:
- `ADDRESS`: Solana wallet address to monitor
- `RPC_URLS`: List of Solana RPC endpoints

## Usage
```bash
python mintCheck.py
```

## Key Dependencies
- `solana-python-sdk`
- `asyncio`
- `requests`

## Functionality
- Continuously polls recent transactions
- Prints transaction details for CREATE operations
- Handles multiple RPC endpoint failovers

## Disclaimer
Use responsibly and in compliance with Solana network terms of service.
