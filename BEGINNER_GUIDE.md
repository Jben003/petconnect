# 🎓 Complete Beginner's Guide - GitHub & PythonAnywhere Deployment

This guide assumes you have **ZERO** prior knowledge. We'll walk through every single click and command.

---

## 🔑 Part 0: Understanding SECRET_KEY

### What is SECRET_KEY?
The `SECRET_KEY` is a random string that Django uses to:
- Encrypt passwords
- Generate secure tokens
- Sign sessions and cookies
- Keep your application secure

### ⚠️ IMPORTANT:
- **NEVER share your SECRET_KEY publicly**
- **NEVER commit it to GitHub**
- Use **different SECRET_KEYs** for development and production
- It should be long and random

### How to Generate SECRET_KEY:

**Option 1: Using Python (Easiest)**
1. Open PowerShell in your project folder
2. Run:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Option 2: Online Generator**
1. Go to: https://djecrety.ir/
2. Click "Generate" button
3. Copy the generated key

**Option 3: Manual Python Script**
1. Create a file `generate_secret.py`:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
2. Run: `python generate_secret.py`

### Example SECRET_KEY:
```
django-insecure-abc123xyz789randomstring890-def456ghi012jkl345mno678pqr901stu234vwx567yz
```

**Keep this key safe!** You'll need it for both local development and PythonAnywhere.

---

## 📤 Part 1: Uploading to GitHub (Step-by-Step)

### Prerequisites Check:
- ✅ Git installed? Check by running in PowerShell:
```bash
git --version
```
If you see a version number, Git is installed. If you see an error, download Git from: https://git-scm.com/download/win

---

### Step 1: Create GitHub Account

1. Go to **https://github.com**
2. Click **"Sign up"** button (top right)
3. Enter:
   - Username (remember this!)
   - Email address
   - Password
4. Verify your email address (check your inbox)
5. Complete the setup questions

**Remember your GitHub username!** You'll need it later.

---

### Step 2: Open PowerShell in Your Project Folder

1. Press `Windows Key + R`
2. Type: `powershell` and press Enter
3. Navigate to your project:
```bash
cd D:\petconnect
```
4. Verify you're in the right place:
```bash
dir
```
You should see folders like `accounts`, `adoption`, `petconnect`, etc.

---

### Step 3: Check if Git is Already Initialized

```bash
git status
```

**If you see:** "fatal: not a git repository"
→ Go to Step 4

**If you see:** a list of files
→ Go to Step 5 (Git is already initialized)

---

### Step 4: Initialize Git Repository

```bash
git init
```

You should see: "Initialized empty Git repository in D:/petconnect/.git/"

---

### Step 5: Configure Git (First Time Only)

Tell Git who you are:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and email (the one you used for GitHub).

---

### Step 6: Check What Will Be Uploaded

```bash
git status
```

This shows:
- **Red files** = Will NOT be uploaded (these are in .gitignore - like venv, db.sqlite3)
- **Green files** = Ready to be uploaded
- **Untracked files** = New files that need to be added

You should see your project files like `manage.py`, `requirements.txt`, etc.

---

### Step 7: Add Files to Git

```bash
git add .
```

The `.` means "add all files in current directory"

You should see no errors. Run `git status` again - files should now be green.

---

### Step 8: Create Your First Commit

```bash
git commit -m "Initial commit: PetConnect Django project"
```

The `-m` flag means "message" - this describes what you're saving.

You should see something like: "X files changed, Y insertions(+)"

---

### Step 9: Create Repository on GitHub

1. Go to **https://github.com** and **log in**
2. Look at the top right corner - you'll see a **"+"** icon
3. Click the **"+"** icon
4. Click **"New repository"** from the dropdown menu

5. Fill in the form:
   - **Repository name:** `petconnect` (or any name you like)
   - **Description:** "Pet adoption and services platform" (optional)
   - **Public** or **Private:** Choose Private if you want (recommended for learning)
   - **⚠️ DO NOT check** "Add a README file" (we already have files)
   - **⚠️ DO NOT check** "Add .gitignore" (we already have one)
   - **⚠️ DO NOT check** "Choose a license" (optional, skip for now)

6. Click the green **"Create repository"** button

---

### Step 10: Copy Repository URL

After creating the repository, GitHub will show you a page with instructions.

1. Look for a section that says **"...or push an existing repository from the command line"**
2. You'll see a URL like: `https://github.com/YOUR_USERNAME/petconnect.git`
3. **Copy this entire URL** (Ctrl+C)

**IMPORTANT:** Replace `YOUR_USERNAME` with your actual GitHub username in your mind (the URL GitHub shows will already have it).

---

### Step 11: Connect Your Local Project to GitHub

In PowerShell (still in your project folder), run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/petconnect.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

Example: If your username is `johndoe`, the command would be:
```bash
git remote add origin https://github.com/johndoe/petconnect.git
```

