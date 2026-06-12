import argparse
import os
import sys
from dotenv import load_dotenv
from client import BinanceFuturesClient

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL"], required=True, help="Order side: BUY or SELL")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT"], required=True, dest="order_type", help="Order type: MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, required=True, help="Amount of the asset to trade")
    parser.add_argument("--price", type=float, help="Desired execution price (Required if type is LIMIT)")

    args = parser.parse_args()

    # CLI-level Validation
    if args.order_type == "LIMIT" and args.price is None:
        parser.error("--price is strictly required when --type is LIMIT")

    # Load credentials
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("❌ Error: API credentials missing. Please check your .env file.")
        sys.exit(1)

    print("\n--- Order Request Summary ---")
    print(f"Symbol:   {args.symbol.upper()}")
    print(f"Side:     {args.side}")
    print(f"Type:     {args.order_type}")
    print(f"Quantity: {args.quantity}")
    if args.order_type == "LIMIT":
        print(f"Price:    {args.price}")
    print("-----------------------------\n")

    client = BinanceFuturesClient(api_key, api_secret)

    try:
        result = client.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price
        )

        print("✅ Order Successfully Placed!")
        print(f"Order ID:     {result.get('orderId')}")
        print(f"Status:       {result.get('status')}")
        print(f"Executed Qty: {result.get('executedQty')}")
        print(f"Avg Price:    {result.get('avgPrice', 'N/A')}\n")

    except Exception as e:
        print(f"❌ Order Failed: {e}")
        print("Check 'trading_bot.log' for detailed debugging information.\n")

if __name__ == "__main__":
    main()