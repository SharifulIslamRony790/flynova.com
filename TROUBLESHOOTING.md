# ⚠️ TROUBLESHOOTING - If Setup Fails

## Problem: "No module named 'django'" even after running setup.bat

### ✅ SOLUTION:

**Delete the `venv` folder and run setup.bat again:**

1. **Delete `venv` folder** (if it exists)
   - Right-click on `venv` folder
   - Click "Delete"

2. **Run setup.bat again**
   - Double-click `setup.bat`
   - Wait for it to complete

3. **Start server**
   - Double-click `start_server.bat`

---

## Why This Happens:

The `venv` folder might be from a different PC or incomplete installation.

---

## Alternative: Manual Setup (Always Works)

If `setup.bat` keeps failing, use manual commands:

```bash
# 1. Delete old venv (if exists)
rmdir /s /q venv

# 2. Create fresh venv
python -m venv venv

# 3. Activate venv
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup database
python manage.py migrate

# 6. Start server
python manage.py runserver 5000
```

---

## Check Python Version:

```bash
python --version
```

**Required:** Python 3.10 or higher

**If too old:** Download from https://www.python.org/downloads/

---

## Still Having Issues?

### Check These:
1. ✅ Python 3.10+ installed?
2. ✅ Internet connection working?
3. ✅ Antivirus not blocking?
4. ✅ Running as Administrator? (try this)

---

## Quick Test:

```bash
# Test if Python works
python --version

# Test if pip works
pip --version

# Test if venv works
python -m venv test_venv
```

If any of these fail, reinstall Python.

---

**Need more help? See `DEPLOYMENT_GUIDE.md`**
