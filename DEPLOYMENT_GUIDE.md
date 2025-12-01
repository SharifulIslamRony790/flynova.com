# FlyNova - Complete Deployment Guide

## ⚠️ IMPORTANT: Read This Before Sharing

This guide ensures the project will work perfectly on any PC.

---

## 📋 Prerequisites

Before running this project, make sure you have:
- **Python 3.10+** installed
- **pip** (Python package manager)

---

## 🚀 Setup Instructions (For New PC)

### Step 1: Extract the Project
Extract the `flynova` folder to your desired location.

### Step 2: Create Virtual Environment
Open Command Prompt/PowerShell in the project folder and run:
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment
**Windows:**
```bash
.\venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run Migrations
```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
- Username: `admin`
- Email: (your email)
- Password: `admin123` (or your choice)

### Step 7: Populate Database with Sample Data
```bash
python populate_data.py
```

This will create:
- 5 Hotels with images
- 4 Holiday Packages with images
- 12 Bangladesh Domestic Flights

### Step 8: Run the Server
```bash
python manage.py runserver 5000
```

Visit: `http://127.0.0.1:5000/`

---

## 🔑 Admin Panel Access

**URL:** `http://127.0.0.1:5000/admin/`
**Username:** `admin`
**Password:** `admin123`

---

## 📧 Email Configuration (Optional)

The project is configured to send booking confirmation emails.

### Current Setup:
- **Email Backend:** SMTP (Gmail)
- **Email:** `nabidahmad.zidan@gmail.com`
- **App Password:** `ftpw edcq sgwt tqza`

### To Change Email Settings:
Edit `config/settings.py` (lines 136-143):
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

**Note:** You need a Gmail App Password, not your regular password.
[How to create App Password](https://support.google.com/accounts/answer/185833)

### To Disable Email (Use Console):
Change line 137 in `config/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

---

## 🖼️ Images

All images are loaded from **Unsplash URLs** (online), so:
- ✅ **No image files to copy**
- ✅ **Works on any PC with internet**
- ✅ **No missing image errors**

Images are stored as URLs in the database:
- Hotels: Unsplash hotel images
- Packages: Unsplash destination images

---

## 📁 Project Structure

```
flynova/
├── accounts/          # User authentication
├── bookings/          # Booking system
├── core/              # Home page
├── flights/           # Flight search
├── hotels/            # Hotel search
├── packages/          # Holiday packages
├── config/            # Django settings
├── templates/         # HTML templates
├── db.sqlite3         # Database (included)
├── manage.py          # Django management
├── populate_data.py   # Data population script
└── requirements.txt     # Dependencies
```

---

## ✅ Features Included

1. **Flight Booking** - 12 Bangladesh domestic flights
2. **Hotel Booking** - 5 hotels with rooms
3. **Holiday Packages** - 4 tour packages
4. **User Authentication** - Sign up, Sign in, Logout
5. **Booking Management** - View bookings, Print tickets
6. **Email Notifications** - Booking confirmations
7. **Admin Panel** - Manage all data
8. **Dynamic Pricing** - Flight prices based on passengers
9. **Professional UI** - Modern, responsive design

---

## 🐛 Troubleshooting

### Issue: "No module named 'django'"
**Solution:** Activate virtual environment first
```bash
.\venv\Scripts\activate
```

### Issue: "Port 5000 already in use"
**Solution:** Use a different port
```bash
python manage.py runserver 8000
```

### Issue: "Database is locked"
**Solution:** Close any other instances of the server

### Issue: "Images not showing"
**Solution:** Check internet connection (images load from Unsplash)

---

## 📝 Important Notes

1. **Database Included:** `db.sqlite3` is included with sample data
2. **No Media Folder Needed:** Images are URLs, not files
3. **Static Files:** All CSS/JS loaded from CDN (Bootstrap, Font Awesome)
4. **Email:** Pre-configured but can be changed
5. **Admin Access:** Username: `admin`, Password: `admin123`

---

## 🔒 Security Notes (For Production)

If deploying to production:
1. Change `SECRET_KEY` in `config/settings.py`
2. Set `DEBUG = False`
3. Update `ALLOWED_HOSTS`
4. Use environment variables for sensitive data
5. Use a production database (PostgreSQL/MySQL)

---

## 📞 Support

If you encounter any issues:
1. Check this guide first
2. Verify Python version (3.10+)
3. Ensure virtual environment is activated
4. Check all dependencies are installed

---

**Created by:** Nabid Ahmad Zidan  
**Email:** nabidahmad.zidan@gmail.com  
**Project:** FlyNova - Travel Booking System
