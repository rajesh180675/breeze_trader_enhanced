# 🚀 START HERE - Complete Setup Guide

**Welcome to Breeze Trader v9.0!**

This guide will get you from ZIP file to running app in **10 minutes**.

---

## ⚡ QUICK START (Choose One Path)

### 🎯 PATH A: GitHub + Streamlit Cloud (Recommended - No Installation)

**Time: 10 minutes** | **Skill: Beginner** | **Cost: Free**

```
1. Extract ZIP file
2. Upload to GitHub
3. Deploy to Streamlit Cloud
4. Access from anywhere!
```

[👉 Follow PATH A Instructions Below](#path-a-github--streamlit-cloud)

---

### 💻 PATH B: Run Locally (For Developers)

**Time: 5 minutes** | **Skill: Intermediate** | **Cost: Free**

```
1. Extract ZIP file
2. Install Python packages
3. Add credentials
4. Run on your computer
```

[👉 Follow PATH B Instructions Below](#path-b-run-locally)

---

## 📋 What You'll Need

**For Both Paths:**
- [ ] ICICI Breeze account
- [ ] API Key & Secret from ICICI portal
- [ ] Session token (get daily from ICICI)

**For Path A (Cloud):**
- [ ] GitHub account (free)
- [ ] Streamlit Cloud account (free)

**For Path B (Local):**
- [ ] Python 3.11 installed
- [ ] Internet connection

---

## 🎯 PATH A: GitHub + Streamlit Cloud

### Step 1: Get API Credentials (5 minutes)

1. **Login** to ICICI Breeze Portal
   - URL: https://api.icicidirect.com/apiuser/home

2. **Navigate** to "API Keys" section

3. **Copy and save** (you'll need these):
   ```
   ✅ API Key: abc123...
   ✅ API Secret: xyz789...
   ```

4. **Generate** Session Token (in same portal)
   ```
   ✅ Session Token: ABCD1234
   (Valid for 24 hours - get new one daily)
   ```

### Step 2: Upload to GitHub (3 minutes)

1. **Login** to GitHub.com (create account if needed)

2. **Click** `+` icon → "New repository"
   ```
   Repository name: breeze-trader
   Description: Options trading platform
   Visibility: ⚫ Private (IMPORTANT!)
   ✅ Add .gitignore: Python
   ✅ Choose license: MIT
   ```

3. **Create repository** → Click "uploading an existing file"

4. **Extract ZIP** on your computer

5. **Drag ALL files** from extracted folder
   - Include: All `.py` files
   - Include: All `.md` files
   - Include: `requirements.txt`
   - Include: `LICENSE`, `.gitignore`
   - Include: `setup.sh`, `setup.bat`
   
   **EXCLUDE these:**
   - ❌ `.streamlit/secrets.toml` (if present)
   - ❌ `data/` folder
   - ❌ `*.db` files

6. **Commit message:** "Initial commit - Breeze Trader v9.0"

7. **Click** "Commit changes"

### Step 3: Create .streamlit Folder (2 minutes)

**In your GitHub repository:**

1. **Click** "Add file" → "Create new file"

2. **Filename:** `.streamlit/config.toml`

3. **Paste this content:**
   ```toml
   [server]
   port = 8501
   headless = true
   
   [browser]
   gatherUsageStats = false
   
   [theme]
   primaryColor = "#1f77b4"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f8f9fa"
   textColor = "#2c3e50"
   font = "sans serif"
   ```

4. **Commit** this file

5. **Create another file:** `.streamlit/secrets.toml.example`

6. **Paste this:**
   ```toml
   # Template - DO NOT commit actual secrets!
   BREEZE_API_KEY = "your_api_key_here"
   BREEZE_API_SECRET = "your_api_secret_here"
   ```

7. **Commit**

### Step 4: Deploy to Streamlit Cloud (5 minutes)

1. **Go to** https://streamlit.io/cloud

2. **Sign up / Sign in** (use your GitHub account)

3. **Click** "New app"

4. **Fill in:**
   ```
   Repository: your-username/breeze-trader
   Branch: main
   Main file path: app.py
   ```

5. **Click** "Advanced settings"

6. **Python version:** 3.11

7. **Secrets** (IMPORTANT - paste your actual credentials):
   ```toml
   BREEZE_API_KEY = "abc123def456..."
   BREEZE_API_SECRET = "xyz789uvw012..."
   ```

8. **Click** "Save"

9. **Click** "Deploy!"

10. **Wait 2-5 minutes** for deployment

11. **You'll get a URL:** `https://your-app.streamlit.app`

### Step 5: Access & Use (1 minute)

1. **Open** the URL from Step 4

2. **You'll see** login screen

3. **Enter** your daily Session Token (from Step 1)

4. **Click** Connect

5. **Start trading!** 🎉

---

## 💻 PATH B: Run Locally

### Step 1: Extract Files

1. **Extract** `breeze_trader_complete_v9.0_FINAL.zip`

2. **Navigate** to folder: `cd breeze_trader_enhanced`

### Step 2: Install Dependencies

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**OR use automated setup:**
```bash
# Linux/Mac
./setup.sh

# Windows
setup.bat
```

### Step 3: Configure Secrets

1. **Copy** template:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **Edit** `.streamlit/secrets.toml`:
   ```toml
   BREEZE_API_KEY = "your_actual_api_key"
   BREEZE_API_SECRET = "your_actual_api_secret"
   ```

3. **Save** file

### Step 4: Run Application

```bash
streamlit run app.py
```

**Opens at:** http://localhost:8501

### Step 5: Login & Trade

1. **Enter** session token in sidebar
2. **Click** Connect
3. **Start trading!**

---

## 📁 File Structure Reference

```
After extraction, you should see:

breeze_trader_enhanced/
├── app.py                    ⭐ MAIN FILE
├── app_config.py
├── analytics.py
├── breeze_api.py
├── breeze_api_complete.py
├── helpers.py
├── option_chain_processor.py
├── persistence.py
├── risk_monitor.py
├── session_manager.py
├── strategies.py
├── validators.py
├── requirements.txt
├── README.md
├── QUICKSTART.md
├── GITHUB_SETUP_GUIDE.md     ← Detailed GitHub guide
├── STRUCTURE_VISUAL_GUIDE.md ← Visual structure
├── CHEAT_SHEET.md           ← One-page reference
├── API_COMPLETE_GUIDE.md
├── DEPLOYMENT_GUIDE.md
├── REVIEW_REPORT.md
├── CHANGELOG.md
├── LICENSE
├── setup.sh
└── setup.bat
```

---

## 🎯 Which Path Should You Choose?

### Choose PATH A (Cloud) if you want:
- ✅ Access from anywhere (phone, tablet, laptop)
- ✅ No installation hassle
- ✅ Automatic updates on git push
- ✅ Always-on URL
- ✅ Free hosting
- ✅ Professional deployment

### Choose PATH B (Local) if you want:
- ✅ Full control
- ✅ No dependency on cloud services
- ✅ Offline development
- ✅ Faster iterations
- ✅ Complete privacy

**My Recommendation: Start with PATH A (easier), migrate to PATH B later if needed**

---

## 🔑 Getting ICICI Credentials

**Detailed Steps:**

1. **Login** to ICICI Direct account
2. **Navigate** to: https://api.icicidirect.com/apiuser/home
3. **Click** "Generate API Key" (first time only)
4. **Save** API Key and Secret (shown only once!)
5. **For daily use:**
   - Login to portal
   - View "Session Token"
   - Copy 8-character code
   - Valid for 24 hours
   - Generate new one each day

---

## 📚 What to Read Next

**After setup, read these in order:**

1. **CHEAT_SHEET.md** - One-page reference
2. **QUICKSTART.md** - 5-minute feature tour
3. **API_COMPLETE_GUIDE.md** - Learn all API features
4. **README.md** - Complete documentation

**For troubleshooting:**
- **DEPLOYMENT_GUIDE.md** - Deployment issues
- **GITHUB_SETUP_GUIDE.md** - Repository issues

---

## ⚠️ IMPORTANT SECURITY NOTES

**NEVER commit these files to GitHub:**
- ❌ `.streamlit/secrets.toml`
- ❌ Any file with API keys
- ❌ Any file with passwords
- ❌ `data/` folder with trades

**Your `.gitignore` file prevents this automatically!**

**Always:**
- ✅ Use Private repository for trading apps
- ✅ Add secrets in Streamlit Cloud dashboard only
- ✅ Keep API keys secure
- ✅ Regenerate keys if compromised

---

## ✅ Success Checklist

**After PATH A:**
- [ ] Repository created on GitHub
- [ ] All files uploaded (except secrets)
- [ ] `.streamlit/` folder created
- [ ] Streamlit Cloud app deployed
- [ ] Secrets added in dashboard
- [ ] App accessible via URL
- [ ] Can login with session token
- [ ] Option chains loading

**After PATH B:**
- [ ] Files extracted
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Secrets file configured
- [ ] App runs locally
- [ ] Can access at localhost:8501
- [ ] Can login and trade

---

## 🆘 Troubleshooting

### "Module not found" error
```bash
# Ensure requirements installed:
pip install -r requirements.txt
```

### "Secrets not found"
```bash
# Check file exists:
cat .streamlit/secrets.toml

# Or on Streamlit Cloud:
# Add in dashboard → Settings → Secrets
```

### "Connection failed"
```bash
# Check:
1. API Key is correct
2. API Secret is correct
3. Session token is fresh (< 24 hours)
4. Internet connection works
```

### "Option chain not loading"
```bash
# This is now FIXED in v9.0!
# Ensure using breeze_api_complete.py
# Check that app.py imports are correct
```

---

## 🎓 Learning Path

**Week 1: Setup & Basics**
- Day 1: Deploy using this guide
- Day 2: Explore option chains
- Day 3: Paper trade with small quantities
- Day 4-7: Learn features, read API guide

**Week 2: Advanced Features**
- Set up risk monitors
- Build strategies
- Analyze Greeks
- Use streaming data

**Week 3: Production**
- Optimize settings
- Set up alerts
- Increase position sizes
- Monitor performance

---

## 💡 Pro Tips

1. **Test with NIFTY first** - most liquid
2. **Use small quantities** initially
3. **Always set stop-losses** via Risk Monitor
4. **Check margin** before placing orders
5. **Get fresh session token** every morning
6. **Monitor circuit breaker** status
7. **Review trades** in persistent database
8. **Backup data/** folder** regularly

---

## 📞 Where to Get Help

**Documentation Hierarchy:**

1. **CHEAT_SHEET.md** - Quick answers
2. **QUICKSTART.md** - Feature overview
3. **README.md** - Complete guide
4. **API_COMPLETE_GUIDE.md** - API reference
5. **DEPLOYMENT_GUIDE.md** - Deploy issues
6. **GITHUB_SETUP_GUIDE.md** - GitHub help

**Everything is self-contained in the documentation!**

---

## 🎉 You're Ready!

**Choose your path:**
- 🌐 **PATH A** → Scroll up to [GitHub + Cloud](#path-a-github--streamlit-cloud)
- 💻 **PATH B** → Scroll up to [Run Locally](#path-b-run-locally)

**Time to start:** NOW!

**Remember:**
- Main file: `app.py`
- Command: `streamlit run app.py`
- Session token: Get daily from ICICI
- Documentation: All included in ZIP

**Let's go!** 🚀📈

---

## 📊 What You're Getting

- ✅ **6,000+ lines** of production code
- ✅ **40+ API methods** fully implemented
- ✅ **Complete option chain** (ALL strikes)
- ✅ **Real-time streaming** via WebSocket
- ✅ **Risk monitoring** with stop-losses
- ✅ **Strategy builder** for multi-leg trades
- ✅ **Persistent database** for trade logs
- ✅ **Complete documentation** (10+ guides)

**Industry-Grade. Production-Ready. Free & Open Source.**

---

**VERSION:** 9.0 Complete  
**RELEASE:** February 2026  
**STATUS:** Production Ready ✅

Made with ❤️ for serious options traders.
