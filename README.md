# Binance Futures Trading Bot - 

A simplified trading bot for Binance Futures Testnet with CLI interface.

## Features Implemented

✅ Market Orders (Buy/Sell)
✅ Limit Orders (Buy/Sell)
✅ Stop-Limit Orders (Advanced feature)
✅ Account Balance Viewing
✅ Open Orders Management
✅ Order Cancellation
✅ Input Validation
✅ Comprehensive Logging
✅ Error Handling
✅ Command-Line Interface

## Setup Instructions

### 1. Get Binance Testnet Credentials

1. Visit https://testnet.binancefuture.com/
2. Register with your email
3. Go to API Key management (top right menu)
4. Generate new API Key and Secret
5. Save both keys securely
6. Set API KEY and API SECRET as environment variables

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv trading_bot_env

# Activate virtual environment
# Windows:
trading_bot_env\Scripts\activate
# Mac/Linux:
source trading_bot_env/bin/activate

# Install requirements
pip install -r requirements.txt


```

### 3. Configure API Keys

```
# Set Environment Variable
set API_KEY= 'Your API KEY here'
set API_SECRET= 'Your API SECRET here'
```

With your actual testnet credentials.

### 4. Create Logs Directory

```bash
mkdir logs
```

## Running the Bot

```bash
python main.py
```

## Usage Examples

### Example 1: Market Order
1. Select option 1 from menu
2. Enter symbol: `BTCUSDT` (or press Enter for default)
3. Enter side: `BUY`
4. Enter quantity: `0.001`
5. Confirm: `yes`

### Example 2: Limit Order
1. Select option 2 from menu
2. Enter symbol: `ETHUSDT`
3. Enter side: `SELL`
4. Enter quantity: `0.01`
5. Enter limit price: `3500`
6. Confirm: `yes`

### Example 3: Stop-Limit Order
1. Select option 3 from menu
2. Enter symbol: `BTCUSDT`
3. Enter side: `BUY`
4. Enter quantity: `0.001`
5. Enter stop price: `65000` (trigger price)
6. Enter limit price: `65100` (execution price)
7. Confirm: `yes`

## Testing Checklist

- [ ] Bot initializes and connects to testnet
- [ ] Account balance displays correctly
- [ ] Market BUY order executes
- [ ] Market SELL order executes
- [ ] Limit BUY order places successfully
- [ ] Limit SELL order places successfully
- [ ] Stop-Limit order places successfully
- [ ] Open orders display correctly
- [ ] Order cancellation works
- [ ] Invalid inputs are rejected
- [ ] Logs are created in logs/ directory
- [ ] Error messages are clear and helpful

## File Structure

```
trading_bot/
├── config.py          # API credentials and configuration
├── bot.py            # Main bot class with order logic
├── main.py           # CLI interface
├── logger_config.py  # Logging setup
├── requirements.txt  # Python dependencies
├── logs/            # Log files directory
│   └── trading_bot.log
└── README.md        # This file
```

## Key Features Explained

### 1. Order Validation
- Checks order type, side, quantity
- Validates price for limit orders
- Validates stop price for stop orders
- Prevents invalid orders from being sent

### 2. Logging System
- All orders logged with timestamps
- Errors logged with details
- Console output for user feedback
- File logging for audit trail

### 3. Error Handling
- Catches API exceptions
- Handles connection errors
- Validates user input
- Provides clear error messages

### 4. Reusable Code Structure
- Separate configuration file
- Modular bot class
- Independent CLI interface
- Easy to extend and modify

## Common Issues & Solutions

### Issue: "Failed to initialize bot"
**Solution**: Check your API credentials in config.py

### Issue: "Order failed: Insufficient balance"
**Solution**: Your testnet account needs funds. Go to https://testnet.binancefuture.com/ and use the faucet to get test USDT

### Issue: "Invalid symbol"
**Solution**: Make sure the symbol is correctly formatted (e.g., BTCUSDT, not BTC-USDT)

### Issue: "Price filter error"
**Solution**: Adjust your price to match the symbol's tick size requirements

## Advanced Features Implemented

### Stop-Limit Orders
Stop-limit orders combine a stop price (trigger) with a limit price (execution). When the market reaches the stop price, a limit order is placed at the specified limit price.

Use case: Set a buy order that triggers when price drops to $50,000 but execute at $49,900.

## Requirements Coverage

| Requirement | Status | Location |
|------------|--------|----------|
| Binance Testnet Registration | ✅ | Manual step |
| API Credentials | ✅ | config.py |
| Testnet Base URL | ✅ | config.py |
| python-binance library | ✅ | bot.py |
| Market Orders | ✅ | bot.py - place_market_order() |
| Limit Orders | ✅ | bot.py - place_limit_order() |
| Buy/Sell sides | ✅ | All order functions |
| Command-line interface | ✅ | main.py |
| Input validation | ✅ | bot.py - validate_order_params() |
| Output order details | ✅ | bot.py - _log_order_details() |
| Logging | ✅ | logger_config.py |
| Error handling | ✅ | Try-except blocks throughout |
| Advanced orders | ✅ | bot.py - place_stop_limit_order() |
| Code reusability | ✅ | Modular structure |

## Next Steps for Enhancement

1. Add WebSocket support for real-time price updates
2. Implement position management
3. Add risk management features (stop-loss, take-profit)
4. Create trading strategies
5. Add backtesting capabilities
6. Build a GUI interface

## Support

For issues:
1. Check logs in `logs/trading_bot.log`
2. Verify API credentials
3. Ensure testnet account has funds
4. Check Binance API status
