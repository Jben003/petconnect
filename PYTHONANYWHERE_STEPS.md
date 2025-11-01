# 🌐 PythonAnywhere Deployment - Step by Step

## ✅ Prerequisites Check

Before starting, make sure you have:
- [ ] GitHub repository successfully uploaded (DONE! ✅)
- [ ] PythonAnywhere account created
- [ ] Generated a SECRET_KEY (if not, see SECRET_KEY_GUIDE.md)

---

## 🚀 Step-by-Step Deployment

### Step 1: Create PythonAnywhere Account (If Not Done)

1. Go to **https://www.pythonanywhere.com/**
2. Click **"Sign up"** button (top right)
3. Choose **"Beginner: $0/month"** (free plan)
4. Fill in:
   - **Username:** Choose a username (remember this!)
   - **Email:** Your email address
   - **Password:** Create a password
5. Click **"Sign up"**
6. **Check your email** and verify your account

**Remember your PythonAnywhere username!** Your site will be at `yourusername.pythonanywhere.com`

---

### Step 2: Access PythonAnywhere Dashboard

1. **Log in** to PythonAnywhere
2. You'll see tabs at the top: **Dashboard**, **Files**, **Consoles**, **Web**, etc.

---

### Step 3: Open a Bash Console

1. Click the **"Consoles"** tab
2. Click the **"Bash"** button (or click on an existing bash console if available)
3. A terminal window will open - this is like PowerShell but on PythonAnywhere's server

**You'll see something like:**
```
15:30 ~ $
```
The `~` means you're in your home directory.

---

### Step 4: Clone Your GitHub Repository

In the PythonAnywhere bash console, type these commands one by one:

```bash
cd ~
```

This ensures you're in your home directory.

Then:

```bash
git clone https://github.com/Jben003/petconnect.git
```

**Press Enter**

You should see:
```
Cloning into 'petconnect'...
remote: Enumerating objects: X objects, done.
...
```

**This will take 30-60 seconds - be patient!**

---

### Step 5: Navigate to Project Folder

```bash
cd petconnect
```

Verify you're in the right place:
```bash
ls
```

You should see: `accounts`, `adoption`, `manage.py`, `requirements.txt`, etc.

---

### Step 6: Create Virtual Environment

```bash
python3.10 -m venv venv
```

**Wait for it to complete** (takes 10-30 seconds)

**If you get an error like "python3.10: command not found":**
- Try: `python3.11 -m venv venv`
- Or check available version: `python3 --version`

---

### Step 7: Activate Virtual Environment

```bash
source venv/bin/activate
```

**After activation, you'll see `(venv)` at the beginning of your prompt:**
```
(venv) 15:35 ~/petconnect $
```

**⚠️ If you don't see `(venv)`, the activation didn't work. Try again.**

---

### Step 8: Upgrade pip

```bash
pip install --upgrade pip
```

Wait for completion.

---

### Step 9: Install Dependencies

```bash
pip install -r requirements.txt
```

**This will take 2-5 minutes** - be patient!

You'll see packages being installed:
```
Collecting Django==5.2.7
  Downloading Django-5.2.7-py3-none-any.whl...
Installing collected packages: ...
Successfully installed Django-5.2.7 ...
```

---

### Step 10: Generate SECRET_KEY

First, let's generate a SECRET_KEY for production. In the same bash console:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** - that's your production SECRET_KEY (save it somewhere safe!)

**Example output:**
```
django-insecure-xyz789abc123differentrandomstring456-def789ghi012
```

---

### Step 11: Create .env File

```bash
nano .env
```

This opens a text editor called "nano".

---

### Step 12: Add Content to .env File

In the nano editor, type (or paste) the following:

```env
SECRET_KEY=paste-your-generated-secret-key-here
DEBUG=False
PYTHONANYWHERE_USERNAME=yourpythonanywhereusername
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

**IMPORTANT:**
- Replace `paste-your-generated-secret-key-here` with the SECRET_KEY you just generated (Step 10)
- Replace `yourpythonanywhereusername` with your actual PythonAnywhere username

**Example:**
```env
SECRET_KEY=django-insecure-xyz789abc123differentrandomstring456-def789ghi012
DEBUG=False
PYTHONANYWHERE_USERNAME=johndoe
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
```

**To save and exit nano:**
1. Press `Ctrl + X`
2. Press `Y` (to confirm yes)
3. Press `Enter` (to confirm filename)

---

### Step 13: Run Database Migrations

```bash
python manage.py migrate
```

You should see:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, ...
Running migrations:
  Applying accounts.0001_initial... OK
  ...
```

---

### Step 14: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

