# FlyNova - Agent Handoff & Architecture Manual

This document provides specialized technical context, structural breakdown, and workflow history so that any AI agent or new developer can instantly understand the **FlyNova** project and resume work immediately.

---

## 1. Project Overview & Tech Stack
**Project Name:** FlyNova
**Type:** Full-Stack Travel Agency & Booking Platform
**Core Technologies:**
- **Backend:** Django (Python), PostgreSQL (Database)
- **Frontend:** HTML5, Bootstrap 5, CSS3, JavaScript
- **Forms & Auth:** Django Crispy Forms, Django Allauth (for Google OAuth & Registration)
- **Payment Gateway:** SSLCommerz Integration
- **Admin Panel:** Jazzmin (Customized UI for Django Admin) & Custom Frontend Dashboard

## 2. Project Architecture & Apps
The project is strictly modularized into the following Django apps:

1. **`accounts`**: Manages CustomUser (extends AbstractUser), UserProfile, Signals (auto-creates profile on user creation), and Authentication Views (Login/Signup via custom logic or Allauth).
2. **`bookings`**: The central transactional engine. Manages `Booking` and `Payment` models. Handles checkout views, SSLCommerz success/fail/cancel API callbacks, and PDF ticket generation.
3. **`core`**: Contains the landing page (`home`) and handles cross-app data aggregations for the frontend.
4. **`dashboard`**: A custom-built, staff-only frontend administration portal. It manages CRUD operations for flights, hotels, packages, bookings, and user suspension.
5. **`flights`**: Manages `Airport`, `Airline`, and `Flight` models. Includes complex search logic dynamically filtering by price tiers and real-time airport arrival info.
6. **`hotels`**: Manages `Hotel` and `Room` models. Features a search engine supporting price range filtering and distinct city queries.
7. **`packages`**: Manages `Package` and `Itinerary` models. Handles specialized holiday tours with daily plans.

## 3. Key Design Decisions & Rules Implemented
Any agent working on this codebase **MUST** strictly follow these established patterns:

- **Security & Environment Variables**: Absolute Zero-Trust. Sensitive data (DB credentials, Secret Key, SSLCommerz keys, OAuth IDs) are managed strictly via `.env` using `django-environ` in `config/settings.py`. Hardcoding is explicitly forbidden.
- **Code Commenting Standards**: All Python files (`views.py`, `models.py`, `admin.py`, `forms.py`, `urls.py`) contain highly professional, sectioned comments with clear headers (e.g., `# ==========================================`).
- **Database Architecture**: PostgreSQL is the primary database. The schema relies heavily on `ForeignKey` relationships (e.g., Bookings linked to User, Flight, Hotel, Package).
- **Payment Flow (SSLCommerz)**: 
  - `bookings/views.py -> create_booking`: Generates transactional payload and redirects to SSLCommerz.
  - Callbacks (`sslcommerz_success`, `sslcommerz_fail`, `sslcommerz_cancel`) capture the POST response, update the `Payment` and `Booking` status, and redirect the user. Note: CSRF is exempted on callbacks (`@csrf_exempt`).
- **N+1 Query Optimizations**: The `dashboard` app uses `select_related` and `prefetch_related` extensively to ensure the DB does not crash under high loads.

## 4. Current State & Recent Fixes
- **Database**: Successfully migrated from SQLite to PostgreSQL.
- **UI/UX Redesign**: The homepage, search results, and checkout flows were overhauled with a dark-themed, modern, glassmorphic UI using Bootstrap 5 and custom CSS.
- **Security Check**: Fixed a critical parameter tampering bug in booking finalization. Added rate limiting (`django-ratelimit`) on authentication and checkout endpoints to prevent brute-force attacks.
- **Code Quality**: Formatted according to PEP 8 / Flake8 standards.

## 5. How to Run Locally
```bash
# 1. Activate Virtual Environment
venv\Scripts\activate

# 2. Install Requirements (if any updates occurred)
pip install -r requirements.txt

# 3. Ensure PostgreSQL is running and .env is configured correctly.

# 4. Run Migrations
python manage.py migrate

# 5. Start the Server
python manage.py runserver
```

## 6. How to Resume Work (For Agents)
If asked to add a new feature or debug:
1. Identify which app the feature belongs to (e.g., if it's a new transport type like Trains, create a new app; if it's a new payment gateway, edit `bookings`).
2. Always review `config/settings.py` for INSTALLED_APPS and third-party middleware before adding new dependencies.
3. Keep the styling consistent with the existing dark-themed Bootstrap classes found in `templates/core/home.html` and `templates/base.html`.
4. Run `flake8` checks after major Python modifications to ensure the 100% clean record is maintained.
