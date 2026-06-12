import time
import hmac
import hashlib
import requests
import urllib.parse
from typing import Optional
from logger import setup_logger


logger = setup_logger()
class BinanceFuturesClient:
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _generate_signature(self, query_strings: str) -> str:
        return hmac.new(self.api_secret.encode('utf-8'), query_strings.encode('utf-8'), hashlib.sha256).hexdigest()
    
    def place_order(self, symbol: str, side: str, quantity: float, order_type: str = "MARKET", price: Optional[float] = None):
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }

        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price must be provided for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = "GTC"

        query_string = urllib.parse.urlencode(params)
        signature = self._generate_signature(query_string)
        params["signature"] = signature

        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"Initiating {side} order for {quantity} {symbol} (Type: {order_type})")
        logger.info(f"Request URL: {url} | Payload: {params}")

        try:
            response = self.session.post(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Order Success. Response: {data}")
            return data
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                error_msg = f"HTTP {e.response.status_code} - {e.response.text}"
            else:
                error_msg = str(e)
            logger.error(f"API Error: {error_msg}")
            raise RuntimeError(f"Binance API Error: {error_msg}") from e
        except requests.exceptions.Timeout:
            logger.error("Request timeout - Binance API took too long to respond")
            raise RuntimeError("Request timeout - failed to connect to Binance Testnet.") from None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Connection Error: {e}")
            raise RuntimeError("Failed to connect to Binance Testnet.") from e

    def get_order_status(self, symbol: str, order_id: int):
        """Get the status of an order"""
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "timestamp": int(time.time() * 1000)
        }

        query_string = urllib.parse.urlencode(params)
        signature = self._generate_signature(query_string)
        params["signature"] = signature

        url = f"{self.BASE_URL}{endpoint}"
        logger.info(f"Fetching order status for {symbol} - Order ID: {order_id}")

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()

            try:
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f"Invalid JSON response from API: {response.text}")
                raise RuntimeError("Received invalid JSON response from Binance API") from e

            logger.info(f"Order Status: {data}")
            return data if isinstance(data, list) else [data]
        except requests.exceptions.HTTPError as e:
            if e.response is not None:
                error_msg = f"HTTP {e.response.status_code} - {e.response.text}"
            else:
                error_msg = str(e)
            logger.error(f"API Error: {error_msg}")
            raise RuntimeError(f"Binance API Error: {error_msg}") from e
        except requests.exceptions.Timeout:
            logger.error("Request timeout - Binance API took too long to respond")
            raise RuntimeError("Request timeout - failed to connect to Binance Testnet.") from None
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Connection Error: {e}")
            raise RuntimeError("Failed to connect to Binance Testnet.") from e