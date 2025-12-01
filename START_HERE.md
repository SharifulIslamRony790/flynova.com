# ⚠️ IMPORTANT - READ THIS FIRST!

## If you see "No module named 'django'" error:

### ✅ SOLUTION (Windows - EASIEST):

**Option 1: Delete venv and re-run setup**
1. Delete the `venv` folder (if it exists)
2. Double-click **`setup.bat`**
3. Double-click **`start_server.bat`**

**Option 2: Fresh setup (if no venv folder)**
1. Double-click **`setup.bat`** (installs everything)
2. Double-click **`start_server.bat`** (starts server)

That's it! The server will start automatically.

---

## Why this happens:

The error means Django is not installed in your virtual environment.

### What `setup.bat` does:
1. Creates virtual environment
2. Installs Django and all dependencies
3. Sets up database
4. Everything ready!

### After running `setup.bat` once:
- Just use `start_server.bat` to start the server
- No need to run `setup.bat` again

---

## Manual Fix (if you prefer command line):

```bash
# 1. Make sure you're in the project folder
cd flynova

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Start server
python manage.py runserver 5000
```

---

## ✅ After Setup:

Visit: **`http://127.0.0.1:5000/`**

Admin Panel:
- URL: `http://127.0.0.1:5000/admin/`
- Username: `admin`
- Password: `admin123`

---

**Need more help? See `QUICK_START.md` or `DEPLOYMENT_GUIDE.md`**
