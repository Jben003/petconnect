# ✅ Deployment Checklist - Print This!

Use this checklist to track your progress as you deploy.

---

## 📤 GitHub Upload Checklist

### Preparation
- [ ] Git installed on computer
- [ ] GitHub account created
- [ ] Remembered GitHub username: ___________________

### Step-by-Step
- [ ] Opened PowerShell in project folder
- [ ] Ran `git init`
- [ ] Configured Git with name and email
- [ ] Ran `git add .`
- [ ] Ran `git commit -m "Initial commit"`
- [ ] Created repository on GitHub.com
- [ ] Copied repository URL
- [ ] Ran `git remote add origin <URL>`
- [ ] Ran `git branch -M main`
- [ ] Ran `git push -u origin main`
- [ ] Authenticated with GitHub (username + token if needed)
- [ ] Verified files visible on GitHub

**GitHub Repository URL:** https://github.com/___________/___________

---

## 🔑 SECRET_KEY Setup

### Generate Key
- [ ] Generated SECRET_KEY using Python command
- [ ] Copied SECRET_KEY to safe location

**My SECRET_KEY (keep secret!):**
```
_____________________________________________________
```

### Local .env File
- [ ] Created `.env` file in project root
- [ ] Added SECRET_KEY to `.env`
- [ ] Added DEBUG=True
- [ ] Verified `.env` is in `.gitignore`

---

## 🌐 PythonAnywhere Deployment Checklist

### Account Setup
- [ ] PythonAnywhere account created
- [ ] Account verified via email
- [ ] Remembered PythonAnywhere username: ___________________

**My PythonAnywhere URL:** https://___________.pythonanywhere.com

### Console Setup
- [ ] Opened Bash console in PythonAnywhere
- [ ] Navigated to home directory (`cd ~`)
- [ ] Cloned GitHub repository
- [ ] Navigated to project folder (`cd petconnect`)

### Environment Setup
- [ ] Created virtual environment (`python3.10 -m venv venv`)
- [ ] Activated virtual environment (`source venv/bin/activate`)
- [ ] Upgraded pip
- [ ] Installed requirements (`pip install -r requirements.txt`)

### Configuration
- [ ] Generated new SECRET_KEY for production
- [ ] Created `.env` file using `nano .env`
- [ ] Added SECRET_KEY to `.env`
- [ ] Added DEBUG=False to `.env`
- [ ] Added PYTHONANYWHERE_USERNAME to `.env`
- [ ] Saved and exited nano (Ctrl+X, Y, Enter)

**My Production SECRET_KEY (keep secret!):**
```
_____________________________________________________
```

### Database Setup
- [ ] Ran migrations (`python manage.py migrate`)
- [ ] Created superuser (`python manage.py createsuperuser`)
- [ ] Remembered admin username: ___________________
- [ ] Remembered admin password: ___________________

### Static Files
- [ ] Collected static files (`python manage.py collectstatic`)
- [ ] Created media directory (`mkdir -p media`)

### Web App Configuration
- [ ] Went to Web tab in PythonAnywhere
- [ ] Created new web app (Manual configuration)
- [ ] Selected Python 3.10
- [ ] Opened WSGI configuration file
- [ ] Replaced content with correct WSGI code
- [ ] Updated username in WSGI file (2 places)
- [ ] Saved WSGI file
- [ ] Added static files mapping (/static/ → /home/username/petconnect/staticfiles)
- [ ] Added media files mapping (/media/ → /home/username/petconnect/media)
- [ ] Clicked Reload button
- [ ] Waited for reload to complete

### Testing
- [ ] Website loads at myusername.pythonanywhere.com
- [ ] Homepage displays correctly
- [ ] Admin panel accessible at /admin/
- [ ] Can log in to admin panel
- [ ] Static files (CSS, JS) loading
- [ ] No 500 errors

---

## 🐛 Troubleshooting (If Needed)

### Errors Encountered:
- [ ] _____________________________________________________
- [ ] _____________________________________________________
- [ ] _____________________________________________________

### Solutions Applied:
- [ ] _____________________________________________________
- [ ] _____________________________________________________
- [ ] _____________________________________________________

---

## 📝 Important Information (Keep Safe!)

**GitHub:**
- Username: ___________________
- Repository: https://github.com/___________/___________
- Personal Access Token: ___________________ (keep secret!)

**PythonAnywhere:**
- Username: ___________________
- Website URL: https://___________.pythonanywhere.com
- Admin Username: ___________________
- Admin Password: ___________________

**Keys:**
- Development SECRET_KEY: _____________________________________________________
- Production SECRET_KEY: _____________________________________________________

---

## ✅ Final Verification

- [ ] Code successfully on GitHub
- [ ] Website live on PythonAnywhere
- [ ] Can access admin panel
- [ ] Can create test user accounts
- [ ] Can upload test pets
- [ ] All features working

---

## 🎉 Deployment Complete!

**Date Completed:** ___________________

**Notes:**
_____________________________________________________
_____________________________________________________
_____________________________________________________

---

**Remember:** 
- Keep your SECRET_KEYs and passwords safe
- Never commit `.env` file to GitHub
- Use different SECRET_KEYs for development and production

