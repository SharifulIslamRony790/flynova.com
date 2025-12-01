# 🚀 FlyNova - Quick Start (2 Steps!)

## For Windows Users (EASIEST):

### Step 1: Run Setup (First Time Only)
Double-click: **`setup.bat`**

This will automatically:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Setup database
- ✅ Everything ready!

### Step 2: Start Server
Double-click: **`start_server.bat`**

Visit: **`http://127.0.0.1:5000/`**

---

## Manual Setup (All Operating Systems):

### Step 1: Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

### Step 2: Start Server
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Start server
python manage.py runserver 5000
```

Visit: **`http://127.0.0.1:5000/`**

---

## 🔑 Admin Access

**URL:** `http://127.0.0.1:5000/admin/`
- **Username:** `admin`
- **Password:** `admin123`

---

## ⚠️ Troubleshooting

### "No module named 'django'"
**Solution:** Virtual environment not activated or dependencies not installed
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### "Port 5000 already in use"
**Solution:** Use different port
```bash
python manage.py runserver 8000
```

---

## 📚 More Help?

See **`DEPLOYMENT_GUIDE.md`** for detailed instructions.
