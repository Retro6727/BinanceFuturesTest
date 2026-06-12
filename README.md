# Binance Futures Testnet Bot

This repository contains a small CLI trading bot for Binance Futures Testnet (USDT-M) with separate client and command layers.

## Requirements
- Python 3.8+
- A virtual environment (recommended)
- Binance Testnet API key and secret

## Setup
1. Create and activate a virtual environment (Windows example):

```powershell
python -m venv env
env\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy sample.env to `.env` and set your Testnet credentials (or edit `.env` directly):

```powershell
Copy-Item sample.env .env
```

Contents of `.env` should contain:

```
BINANCE_API_KEY="<your_testnet_api_key>"
BINANCE_API_SECRET="<your_testnet_api_secret>"
```

## Files
- `bot.py` - CLI to place Market and Limit orders
- `client.py` - Binance API client (signed requests, order placement, status)
- `check_order.py` - CLI to fetch order status by `orderId`
- `logger.py` - Logging to `t_binance.log`

## How to run
Place a MARKET order:

```bash
python bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Place a LIMIT order:

```bash
python bot.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3500
```

Check order status (use the `orderId` returned by `bot.py`):

```bash
python check_order.py --symbol ETHUSDT --order-id 12345678
```

## Logging
API requests, responses, and errors are logged to `t_binance.log` in the project directory.

## Assumptions & Notes
- This project is configured to use the Binance Futures Testnet base URL.
- Do NOT use your mainnet API keys with this test code unless you understand the risk.
- The CLI validates required fields and will error for invalid input (e.g., missing `--price` for LIMIT orders).
- The code demonstrates a minimal, structured approach and is suitable for extension (order status checks, cancel orders, strategies, etc.).

## Troubleshooting
- If you see credential errors, confirm `.env` exists and contains correct values.
- Check `t_binance.log` for detailed API request/response info.

## License
Use at your own risk. No license provided.
