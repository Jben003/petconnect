# ⚡ Quick Start Guide - GitHub & PythonAnywhere Deployment

## 🚀 Fast Track Deployment

### GitHub Upload (5 minutes)

```bash
# 1. Initialize Git (if not done)
git init

# 2. Add files
git add .

# 3. Commit
git commit -m "Initial commit: PetConnect Django project"

# 4. Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/petconnect.git

# 5. Push
git branch -M main
git push -u origin main
```

**Note:** If authentication fails, use a Personal Access Token from GitHub Settings → Developer settings → Personal access tokens

---

### PythonAnywhere Deployment (15 minutes)

#### 1. Clone Repository
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/petconnect.git
cd petconnect
```

#### 2. Setup Virtual Environment
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
nano .env
```

Add:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
PYTHONANYWHERE_USERNAME=yourusername
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

Save: `Ctrl+X` → `Y` → `Enter`

#### 4. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

#### 5. Configure Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"** → **Manual configuration** → **Python 3.10**
3. Edit **WSGI configuration file**:

```python
import os
import sys

path = '/home/yourusername/petconnect'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'petconnect.settings'

venv_python_lib = os.path.join(path, 'venv', 'lib', 'python3.10', 'site-packages')
if os.path.exists(venv_python_lib):
    sys.path.insert(0, venv_python_lib)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `yourusername` with your actual username!**

4. Add Static Files Mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/petconnect/staticfiles`

5. Add Media Files Mapping:
   - URL: `/media/`
   - Directory: `/home/yourusername/petconnect/media`

6. Click **Reload** button

#### 6. Access Your Site
```
https://yourusername.pythonanywhere.com
```

---

## 🔄 Update After Changes

### Update GitHub:
```bash
git add .
git commit -m "Your message"
git push origin main
```

### Update PythonAnywhere:
```bash
cd ~/petconnect
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If requirements changed
python manage.py migrate         # If DB changes
python manage.py collectstatic   # If static files changed
```

Then **Reload** web app in PythonAnywhere Web tab.

---

## ❗ Common Issues

| Issue | Solution |
|-------|----------|
| Static files not loading | Run `collectstatic`, check mapping |
| 500 Error | Check error log in Web tab |
| Module not found | Verify venv path in WSGI file |
| Media files not showing | Add media mapping, create media directory |

---

## 📞 Need Help?

See full detailed guide in **[DEPLOYMENT.md](DEPLOYMENT.md)**

