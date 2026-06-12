import argparse
import os
import sys
from dotenv import load_dotenv
from client import BinanceFuturesClient

def main():
    parser = argparse.ArgumentParser(description="Check Binance Futures Order Status")
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair (e.g., BTCUSDT)")
    parser.add_argument("--order-id", type=int, required=True, help="Order ID to check")

    args = parser.parse_args()

    # Load credentials
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("❌ Error: API credentials missing. Please check your .env file.")
        sys.exit(1)

    # Initialize the client
    client = BinanceFuturesClient(api_key, api_secret)

    try:
        # Get order status
        orders = client.get_order_status(args.symbol, args.order_id)

        print("\n--- Order Status ---")
        for order in orders:
            print(f"Order ID:      {order.get('orderId')}")
            print(f"Symbol:        {order.get('symbol')}")
            print(f"Side:          {order.get('side')}")
            print(f"Type:          {order.get('type')}")
            print(f"Status:        {order.get('status')}")
            print(f"Quantity:      {order.get('origQty')}")
            print(f"Executed Qty:  {order.get('executedQty')}")
            print(f"Avg Price:     {order.get('avgPrice', 'N/A')}")
            print(f"Price:         {order.get('price', 'N/A')}")
            print(f"Time:          {order.get('time')}")
            print(f"Update Time:   {order.get('updateTime')}\n")

    except Exception as e:
        print(f"❌ Failed to get order status: {e}")
        print("Check 'trading_bot.log' for detailed debugging information.\n")

if __name__ == "__main__":
    main()