If successful, you'll see no error message.

---

### Step 12: Rename Branch to "main"

```bash
git branch -M main
```

This ensures your branch is named "main" (GitHub's default).

---

### Step 13: Push to GitHub

```bash
git push -u origin main
```

**This is where authentication happens:**

#### Scenario A: GitHub Desktop Authentication
- A browser window might open
- Sign in to GitHub
- Authorize Git
- The push will complete automatically

#### Scenario B: Username/Password Prompt
You'll be asked for:
- **Username:** Your GitHub username
- **Password:** ⚠️ **NOT your GitHub password!** You need a **Personal Access Token**

---

### Step 14: Create Personal Access Token (If Needed)

If password authentication fails, you need a token:

1. Go to **GitHub.com** → Click your **profile picture** (top right)
2. Click **"Settings"**
3. Scroll down in the left sidebar → Click **"Developer settings"**
4. Click **"Personal access tokens"** → **"Tokens (classic)"**
5. Click **"Generate new token"** → **"Generate new token (classic)"**
6. Fill in:
   - **Note:** "PetConnect Project" (or any name)
   - **Expiration:** Choose 90 days (or No expiration if you prefer)
   - **Select scopes:** Check **"repo"** (this selects all repo permissions)
7. Scroll down and click **"Generate token"**
8. **⚠️ COPY THE TOKEN IMMEDIATELY!** It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You won't be able to see it again!
   - Paste it somewhere safe temporarily

9. Go back to PowerShell
10. Run `git push -u origin main` again
11. When asked for password, **paste your token** (not your GitHub password)

---

### Step 15: Verify Upload

1. Go to your repository page on GitHub
2. You should see all your project files!
3. Refresh the page if needed

**🎉 Congratulations! Your code is now on GitHub!**

---

## 🌐 Part 2: Deploying to PythonAnywhere (Step-by-Step)

### Step 1: Create PythonAnywhere Account

1. Go to **https://www.pythonanywhere.com/**
2. Click **"Sign up"** button (top right)
3. Choose **"Beginner: $0/month"** (free plan)
4. Fill in:
   - Username (remember this!)
   - Email address
   - Password
5. Click **"Sign up"**
6. Check your email and verify your account

**Remember your PythonAnywhere username!** Your site will be at `yourusername.pythonanywhere.com`

---

### Step 2: Access Dashboard

1. Log in to PythonAnywhere
2. You'll see a **Dashboard** with tabs at the top:
   - **Dashboard**
   - **Files**
   - **Consoles**
   - **Web**
   - **Tasks**
   - **Databases**

---

### Step 3: Open a Bash Console

1. Click the **"Consoles"** tab
2. Click the **"Bash"** button (or click on an existing bash console)
3. A terminal window will open (this is like PowerShell, but on PythonAnywhere's server)

**You'll see something like:**
```
15:30 ~ $
```
The `~` means you're in your home directory.

---

### Step 4: Clone Your GitHub Repository

In the PythonAnywhere bash console, type:

```bash
cd ~
```

This ensures you're in your home directory.

Then:

```bash
git clone https://github.com/YOUR_USERNAME/petconnect.git
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

Example:
```bash
git clone https://github.com/johndoe/petconnect.git
```

**Press Enter**

You should see:
```
Cloning into 'petconnect'...
remote: Enumerating objects: X objects, done.
...
```

This might take 30-60 seconds.

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

If you get an error like "python3.10: command not found", try:
```bash
python3.11 -m venv venv
```

Check which Python version is available:
```bash
python3 --version
```

---

### Step 7: Activate Virtual Environment

```bash
source venv/bin/activate
```

After activation, you'll see `(venv)` at the beginning of your prompt:
```
(venv) 15:35 ~/petconnect $
```

**If you don't see `(venv)`, the activation didn't work. Try again.**

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

### Step 10: Create .env File

First, let's generate a SECRET_KEY. In the same bash console:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Copy the output** (it's your SECRET_KEY).

Now create the .env file:

```bash
nano .env
```

This opens a text editor called "nano".

---

### Step 11: Add Content to .env File

In the nano editor, type (or paste) the following:

```env
SECRET_KEY=paste-your-generated-secret-key-here
DEBUG=False
PYTHONANYWHERE_USERNAME=yourpythonanywhereusername
RAZORPAY_KEY_ID=your_razorpay_key_id_if_you_have_one
RAZORPAY_KEY_SECRET=your_razorpay_key_secret_if_you_have_one
```

**IMPORTANT:**
- Replace `paste-your-generated-secret-key-here` with the SECRET_KEY you just generated
- Replace `yourpythonanywhereusername` with your actual PythonAnywhere username
- Replace the Razorpay keys if you have them, or leave them empty if you don't

**Example:**
```env
SECRET_KEY=django-insecure-abc123xyz789randomstring890-def456ghi012
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

### Step 12: Run Database Migrations

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

### Step 13: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

You'll be prompted:
1. **Username:** Type a username (e.g., `admin`)
2. **Email address:** Type your email (optional, can press Enter)
3. **Password:** Type a password (you won't see it as you type - this is normal!)
4. **Password (again):** Type the same password again

**Remember these credentials!** You'll use them to access the admin panel.

---

### Step 14: Collect Static Files

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

### Step 15: Create Media Directory (If Needed)

```bash
mkdir -p media
```

This creates a folder for uploaded images.

---

### Step 16: Go to Web Tab

1. Click the **"Web"** tab in PythonAnywhere dashboard
2. If you see **"Add a new web app"** button, click it
   - If you already have a web app, we'll configure it in the next step

---

### Step 17: Configure Web App (First Time)

1. Click **"Add a new web app"**
2. You'll see a domain selection - click **"Next"** (use the default)
3. **Choose "Manual configuration"** (NOT the Flask/Django wizard)
4. **Select Python version:** Choose **Python 3.10** (or whatever version you used)
5. Click **"Next"** until you see the configuration page

**If you already have a web app:** Skip to Step 18.

---

### Step 18: Edit WSGI Configuration File

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

**CRITICAL:** Replace `yourusername` in TWO places:
- Line 5: `/home/yourusername/petconnect`
- Replace with your actual PythonAnywhere username!

**Example:** If your username is `johndoe`, it should be:
```python
path = '/home/johndoe/petconnect'
```

6. **Click the green "Save" button** at the top

---

### Step 19: Configure Static Files Mapping

1. Still in the **Web** tab, scroll down to **"Static files"** section
2. You'll see a table with "URL" and "Directory" columns
3. Click in the **"URL"** field and type: `/static/`
4. Click in the **"Directory"** field and type: `/home/yourusername/petconnect/staticfiles`
   - **Replace `yourusername` with your actual username!**
5. Click the green **"Add"** button

**You should see a new row appear in the table.**

---

### Step 20: Configure Media Files Mapping

1. In the same **"Static files"** section, add another mapping:
2. **URL:** `/media/`
3. **Directory:** `/home/yourusername/petconnect/media`
   - **Replace `yourusername` with your actual username!**
4. Click the green **"Add"** button

---

### Step 21: Reload Your Web App

1. Scroll to the top of the **Web** tab
2. You'll see a big green button that says **"Reload yourusername.pythonanywhere.com"**
3. **Click it!**
4. Wait 10-30 seconds (it will show "Reloading...")

---

### Step 22: Access Your Website!

Open a new browser tab and go to:

```
https://yourusername.pythonanywhere.com
```

**Replace `yourusername` with your actual PythonAnywhere username!**

**🎉 Your website should now be live!**

---

### Step 23: Test Your Site

1. Visit your site URL
2. Try accessing:
   - Homepage: `https://yourusername.pythonanywhere.com/`
   - Admin panel: `https://yourusername.pythonanywhere.com/admin/`
   - Login: `https://yourusername.pythonanywhere.com/accounts/login/`

---

## 🐛 Troubleshooting

### If You See "500 Internal Server Error":

1. Go to **Web** tab → Scroll to **"Error log"**
2. Click the link to view the error log
3. Read the error message - it will tell you what's wrong

**Common fixes:**
- **"Module not found"** → Check WSGI file has correct paths
- **"No module named 'petconnect'"** → Verify project path in WSGI file
- **"SECRET_KEY" error** → Check .env file exists and has SECRET_KEY

### If Static Files Don't Load:

1. Go back to bash console
2. Run: `python manage.py collectstatic --noinput`
3. Verify the staticfiles folder exists: `ls staticfiles`
4. Check the static files mapping in Web tab
5. Reload web app

### If Media Files Don't Show:

1. Create media directory: `mkdir -p media`
2. Check media files mapping in Web tab
3. Reload web app

---

## ✅ Success Checklist

- [ ] Code uploaded to GitHub
- [ ] Repository visible on GitHub with all files
- [ ] PythonAnywhere account created
- [ ] Project cloned on PythonAnywhere
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
- [ ] Website accessible at yourusername.pythonanywhere.com

---

## 📝 What's Next?

After deployment:
1. Test all features on your live site
2. Upload some test pets through admin panel
3. Create test user accounts
4. Test the adoption flow

---

## 💡 Tips

1. **Keep your .env file safe** - Never commit it to GitHub
2. **Use different SECRET_KEYs** for local and production
3. **Check error logs regularly** in PythonAnywhere Web tab
4. **Backup your database** periodically (download db.sqlite3)

---

**Congratulations! You've successfully deployed your Django app! 🎉**

If you get stuck at any step, check the error messages carefully - they usually tell you exactly what's wrong!

