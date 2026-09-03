# How to Setup a 100% Free PostgreSQL Database on Supabase

Since you don't have a credit card, **Supabase** is the perfect choice! It offers a completely free PostgreSQL database forever, and **it does NOT require any card to sign up**.

## Step 1: Create a Free Account
1. Go to [supabase.com](https://supabase.com/).
2. Click on **Start your project** (or Sign Up).
3. Continue with your **GitHub** account or **Email**.
4. No card will be asked!

## Step 2: Create a New Project
1. Once logged in, click on **New Project**.
2. Select your Organization (it should automatically create a default one for you).
3. Fill in the details:
   - **Name**: `flynova-db`
   - **Database Password**: Write a strong password and **copy it somewhere safe** (you will need this later).
   - **Region**: Select a region closest to your users (e.g., Singapore or South Asia).
4. Click **Create new project**.
5. *Wait for 1-2 minutes while Supabase sets up your database.*

## Step 3: Get Your Database URL
Once the project is ready, you need to copy the Database URL so we can connect it to Render.

1. On the left sidebar of your Supabase dashboard, click on the **⚙️ Settings** icon (Project Settings).
2. Click on **Database** under the Configuration section.
3. Scroll down to the **Connection string** section.
4. Select the **URI** tab.
5. You will see a link that looks like this:
   `postgresql://postgres.your_project_ref:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres`
6. **Copy this entire link.** 
7. *Note: Replace `[YOUR-PASSWORD]` in the link with the actual database password you created in Step 2.*

## Next Step: Deploy to Render
1. Go to [Render](https://render.com/).
2. Create a **New Web Service** and connect your GitHub repository.
3. Configure the service:
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`
4. Add the following **Environment Variables**:
   - `DATABASE_URL`: *(Paste the Supabase URI you copied in Step 3)*
   - `SECRET_KEY`: *(Enter a random strong key)*
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*`
5. Click **Deploy Web Service**!
