# main.py
"""
Command-line interface for the Trading Bot
Handles user input and executes trading commands
"""

from bot import BasicBot
from config import API_KEY, API_SECRET, TESTNET, DEFAULT_SYMBOL
from logger_config import setup_logger
import sys

def print_banner():
    """Print welcome banner"""
    print("=" * 60)
    print("  BINANCE FUTURES TRADING BOT - TESTNET")
    print("=" * 60)
    print()

def print_menu():
    """Print main menu options"""
    print("\n--- MAIN MENU ---")
    print("1. Place Market Order")
    print("2. Place Limit Order")
    print("3. Place Stop-Limit Order")
    print("4. View Account Balance")
    print("5. View Open Orders")
    print("6. Cancel Order")
    print("7. Exit")
    print("-" * 40)

def get_user_input(prompt, input_type=str, valid_options=None):
    """
    Get and validate user input
    
    Args:
        prompt (str): Input prompt message
        input_type (type): Expected input type (str, float, int)
        valid_options (list, optional): List of valid options for the input
    
    Returns:
        Validated user input
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            if user_input.lower() == 'cancel':
                return None
            
            # Convert to appropriate type
            if input_type == float:
                value = float(user_input)
            elif input_type == int:
                value = int(user_input)
            else:
                value = user_input
            
            # Check valid options if provided
            if valid_options and value not in valid_options:
                print(f"Invalid input. Must be one of: {valid_options}")
                continue
            
            return value
            
        except ValueError:
            print(f"Invalid input. Expected {input_type.__name__}. Try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None

def handle_market_order(bot):
    """Handle market order placement"""
    print("\n--- PLACE MARKET ORDER ---")
    print("(Type 'cancel' at any time to return to main menu)")
    
    # Get symbol
    symbol = get_user_input(f"Enter symbol (default: {DEFAULT_SYMBOL}): ", str)
    if symbol is None:
        return
    if not symbol:
        symbol = DEFAULT_SYMBOL
    
    # Get side
    side = get_user_input("Enter side (BUY/SELL): ", str, ['BUY', 'SELL', 'buy', 'sell'])
    if side is None:
        return
    
    # Get quantity
    quantity = get_user_input("Enter quantity: ", float)
    if quantity is None:
        return
    
    # Confirm order
    print(f"\nOrder Summary:")
    print(f"  Type: MARKET")
    print(f"  Symbol: {symbol}")
    print(f"  Side: {side.upper()}")
    print(f"  Quantity: {quantity}")
    
    confirm = get_user_input("\nConfirm order? (yes/no): ", str, ['yes', 'no', 'y', 'n'])
    if confirm and confirm.lower() in ['yes', 'y']:
        result = bot.place_market_order(symbol, side, quantity)
        if result:
            print("\n✓ Order placed successfully!")
            print(f"  Order ID: {result.get('orderId')}")
            print(f"  Status: {result.get('status')}")
        else:
            print("\n✗ Order failed. Check logs for details.")
    else:
        print("Order cancelled.")

def handle_limit_order(bot):
    """Handle limit order placement"""
    print("\n--- PLACE LIMIT ORDER ---")
    print("(Type 'cancel' at any time to return to main menu)")
    
    # Get symbol
    symbol = get_user_input(f"Enter symbol (default: {DEFAULT_SYMBOL}): ", str)
    if symbol is None:
        return
    if not symbol:
        symbol = DEFAULT_SYMBOL
    
    # Get side
    side = get_user_input("Enter side (BUY/SELL): ", str, ['BUY', 'SELL', 'buy', 'sell'])
    if side is None:
        return
    
    # Get quantity
    quantity = get_user_input("Enter quantity: ", float)
    if quantity is None:
        return
    
    # Get price
    price = get_user_input("Enter limit price: ", float)
    if price is None:
        return
    
    # Confirm order
    print(f"\nOrder Summary:")
    print(f"  Type: LIMIT")
    print(f"  Symbol: {symbol}")
    print(f"  Side: {side.upper()}")
    print(f"  Quantity: {quantity}")
    print(f"  Price: {price}")
    
    confirm = get_user_input("\nConfirm order? (yes/no): ", str, ['yes', 'no', 'y', 'n'])
    if confirm and confirm.lower() in ['yes', 'y']:
        result = bot.place_limit_order(symbol, side, quantity, price)
        if result:
            print("\n✓ Order placed successfully!")
            print(f"  Order ID: {result.get('orderId')}")
            print(f"  Status: {result.get('status')}")
        else:
            print("\n✗ Order failed. Check logs for details.")
    else:
        print("Order cancelled.")

def handle_stop_limit_order(bot):
    """Handle stop-limit order placement"""
    print("\n--- PLACE STOP-LIMIT ORDER ---")
    print("(Type 'cancel' at any time to return to main menu)")
    
    # Get symbol
    symbol = get_user_input(f"Enter symbol (default: {DEFAULT_SYMBOL}): ", str)
    if symbol is None:
        return
    if not symbol:
        symbol = DEFAULT_SYMBOL
    
    # Get side
    side = get_user_input("Enter side (BUY/SELL): ", str, ['BUY', 'SELL', 'buy', 'sell'])
    if side is None:
        return
    
    # Get quantity
    quantity = get_user_input("Enter quantity: ", float)
    if quantity is None:
        return
    
    # Get stop price
    stop_price = get_user_input("Enter stop price (trigger): ", float)
    if stop_price is None:
        return
    
    # Get limit price
    price = get_user_input("Enter limit price: ", float)
    if price is None:
        return
    
    # Confirm order
    print(f"\nOrder Summary:")
    print(f"  Type: STOP-LIMIT")
    print(f"  Symbol: {symbol}")
    print(f"  Side: {side.upper()}")
    print(f"  Quantity: {quantity}")
    print(f"  Stop Price: {stop_price}")
    print(f"  Limit Price: {price}")
    
    confirm = get_user_input("\nConfirm order? (yes/no): ", str, ['yes', 'no', 'y', 'n'])
    if confirm and confirm.lower() in ['yes', 'y']:
        result = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
        if result:
            print("\n✓ Order placed successfully!")
            print(f"  Order ID: {result.get('orderId')}")
            print(f"  Status: {result.get('status')}")
        else:
            print("\n✗ Order failed. Check logs for details.")
    else:
        print("Order cancelled.")

def handle_view_balance(bot):
    """Display account balance"""
    print("\n--- ACCOUNT BALANCE ---")
    balance = bot.get_account_balance()
    if balance:
        print(f"  Total Balance: {balance['total_balance']} USDT")
        print(f"  Available Balance: {balance['available_balance']} USDT")
    else:
        print("Failed to retrieve balance.")

def handle_view_orders(bot):
    """Display open orders"""
    print("\n--- OPEN ORDERS ---")
    symbol = get_user_input("Enter symbol (or press Enter for all): ", str)
    
    orders = bot.get_open_orders(symbol if symbol else None)
    
    if not orders:
        print("No open orders.")
        return
    
    print(f"\nFound {len(orders)} open order(s):")
    for order in orders:
        print(f"\n  Order ID: {order.get('orderId')}")
        print(f"  Symbol: {order.get('symbol')}")
        print(f"  Side: {order.get('side')}")
        print(f"  Type: {order.get('type')}")
        print(f"  Price: {order.get('price')}")
        print(f"  Quantity: {order.get('origQty')}")
        print(f"  Status: {order.get('status')}")

def handle_cancel_order(bot):
    """Cancel an order"""
    print("\n--- CANCEL ORDER ---")
    
    symbol = get_user_input("Enter symbol: ", str)
    if symbol is None:
        return
    
    order_id = get_user_input("Enter order ID to cancel: ", int)
    if order_id is None:
        return
    
    confirm = get_user_input(f"\nCancel order {order_id} for {symbol}? (yes/no): ", str, ['yes', 'no', 'y', 'n'])
    if confirm and confirm.lower() in ['yes', 'y']:
        result = bot.cancel_order(symbol, order_id)
        if result:
            print("\n✓ Order cancelled successfully!")
        else:
            print("\n✗ Failed to cancel order. Check logs for details.")
    else:
        print("Cancellation aborted.")

def main():
    """Main program loop"""
    logger = setup_logger("CLI")
    
    print_banner()
    
    # Check API credentials
    if API_KEY == "your_api_key_here" or API_SECRET == "your_api_secret_here":
        print("ERROR: Please update your API credentials in config.py")
        print("Get your testnet API keys from: https://testnet.binancefuture.com/")
        sys.exit(1)
    
    # Initialize bot
    try:
        print("Initializing bot...")
        bot = BasicBot(API_KEY, API_SECRET, testnet=TESTNET)
        print("✓ Bot initialized successfully!\n")
    except Exception as e:
        print(f"✗ Failed to initialize bot: {e}")
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)
    
    # Main loop
    while True:
        try:
            print_menu()
            choice = get_user_input("Select option (1-7): ", str, ['1', '2', '3', '4', '5', '6', '7'])
            
            if choice is None or choice == '7':
                print("\nExiting bot. Goodbye!")
                break
            elif choice == '1':
                handle_market_order(bot)
            elif choice == '2':
                handle_limit_order(bot)
            elif choice == '3':
                handle_stop_limit_order(bot)
            elif choice == '4':
                handle_view_balance(bot)
            elif choice == '5':
                handle_view_orders(bot)
            elif choice == '6':
                handle_cancel_order(bot)
            
        except KeyboardInterrupt:
            print("\n\nExiting bot. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()