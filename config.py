# config.py
"""
Configuration file for Binance Trading Bot
Store your API credentials here (for testnet only!)
"""
import os

# Binance Testnet API Credentials
# IMPORTANT: Replace these with your actual testnet API credentials

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# API_KEY = "rIPDspSuhog6RCfArJYDRsaGQcjcV53J6tom4VAydbFZ5zaE5hok57ywzXsB13PH"
# API_SECRET = "7QEuAqO7wkCuqt5yU5JkYAScPXIEECxW53y4YYCMz0nfI5GVRsEDCr1Dzrl6MUBI"

# Binance Testnet Configuration
TESTNET = True
TESTNET_BASE_URL = "https://testnet.binance.vision"

# Trading Parameters
DEFAULT_SYMBOL = "BTCUSDT"
DEFAULT_QUANTITY = 0.001  # Small amount for testing

# Logging Configuration
LOG_FILE = "logs/trading_bot.log"
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

# Order Types Supported
ORDER_TYPES = ["MARKET", "LIMIT", "STOP_LIMIT", "STOP_MARKET"]
ORDER_SIDES = ["BUY", "SELL"]

# Validation Rules
MIN_QUANTITY = 0.001
MAX_QUANTITY = 100.0

print(API_KEY,API_SECRET)