# 🔐 Fix GitHub Authentication Error

## Problem
You're getting: `Authentication failed for https://github.com/Jben003/petconnect.git`

This happens because GitHub no longer accepts passwords for Git operations. You need a **Personal Access Token** instead.

---

## ✅ Solution: Create Personal Access Token

### Step 1: Generate Token on GitHub

1. **Go to GitHub.com** and **sign in**

2. **Click your profile picture** (top right corner)

3. **Click "Settings"**

4. **Scroll down** in the left sidebar until you see **"Developer settings"** (at the bottom)

5. **Click "Developer settings"**

6. **Click "Personal access tokens"** → **"Tokens (classic)"**

7. **Click "Generate new token"** → **"Generate new token (classic)"**

8. **Fill in the form:**
   - **Note:** Type something like "PetConnect Project" or "My PC Git Access"
   - **Expiration:** 
     - Choose **90 days** (good for learning)
     - OR **No expiration** (easier, but less secure)
   - **Select scopes:** Scroll down and check the box **"repo"**
     - This automatically selects all repository permissions
     - This is what you need!

9. **Scroll to bottom** and click **"Generate token"** (green button)

10. **⚠️ IMPORTANT - Copy the Token Now!**
    - You'll see a token that starts with `ghp_` followed by a long string
    - Example: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
    - **Copy this ENTIRE token immediately!**
    - **You won't be able to see it again after you leave this page!**
    - Paste it somewhere safe temporarily (notepad, etc.)

### Step 2: Use Token to Push

**Option A: Push with Token Prompt (Easiest)**

1. Go back to PowerShell in your project:
```powershell
cd D:\petconnect
```

2. Try pushing again:
```powershell
git push -u origin main
```

3. When prompted:
   - **Username:** Enter your GitHub username (`Jben003`)
   - **Password:** ⚠️ **Paste your token** (NOT your GitHub password!)

**Option B: Store Token in Git Credential Manager (Recommended)**

This way you won't have to enter it every time:

1. **Push once with token:**
```powershell
git push -u origin main
```
   - Username: `Jben003`
   - Password: Paste your token

2. Windows will ask if you want to save credentials - **Click "Yes"** or **"Save"**

---

## 🔄 Alternative: Use GitHub CLI (If Above Doesn't Work)

If you prefer, you can install GitHub CLI:

1. Download from: https://cli.github.com/
2. Install it
3. Run: `gh auth login`
4. Follow the prompts

---

## 🐛 Troubleshooting

### "Invalid username or password"
- Make sure you're using the **token** (starts with `ghp_`) as the password
- NOT your GitHub account password!

### "Permission denied"
- Make sure you checked the **"repo"** scope when creating the token
- Create a new token if you didn't

### Token Not Working After 90 Days
- Create a new token and use it instead
- Or recreate token with "No expiration"

---

## ✅ Verify It Worked

After successful push:

1. Go to: https://github.com/Jben003/petconnect
2. You should see all your project files!
3. The repository should no longer say "This repository is empty"

---

## 🔐 Security Tips

1. **Don't share your token** with anyone
2. **Don't commit tokens** to your code
3. **Revoke old tokens** if they're compromised:
   - GitHub → Settings → Developer settings → Personal access tokens
   - Click on the token → Delete

---

**Once you have your token, try pushing again and let me know if it works!** 🚀

