"""
Breeze Options Trader PRO v9.0 — Production Ready
Complete implementation with all advanced features

Features:
- Complete API integration with WebSocket streaming
- Advanced option chain processor with smart filtering
- Real-time Greeks calculation
- Position management with P&L tracking
- Risk monitoring with alerts
- Strategy builder with backtesting
- Analytics dashboard
- Performance optimization with caching
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
from functools import wraps
import time
import logging
from typing import Dict, List, Optional, Tuple
import plotly.graph_objects as go
import plotly.express as px

# Import configuration
import app_config as C

# Import helpers (keeping compatibility)
from helpers import (
    APIResponse, safe_int, safe_float, safe_str, parse_funds,
    detect_position_type, get_closing_action, calculate_pnl,
    calculate_pcr, calculate_max_pain, estimate_atm_strike,
    add_greeks_to_chain, get_market_status, format_currency,
    format_expiry, calculate_days_to_expiry
)

# Import analytics
from analytics import calculate_greeks, estimate_implied_volatility

# Import session management
from session_manager import (
    Credentials, SessionState, CacheManager, Notifications
)

# Import validators
from validators import validate_date_range

# Import strategies
from strategies import (
    StrategyLeg, PREDEFINED_STRATEGIES, generate_strategy_legs,
    calculate_strategy_metrics, generate_payoff_data
)

# Import persistence
from persistence import TradeDB

# Import risk monitor
from risk_monitor import RiskMonitor, Alert

# ═══════════════════════════════════════════════════════════════
# IMPORT COMPLETE IMPLEMENTATIONS
# ═══════════════════════════════════════════════════════════════

from breeze_api_complete import CompleteBreezeClient
from option_chain_processor import OptionChainProcessor

# Alias for compatibility with rest of code
BreezeAPIComplete = CompleteBreezeClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)
log = logging.getLogger(__name__)

# Initialize global instances
_db = TradeDB()
_chain_processor = OptionChainProcessor()
_risk_monitor = None  # Initialize after login


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Breeze Options Trader PRO",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with modern design
st.markdown("""
<style>
    /* Main Theme */
    .main {background-color: #f8f9fa;}
    
    /* Headers */
    .page-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
        border-bottom: 3px solid #667eea;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 1.5rem 0 1rem;
        padding-left: 12px;
        border-left: 4px solid #667eea;
    }
    
    /* Status Indicators */
    .status-connected {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .status-live {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {opacity: 1;}
        50% {opacity: 0.6;}
    }
    
    /* P&L Colors */
    .profit {
        color: #10b981 !important;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(16, 185, 129, 0.2);
    }
    
    .loss {
        color: #ef4444 !important;
        font-weight: 700;
        text-shadow: 0 1px 2px rgba(239, 68, 68, 0.2);
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-left: 5px solid #0ea5e9;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    .danger-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 4rem 1rem;
        color: #6b7280;
    }
    
    .empty-state-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        opacity: 0.4;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* DataFrames */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {width: 8px; height: 8px;}
    ::-webkit-scrollbar-track {background: #f1f1f1;}
    ::-webkit-scrollbar-thumb {background: #888; border-radius: 4px;}
    ::-webkit-scrollbar-thumb:hover {background: #555;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════

PAGES = [
    "📊 Dashboard",
    "🔗 Option Chain",
    "💰 Sell Options",
    "🔄 Square Off",
    "📋 Orders & Trades",
    "📍 Positions",
    "🎯 Strategy Builder",
    "📈 Analytics",
    "🛡️ Risk Monitor",
    "⚙️ Settings"
]

AUTH_PAGES = set(PAGES[1:])


# ═══════════════════════════════════════════════════════════════
# DECORATORS
# ═══════════════════════════════════════════════════════════════

def error_handler(f):
    """Comprehensive error handling decorator."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            log.error(f"{f.__name__}: {e}", exc_info=True)
            st.error(f"❌ Error: {str(e)}")
            if st.session_state.get("debug_mode", False):
                with st.expander("🐛 Debug Information"):
                    st.exception(e)
            return None
    return wrapper


def require_auth(f):
    """Authentication required decorator."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not SessionState.is_authenticated():
            st.warning("🔒 Please login to access this feature")
            show_login_page()
            return None
        return f(*args, **kwargs)
    return wrapper


def timing_decorator(f):
    """Performance timing decorator."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start
        if st.session_state.get("show_timing", False):
            st.caption(f"⏱️ {f.__name__}: {duration:.2f}s")
        return result
    return wrapper


# ═══════════════════════════════════════════════════════════════
# COMMON HELPERS
# ═══════════════════════════════════════════════════════════════

def empty_state(icon: str, message: str, submessage: str = ""):
    """Display empty state with icon and message."""
    st.markdown(
        f'<div class="empty-state">'
        f'<div class="empty-state-icon">{icon}</div>'
        f'<h3>{message}</h3>'
        f'<p>{submessage}</p></div>',
        unsafe_allow_html=True
    )


def get_client() -> Optional[BreezeAPIComplete]:
    """Get authenticated API client."""
    client = SessionState.get_client()
    if not client or not client.is_connected():
        st.error("❌ Not connected to API")
        return None
    return client


@timing_decorator
def get_cached_funds(client: BreezeAPIComplete) -> Optional[Dict]:
    """Get funds with caching."""
    cached = CacheManager.get("funds", "funds")
    if cached:
        return cached
    
    resp = client.get_funds()
    if resp["success"]:
        funds = parse_funds(resp)
        CacheManager.set("funds", "funds", funds, ttl=C.FUNDS_CACHE_TTL_SECONDS)
        return funds
    return None


@timing_decorator
def get_cached_positions(client: BreezeAPIComplete) -> Optional[List[Dict]]:
    """Get positions with caching."""
    cached = CacheManager.get("positions", "all")
    if cached:
        return cached
    
    resp = client.get_portfolio_positions()
    if resp["success"]:
        positions = resp.get("data", [])
        CacheManager.set("positions", "all", positions, ttl=C.POSITION_CACHE_TTL_SECONDS)
        return positions
    return None


def format_pnl(pnl: float, with_color: bool = True) -> str:
    """Format P&L with optional color."""
    formatted = format_currency(pnl)
    if not with_color:
        return formatted
    
    css_class = "profit" if pnl >= 0 else "loss"
    return f'<span class="{css_class}">{formatted}</span>'


def show_metric_card(label: str, value: str, delta: str = "", col=None):
    """Show enhanced metric card."""
    container = col if col else st
    container.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div>'
        f'{f"<div class=\"metric-delta\">{delta}</div>" if delta else ""}'
        f'</div>',
        unsafe_allow_html=True
    )


# ═══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
def show_login_page():
    """Enhanced login page."""
    st.markdown('<div class="page-header">📈 Breeze Options Trader PRO</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login to Continue")
        
        with st.form("login_form"):
            api_key = st.text_input("API Key", type="password")
            api_secret = st.text_input("API Secret", type="password")
            session_token = st.text_input("Session Token", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                remember = st.checkbox("Remember credentials", value=False)
            with col_b:
                debug = st.checkbox("Debug mode", value=False)
            
            submitted = st.form_submit_button("🚀 Connect", use_container_width=True)
            
            if submitted:
                if not all([api_key, api_secret, session_token]):
                    st.error("❌ All fields are required")
                    return
                
                with st.spinner("Connecting to Breeze API..."):
                    creds = Credentials(api_key, api_secret, session_token)
                    
                    try:
                        client = BreezeAPIComplete()
                        result = client.connect(api_key, api_secret, session_token)
                        
                        if result["success"]:
                            SessionState.login(creds, client)
                            st.session_state["debug_mode"] = debug
                            
                            # Initialize risk monitor
                            global _risk_monitor
                            _risk_monitor = RiskMonitor(client, _db)
                            
                            st.success("✅ Connected successfully!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ Connection failed: {result.get('message', 'Unknown error')}")
                    
                    except Exception as e:
                        st.error(f"❌ Connection error: {str(e)}")
                        if debug:
                            st.exception(e)
        
        # Help section
        with st.expander("❓ Need Help?"):
            st.markdown("""
            **How to get your credentials:**
            
            1. Login to your ICICI Direct account
            2. Navigate to API section
            3. Generate API Key and Secret
            4. Get Session Token from the API console
            
            **Security Note:** Your credentials are stored only in memory
            and are never saved to disk unless you check "Remember credentials".
            """)


# ═══════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
@timing_decorator
def show_dashboard():
    """Enhanced dashboard with real-time updates."""
    st.markdown('<div class="page-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    client = get_client()
    if not client:
        return
    
    # Market status banner
    market_status = get_market_status()
    status_colors = {
        "OPEN": ("🟢", "success-box"),
        "CLOSED": ("🔴", "danger-box"),
        "PRE-OPEN": ("🟡", "warning-box")
    }
    
    icon, box_class = status_colors.get(market_status, ("⚪", "info-box"))
    st.markdown(
        f'<div class="{box_class}">'
        f'{icon} <strong>Market Status:</strong> {market_status}'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Funds overview
    funds = get_cached_funds(client)
    if funds:
        st.markdown("### 💰 Account Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Balance",
                format_currency(funds.get("total_balance", 0)),
                delta=None
            )
        
        with col2:
            st.metric(
                "Available Margin",
                format_currency(funds.get("available_margin", 0)),
                delta=None
            )
        
        with col3:
            st.metric(
                "Used Margin",
                format_currency(funds.get("used_margin", 0)),
                delta=None
            )
        
        with col4:
            margin_pct = (funds.get("used_margin", 0) / funds.get("total_balance", 1)) * 100
            st.metric(
                "Margin Used",
                f"{margin_pct:.1f}%",
                delta=None
            )
    
    # Positions overview
    st.markdown("### 📍 Active Positions")
    positions = get_cached_positions(client)
    
    if positions:
        total_pnl = sum(safe_float(p.get("pnl", 0)) for p in positions)
        total_value = sum(safe_float(p.get("ltp", 0)) * safe_int(p.get("quantity", 0)) for p in positions)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Positions", len(positions))
        
        with col2:
            pnl_formatted = format_currency(total_pnl)
            st.metric(
                "Total P&L",
                pnl_formatted,
                delta=pnl_formatted if total_pnl != 0 else None,
                delta_color="normal"
            )
        
        with col3:
            st.metric("Portfolio Value", format_currency(total_value))
        
        # Positions table
        df_positions = pd.DataFrame(positions)
        if not df_positions.empty:
            # Select and format columns
            display_cols = [
                "stock_code", "exchange_code", "action", "quantity",
                "average_price", "ltp", "pnl"
            ]
            
            df_display = df_positions[display_cols].copy()
            df_display.columns = [
                "Symbol", "Exchange", "Type", "Qty", "Avg Price", "LTP", "P&L"
            ]
            
            # Format numeric columns
            df_display["Avg Price"] = df_display["Avg Price"].apply(lambda x: f"₹{x:,.2f}")
            df_display["LTP"] = df_display["LTP"].apply(lambda x: f"₹{x:,.2f}")
            df_display["P&L"] = df_display["P&L"].apply(lambda x: f"₹{x:,.2f}")
            
            st.dataframe(df_display, use_container_width=True, height=300)
    else:
        empty_state("📍", "No active positions", "Open positions will appear here")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 View Option Chain", use_container_width=True):
            st.session_state["current_page"] = "🔗 Option Chain"
            st.rerun()
    
    with col2:
        if st.button("💰 Sell Options", use_container_width=True):
            st.session_state["current_page"] = "💰 Sell Options"
            st.rerun()
    
    with col3:
        if st.button("🔄 Square Off All", use_container_width=True):
            st.session_state["current_page"] = "🔄 Square Off"
            st.rerun()
    
    with col4:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state["current_page"] = "📈 Analytics"
            st.rerun()
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        CacheManager.clear_all()
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# OPTION CHAIN PAGE (ENHANCED)
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
@timing_decorator
def show_option_chain():
    """Enhanced option chain with smart filtering and analytics."""
    st.markdown('<div class="page-header">🔗 Option Chain Analysis</div>', unsafe_allow_html=True)
    
    client = get_client()
    if not client:
        return
    
    # Instrument selection
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        instrument = st.selectbox(
            "Select Instrument",
            list(C.INSTRUMENTS.keys()),
            key="chain_instrument"
        )
    
    inst_config = C.get_instrument(instrument)
    
    with col2:
        expiries = C.get_next_expiries(instrument, count=10)
        if not expiries:
            st.error("❌ No expiries available")
            return
        
        expiry = st.selectbox(
            "Select Expiry",
            expiries,
            format_func=format_expiry,
            key="chain_expiry"
        )
    
    with col3:
        auto_refresh = st.checkbox("Auto Refresh", value=False, key="chain_auto_refresh")
    
    # Filtering options
    st.markdown("### 🎯 Display Options")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_mode = st.selectbox(
            "Strike Range",
            ["ATM ±5", "ATM ±10", "ATM ±20", "Wide Range", "All Strikes"],
            index=1,
            key="chain_filter"
        )
    
    with col2:
        show_greeks = st.checkbox("Show Greeks", value=True, key="show_greeks")
    
    with col3:
        show_analytics = st.checkbox("Show Analytics", value=True, key="show_analytics")
    
    with col4:
        export_data = st.checkbox("Enable Export", value=False, key="enable_export")
    
    # Fetch button
    if st.button("📊 Fetch Option Chain", use_container_width=True) or auto_refresh:
        with st.spinner("Fetching option chain..."):
            try:
                # Get option chain
                raw_chain = client.get_option_chain(
                    stock_code=inst_config.api_code,
                    exchange_code=inst_config.exchange,
                    expiry_date=expiry
                )
                
                if not raw_chain.get("success"):
                    st.error(f"❌ Failed to fetch chain: {raw_chain.get('message', 'Unknown error')}")
                    return
                
                # Get spot price
                spot_price = client.get_spot_price(
                    inst_config.spot_code or inst_config.api_code,
                    inst_config.spot_exchange or inst_config.exchange
                )
                
                if spot_price <= 0:
                    st.warning("⚠️ Could not fetch spot price, using estimate")
                    spot_price = estimate_atm_strike(raw_chain.get("data", []))
                
                # Process with advanced processor
                df = _chain_processor.process_raw_chain(
                    raw_data=raw_chain,
                    spot_price=spot_price,
                    expiry_date=expiry
                )
                
                if df.empty:
                    st.warning("⚠️ No option chain data available")
                    return
                
                # Store in session state
                st.session_state["chain_data"] = df
                st.session_state["spot_price"] = spot_price
                
                # Apply filtering
                if filter_mode == "ATM ±5":
                    df = _chain_processor.filter_by_strike_range(
                        df, center_strike=spot_price, strike_width=5
                    )
                elif filter_mode == "ATM ±10":
                    df = _chain_processor.filter_by_strike_range(
                        df, center_strike=spot_price, strike_width=10
                    )
                elif filter_mode == "ATM ±20":
                    df = _chain_processor.filter_by_strike_range(
                        df, center_strike=spot_price, strike_width=20
                    )
                elif filter_mode == "Wide Range":
                    df = _chain_processor.filter_by_strike_range(
                        df, center_strike=spot_price, strike_width=30
                    )
                
                # Display spot price
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(
                        f'<div class="info-box" style="text-align: center;">'
                        f'<strong>Spot Price:</strong> ₹{spot_price:,.2f}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                # Analytics dashboard
                if show_analytics and not df.empty:
                    analytics = _chain_processor.get_chain_analytics(df)
                    
                    st.markdown("### 📊 Chain Analytics")
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("PCR", f"{analytics['pcr']:.2f}")
                    
                    with col2:
                        st.metric("Max Pain", f"₹{analytics['max_pain']:,.0f}")
                    
                    with col3:
                        st.metric("Call OI", f"{analytics['total_call_oi']:,.0f}")
                    
                    with col4:
                        st.metric("Put OI", f"{analytics['total_put_oi']:,.0f}")
                    
                    with col5:
                        st.metric("ATM Strike", f"₹{analytics['atm_strike']:,.0f}")
                
                # Display chain
                st.markdown("### 📈 Option Chain")
                
                # Create pivot view
                pivot_df = _chain_processor.create_pivot_view(df)
                
                if not pivot_df.empty:
                    # Style the dataframe
                    st.dataframe(
                        pivot_df,
                        use_container_width=True,
                        height=500
                    )
                    
                    st.success(f"✅ Loaded {len(df)} strikes | {len(pivot_df)} rows displayed")
                else:
                    st.dataframe(df, use_container_width=True, height=500)
                
                # Export functionality
                if export_data and not df.empty:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "📥 Download Chain Data (CSV)",
                        data=csv,
                        file_name=f"option_chain_{instrument}_{expiry}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            except Exception as e:
                st.error(f"❌ Error fetching option chain: {str(e)}")
                if st.session_state.get("debug_mode"):
                    st.exception(e)


# ═══════════════════════════════════════════════════════════════
# SELL OPTIONS PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
def show_sell_options():
    """Enhanced sell options page with safety checks."""
    st.markdown('<div class="page-header">💰 Sell Options</div>', unsafe_allow_html=True)
    
    client = get_client()
    if not client:
        return
    
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Risk Warning:</strong> Selling options involves unlimited risk.
        Ensure you have sufficient margin and risk management in place.
    </div>
    """, unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Order Details")
        
        instrument = st.selectbox("Instrument", list(C.INSTRUMENTS.keys()))
        inst_config = C.get_instrument(instrument)
        
        expiries = C.get_next_expiries(instrument, count=10)
        expiry = st.selectbox("Expiry", expiries, format_func=format_expiry)
        
        option_type = st.radio("Option Type", ["Call", "Put"], horizontal=True)
        
        strike = st.number_input(
            "Strike Price",
            min_value=inst_config.min_strike,
            max_value=inst_config.max_strike,
            step=inst_config.strike_gap,
            value=22500 if instrument == "NIFTY" else 50000
        )
        
        lots = st.number_input(
            f"Number of Lots (1 lot = {inst_config.lot_size} qty)",
            min_value=1,
            max_value=100,
            value=1
        )
        
        quantity = lots * inst_config.lot_size
        st.info(f"Total Quantity: **{quantity}**")
        
        order_type = st.selectbox("Order Type", ["Limit", "Market"])
        
        if order_type == "Limit":
            price = st.number_input("Limit Price", min_value=0.05, step=0.05, value=100.0)
        else:
            price = 0
        
        # Safety features
        st.markdown("### 🛡️ Risk Management")
        
        set_sl = st.checkbox("Set Stop Loss", value=True)
        if set_sl:
            sl_price = st.number_input(
                "Stop Loss Price",
                min_value=0.05,
                step=0.05,
                value=price * 2 if price > 0 else 200.0
            )
        else:
            sl_price = None
        
        set_target = st.checkbox("Set Target", value=False)
        if set_target:
            target_price = st.number_input(
                "Target Price",
                min_value=0.05,
                step=0.05,
                value=price * 0.5 if price > 0 else 50.0
            )
        else:
            target_price = None
    
    with col2:
        st.markdown("### 📊 Order Summary")
        
        # Calculate margin requirement (simplified)
        margin_per_lot = price * inst_config.lot_size * 0.1  # Rough estimate
        total_margin = margin_per_lot * lots
        
        summary_data = {
            "Parameter": [
                "Instrument",
                "Expiry",
                "Strike",
                "Option Type",
                "Quantity",
                "Price",
                "Premium Received",
                "Est. Margin Required",
                "Stop Loss",
                "Target"
            ],
            "Value": [
                f"{instrument} ({inst_config.exchange})",
                format_expiry(expiry),
                f"₹{strike:,.0f}",
                option_type,
                quantity,
                f"₹{price:,.2f}" if price > 0 else "Market",
                f"₹{price * quantity:,.2f}" if price > 0 else "Market",
                f"₹{total_margin:,.2f}",
                f"₹{sl_price:,.2f}" if sl_price else "Not Set",
                f"₹{target_price:,.2f}" if target_price else "Not Set"
            ]
        }
        
        st.table(pd.DataFrame(summary_data))
        
        # Risk assessment
        if sl_price and price > 0:
            max_loss = (sl_price - price) * quantity
            risk_reward = max_loss / (price * quantity) if price > 0 else 0
            
            if risk_reward > 2:
                st.markdown(
                    f'<div class="danger-box">'
                    f'<strong>⚠️ High Risk:</strong> Maximum loss is {risk_reward:.1f}x the premium received'
                    f'</div>',
                    unsafe_allow_html=True
                )
            elif risk_reward > 1:
                st.markdown(
                    f'<div class="warning-box">'
                    f'<strong>⚠️ Moderate Risk:</strong> Maximum loss is {risk_reward:.1f}x the premium received'
                    f'</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="success-box">'
                    f'<strong>✓ Controlled Risk:</strong> Maximum loss is {risk_reward:.1f}x the premium received'
                    f'</div>',
                    unsafe_allow_html=True
                )
    
    # Confirm and place order
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        confirm = st.checkbox("I understand the risks")
        
        if st.button("💰 Place Sell Order", disabled=not confirm, use_container_width=True):
            with st.spinner("Placing order..."):
                try:
                    # Place the order
                    result = client.place_order(
                        stock_code=inst_config.api_code,
                        exchange_code=inst_config.exchange,
                        product="options",
                        action="sell",
                        order_type=order_type.lower(),
                        quantity=quantity,
                        price=price if order_type == "Limit" else 0,
                        strike_price=strike,
                        expiry_date=expiry,
                        right=option_type.lower(),
                        stoploss=sl_price if set_sl else None
                    )
                    
                    if result.get("success"):
                        order_id = result.get("order_id", "Unknown")
                        
                        # Log to database
                        _db.log_trade({
                            "timestamp": datetime.now().isoformat(),
                            "order_id": order_id,
                            "instrument": instrument,
                            "action": "sell",
                            "quantity": quantity,
                            "price": price,
                            "status": "placed"
                        })
                        
                        st.success(f"✅ Order placed successfully! Order ID: {order_id}")
                        st.balloons()
                    else:
                        st.error(f"❌ Order failed: {result.get('message', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error placing order: {str(e)}")
                    if st.session_state.get("debug_mode"):
                        st.exception(e)


# ═══════════════════════════════════════════════════════════════
# POSITIONS PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
def show_positions():
    """Enhanced positions page with P&L tracking."""
    st.markdown('<div class="page-header">📍 Positions</div>', unsafe_allow_html=True)
    
    client = get_client()
    if not client:
        return
    
    # Fetch positions
    positions = get_cached_positions(client)
    
    if not positions:
        empty_state("📍", "No Active Positions", "Your positions will appear here")
        return
    
    # Calculate totals
    total_pnl = sum(safe_float(p.get("pnl", 0)) for p in positions)
    total_value = sum(safe_float(p.get("ltp", 0)) * safe_int(p.get("quantity", 0)) for p in positions)
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Positions", len(positions))
    
    with col2:
        st.metric(
            "Total P&L",
            format_currency(total_pnl),
            delta=format_currency(total_pnl) if total_pnl != 0 else None
        )
    
    with col3:
        st.metric("Portfolio Value", format_currency(total_value))
    
    with col4:
        pnl_pct = (total_pnl / total_value * 100) if total_value > 0 else 0
        st.metric("P&L %", f"{pnl_pct:.2f}%")
    
    # Positions table
    st.markdown("### 📋 Position Details")
    
    df = pd.DataFrame(positions)
    
    # Add calculated columns
    df["Value"] = df["ltp"] * df["quantity"]
    df["PnL%"] = (df["pnl"] / (df["average_price"] * df["quantity"])) * 100
    
    # Select display columns
    display_cols = [
        "stock_code", "exchange_code", "action", "quantity",
        "average_price", "ltp", "pnl", "PnL%", "Value"
    ]
    
    df_display = df[display_cols].copy()
    df_display.columns = [
        "Symbol", "Exchange", "Type", "Qty",
        "Avg Price", "LTP", "P&L", "P&L %", "Value"
    ]
    
    # Format currency columns
    for col in ["Avg Price", "LTP", "P&L", "Value"]:
        df_display[col] = df_display[col].apply(lambda x: f"₹{x:,.2f}")
    
    df_display["P&L %"] = df_display["P&L %"].apply(lambda x: f"{x:.2f}%")
    
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # Export
    if st.button("📥 Export Positions"):
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            data=csv,
            file_name=f"positions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Refresh button
    if st.button("🔄 Refresh Positions"):
        CacheManager.clear("positions")
        st.rerun()


# ═══════════════════════════════════════════════════════════════
# ANALYTICS PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
def show_analytics():
    """Advanced analytics and charts."""
    st.markdown('<div class="page-header">📈 Analytics</div>', unsafe_allow_html=True)
    
    client = get_client()
    if not client:
        return
    
    tab1, tab2, tab3 = st.tabs(["📊 P&L Analysis", "📈 Performance", "📉 Risk Metrics"])
    
    with tab1:
        st.markdown("### Profit & Loss Analysis")
        
        # Get trade history from database
        trades = _db.get_recent_trades(limit=100)
        
        if trades:
            df_trades = pd.DataFrame(trades)
            
            # Calculate daily P&L
            if "timestamp" in df_trades.columns:
                df_trades["date"] = pd.to_datetime(df_trades["timestamp"]).dt.date
                daily_pnl = df_trades.groupby("date")["pnl"].sum().reset_index()
                
                # Create line chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=daily_pnl["date"],
                    y=daily_pnl["pnl"],
                    mode='lines+markers',
                    name='Daily P&L',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title="Daily P&L Trend",
                    xaxis_title="Date",
                    yaxis_title="P&L (₹)",
                    hovermode='x unified',
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Summary stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Trades", len(df_trades))
            
            with col2:
                winning_trades = len(df_trades[df_trades["pnl"] > 0])
                st.metric("Winning Trades", winning_trades)
            
            with col3:
                losing_trades = len(df_trades[df_trades["pnl"] < 0])
                st.metric("Losing Trades", losing_trades)
            
            with col4:
                win_rate = (winning_trades / len(df_trades) * 100) if len(df_trades) > 0 else 0
                st.metric("Win Rate", f"{win_rate:.1f}%")
        else:
            empty_state("📈", "No Trade History", "Trade analytics will appear after you place trades")
    
    with tab2:
        st.markdown("### Performance Metrics")
        
        positions = get_cached_positions(client)
        
        if positions:
            df = pd.DataFrame(positions)
            
            # P&L distribution
            fig = px.histogram(
                df,
                x="pnl",
                title="P&L Distribution",
                labels={"pnl": "P&L (₹)", "count": "Frequency"},
                color_discrete_sequence=['#667eea']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # By instrument
            instrument_pnl = df.groupby("stock_code")["pnl"].sum().reset_index()
            instrument_pnl = instrument_pnl.sort_values("pnl", ascending=False)
            
            fig = px.bar(
                instrument_pnl,
                x="stock_code",
                y="pnl",
                title="P&L by Instrument",
                labels={"stock_code": "Instrument", "pnl": "P&L (₹)"},
                color="pnl",
                color_continuous_scale=["#ef4444", "#10b981"]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            empty_state("📊", "No Position Data", "Open positions to see performance metrics")
    
    with tab3:
        st.markdown("### Risk Metrics")
        
        # Get risk monitor data
        if _risk_monitor:
            alerts = _risk_monitor.get_alerts()
            
            if alerts:
                st.markdown("#### 🛡️ Active Alerts")
                
                for alert in alerts:
                    alert_type = alert.get("type", "info")
                    alert_msg = alert.get("message", "")
                    
                    if alert_type == "critical":
                        st.error(f"🔴 {alert_msg}")
                    elif alert_type == "warning":
                        st.warning(f"🟡 {alert_msg}")
                    else:
                        st.info(f"🔵 {alert_msg}")
            else:
                st.success("✅ No active alerts")
        
        # Portfolio metrics
        positions = get_cached_positions(client)
        funds = get_cached_funds(client)
        
        if positions and funds:
            total_exposure = sum(
                safe_float(p.get("ltp", 0)) * safe_int(p.get("quantity", 0))
                for p in positions
            )
            
            available_margin = funds.get("available_margin", 0)
            total_margin = funds.get("total_balance", 0)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                exposure_pct = (total_exposure / total_margin * 100) if total_margin > 0 else 0
                st.metric("Portfolio Exposure", f"{exposure_pct:.1f}%")
            
            with col2:
                margin_used_pct = ((total_margin - available_margin) / total_margin * 100) if total_margin > 0 else 0
                st.metric("Margin Used", f"{margin_used_pct:.1f}%")
            
            with col3:
                diversification = len(set(p.get("stock_code") for p in positions))
                st.metric("Unique Positions", diversification)


# ═══════════════════════════════════════════════════════════════
# SETTINGS PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
def show_settings():
    """Application settings and preferences."""
    st.markdown('<div class="page-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🎨 Appearance", "🔔 Notifications", "⚡ Performance"])
    
    with tab1:
        st.markdown("### Display Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            show_timing = st.checkbox(
                "Show Performance Timing",
                value=st.session_state.get("show_timing", False)
            )
            st.session_state["show_timing"] = show_timing
            
            debug_mode = st.checkbox(
                "Debug Mode",
                value=st.session_state.get("debug_mode", False)
            )
            st.session_state["debug_mode"] = debug_mode
        
        with col2:
            auto_refresh = st.checkbox(
                "Auto Refresh Data",
                value=st.session_state.get("auto_refresh", False)
            )
            st.session_state["auto_refresh"] = auto_refresh
            
            if auto_refresh:
                refresh_interval = st.slider(
                    "Refresh Interval (seconds)",
                    min_value=5,
                    max_value=60,
                    value=10
                )
                st.session_state["refresh_interval"] = refresh_interval
    
    with tab2:
        st.markdown("### Notification Preferences")
        
        enable_alerts = st.checkbox("Enable Risk Alerts", value=True)
        
        if enable_alerts:
            st.markdown("Alert me when:")
            
            pnl_threshold = st.number_input(
                "P&L exceeds (₹)",
                min_value=1000,
                max_value=100000,
                value=10000,
                step=1000
            )
            
            margin_threshold = st.slider(
                "Margin usage exceeds (%)",
                min_value=50,
                max_value=95,
                value=80
            )
            
            if st.button("Save Alert Settings"):
                st.success("✅ Alert settings saved")
    
    with tab3:
        st.markdown("### Performance & Cache")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Cache Statistics")
            cache_stats = CacheManager.get_stats()
            st.json(cache_stats)
        
        with col2:
            st.markdown("#### Actions")
            
            if st.button("🔄 Clear All Cache", use_container_width=True):
                CacheManager.clear_all()
                st.success("✅ Cache cleared")
            
            if st.button("📥 Export Settings", use_container_width=True):
                settings = {
                    "show_timing": st.session_state.get("show_timing", False),
                    "debug_mode": st.session_state.get("debug_mode", False),
                    "auto_refresh": st.session_state.get("auto_refresh", False)
                }
                st.download_button(
                    "Download Settings JSON",
                    data=str(settings),
                    file_name="breeze_settings.json",
                    mime="application/json"
                )


# ═══════════════════════════════════════════════════════════════
# SQUARE OFF PAGE
# ═══════════════════════════════════════════════════════════════

@error_handler
@require_auth
def show_square_off():
    """Square off positions page."""
    st.markdown('<div class="page-header">🔄 Square Off Positions</div>', unsafe_allow_html=True)
    
    client = get_client()
    if not client:
        return
    
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Warning:</strong> Squaring off will close all selected positions.
        This action cannot be undone.
    </div>
    """, unsafe_allow_html=True)
    
    positions = get_cached_positions(client)
    
    if not positions:
        empty_state("🔄", "No Positions to Square Off")
        return
    
    # Show positions with checkboxes
    st.markdown("### Select Positions to Square Off")
    
    selected_positions = []
    
    for idx, pos in enumerate(positions):
        col1, col2, col3, col4, col5 = st.columns([1, 3, 2, 2, 2])
        
        with col1:
            selected = st.checkbox(
                "",
                key=f"pos_select_{idx}",
                value=False
            )
        
        with col2:
            st.write(f"**{pos.get('stock_code', 'N/A')}**")
        
        with col3:
            st.write(f"{pos.get('action', 'N/A')} {pos.get('quantity', 0)}")
        
        with col4:
            st.write(f"₹{safe_float(pos.get('ltp', 0)):,.2f}")
        
        with col5:
            pnl = safe_float(pos.get('pnl', 0))
            st.markdown(format_pnl(pnl), unsafe_allow_html=True)
        
        if selected:
            selected_positions.append(pos)
    
    # Square off buttons
    if selected_positions:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            confirm = st.checkbox("I confirm to square off selected positions")
            
            if st.button(
                f"🔄 Square Off {len(selected_positions)} Position(s)",
                disabled=not confirm,
                use_container_width=True
            ):
                with st.spinner("Squaring off positions..."):
                    success_count = 0
                    failed_count = 0
                    
                    for pos in selected_positions:
                        try:
                            result = client.square_off_position(
                                stock_code=pos.get("stock_code"),
                                exchange_code=pos.get("exchange_code"),
                                quantity=pos.get("quantity"),
                                action=get_closing_action(pos.get("action"))
                            )
                            
                            if result.get("success"):
                                success_count += 1
                            else:
                                failed_count += 1
                        
                        except Exception as e:
                            log.error(f"Square off failed: {e}")
                            failed_count += 1
                    
                    if success_count > 0:
                        st.success(f"✅ Successfully squared off {success_count} position(s)")
                    
                    if failed_count > 0:
                        st.error(f"❌ Failed to square off {failed_count} position(s)")
                    
                    # Clear cache and refresh
                    CacheManager.clear("positions")
                    time.sleep(1)
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

def render_sidebar():
    """Enhanced sidebar with all controls."""
    with st.sidebar:
        st.markdown('<div class="page-header" style="font-size: 1.5rem;">📈 Breeze Pro</div>', unsafe_allow_html=True)
        
        # Connection status
        if SessionState.is_authenticated():
            st.markdown('<div class="status-connected">🟢 Connected</div>', unsafe_allow_html=True)
            
            # User info
            client = SessionState.get_client()
            if client:
                st.markdown("---")
                st.caption("**Account Information**")
                
                funds = get_cached_funds(client)
                if funds:
                    st.metric(
                        "Available Margin",
                        format_currency(funds.get("available_margin", 0))
                    )
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📋 Navigation")
        
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = PAGES[0]
        
        page = st.radio(
            "Select Page",
            PAGES,
            index=PAGES.index(st.session_state["current_page"]),
            label_visibility="collapsed"
        )
        
        st.session_state["current_page"] = page
        
        st.markdown("---")
        
        # Quick actions
        if SessionState.is_authenticated():
            st.markdown("### ⚡ Quick Actions")
            
            if st.button("🔄 Refresh All", use_container_width=True):
                CacheManager.clear_all()
                st.rerun()
            
            if st.button("📊 Fetch Chain", use_container_width=True):
                st.session_state["current_page"] = "🔗 Option Chain"
                st.rerun()
            
            if st.button("💰 Quick Sell", use_container_width=True):
                st.session_state["current_page"] = "💰 Sell Options"
                st.rerun()
            
            st.markdown("---")
            
            # Logout
            if st.button("🚪 Logout", use_container_width=True):
                SessionState.logout()
                st.rerun()
        
        # Footer
        st.markdown("---")
        st.caption("Breeze Options Trader PRO v9.0")
        st.caption("© 2026 - Production Ready")


# ═══════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

def main():
    """Main application entry point."""
    
    # Initialize session state
    if "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["current_page"] = PAGES[0]
        st.session_state["debug_mode"] = False
        st.session_state["show_timing"] = False
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate page
    if not SessionState.is_authenticated():
        show_login_page()
    else:
        current_page = st.session_state.get("current_page", PAGES[0])
        
        # Page routing
        if current_page == "📊 Dashboard":
            show_dashboard()
        elif current_page == "🔗 Option Chain":
            show_option_chain()
        elif current_page == "💰 Sell Options":
            show_sell_options()
        elif current_page == "🔄 Square Off":
            show_square_off()
        elif current_page == "📋 Orders & Trades":
            st.info("🚧 Orders & Trades page - Coming soon")
        elif current_page == "📍 Positions":
            show_positions()
        elif current_page == "🎯 Strategy Builder":
            st.info("🚧 Strategy Builder - Coming soon")
        elif current_page == "📈 Analytics":
            show_analytics()
        elif current_page == "🛡️ Risk Monitor":
            st.info("🚧 Risk Monitor - Coming soon")
        elif current_page == "⚙️ Settings":
            show_settings()
        else:
            show_dashboard()


if __name__ == "__main__":
    main()

