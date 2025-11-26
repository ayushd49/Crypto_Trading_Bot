# bot.py
"""
Main Trading Bot Class
Handles connection to Binance Futures Testnet and order execution
"""

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from logger_config import setup_logger
from config import (
    TESTNET_BASE_URL, MIN_QUANTITY, MAX_QUANTITY,
    ORDER_TYPES, ORDER_SIDES
)
import json

class BasicBot:
    """
    A simplified trading bot for Binance Futures Testnet
    Supports market, limit, and stop orders
    """
    
    def __init__(self, api_key, api_secret, testnet=True):
        """
        Initialize the trading bot
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            testnet (bool): Use testnet if True, live trading if False
        """
        self.logger = setup_logger("TradingBot")
        self.testnet = testnet
        
        try:
            # Initialize Binance client
            self.client = Client(api_key, api_secret, testnet=testnet)
            
            # Set testnet URL for futures
            if testnet:
                self.client.API_URL = TESTNET_BASE_URL
            
            self.logger.info(f"Bot initialized - Testnet: {testnet}")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {e}")
            raise
    
    def _test_connection(self):
        """Test API connection and log account info"""
        try:
            account_info = self.client.futures_account()
            balance = account_info.get('totalWalletBalance', 'N/A')
            self.logger.info(f"Connection successful - Wallet Balance: {balance} USDT")
            return True
        except BinanceAPIException as e:
            self.logger.error(f"API connection failed: {e}")
            raise
    
    def validate_order_params(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        """
        Validate order parameters before sending
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            order_type (str): Order type (MARKET, LIMIT, etc.)
            quantity (float): Order quantity
            price (float, optional): Limit price
            stop_price (float, optional): Stop price
        
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        # Validate side
        if side.upper() not in ORDER_SIDES:
            return False, f"Invalid side. Must be one of: {ORDER_SIDES}"
        
        # Validate order type
        if order_type.upper() not in ORDER_TYPES:
            return False, f"Invalid order type. Must be one of: {ORDER_TYPES}"
        
        # Validate quantity
        if not isinstance(quantity, (int, float)) or quantity <= 0:
            return False, "Quantity must be a positive number"
        
        if quantity < MIN_QUANTITY or quantity > MAX_QUANTITY:
            return False, f"Quantity must be between {MIN_QUANTITY} and {MAX_QUANTITY}"
        
        # Validate price for limit orders
        if order_type.upper() in ['LIMIT', 'STOP_LIMIT'] and price is None:
            return False, f"{order_type} orders require a price"
        
        # Validate stop price for stop orders
        if order_type.upper() in ['STOP_LIMIT', 'STOP_MARKET'] and stop_price is None:
            return False, f"{order_type} orders require a stop_price"
        
        return True, "Valid"
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order
        
        Args:
            symbol (str): Trading pair (e.g., 'BTCUSDT')
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
        
        Returns:
            dict: Order response or None if failed
        """
        # Validate parameters
        is_valid, error_msg = self.validate_order_params(symbol, side, "MARKET", quantity)
        if not is_valid:
            self.logger.error(f"Validation failed: {error_msg}")
            return None
        
        try:
            self.logger.info(f"Placing MARKET {side} order: {quantity} {symbol}")
            
            # Place market order
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='MARKET',
                quantity=quantity,
                reduce_only=True
            )
            
            self.logger.info(f"Order placed successfully - Order ID: {order.get('orderId')}")
            self._log_order_details(order)
            
            return order
            
        except BinanceOrderException as e:
            self.logger.error(f"Order failed: {e}")
            return None
        except BinanceAPIException as e:
            self.logger.error(f"API error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
    
    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order
        
        Args:
            symbol (str): Trading pair
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            price (float): Limit price
        
        Returns:
            dict: Order response or None if failed
        """
        # Validate parameters
        is_valid, error_msg = self.validate_order_params(symbol, side, "LIMIT", quantity, price=price)
        if not is_valid:
            self.logger.error(f"Validation failed: {error_msg}")
            return None
        
        try:
            self.logger.info(f"Placing LIMIT {side} order: {quantity} {symbol} @ {price}")
            
            # Place spot limit order
            order = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',  # Good Till Cancel
                quantity=quantity,
                price=price
            )
            
            self.logger.info(f"Order placed successfully - Order ID: {order.get('orderId')}")
            self._log_order_details(order)
            
            return order
            
        except BinanceOrderException as e:
            self.logger.error(f"Order failed: {e}")
            return None
        except BinanceAPIException as e:
            self.logger.error(f"API error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
    
    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        """
        Place a stop-limit order (Optional advanced feature)
        
        Args:
            symbol (str): Trading pair
            side (str): 'BUY' or 'SELL'
            quantity (float): Order quantity
            price (float): Limit price after stop is triggered
            stop_price (float): Stop trigger price
        
        Returns:
            dict: Order response or None if failed
        """
        # Validate parameters
        is_valid, error_msg = self.validate_order_params(
            symbol, side, "STOP_LIMIT", quantity, price=price, stop_price=stop_price
        )
        if not is_valid:
            self.logger.error(f"Validation failed: {error_msg}")
            return None
        
        try:
            self.logger.info(f"Placing STOP_LIMIT {side} order: {quantity} {symbol} @ {price}, stop @ {stop_price}")
            oside='SELL' if side.upper()=='BUY' else 'BUY'
            # Place spot stop-limit order
            order_limit = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=side.upper(),
                type='LIMIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                # stopPrice=stop_price
                workingType='CONTRACT_PRICE'
            )

            order_profit = self.client.futures_create_order(
                symbol=symbol.upper(),
                side=oside,
                type='TAKE PROFIT',
                timeInForce='GTC',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                workingType='CONTRACT_PRICE'
            )
            
            
            self.logger.info(f"Order placed successfully - Order ID: {order_limit.get('orderId')}")
            self._log_order_details(order_limit)

            self.logger.info(f"Order placed successfully - Order ID: {order_profit.get('orderId')}")
            self._log_order_details(order_profit)
            
            return (order_limit,order_profit)
            
        except BinanceOrderException as e:
            self.logger.error(f"Order failed: {e}")
            return None
        except BinanceAPIException as e:
            self.logger.error(f"API error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
    
    def get_account_balance(self):
        """
        Get current account balance
        
        Returns:
            dict: Account balance information
        """
        try:
            account = self.client.futures_account()
            balances = account.get('assets',[])
            
            # Get USDT balance
            usdt_balance = next((b for b in balances if b['asset'] == 'USDT'), None)
            
            if usdt_balance:
                balance_info = {
                    'total_balance': float(usdt_balance['availableBalance']) + float(usdt_balance['unrealizedProfit']),
                    'available_balance': float(usdt_balance['availableBalance'])
                }
            else:
                balance_info = {
                    'total_balance': 0.0,
                    'available_balance': 0.0
                }
            
            self.logger.info(f"Account Balance: {balance_info}")
            return balance_info
            
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get balance: {e}")
            return None
    
    def get_open_orders(self, symbol=None):
        """
        Get all open orders
        
        Args:
            symbol (str, optional): Filter by symbol
        
        Returns:
            list: List of open orders
        """
        try:
            if symbol:
                orders = self.client.futures_get_open_orders(symbol=symbol.upper())
            else:
                orders = self.client.futures_get_open_orders()
            
            self.logger.info(f"Retrieved {len(orders)} open orders")
            return orders
            
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get open orders: {e}")
            return []
    
    def cancel_order(self, symbol, order_id):
        """
        Cancel an open order
        
        Args:
            symbol (str): Trading pair
            order_id (int): Order ID to cancel
        
        Returns:
            dict: Cancellation response or None if failed
        """
        try:
            self.logger.info(f"Cancelling order {order_id} for {symbol}")
            
            result = self.client.futures_cancel_order(
                symbol=symbol.upper(),
                orderId=order_id
            )
            
            self.logger.info(f"Order {order_id} cancelled successfully")
            return result
            
        except BinanceAPIException as e:
            self.logger.error(f"Failed to cancel order: {e}")
            return None
    
    def _log_order_details(self, order):
        """
        Log detailed order information
        
        Args:
            order (dict): Order response from Binance
        """
        order_details = {
            'orderId': order.get('orderId'),
            'symbol': order.get('symbol'),
            'side': order.get('side'),
            'type': order.get('type'),
            'status': order.get('status'),
            'quantity': order.get('origQty'),
            'price': order.get('price'),
            'executedQty': order.get('executedQty'),
            'avgPrice': order.get('avgPrice')
        }
        
        self.logger.debug(f"Order Details: {json.dumps(order_details, indent=2)}")