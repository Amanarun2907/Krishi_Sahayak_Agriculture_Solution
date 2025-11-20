# 🔒 GitHub Security Checklist - Before Pushing to GitHub

## ✅ Pre-Push Security Checklist

Before pushing your code to GitHub, verify ALL these items:

---

### 1. ✅ API Keys Removed from Code

- [ ] No API keys in `config.py`
- [ ] No API keys in any `.py` files
- [ ] No API keys in comments
- [ ] No API keys in documentation

**Check with:**
```bash
# Search for potential API keys
grep -r "gsk_" .
grep -r "api_key" . --include="*.py"
grep -r "API_KEY" . --include="*.py"
```

---

### 2. ✅ .env File Created and Configured

- [ ] `.env` file exists with your API key
- [ ] `.env.example` exists (without actual keys)
- [ ] `.env` is listed in `.gitignore`

**Verify:**
```bash
# Check if .env is ignored
git check-ignore .env
# Should output: .env
```

---

### 3. ✅ .gitignore Properly Configured

- [ ] `.gitignore` file exists
- [ ] `.env` is in `.gitignore`
- [ ] `__pycache__/` is in `.gitignore`
- [ ] Model files (*.h5, *.pt) are in `.gitignore`
- [ ] Large datasets are in `.gitignore`

**Check:**
```bash
cat .gitignore | grep ".env"
cat .gitignore | grep "__pycache__"
```

---

### 4. ✅ Environment Variables Working

- [ ] `python-dotenv` installed
- [ ] `load_dotenv()` called in `config.py`
- [ ] API key loads correctly

**Test:**
```bash
python -c "from config import GROQ_API_KEY; print('✅ OK' if GROQ_API_KEY else '❌ FAIL')"
```

---

### 5. ✅ Git History Clean

- [ ] No API keys in previous commits
- [ ] No sensitive data in commit history

**Check history:**
```bash
git log --all --full-history --source -- "*config.py"
```

**If you find API keys in history, you MUST clean it:**
```bash
# WARNING: This rewrites history!
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.py" \
  --prune-empty --tag-name-filter cat -- --all
```

---

### 6. ✅ Documentation Updated

- [ ] README.md mentions environment variables
- [ ] SETUP_GUIDE.md created
- [ ] .env.example provided
- [ ] Installation instructions clear

---

### 7. ✅ Test Before Pushing

```bash
# 1. Remove .env temporarily
mv .env .env.backup

# 2. Try running the app
streamlit run app.py
# Should show error about missing API key

# 3. Restore .env
mv .env.backup .env

# 4. Run again
streamlit run app.py
# Should work now
```

---

## 🚀 Safe Push Procedure

### Step 1: Initialize Git (if not done)
```bash
git init
```

### Step 2: Add .gitignore FIRST
```bash
git add .gitignore
git commit -m "Add .gitignore to protect sensitive files"
```

### Step 3: Verify What Will Be Committed
```bash
git status
git diff --cached
```

**Make sure you DON'T see:**
- ❌ `.env` file
- ❌ API keys in any file
- ❌ Large model files
- ❌ Dataset files

### Step 4: Add Files
```bash
git add .
```

### Step 5: Final Check
```bash
# List all files that will be committed
git ls-files

# Search for API keys in staged files
git grep "gsk_" $(git diff --cached --name-only)
```

### Step 6: Commit
```bash
git commit -m "Initial commit - Krishi Sahayak AI Agriculture Assistant"
```

### Step 7: Add Remote
```bash
git remote add origin https://github.com/yourusername/krishi-sahayak.git
```

### Step 8: Push
```bash
git push -u origin main
```

---

## 🔍 Post-Push Verification

### 1. Check GitHub Repository

Visit your repository and verify:
- [ ] No `.env` file visible
- [ ] `.env.example` is present
- [ ] `.gitignore` is present
- [ ] No API keys in any file

### 2. Search for Exposed Secrets

On GitHub, use the search bar:
```
gsk_ repo:yourusername/krishi-sahayak
```

Should return: **No results**

### 3. Check GitHub Security Alerts

- Go to: Settings → Security → Secret scanning
- Should show: **No alerts**

---

## 🚨 If You Accidentally Pushed API Keys

### IMMEDIATE ACTIONS:

1. **Revoke the API Key Immediately!**
   - Go to https://console.groq.com/keys
   - Delete the exposed key
   - Generate a new one

2. **Remove from Git History:**
   ```bash
   # Install BFG Repo Cleaner
   # Download from: https://rtyley.github.io/bfg-repo-cleaner/
   
   # Remove API keys from history
   bfg --replace-text passwords.txt
   
   # Force push
   git push --force
   ```

3. **Update .env with New Key:**
   ```bash
   # Edit .env with new API key
   nano .env
   ```

4. **Notify Team:**
   - If working in a team, inform everyone
   - Ask them to update their .env files

---

## 📋 Quick Reference Commands

### Check if file is ignored:
```bash
git check-ignore -v .env
```

### See what will be committed:
```bash
git status
git diff --cached
```

### Search for API keys:
```bash
grep -r "gsk_" . --exclude-dir=.git
```

### Remove file from Git (keep local):
```bash
git rm --cached .env
```

### Remove file from Git (delete):
```bash
git rm .env
```

---

## ✅ Final Checklist Before Push

```
[ ] .env file created with API key
[ ] .env.example created (template)
[ ] .gitignore includes .env
[ ] config.py uses os.getenv()
[ ] python-dotenv installed
[ ] Tested app without .env (should fail)
[ ] Tested app with .env (should work)
[ ] No API keys in any .py files
[ ] No API keys in comments
[ ] git status shows no .env
[ ] git grep finds no API keys
[ ] Documentation updated
[ ] README mentions setup steps
```

---

## 🎯 Summary

**The Golden Rules:**
1. ✅ **NEVER** commit `.env` to Git
2. ✅ **ALWAYS** use environment variables
3. ✅ **ALWAYS** add `.env` to `.gitignore` FIRST
4. ✅ **ALWAYS** provide `.env.example`
5. ✅ **ALWAYS** check before pushing

**Remember:**
> "Once an API key is on GitHub, consider it compromised forever!"

Even if you delete it later, it's in the Git history and bots have already found it.

---

**Status: 🔒 SECURE**

Your project is now safe to push to GitHub! 🚀
