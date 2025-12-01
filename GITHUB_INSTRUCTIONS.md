# How to Upload FlyNova to GitHub 🚀

Follow these simple steps to get your project live on GitHub.

## Step 1: Create a GitHub Repository
1.  Log in to your [GitHub account](https://github.com/).
2.  Click the **+** icon in the top-right corner and select **New repository**.
3.  **Repository name:** Enter `flynova` (or any name you prefer).
4.  **Description:** (Optional) "Complete Flight Booking System with Django".
5.  **Public/Private:** Choose **Public** (anyone can see) or **Private** (only you).
6.  **Initialize this repository with:** Leave all these unchecked (we already have code).
7.  Click **Create repository**.

## Step 2: Initialize Local Repository
1.  Go to your project folder: `c:\Users\USER\Downloads\flynova2.0\flynova`
2.  Double-click the **`init_git.bat`** file I just created for you.
    *   This will initialize Git, add all your files, and make the first commit.

## Step 3: Connect and Push
Once the script finishes, it will tell you what to do, but here are the commands you'll need to run in your terminal (Command Prompt or PowerShell):

1.  **Link your local project to GitHub:**
    *(Replace `YOUR_USERNAME` and `REPO_NAME` with your actual details from the GitHub page you just created)*
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
    ```

2.  **Push your code:**
    ```bash
    git push -u origin main
    ```

## Step 4: Verify
Refresh your GitHub repository page. You should see all your code, the `README.md`, and your project is now live! 

---

### Future Updates
When you make changes in the future, simply run:
```bash
git add .
git commit -m "Description of changes"
git push
```
