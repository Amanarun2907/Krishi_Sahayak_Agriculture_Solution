# 🔑 API Key Not Loading - Quick Fix

## Problem
Chatbot shows "API Key Not Configured" even though the `.env` file has the GROQ_API_KEY set.

## Root Cause
**Streamlit doesn't automatically reload environment variables.** When you:
1. Start Streamlit
2. Then create/modify `.env` file
3. The running Streamlit app doesn't see the changes

## Solution

### Option 1: Restart Streamlit (Recommended)

**Step 1: Stop Streamlit**
- Press `Ctrl + C` in the terminal where Streamlit is running
- Or close the terminal

**Step 2: Start Streamlit Again**
```bash
streamlit run app.py
```

**Step 3: Test the Chatbot**
- Navigate to any chatbot page
- Type "Hello"
- Should get a proper AI response

### Option 2: Verify .env File

**Step 1: Check .env file exists**
```bash
# Windows
dir .env

# Linux/Mac
ls -la .env
```

**Step 2: Check .env content**
```bash
# Windows
type .env

# Linux/Mac
cat .env
```

Should show:
```
GROQ_API_KEY=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
```

**Step 3: Check for issues**
- ❌ No spaces before/after `=`
- ❌ No quotes around the key (unless part of the key)
- ❌ No extra blank lines
- ✅ Should be: `GROQ_API_KEY=your_key_here`

### Option 3: Test Environment Loading

Run the test script:
```bash
python test_env_loading.py
```

Should show:
```
✅ API Key found!
✅ Config loaded API key!
✅ Keys match!
```

If it shows ❌, there's an issue with the .env file.

## Common Issues

### Issue 1: .env in Wrong Location
**Problem:** .env file is not in the project root

**Solution:**
```bash
# Check current directory
pwd  # Linux/Mac
cd   # Windows

# .env should be in same folder as app.py
ls -la  # Should show both app.py and .env
```

### Issue 2: Streamlit Not Restarted
**Problem:** Made changes but didn't restart Streamlit

**Solution:**
1. Stop Streamlit (Ctrl+C)
2. Start again: `streamlit run app.py`

### Issue 3: Wrong API Key Format
**Problem:** Extra spaces, quotes, or newlines

**Bad:**
```
GROQ_API_KEY = "your_key"  # Has spaces and quotes
GROQ_API_KEY=              # Empty
GROQ_API_KEY="your_key"    # Has quotes
```

**Good:**
```
GROQ_API_KEY=your_key_here
```

### Issue 4: Invalid API Key
**Problem:** API key is expired or invalid

**Solution:**
1. Go to: https://console.groq.com
2. Create new API key
3. Replace in .env file
4. Restart Streamlit

## Verification Steps

### Step 1: Test Environment Loading
```bash
python test_env_loading.py
```

Expected output:
```
✅ API Key found!
   Length: 56 characters
   Preview: gsk_gqtMv3...vG0d
✅ Config loaded API key!
✅ Keys match!
```

### Step 2: Test API Connection
```bash
python test_api_connection.py
```

Expected output:
```
✅ API Key found
✅ Client initialized successfully
✅ API Response: Hello from Krishi Sahayak!
🎉 All tests passed!
```

### Step 3: Test in Streamlit
1. Start Streamlit: `streamlit run app.py`
2. Go to any chatbot page
3. Type: "Hello"
4. Should get AI response (not error message)

## Debug Mode

The chatbot now shows debug info when API key is missing:

```
❌ API Key Not Configured

Debug Info:
- API Key exists: True/False
- API Key length: 0 or 56

To fix this:
1. Check your .env file
2. Restart Streamlit
```

This helps identify if:
- API key is completely missing (exists: False)
- API key is empty (length: 0)
- API key is loaded but invalid (length: 56)

## Quick Fix Checklist

- [ ] .env file exists in project root (same folder as app.py)
- [ ] .env contains: `GROQ_API_KEY=your_actual_key`
- [ ] No extra spaces or quotes in .env
- [ ] Streamlit was restarted after creating/modifying .env
- [ ] Test script shows API key is loaded
- [ ] API key is valid (from console.groq.com)

## Still Not Working?

### Try This:
1. **Delete .env and recreate:**
   ```bash
   # Windows
   del .env
   echo GROQ_API_KEY=your_key_here > .env
   
   # Linux/Mac
   rm .env
   echo "GROQ_API_KEY=your_key_here" > .env
   ```

2. **Set environment variable directly:**
   ```bash
   # Windows (PowerShell)
   $env:GROQ_API_KEY="your_key_here"
   streamlit run app.py
   
   # Linux/Mac
   export GROQ_API_KEY="your_key_here"
   streamlit run app.py
   ```

3. **Check Python can read .env:**
   ```python
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"
   ```
   Should print your API key

## For Streamlit Cloud

If deploying to Streamlit Cloud:

1. **Don't use .env file** (it's not deployed)
2. **Use Streamlit Secrets instead:**
   - Go to app settings
   - Click "Secrets"
   - Add:
     ```toml
     GROQ_API_KEY = "your_key_here"
     ```
3. **Restart the app**

## Summary

**Most Common Solution:**
```bash
# Stop Streamlit (Ctrl+C)
# Then restart:
streamlit run app.py
```

**Why:** Streamlit loads environment variables only at startup. Changes to .env require a restart.

---

**Status:** ✅ Solution provided
**Date:** November 20, 2025
**Key Point:** Always restart Streamlit after modifying .env
