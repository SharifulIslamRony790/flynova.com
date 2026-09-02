<div align="center">
  <img src="https://img.icons8.com/color/96/000000/airplane-take-off.png" alt="FlyNova Logo"/>
  <h1>FlyNova - Premium Flight Booking System ✈️</h1>
  
  <p>
    <strong>A comprehensive, modern, and production-ready flight booking web application built with Django.</strong>
  </p>

  <p>
    <a href="https://mdsharifulislamrony790.pythonanywhere.com/"><b>🔴 LIVE DEMO</b></a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python" />
    <img src="https://img.shields.io/badge/Django-5.2.8-092E20.svg" alt="Django" />
    <img src="https://img.shields.io/badge/Database-PostgreSQL-336791.svg" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Styling-Bootstrap%205-563D7C.svg" alt="Bootstrap" />
    <img src="https://img.shields.io/badge/Status-Production%20Ready-success.svg" alt="Status" />
  </p>
</div>

---

## 📖 1. Project Summary
**FlyNova** allows users to search for flights, book tickets, manage bookings, and explore holiday packages and hotels. The system features a modern, responsive UI/UX, secure authentication (including Google OAuth), and real-time flight information. It is designed to provide a seamless, premium travel booking experience.

## ✨ 2. Key Features
*   🔐 **Secure User Authentication:** Encrypted sign-up and login, including **Google OAuth** integration for one-click access.
*   🔍 **Advanced Flight Search:** Powerful search functionality with filtering by origin, destination, date, and passenger count.
*   💰 **Smart Price Filtering:** Filter flight results instantly by price categories: **Low**, **Mid**, and **High**.
*   🕒 **Real-Time Airport Info:** Live dashboard showing flight arrivals and status (On Time, Landing Soon, Landed).
*   🎟️ **Booking Management:** Users can view their booking history, print tickets, and generate/download PDF tickets.
*   🏖️ **Holiday Packages & Hotels:** Dedicated premium sections for browsing and booking holiday packages and hotels.
*   📱 **Fully Responsive:** A beautiful interface that adapts flawlessly to desktop, tablet, and mobile devices.
*   ⚙️ **Secure Admin Dashboard:** Customized Jazzmin admin panel (`/flynova-admin/`) for managing flights, airports, bookings, and users securely.

---

## 🛠️ 3. Tech Stack & Requirements
*   **Backend:** Python 3.8+, Django 5.2.8
*   **Database:** PostgreSQL (with `psycopg2-binary`)
*   **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome, Google Fonts (Poppins)
*   **Authentication:** `django-allauth` (Social Authentication)
*   **Utilities:** `pillow` (Images), `reportlab` (PDFs), `django-environ` (Environment Variables)

---

## 🚀 4. Installation & Setup

Follow these steps to get your development environment running:

**1. Clone the repository:**
```bash
git clone <repository-url>
cd flynova
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up Environment Variables:**
Copy the example environment file and fill in your credentials (including your PostgreSQL database info):
```bash
cp .env.example .env
```

**5. Database Setup (PostgreSQL):**
Ensure PostgreSQL is running and your database is created as specified in your `.env` file, then run:
```bash
python manage.py migrate
```

**6. Create a Superuser:**
```bash
python manage.py createsuperuser
```

**7. Run the Application:**
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔒 5. Environment Variables (`.env`)
For security, FlyNova uses `django-environ` to keep secrets out of the codebase. Your `.env` file must include:
*   `SECRET_KEY`: Django secret key.
*   `DEBUG`: `True` for development, `False` for production.
*   `ALLOWED_HOSTS`: Comma-separated list of allowed domain names.
*   `DATABASE_URL`: Connection string (e.g., `postgres://user:password@localhost:5432/dbname`).
*   `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`: SMTP credentials for sending emails.
*   `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`: OAuth credentials for Google Login.
*   `SSLCOMMERZ_STORE_ID` / `SSLCOMMERZ_STORE_PASSWORD`: Payment gateway credentials.

---

## 📁 6. Project Structure
```text
flynova/
├── accounts/           # User authentication and profiles
├── bookings/           # Booking logic and payment generation
├── config/             # Project configuration (settings.py, urls.py)
├── core/               # Core routing and Home page
├── flights/            # Flight management and search algorithms
├── hotels/             # Hotel booking management
├── packages/           # Holiday packages
├── media/              # User-uploaded content (images)
├── static/             # Static assets (CSS, JS, images, videos)
├── templates/          # HTML templates (Django templating)
├── .env.example        # Environment variables template
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

---

## 🛡️ 7. Production Security Readiness
This project has been heavily audited and secured for live production environments:
*   **Database:** Fully migrated to PostgreSQL.
*   **Admin Protection:** Default `/admin/` URL changed to prevent automated brute-force attacks.
*   **HTTPS/SSL Enforced:** Secure cookies and SSL redirects are automatically enabled when `DEBUG = False`.
*   **Secrets Management:** All sensitive API keys and database passwords are read securely from the `.env` file.
*   **Static Files:** Configured with `STATIC_ROOT` ready for `collectstatic` deployment.

---

## 👨‍💻 8. Credits
Architected and Developed by **Md. Shariful Islam Rony**.
