# 🚀 Deployment Guide: PetConnect to GitHub and PythonAnywhere

This guide will walk you through deploying your PetConnect Django application to GitHub and PythonAnywhere.

---

## 📋 Prerequisites

Before starting, make sure you have:
- ✅ Git installed on your computer
- ✅ A GitHub account
- ✅ A PythonAnywhere account (free tier available at https://www.pythonanywhere.com/)
- ✅ Your Django project working locally

---

## Part 1: Uploading to GitHub

### Step 1: Initialize Git Repository (if not already done)

Open PowerShell/Terminal in your project directory and run:

```bash
cd D:\petconnect
git init
```

### Step 2: Check Current Status

```bash
git status
```

This will show you which files are untracked or modified.

### Step 3: Add All Files to Git

```bash
git add .
```

**Note:** This will add all files except those listed in `.gitignore` (like `venv/`, `db.sqlite3`, `.env`, etc.)

### Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: PetConnect Django project"
```

### Step 5: Create Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name:** `petconnect` (or any name you prefer)
   - **Description:** "Pet adoption and services platform built with Django"
   - **Visibility:** Choose Public or Private
   - **DO NOT** check "Initialize with README" (we already have files)
5. Click **"Create repository"**

### Step 6: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use the "push an existing repository" option:

```bash
git remote add origin https://github.com/YOUR_USERNAME/petconnect.git
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 7: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

You may be prompted to enter your GitHub username and password (or personal access token).

**If authentication fails**, you'll need to use a Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate a new token with `repo` permissions
3. Use this token as your password when pushing

### Step 8: Verify Upload

Visit your repository on GitHub to confirm all files are uploaded.

---

## Part 2: Deploying to PythonAnywhere

### Step 1: Sign Up for PythonAnywhere

1. Go to [https://www.pythonanywhere.com/](https://www.pythonanywhere.com/)
2. Click **"Sign up"** and create a free account
3. Choose the **"Beginner"** free plan (sufficient for testing)

### Step 2: Access Your Dashboard

After signing up, you'll see your dashboard. Note your **username** (shown at the top right).

### Step 3: Open a Bash Console

1. Click on the **"Consoles"** tab
2. Click **"Bash"** to open a new console
3. You'll now have a terminal in PythonAnywhere

### Step 4: Clone Your GitHub Repository

In the PythonAnywhere bash console, run:

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/petconnect.git
```

Replace `YOUR_USERNAME` with your GitHub username.

### Step 5: Create Virtual Environment

```bash
cd petconnect
python3.10 -m venv venv
source venv/bin/activate
```

**Note:** PythonAnywhere uses Python 3.10 by default. Adjust if needed.

### Step 6: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7: Create .env File

```bash
nano .env
```

Add the following content (replace with your actual values):

```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
PYTHONANYWHERE_USERNAME=yourusername
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

**Important:**
- Generate a new SECRET_KEY (you can use Django's secret key generator online)
- Replace `yourusername` with your actual PythonAnywhere username
- Save and exit: Press `Ctrl+X`, then `Y`, then `Enter`

### Step 8: Run Migrations

```bash
python manage.py migrate
```

### Step 9: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Step 10: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This collects all static files into the `staticfiles` directory.

### Step 11: Configure Web App

1. Go to the **"Web"** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Select **"Manual configuration"** (not the wizard)
4. Select **Python 3.10** (or the version you used)
5. Click **"Next"** until you reach the configuration page

### Step 12: Edit WSGI Configuration

1. In the Web tab, find the section **"Code"**
2. Click on the link that says **"WSGI configuration file"** (usually `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. Delete all the default content
4. Replace it with the following:

```python
import os
import sys

# Add your project directory to the path
# REPLACE 'yourusername' with your actual PythonAnywhere username
path = '/home/yourusername/petconnect'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'petconnect.settings'

# Add virtual environment site-packages to path
venv_python_lib = os.path.join(path, 'venv', 'lib', 'python3.10', 'site-packages')
if os.path.exists(venv_python_lib):
    sys.path.insert(0, venv_python_lib)

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important:** 
- Replace `yourusername` with your actual PythonAnywhere username (appears twice in the code above)
- If you're using a different Python version, change `python3.10` to your version (e.g., `python3.11`)
- **Alternative:** You can also copy the content from `pythonanywhere_wsgi.py` file in your project

5. Click **"Save"**

### Step 13: Configure Static Files Mapping

1. In the **"Web"** tab, scroll down to **"Static files"**
2. Add a new mapping:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/petconnect/staticfiles`
3. Click the green **"Add"** button

### Step 14: Configure Media Files Mapping

1. In the same **"Static files"** section, add another mapping:
   - **URL:** `/media/`
   - **Directory:** `/home/yourusername/petconnect/media`
2. Click the green **"Add"** button

**Note:** If the `media` directory doesn't exist yet, create it:
```bash
mkdir -p ~/petconnect/media
```

### Step 15: Reload Web App

1. Scroll to the top of the **"Web"** tab
2. Click the big green **"Reload"** button
3. Wait for it to reload (may take 10-30 seconds)

### Step 16: Access Your Website

Your site should now be live at:
```
https://yourusername.pythonanywhere.com
```

---

## 🔧 Troubleshooting

### Common Issues:

#### 1. **Static Files Not Loading**
- Make sure you ran `collectstatic`
- Check the static files mapping in the Web tab
- Verify the `staticfiles` directory exists and has files

#### 2. **500 Internal Server Error**
- Check the error log in the **"Web"** tab → **"Error log"** section
- Common causes:
  - Missing environment variables in `.env`
  - Database not migrated
  - Incorrect paths in WSGI file

#### 3. **Module Not Found Errors**
- Verify your virtual environment is activated in WSGI file
- Check that all packages are installed: `pip list`

#### 4. **Media Files Not Showing**
- Create the `media` directory if it doesn't exist
- Add the media files mapping in the Web tab
- Reload the web app

#### 5. **Database Issues**
- Free accounts on PythonAnywhere use SQLite (which is fine)
- If you need to reset: delete `db.sqlite3` and run migrations again

### Viewing Logs:

- **Error log:** Web tab → "Error log" section
- **Server log:** Web tab → "Server log" section

---

## 📝 Post-Deployment Checklist

- [ ] Website loads without errors
- [ ] Static files (CSS, JS) are loading
- [ ] Media files (images) are displaying
- [ ] Database migrations completed
- [ ] Admin panel accessible at `/admin/`
- [ ] User registration/login works
- [ ] Pet listing and adoption flow works
- [ ] Payment integration (if using Razorpay) configured

---

## 🔄 Updating Your Deployment

When you make changes to your code:

### 1. Update GitHub:
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

### 2. Update PythonAnywhere:
In PythonAnywhere bash console:
```bash
cd ~/petconnect
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If requirements changed
python manage.py migrate  # If database changes
python manage.py collectstatic --noinput  # If static files changed
```

Then **reload** your web app in the Web tab.

---

## 🔐 Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Set `DEBUG=False`** in production (`.env` file)
3. **Use strong SECRET_KEY** in production
4. **Keep dependencies updated** regularly

---

## 📚 Additional Resources

- [PythonAnywhere Documentation](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

---

## 💡 Tips

1. **Test locally first** before deploying
2. **Keep your requirements.txt updated** - Run `pip freeze > requirements.txt` locally
3. **Use environment variables** for all sensitive data
4. **Monitor error logs** regularly on PythonAnywhere
5. **Backup your database** periodically (download `db.sqlite3`)

---

**Good luck with your deployment! 🎉**

If you encounter any issues, check the error logs and refer to the troubleshooting section above.

