# 📋 BREEZE TRADER - ONE PAGE CHEAT SHEET

## 🎯 THE ESSENTIALS

| What | Answer |
|------|--------|
| **Main file to run** | `app.py` |
| **Command to run** | `streamlit run app.py` |
| **Repository name** | `breeze-trader` (or your choice) |
| **Required credentials** | API Key, API Secret (from ICICI portal) |
| **Session token** | Enter daily in app (expires 24hrs) |
| **Python version** | 3.11 (recommended) |

---

## 📁 UPLOAD TO GITHUB - 5 STEPS

```
1. Create repository on GitHub.com
   → Name: breeze-trader
   → Visibility: Private (recommended)

2. Extract zip file on your computer

3. Upload ALL files EXCEPT:
   ❌ .streamlit/secrets.toml
   ❌ data/ folder
   ❌ *.db files
   ❌ __pycache__/ folders

4. Commit with message: "Initial commit"

5. Done! ✅
```

---

## 🚀 DEPLOY TO STREAMLIT CLOUD - 4 STEPS

```
1. Go to: https://streamlit.io/cloud

2. Click "New app"
   → Repository: your-username/breeze-trader
   → Branch: main
   → Main file: app.py
   → Python: 3.11

3. Add Secrets (in Advanced settings):
   BREEZE_API_KEY = "your_key"
   BREEZE_API_SECRET = "your_secret"

4. Click "Deploy!" 
   → Get URL: https://your-app.streamlit.app
```

---

## 📂 FILE STRUCTURE (SIMPLE)

```
breeze-trader/              ← Repository root
├── .streamlit/
│   ├── config.toml         ← Upload ✅
│   └── secrets.toml.example ← Upload ✅
├── app.py                  ← ⭐ MAIN FILE
├── app_config.py           ← Upload ✅
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
├── requirements.txt        ← Upload ✅
├── .gitignore             ← Upload ✅
├── README.md
├── LICENSE
└── [all .md documentation files]
```

---

## ⚙️ LOCAL SETUP - 3 COMMANDS

```bash
# 1. Install
pip install -r requirements.txt

# 2. Add secrets
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit with your API keys

# 3. Run
streamlit run app.py
```

---

## 🔑 SECRETS FORMAT

**File: `.streamlit/secrets.toml`**

```toml
BREEZE_API_KEY = "your_api_key_here"
BREEZE_API_SECRET = "your_api_secret_here"
```

**Get from:** https://api.icicidirect.com/apiuser/home

---

## ✅ FILES TO UPLOAD

**Upload these (24 files):**
- ✅ All `.py` files (12 files)
- ✅ All `.md` files (8 files)
- ✅ requirements.txt
- ✅ .gitignore
- ✅ LICENSE
- ✅ setup.sh / setup.bat
- ✅ .streamlit/config.toml
- ✅ .streamlit/secrets.toml.example

**DO NOT upload:**
- ❌ .streamlit/secrets.toml (has your keys!)
- ❌ data/ folder
- ❌ *.db files
- ❌ __pycache__/

---

## 🎯 QUICK TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Module not found | Add to requirements.txt |
| Secrets not found | Add in Streamlit Cloud dashboard |
| App won't start | Check Python version = 3.11 |
| Can't find app.py | Must be in repository root |
| API error | Check credentials, get new session token |

---

## 📱 ACCESS YOUR APP

**After deployment:**
```
Local: http://localhost:8501
Cloud: https://your-app.streamlit.app
```

**On mobile:** Same URL works!

---

## 🔒 SECURITY CHECKLIST

- [ ] .gitignore includes secrets
- [ ] No API keys in code
- [ ] Repository is Private
- [ ] secrets.toml.example uploaded (not actual secrets)
- [ ] No .db files uploaded

---

## 🎓 COMPLETE PROCESS

```mermaid
1. Extract ZIP
   ↓
2. Upload to GitHub (web interface)
   ↓
3. Sign up at streamlit.io/cloud
   ↓
4. Deploy app
   ↓
5. Add secrets
   ↓
6. Access at your-app.streamlit.app
   ↓
7. Login with session token
   ↓
8. Start trading! 🚀
```

---

## 📚 DOCUMENTATION MAP

| File | Purpose |
|------|---------|
| README.md | Main documentation |
| QUICKSTART.md | 5-minute setup |
| GITHUB_SETUP_GUIDE.md | This guide - GitHub upload |
| STRUCTURE_VISUAL_GUIDE.md | Folder structure |
| API_COMPLETE_GUIDE.md | All API methods (800+ lines) |
| DEPLOYMENT_GUIDE.md | Production deployment |
| REVIEW_REPORT.md | Code review findings |
| CHANGELOG.md | Version history |

---

## ⚡ POWER USER COMMANDS

```bash
# Run app
streamlit run app.py

# Run with port
streamlit run app.py --server.port 8502

# Update packages
pip install -r requirements.txt --upgrade

# Generate new requirements
pip freeze > requirements.txt

# Git commands
git status
git add .
git commit -m "Update"
git push origin main
```

---

## 🎯 REPOSITORY SETTINGS

**After creation, configure:**

```
Settings → General:
  → Features: Disable Wiki (if not needed)
  → Pull Requests: Enable
  
Settings → Security:
  → Dependency alerts: Enable
  → Secret scanning: Enable (if public)
  
Settings → Pages: (optional)
  → Can host docs here
```

---

## 📊 WHAT HAPPENS AFTER UPLOAD?

1. **GitHub** stores your code
2. **Others** can fork/clone (if public)
3. **Streamlit Cloud** deploys automatically
4. **Updates** auto-deploy on git push
5. **URL** stays same
6. **Secrets** stay secure in Streamlit dashboard

---

## 🔄 UPDATE WORKFLOW

```
Make changes locally
   ↓
git add .
   ↓
git commit -m "message"
   ↓
git push origin main
   ↓
Streamlit Cloud auto-deploys (1-2 min)
   ↓
Refresh browser ✅
```

---

## 🆘 NEED HELP?

1. **Check logs** in Streamlit Cloud
2. **Review documentation** (8 guide files included)
3. **Check GitHub Issues** (if public repo)
4. **Test locally first** before deploying

---

## 🎉 YOU'RE READY!

**Remember:**
- Main file: `app.py`
- Command: `streamlit run app.py`
- Upload everything except secrets
- Deploy to Streamlit Cloud
- Add secrets there
- Done! ✅

---

## 📞 KEY URLS

| Service | URL |
|---------|-----|
| GitHub | github.com |
| Streamlit Cloud | streamlit.io/cloud |
| ICICI Breeze API | api.icicidirect.com/apiuser/home |
| Python | python.org |
| Streamlit Docs | docs.streamlit.io |

---

## ✨ FINAL TIPS

1. **Test locally first** before cloud deployment
2. **Keep secrets secure** - never commit to Git
3. **Use Private repo** for trading apps
4. **Monitor API usage** - rate limits apply
5. **Set up stop-losses** - always!
6. **Start with small orders** - test everything
7. **Keep session token fresh** - expires daily
8. **Backup your data** - copy data/ folder locally

---

**THIS IS ALL YOU NEED!** 🚀

Print this page and keep it handy while setting up your repository.
