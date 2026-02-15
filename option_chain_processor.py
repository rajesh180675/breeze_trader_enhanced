"""
Complete Option Chain Processor
Handles ALL strikes with intelligent filtering and display optimization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import logging

import app_config as C
from analytics import calculate_greeks, estimate_implied_volatility

log = logging.getLogger(__name__)


class OptionChainProcessor:
    """
    Production-grade option chain processor.
    Handles complete chains with thousands of strikes efficiently.
    """
    
    def __init__(self):
        self.last_processed = None
        self.cache = {}
    
    def process_raw_chain(
        self,
        raw_data: Dict,
        spot_price: float = 0,
        expiry_date: str = ""
    ) -> pd.DataFrame:
        """
        Process raw API response into structured DataFrame.
        
        Args:
            raw_data: Raw response from Breeze API
            spot_price: Spot price for Greeks calculation
            expiry_date: Expiry date for Greeks calculation
            
        Returns:
            Processed DataFrame with all option data
        """
        if not raw_data:
            log.warning("Empty option chain data received")
            return pd.DataFrame()
        
        # Extract records
        if "Success" in raw_data:
            records = raw_data["Success"]
        elif isinstance(raw_data, list):
            records = raw_data
        else:
            log.error(f"Unexpected data format: {type(raw_data)}")
            return pd.DataFrame()
        
        if not records:
            log.warning("No records in option chain")
            return pd.DataFrame()
        
        log.info(f"Processing {len(records)} option chain records")
        
        # Create DataFrame
        df = pd.DataFrame(records)
        
        if df.empty:
            return df
        
        # Normalize column names (handle variations)
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Key columns to process
        numeric_cols = [
            'strike_price', 'ltp', 'ltq', 'volume', 'open_interest',
            'best_bid_price', 'best_offer_price', 'best_bid_quantity',
            'best_offer_quantity', 'open', 'high', 'low', 'close',
            'ltp_percent_change', 'oi_change', 'iv', 'vega', 'theta',
            'gamma', 'delta', 'rho'
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Normalize option type
        if 'right' in df.columns:
            df['right'] = df['right'].astype(str).str.strip().str.capitalize()
            # Standardize to Call/Put
            df['right'] = df['right'].replace({
                'C': 'Call', 'CE': 'Call', 'Ca': 'Call',
                'P': 'Put', 'PE': 'Put', 'Pu': 'Put'
            })
        elif 'option_type' in df.columns:
            df['right'] = df['option_type'].astype(str).str.strip().str.capitalize()
        
        # Ensure strike_price exists
        if 'strike_price' not in df.columns and 'strike' in df.columns:
            df['strike_price'] = df['strike']
        
        # Remove invalid strikes
        if 'strike_price' in df.columns:
            df = df[df['strike_price'] > 0]
        
        # Sort by strike and option type
        if 'strike_price' in df.columns and 'right' in df.columns:
            df = df.sort_values(['strike_price', 'right'])
        
        # Add Greeks if spot price available
        if spot_price > 0 and expiry_date and 'strike_price' in df.columns:
            df = self._add_greeks(df, spot_price, expiry_date)
        
        # Add derived columns
        df = self._add_derived_columns(df)
        
        log.info(f"Processed chain: {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def _add_greeks(
        self,
        df: pd.DataFrame,
        spot_price: float,
        expiry_date: str
    ) -> pd.DataFrame:
        """
        Calculate and add Greeks to DataFrame.
        
        Args:
            df: Option chain DataFrame
            spot_price: Underlying spot price
            expiry_date: Expiry date
            
        Returns:
            DataFrame with Greeks columns added
        """
        try:
            # Calculate time to expiry
            expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
            tte = max(
                (expiry - datetime.now(C.IST).replace(tzinfo=None)).days / C.DAYS_PER_YEAR,
                0.001
            )
        except Exception as e:
            log.warning(f"Could not calculate time to expiry: {e}")
            tte = 0.05
        
        greeks_list = []
        
        for idx, row in df.iterrows():
            strike = row.get('strike_price', 0)
            option_type = C.normalize_option_type(row.get('right'))
            ltp = row.get('ltp', 0)
            
            if option_type in ('CE', 'PE') and strike > 0 and spot_price > 0:
                try:
                    # Get or estimate IV
                    iv_raw = row.get('iv', 0)
                    if iv_raw > 1:  # Percentage format
                        iv = iv_raw / 100
                    elif iv_raw > 0:
                        iv = iv_raw
                    else:
                        # Estimate IV from LTP
                        if ltp > 0:
                            iv = estimate_implied_volatility(
                                ltp, spot_price, strike, tte, option_type
                            )
                        else:
                            iv = 0.20  # Default
                    
                    # Calculate Greeks
                    greeks = calculate_greeks(
                        spot_price, strike, tte, iv, option_type
                    )
                    greeks_list.append(greeks)
                    
                except Exception as e:
                    log.debug(f"Greeks calculation failed for strike {strike}: {e}")
                    greeks_list.append({
                        'delta': 0, 'gamma': 0, 'theta': 0,
                        'vega': 0, 'rho': 0
                    })
            else:
                greeks_list.append({
                    'delta': 0, 'gamma': 0, 'theta': 0,
                    'vega': 0, 'rho': 0
                })
        
        # Add Greeks columns
        greeks_df = pd.DataFrame(greeks_list)
        
        # Only add columns that don't exist
        for col in greeks_df.columns:
            if col not in df.columns:
                df[col] = greeks_df[col]
        
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add useful derived columns to DataFrame.
        
        Args:
            df: Option chain DataFrame
            
        Returns:
            DataFrame with additional calculated columns
        """
        if df.empty:
            return df
        
        # Moneyness indicator
        if 'strike_price' in df.columns and 'ltp' in df.columns:
            # Simple moneyness classification
            if 'right' in df.columns:
                # This requires spot price, but we can classify based on premium
                df['moneyness'] = 'ATM'  # Placeholder
        
        # Bid-Ask spread
        if 'best_bid_price' in df.columns and 'best_offer_price' in df.columns:
            df['spread'] = df['best_offer_price'] - df['best_bid_price']
            df['spread_pct'] = np.where(
                df['ltp'] > 0,
                (df['spread'] / df['ltp'] * 100),
                0
            )
        
        # Volume to OI ratio
        if 'volume' in df.columns and 'open_interest' in df.columns:
            df['vol_oi_ratio'] = np.where(
                df['open_interest'] > 0,
                df['volume'] / df['open_interest'],
                0
            )
        
        # Liquidity score (simple)
        if 'volume' in df.columns and 'open_interest' in df.columns:
            df['liquidity_score'] = df['volume'] + (df['open_interest'] / 10)
        
        return df
    
    def create_pivot_view(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create traditional option chain pivot view.
        Calls on left, strikes in middle, Puts on right.
        
        Args:
            df: Processed option chain DataFrame
            
        Returns:
            Pivot table with traditional layout
        """
        if df.empty or 'strike_price' not in df.columns or 'right' not in df.columns:
            return pd.DataFrame()
        
        # Fields to show
        display_fields = {
            'open_interest': 'OI',
            'volume': 'Vol',
            'ltp': 'LTP',
            'iv': 'IV',
            'delta': 'Delta',
            'best_bid_price': 'Bid',
            'best_offer_price': 'Ask'
        }
        
        available_fields = {
            k: v for k, v in display_fields.items()
            if k in df.columns
        }
        
        if not available_fields:
            return df
        
        # Separate calls and puts
        calls = df[df['right'] == 'Call'].set_index('strike_price')
        puts = df[df['right'] == 'Put'].set_index('strike_price')
        
        # Get all unique strikes
        all_strikes = sorted(df['strike_price'].unique())
        
        # Create result DataFrame
        result = pd.DataFrame({'Strike': all_strikes})
        result = result.set_index('Strike')
        
        # Add call columns (left side)
        for field, label in available_fields.items():
            if field in calls.columns:
                result[f'C_{label}'] = calls[field]
        
        # Add put columns (right side)
        for field, label in available_fields.items():
            if field in puts.columns:
                result[f'P_{label}'] = puts[field]
        
        # Reset index to have Strike as column
        result = result.fillna(0).reset_index()
        
        # Reorder: Call columns, Strike, Put columns
        call_cols = [c for c in result.columns if c.startswith('C_')]
        put_cols = [c for c in result.columns if c.startswith('P_')]
        
        return result[call_cols + ['Strike'] + put_cols]
    
    def filter_around_atm(
        self,
        df: pd.DataFrame,
        atm_strike: float,
        num_strikes: int = 20
    ) -> pd.DataFrame:
        """
        Filter option chain around ATM strike.
        
        Args:
            df: Complete option chain
            atm_strike: ATM strike price
            num_strikes: Number of strikes on each side
            
        Returns:
            Filtered DataFrame
        """
        if df.empty or 'strike_price' not in df.columns:
            return df
        
        strikes = sorted(df['strike_price'].unique())
        
        if not strikes:
            return df
        
        # Find closest strike to ATM
        atm_idx = min(
            range(len(strikes)),
            key=lambda i: abs(strikes[i] - atm_strike)
        )
        
        # Get range
        start_idx = max(0, atm_idx - num_strikes)
        end_idx = min(len(strikes), atm_idx + num_strikes + 1)
        
        selected_strikes = strikes[start_idx:end_idx]
        
        return df[df['strike_price'].isin(selected_strikes)].copy()
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate key option chain metrics.
        
        Args:
            df: Option chain DataFrame
            
        Returns:
            Dict of calculated metrics
        """
        metrics = {}
        
        if df.empty:
            return metrics
        
        # PCR (Put-Call Ratio)
        if 'right' in df.columns and 'open_interest' in df.columns:
            call_oi = df[df['right'] == 'Call']['open_interest'].sum()
            put_oi = df[df['right'] == 'Put']['open_interest'].sum()
            metrics['pcr'] = put_oi / call_oi if call_oi > 0 else 0
            metrics['call_oi_total'] = call_oi
            metrics['put_oi_total'] = put_oi
        
        # Max Pain
        if 'strike_price' in df.columns and 'right' in df.columns and 'open_interest' in df.columns:
            metrics['max_pain'] = self._calculate_max_pain(df)
        
        # ATM estimation
        if 'strike_price' in df.columns and 'right' in df.columns and 'ltp' in df.columns:
            metrics['atm_strike'] = self._estimate_atm(df)
        
        # Total volume and OI
        if 'volume' in df.columns:
            metrics['total_volume'] = df['volume'].sum()
        
        if 'open_interest' in df.columns:
            metrics['total_oi'] = df['open_interest'].sum()
        
        # Active strikes (with volume)
        if 'volume' in df.columns and 'strike_price' in df.columns:
            active = df[df['volume'] > 0]['strike_price'].nunique()
            metrics['active_strikes'] = active
        
        return metrics
    
    def _calculate_max_pain(self, df: pd.DataFrame) -> float:
        """Calculate max pain strike."""
        strikes = df['strike_price'].unique()
        
        if len(strikes) == 0:
            return 0
        
        pain = {}
        
        for strike in strikes:
            # Call pain: all calls ITM
            call_pain = (
                (strike - df[(df['right'] == 'Call') & (df['strike_price'] < strike)]['strike_price']) *
                df[(df['right'] == 'Call') & (df['strike_price'] < strike)]['open_interest']
            ).sum()
            
            # Put pain: all puts ITM  
            put_pain = (
                (df[(df['right'] == 'Put') & (df['strike_price'] > strike)]['strike_price'] - strike) *
                df[(df['right'] == 'Put') & (df['strike_price'] > strike)]['open_interest']
            ).sum()
            
            pain[strike] = call_pain + put_pain
        
        return float(min(pain, key=pain.get)) if pain else 0
    
    def _estimate_atm(self, df: pd.DataFrame) -> float:
        """Estimate ATM strike from option prices."""
        calls = df[df['right'] == 'Call'][['strike_price', 'ltp']].set_index('strike_price')
        puts = df[df['right'] == 'Put'][['strike_price', 'ltp']].set_index('strike_price')
        
        combined = calls.join(puts, lsuffix='_call', rsuffix='_put').dropna()
        
        if combined.empty:
            # Fallback to middle strike
            strikes = sorted(df['strike_price'].unique())
            return strikes[len(strikes) // 2] if strikes else 0
        
        # ATM is where call and put prices are closest
        combined['diff'] = abs(combined['ltp_call'] - combined['ltp_put'])
        
        return float(combined['diff'].idxmin())
    
    def get_most_active_strikes(
        self,
        df: pd.DataFrame,
        top_n: int = 10,
        by: str = 'volume'
    ) -> pd.DataFrame:
        """
        Get most active strikes by volume or OI.
        
        Args:
            df: Option chain DataFrame
            top_n: Number of top strikes
            by: 'volume' or 'open_interest'
            
        Returns:
            DataFrame with top strikes
        """
        if df.empty or by not in df.columns:
            return pd.DataFrame()
        
        # Group by strike and sum
        grouped = df.groupby('strike_price')[by].sum().sort_values(ascending=False)
        
        top_strikes = grouped.head(top_n).index.tolist()
        
        return df[df['strike_price'].isin(top_strikes)].copy()
    
    def get_call_put_summary(self, df: pd.DataFrame) -> Dict:
        """
        Get summary statistics for calls and puts separately.
        
        Args:
            df: Option chain DataFrame
            
        Returns:
            Dict with call and put summaries
        """
        summary = {'calls': {}, 'puts': {}}
        
        if df.empty or 'right' not in df.columns:
            return summary
        
        for option_type, key in [('Call', 'calls'), ('Put', 'puts')]:
            subset = df[df['right'] == option_type]
            
            if subset.empty:
                continue
            
            summary[key] = {
                'total_oi': subset['open_interest'].sum() if 'open_interest' in subset.columns else 0,
                'total_volume': subset['volume'].sum() if 'volume' in subset.columns else 0,
                'avg_iv': subset['iv'].mean() if 'iv' in subset.columns else 0,
                'strikes_count': subset['strike_price'].nunique() if 'strike_price' in subset.columns else 0,
                'max_oi_strike': subset.loc[subset['open_interest'].idxmax(), 'strike_price'] if 'open_interest' in subset.columns and not subset.empty else 0,
                'max_volume_strike': subset.loc[subset['volume'].idxmax(), 'strike_price'] if 'volume' in subset.columns and not subset.empty else 0,
            }
        
        return summary


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def process_option_chain_complete(
    raw_data: Dict,
    spot_price: float = 0,
    expiry_date: str = "",
    atm_strike: float = 0,
    num_strikes: int = 0
) -> Tuple[pd.DataFrame, Dict]:
    """
    Complete option chain processing with metrics.
    
    Args:
        raw_data: Raw API response
        spot_price: Spot price for Greeks
        expiry_date: Expiry date
        atm_strike: ATM strike for filtering (0 for all)
        num_strikes: Number of strikes around ATM (0 for all)
        
    Returns:
        Tuple of (processed_df, metrics_dict)
    """
    processor = OptionChainProcessor()
    
    # Process complete chain
    df = processor.process_raw_chain(raw_data, spot_price, expiry_date)
    
    # Filter if requested
    if atm_strike > 0 and num_strikes > 0:
        df = processor.filter_around_atm(df, atm_strike, num_strikes)
    
    # Calculate metrics
    metrics = processor.calculate_metrics(df)
    
    return df, metrics


__all__ = ['OptionChainProcessor', 'process_option_chain_complete']
