# 🚀 Quick Start Guide - Breeze Options Trader Enhanced v8.5

Get up and running in 5 minutes!

## Prerequisites

✅ Python 3.8 or higher  
✅ ICICI Breeze trading account  
✅ API credentials from ICICI Breeze portal

## Step 1: Install (2 minutes)

### Windows
```bash
# Double-click setup.bat OR run in CMD:
setup.bat
```

### Linux / macOS
```bash
# Run in terminal:
chmod +x setup.sh
./setup.sh
```

### Manual Installation
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure Credentials (1 minute)

Create `.streamlit/secrets.toml`:

```toml
BREEZE_API_KEY = "your_api_key_here"
BREEZE_API_SECRET = "your_api_secret_here"
```

**Get your credentials:**
1. Login to ICICI Breeze portal: https://api.icicidirect.com/apiuser/home
2. Go to API Key section
3. Copy API Key and API Secret

## Step 3: Run Application (30 seconds)

```bash
streamlit run app.py
```

Application opens at: **http://localhost:8501**

## Step 4: Login (30 seconds)

1. **Get Session Token** (daily):
   - Login to ICICI Breeze
   - Navigate to API section
   - Generate/View session token

2. **In the app**:
   - Paste session token in sidebar
   - Click "Connect"
   - ✅ You're in!

## Step 5: Start Trading (1 minute)

### View Market Data
1. Click "📊 Option Chain"
2. Select instrument (NIFTY/BANKNIFTY)
3. Choose expiry date
4. View live data with Greeks

### Place Your First Order
1. Click "💰 Sell Options"
2. Select instrument & expiry
3. Choose strike price
4. Set quantity (in lots)
5. Preview and confirm

### Set Stop-Loss (Recommended!)
1. Click "🛡️ Risk Monitor"
2. Add position to monitor
3. Set stop-loss (fixed or trailing)
4. Relax - it monitors automatically!

## Common Tasks

### Check Your Positions
- Dashboard → View all positions
- Real-time P&L updates
- Greeks for each position

### View Orders & Trades
- "📋 Orders & Trades" page
- Filter by date/status
- Download history

### Build Strategies
- "🎯 Strategy Builder"
- Choose from 7 pre-defined strategies
- View payoff curves
- See break-even points

### Analytics
- "📈 Analytics" page
- Portfolio Greeks
- P&L analysis
- Risk metrics

## Troubleshooting

### "Connection Failed"
- ✅ Check API credentials
- ✅ Get fresh session token (expires daily)
- ✅ Verify internet connection

### "Session Expired"
- ✅ Session tokens expire after 24 hours
- ✅ Login to ICICI portal
- ✅ Get new token and reconnect

### Data Not Loading
- ✅ Check market hours (9:15 AM - 3:30 PM IST)
- ✅ Click "🔄 Refresh" button
- ✅ Try different instrument

### Slow Performance
- ✅ Reduce number of strikes in option chain
- ✅ Clear cache periodically
- ✅ Close unused browser tabs

## Safety Tips

⚠️ **IMPORTANT - READ BEFORE TRADING**

1. **Test First**: Place small test orders before going live
2. **Use Stop-Losses**: ALWAYS set stop-losses on positions
3. **Check Margins**: Verify you have sufficient margin
4. **Monitor Actively**: Keep an eye on positions
5. **Daily Tokens**: Get fresh session token every day
6. **Backup Data**: Data stored in `data/` directory

## Key Features at a Glance

| Feature | Location | Description |
|---------|----------|-------------|
| Live Quotes | Option Chain | Real-time option prices |
| Greeks | Option Chain | Delta, Gamma, Theta, Vega, Rho |
| Sell Options | Sell Options | One-click option selling |
| Stop-Loss | Risk Monitor | Automated risk management |
| Strategies | Strategy Builder | Pre-built multi-leg strategies |
| Analytics | Analytics | Portfolio analysis & metrics |
| History | Orders & Trades | Complete trade history |

## Keyboard Shortcuts

(When implemented - coming soon!)

- `Ctrl+R` - Refresh data
- `Ctrl+S` - Quick sell
- `Ctrl+B` - Quick buy
- `Esc` - Close modals

## Support

**Common Questions?** Check:
1. README.md - Full documentation
2. REVIEW_REPORT.md - Technical details
3. Inline help in the app

**Still Stuck?**
- Double-check credentials
- Verify market hours
- Review error messages carefully
- Check ICICI Breeze API status

## Next Steps

After getting comfortable:

1. **Explore Strategies**: Try Iron Condor or Strangle
2. **Set Up Monitoring**: Add all positions to risk monitor
3. **Review Analytics**: Understand your portfolio Greeks
4. **Track Performance**: Export trade history regularly
5. **Optimize**: Adjust cache settings for your use case

## Pro Tips

💡 **Keep session token handy**: Store securely, update daily  
💡 **Use market orders**: Faster execution during volatility  
💡 **Monitor margin**: Check before large positions  
💡 **Set alerts**: Enable risk monitor for all positions  
💡 **Backup database**: Copy `data/` directory regularly  

## Files Structure

```
breeze_trader_enhanced/
├── app.py                 # Main application
├── setup.sh / setup.bat   # Installation scripts
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
├── CHANGELOG.md          # Version history
├── REVIEW_REPORT.md      # Technical review
└── .streamlit/
    └── secrets.toml      # Your credentials (create this)
```

## One-Line Deployment

```bash
# Clone → Setup → Run
git clone <repo> && cd breeze_trader_enhanced && ./setup.sh && streamlit run app.py
```

## Update Check

Current Version: **8.5 Enhanced**  
Check for updates: See CHANGELOG.md

---

## Happy Trading! 🎉

Remember:
- Start small
- Use stop-losses
- Monitor actively
- Never risk more than you can afford to lose

**Questions?** Review the full README.md for detailed information.

---

⚠️ **Disclaimer**: This software is provided as-is. Trading involves risk of loss. Use at your own risk.
