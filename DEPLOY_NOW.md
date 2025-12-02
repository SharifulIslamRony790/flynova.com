# 🚀 How to Make Your Website Live (Deploy to PythonAnywhere)

You are currently seeing the **Source Code** on GitHub. To make the website run (so people can visit it), you need to host it.

**We recommend PythonAnywhere** because it is free and works best with your database (SQLite).

## Step 1: Create an Account
1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com/).
2. Click **Sign Up** and create a **Beginner (Free)** account.

## Step 2: Upload Your Code
1. Log in to PythonAnywhere.
2. Click on **Consoles** > **Bash**.
3. In the black screen, type this command and hit Enter:
   ```bash
   git clone https://github.com/SharifulIslamRony790/flynova.com.git mysite
   ```

## Step 3: Install Requirements
1. Still in the Bash console, run these commands:
   ```bash
   cd mysite
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```

## Step 4: Configure Web App
1. Go to the **Web** tab (top right).
2. Click **Add a new web app**.
3. Click **Next** > **Manual configuration** > **Python 3.10** > **Next**.
4. Scroll down to **Virtualenv**:
   - Enter: `/home/yourusername/.virtualenvs/myenv` (Replace `yourusername` with your actual username).
5. Scroll to **Code**:
   - Source code: `/home/yourusername/mysite`
   - Working directory: `/home/yourusername/mysite`

## Step 5: Configure WSGI File
1. In the **Web** tab, click the link next to **WSGI configuration file** (it looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`).
2. Delete **everything** in that file.
3. Paste this code:
   ```python
   import os
   import sys

   path = '/home/yourusername/mysite'  # Replace yourusername
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
4. Click **Save** (top right).

## Step 6: Setup Environment Variables
1. Go back to the **Bash** console.
2. Create the `.env` file:
   ```bash
   cd ~/mysite
   nano .env
   ```
3. Paste your secrets (copy from your local `.env` file):
   ```
   SECRET_KEY=django-insecure-...
   EMAIL_HOST_PASSWORD=...
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   ```
4. Press `Ctrl+X`, then `Y`, then `Enter` to save.

## Step 7: Finalize
1. In the Bash console, run:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
2. Go to the **Web** tab and click the big green **Reload** button.
3. Click the link at the top (e.g., `yourusername.pythonanywhere.com`).

**Your site is now LIVE!** 🎉
