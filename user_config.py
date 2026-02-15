# ═══════════════════════════════════════════════════════════════
# Breeze Options Trader PRO - Configuration File
# ═══════════════════════════════════════════════════════════════

"""
User Configuration File

Customize your trading experience by modifying the settings below.
All changes take effect immediately upon app restart.
"""

# ═══════════════════════════════════════════════════════════════
# TRADING PREFERENCES
# ═══════════════════════════════════════════════════════════════

TRADING = {
    # Default order type
    "default_order_type": "Limit",  # Options: "Limit", "Market"
    
    # Risk management
    "enable_stoploss": True,  # Always prompt for stop loss
    "default_sl_multiplier": 2.0,  # Stop loss = premium × multiplier
    "max_loss_per_trade": 10000,  # Maximum loss per trade in INR
    
    # Position sizing
    "max_lots_per_order": 10,  # Maximum lots in single order
    "default_lots": 1,  # Default number of lots
    
    # Safety features
    "require_confirmation": True,  # Ask for confirmation before orders
    "enable_risk_warnings": True,  # Show risk warnings
    
    # Auto square-off
    "enable_auto_square_off": False,  # Auto square off at EOD
    "square_off_time": "15:15",  # Time to auto square off (HH:MM)
}


# ═══════════════════════════════════════════════════════════════
# DISPLAY PREFERENCES
# ═══════════════════════════════════════════════════════════════

DISPLAY = {
    # Option chain display
    "default_strike_range": "ATM ±10",  # Options: "ATM ±5", "ATM ±10", "ATM ±20", "Wide Range", "All Strikes"
    "show_greeks": True,  # Show Greeks in option chain
    "show_analytics": True,  # Show PCR, Max Pain, etc.
    
    # Charts and graphs
    "chart_theme": "plotly_white",  # Options: "plotly", "plotly_white", "plotly_dark"
    "enable_animations": True,  # Enable chart animations
    
    # Data refresh
    "auto_refresh_enabled": False,  # Auto refresh data
    "refresh_interval_seconds": 10,  # Refresh interval
    
    # Performance
    "show_timing": False,  # Show execution timing
    "cache_enabled": True,  # Enable data caching
}


# ═══════════════════════════════════════════════════════════════
# ALERTS AND NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════

ALERTS = {
    # P&L alerts
    "enable_pnl_alerts": True,  # Enable P&L alerts
    "profit_alert_threshold": 5000,  # Alert when profit exceeds (INR)
    "loss_alert_threshold": -3000,  # Alert when loss exceeds (INR)
    
    # Margin alerts
    "enable_margin_alerts": True,  # Alert on high margin usage
    "margin_warning_threshold": 80,  # Warning at % margin usage
    "margin_critical_threshold": 90,  # Critical at % margin usage
    
    # Position alerts
    "alert_on_position_change": True,  # Alert when positions change
    "alert_on_order_fill": True,  # Alert when orders fill
    
    # Market alerts
    "alert_on_market_close": True,  # Alert 15 mins before market close
    "alert_on_expiry_day": True,  # Alert on expiry day
}


# ═══════════════════════════════════════════════════════════════
# ADVANCED SETTINGS
# ═══════════════════════════════════════════════════════════════

ADVANCED = {
    # API settings
    "api_timeout_seconds": 30,  # API request timeout
    "max_retries": 3,  # Maximum API retries
    "retry_delay_seconds": 1,  # Delay between retries
    
    # WebSocket settings
    "enable_websocket": False,  # Enable real-time streaming (Beta)
    "websocket_reconnect": True,  # Auto reconnect WebSocket
    
    # Database settings
    "db_path": "data/breeze_trader.db",  # Database location
    "keep_trade_history_days": 90,  # Keep trade history for N days
    
    # Logging
    "log_level": "INFO",  # Options: "DEBUG", "INFO", "WARNING", "ERROR"
    "log_to_file": True,  # Save logs to file
    "log_file_path": "logs/app.log",  # Log file location
    
    # Debug mode
    "debug_mode": False,  # Enable debug information
    "verbose_logging": False,  # Detailed logging
}


# ═══════════════════════════════════════════════════════════════
# CUSTOMIZATION
# ═══════════════════════════════════════════════════════════════

CUSTOMIZATION = {
    # Appearance
    "theme_color": "#667eea",  # Primary theme color (hex)
    "use_custom_css": True,  # Enable custom styling
    
    # Default instrument
    "default_instrument": "NIFTY",  # Default instrument on app load
    
    # Favorite instruments (show these first)
    "favorite_instruments": [
        "NIFTY",
        "BANKNIFTY",
        "FINNIFTY"
    ],
    
    # Quick actions (show in dashboard)
    "quick_actions": [
        "View Option Chain",
        "Sell Options",
        "Square Off All",
        "Analytics"
    ],
}


# ═══════════════════════════════════════════════════════════════
# INSTRUMENT OVERRIDES
# ═══════════════════════════════════════════════════════════════

"""
Override default instrument settings here.
Leave empty dict {} to use defaults from app_config.py
"""

INSTRUMENT_OVERRIDES = {
    # Example:
    # "NIFTY": {
    #     "lot_size": 65,  # Override lot size
    #     "strike_gap": 50,  # Override strike gap
    # }
}


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_config(section: str, key: str = None):
    """
    Get configuration value.
    
    Args:
        section: Configuration section (e.g., 'TRADING')
        key: Specific key within section (optional)
    
    Returns:
        Configuration value or entire section
    
    Examples:
        >>> get_config('TRADING', 'default_order_type')
        'Limit'
        
        >>> get_config('DISPLAY')
        {...}  # Entire DISPLAY section
    """
    sections = {
        'TRADING': TRADING,
        'DISPLAY': DISPLAY,
        'ALERTS': ALERTS,
        'ADVANCED': ADVANCED,
        'CUSTOMIZATION': CUSTOMIZATION,
        'INSTRUMENT_OVERRIDES': INSTRUMENT_OVERRIDES
    }
    
    section_data = sections.get(section.upper())
    
    if section_data is None:
        return None
    
    if key is None:
        return section_data
    
    return section_data.get(key)


def validate_config():
    """Validate configuration settings."""
    errors = []
    
    # Validate trading settings
    if TRADING['max_lots_per_order'] < 1:
        errors.append("max_lots_per_order must be >= 1")
    
    if TRADING['default_sl_multiplier'] < 1:
        errors.append("default_sl_multiplier must be >= 1")
    
    # Validate display settings
    valid_strike_ranges = ["ATM ±5", "ATM ±10", "ATM ±20", "Wide Range", "All Strikes"]
    if DISPLAY['default_strike_range'] not in valid_strike_ranges:
        errors.append(f"default_strike_range must be one of {valid_strike_ranges}")
    
    # Validate alert thresholds
    if ALERTS['margin_warning_threshold'] >= ALERTS['margin_critical_threshold']:
        errors.append("margin_warning_threshold must be < margin_critical_threshold")
    
    return errors


# Validate on import
_validation_errors = validate_config()
if _validation_errors:
    print("⚠️ Configuration Validation Errors:")
    for error in _validation_errors:
        print(f"   - {error}")
    print("\nPlease fix these errors in user_config.py")


# ═══════════════════════════════════════════════════════════════
# EXPORT CONFIGURATION
# ═══════════════════════════════════════════════════════════════

__all__ = [
    'TRADING',
    'DISPLAY',
    'ALERTS',
    'ADVANCED',
    'CUSTOMIZATION',
    'INSTRUMENT_OVERRIDES',
    'get_config',
    'validate_config'
]
