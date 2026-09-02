# How to Setup a 100% Free PostgreSQL Database on Google Cloud (e2-micro VM)

This guide explains how to use Google Cloud's **Always Free** tier to host a PostgreSQL database for FlyNova.

## Step 1: Create the Free Virtual Machine (VM)
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **Compute Engine > VM instances** and click **Create Instance**.
3. **Name**: `flynova-db`
4. **Region**: Select a US region like `us-central1` (Iowa), `us-east1` (South Carolina), or `us-west1` (Oregon) to ensure it qualifies for the Always Free tier.
5. **Machine Configuration**: 
   - Series: `E2`
   - Machine type: `e2-micro` (This is the free one!).
6. **Boot Disk**: Select **Ubuntu 22.04 LTS** (or 20.04) and set the size to `30 GB` Standard Persistent Disk (also free).
7. **Firewall**: Check **Allow HTTP traffic** and **Allow HTTPS traffic**.
8. Click **Create**.

## Step 2: Install PostgreSQL
Once the VM is running, click the **SSH** button next to your VM instance to open the terminal.

Run the following commands:
```bash
# Update packages
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Start and enable the service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 3: Create the Database and User
Still inside the SSH terminal, switch to the Postgres user:
```bash
sudo -i -u postgres
```
Now, open the Postgres prompt:
```bash
psql
```
Create the database and user (Replace `yourpassword` with a strong password):
```sql
CREATE DATABASE flynova_db;
CREATE USER fly_nova WITH PASSWORD 'yourpassword';
ALTER ROLE fly_nova SET client_encoding TO 'utf8';
ALTER ROLE fly_nova SET default_transaction_isolation TO 'read committed';
ALTER ROLE fly_nova SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE flynova_db TO fly_nova;
\q
```
Type `exit` to return to your normal ubuntu user.

## Step 4: Allow External Connections (From Render)
By default, PostgreSQL only allows local connections. We need to open it up so Render can connect.

1. Open the PostgreSQL config file:
```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
# Note: The version number '14' might be different (e.g., 12, 13, 15). Check with `ls /etc/postgresql/` if it fails.
```
2. Find the line `#listen_addresses = 'localhost'` and change it to:
```text
listen_addresses = '*'
```
Save (`Ctrl+O`, `Enter`) and Exit (`Ctrl+X`).

3. Open the `pg_hba.conf` file:
```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```
4. Scroll to the very bottom and add this line to allow all IPs to connect securely:
```text
host    all             all             0.0.0.0/0               md5
```
Save and Exit.

5. Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

## Step 5: Open Port 5432 in Google Cloud Firewall
1. Go back to the Google Cloud Console.
2. Search for **VPC network > Firewall**.
3. Click **Create Firewall Rule**.
   - **Name**: `allow-postgres`
   - **Targets**: `All instances in the network`
   - **Source IPv4 ranges**: `0.0.0.0/0`
   - **Protocols and ports**: Select `tcp` and type `5432`.
4. Click **Create**.

## Step 6: Get Your Database URL
Go back to your VM Instances page and copy the **External IP** of your `flynova-db` machine.

Your `DATABASE_URL` is now ready:
```text
postgres://fly_nova:yourpassword@<EXTERNAL_IP_ADDRESS>:5432/flynova_db
```

## Next Step: Deploy to Render
1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. **Build Command**: `./build.sh`
4. **Start Command**: `gunicorn config.wsgi:application`
5. **Environment Variables**:
   - `DATABASE_URL`: (Paste the URL you created in Step 6)
   - `SECRET_KEY`: (Enter a random strong key)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*` (or your render URL)
