# FlyNova - Flight Booking System ✈️

## 1. FlyNova Project Summary
FlyNova is a comprehensive flight booking web application built with Django. It allows users to search for flights, book tickets, manage bookings, and explore holiday packages and hotels. The system features a modern, responsive UI/UX, secure authentication (including Google OAuth), and real-time flight information. It is designed to provide a seamless travel booking experience for users in Bangladesh and beyond.

## 2. Features
*   **User Authentication:** Secure sign-up and login, including **Google OAuth** integration for one-click access.
*   **Flight Search:** Advanced search functionality with filtering by origin, destination, date, and passengers.
*   **Smart Price Filtering:** Filter flight results by price categories: **Low**, **Mid**, and **High**.
*   **Recent Flights First:** Search results and bookings are automatically sorted to show the most recent options first.
*   **Real-Time Airport Info:** Live dashboard showing flight arrivals and status (On Time, Landing Soon, Landed) for the next 24 hours.
*   **Booking Management:** Users can view their booking history, print tickets, and download PDF tickets.
*   **Holiday Packages & Hotels:** Dedicated sections for browsing and booking holiday packages and hotels.
*   **Responsive Design:** A fully responsive interface that works beautifully on desktop, tablet, and mobile devices.
*   **Admin Dashboard:** Comprehensive admin panel for managing flights, airports, bookings, and users.

## 3. Requirements
*   Python 3.8+
*   Django 5.2.8
*   django-allauth 0.57.0 (for social authentication)
*   pillow 12.0.0 (for image handling)
*   reportlab 4.0.7 (for PDF generation)
*   sqlparse 0.5.3
*   tzdata 2025.2
*   asgiref 3.11.0

## 4. Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd flynova
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```

## 5. Environment Variables
The project uses the following environment variables (configured in `config/settings.py`). For production, these should be set in a `.env` file or environment configuration:

*   `SECRET_KEY`: Django secret key.
*   `DEBUG`: Set to `True` for development, `False` for production.
*   `EMAIL_HOST_USER`: Email address for sending notifications (currently configured for Gmail).
*   `EMAIL_HOST_PASSWORD`: App password for the email account.
*   `GOOGLE_OAUTH_CLIENT_ID`: Client ID for Google OAuth.
*   `GOOGLE_OAUTH_SECRET`: Client Secret for Google OAuth.

## 6. Settings Summary
The main settings are located in `config/settings.py`:
*   **INSTALLED_APPS:** Includes core Django apps, `allauth` for authentication, and custom apps (`core`, `flights`, `hotels`, `packages`, `bookings`, `accounts`).
*   **MIDDLEWARE:** Standard Django middleware plus `allauth.account.middleware.AccountMiddleware`.
*   **TEMPLATES:** Configured to use Django templates with `allauth` context processors.
*   **DATABASES:** SQLite is used for development.
*   **AUTH_USER_MODEL:** Custom user model `accounts.CustomUser`.
*   **EMAIL_BACKEND:** SMTP backend configured for Gmail.
*   **SOCIALACCOUNT_PROVIDERS:** Configuration for Google OAuth.

## 7. Run Locally

To run the development server:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## 8. Project Structure

```
flynova/
├── accounts/           # User authentication and custom user model
├── bookings/           # Booking logic and management
├── config/             # Project configuration (settings, urls)
├── core/               # Core functionality (home page, etc.)
├── flights/            # Flight management, search, and airport info
├── hotels/             # Hotel management
├── packages/           # Holiday package management
├── media/              # User-uploaded content (images)
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
│   ├── account/        # Allauth templates
│   ├── accounts/       # Custom auth templates
│   ├── bookings/       # Booking templates
│   ├── flights/        # Flight templates
│   ├── socialaccount/  # Social auth templates
│   └── base.html       # Base template
├── db.sqlite3          # SQLite database
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```

## 9. Production Tips
*   **Debug Mode:** Ensure `DEBUG = False` in production.
*   **Secret Key:** Use a strong, unique `SECRET_KEY` and keep it secret.
*   **Database:** Switch to a more robust database like PostgreSQL for production.
*   **Static Files:** Configure `STATIC_ROOT` and use a web server (like Nginx or Apache) or a service like WhiteNoise to serve static files.
*   **HTTPS:** Always use HTTPS in production.
*   **Allowed Hosts:** Update `ALLOWED_HOSTS` with your domain name.

## 10. Credits
Developed by **Md. Shariful Islam Rony**.
*   **Framework:** Django
*   **Styling:** Bootstrap 5, Custom CSS
*   **Icons:** FontAwesome
*   **Fonts:** Google Fonts (Poppins)