You'll be prompted:
1. **Username:** Type a username (e.g., `admin`)
2. **Email address:** Type your email (optional, can press Enter)
3. **Password:** Type a password (you won't see it as you type - this is normal!)
4. **Password (again):** Type the same password again

**⚠️ Remember these credentials!** You'll use them to access the admin panel.

---

### Step 15: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This collects all CSS, JavaScript, and image files into a `staticfiles` folder.

You should see:
```
Copying '/static/...'
...
X static files copied to '/home/yourusername/petconnect/staticfiles'.
```

---

### Step 16: Create Media Directory

```bash
mkdir -p media
```

This creates a folder for uploaded images.

---

### Step 17: Go to Web Tab

1. Click the **"Web"** tab in PythonAnywhere dashboard (top navigation)
2. If you see **"Add a new web app"** button, click it
   - If you already have a web app, skip to Step 18

---

### Step 18: Configure Web App (First Time Only)

1. Click **"Add a new web app"**
2. You'll see a domain selection - click **"Next"** (use the default domain)
3. **Choose "Manual configuration"** (NOT the Flask/Django wizard!)
4. **Select Python version:** Choose **Python 3.10** (or whatever version you used earlier)
5. Click **"Next"** until you see the configuration page

**If you already have a web app:** Skip to Step 19.

---

### Step 19: Edit WSGI Configuration File

**This is CRITICAL - follow carefully!**

1. In the **Web** tab, scroll down to find **"Code"** section
2. You'll see a link like: **"WSGI configuration file: /var/www/yourusername_pythonanywhere_com_wsgi.py"**
3. **Click on that link** - it opens the WSGI file editor

4. **Delete ALL the existing content** in the file (select all with Ctrl+A, then delete)

5. **Copy and paste this code:**

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

**⚠️ CRITICAL:** Replace `yourusername` with your actual PythonAnywhere username!

**Example:** If your username is `johndoe`, it should be:
```python
path = '/home/johndoe/petconnect'
```

6. **Click the green "Save" button** at the top

---

### Step 20: Configure Static Files Mapping

1. Still in the **Web** tab, scroll down to **"Static files"** section
2. You'll see a table with "URL" and "Directory" columns
3. Click in the **"URL"** field and type: `/static/`
4. Click in the **"Directory"** field and type: `/home/yourusername/petconnect/staticfiles`
   - **Replace `yourusername` with your actual PythonAnywhere username!**
5. Click the green **"Add"** button

**You should see a new row appear in the table.**

---

### Step 21: Configure Media Files Mapping

1. In the same **"Static files"** section, add another mapping:
2. **URL:** `/media/`
3. **Directory:** `/home/yourusername/petconnect/media`
   - **Replace `yourusername` with your actual PythonAnywhere username!**
4. Click the green **"Add"** button

---

### Step 22: Reload Your Web App

1. Scroll to the top of the **Web** tab
2. You'll see a big green button that says **"Reload yourusername.pythonanywhere.com"**
3. **Click it!**
4. Wait 10-30 seconds (it will show "Reloading...")

---

### Step 23: Access Your Website! 🎉

Open a new browser tab and go to:

```
https://yourusername.pythonanywhere.com
```

**Replace `yourusername` with your actual PythonAnywhere username!**

**Your website should now be live!** 🚀

---

### Step 24: Test Your Site

1. Visit your site URL
2. Try accessing:
   - **Homepage:** `https://yourusername.pythonanywhere.com/`
   - **Admin panel:** `https://yourusername.pythonanywhere.com/admin/`
   - **Login:** `https://yourusername.pythonanywhere.com/accounts/login/`

---

## 🐛 Troubleshooting

### "500 Internal Server Error"
1. Go to **Web** tab → Scroll to **"Error log"**
2. Click the link to view the error log
3. Read the error message - it will tell you what's wrong

**Common fixes:**
- **"Module not found"** → Check WSGI file has correct paths
- **"No module named 'petconnect'"** → Verify project path in WSGI file
- **"SECRET_KEY" error** → Check .env file exists and has SECRET_KEY

### Static Files Don't Load
1. Go back to bash console
2. Run: `python manage.py collectstatic --noinput`
3. Verify the staticfiles folder exists: `ls staticfiles`
4. Check the static files mapping in Web tab
5. Reload web app

### Media Files Don't Show
1. Create media directory: `mkdir -p media`
2. Check media files mapping in Web tab
3. Reload web app

---

## ✅ Success Checklist

- [ ] PythonAnywhere account created
- [ ] Project cloned from GitHub
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] .env file created with SECRET_KEY
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] Static files collected
- [ ] WSGI file configured
- [ ] Static files mapping added
- [ ] Media files mapping added
- [ ] Web app reloaded
- [ ] Website accessible!

---

**Ready? Start from Step 1 above and let me know if you get stuck at any step!** 🎯

