# Deploy Study Buddy to Render.com

## 🚀 Quick Start (5 Minutes)

### Step 1: Sign Up with GitHub
1. Go to https://render.com
2. Click "Sign up"
3. Choose "Sign up with GitHub"
4. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click "New +"
2. Select "Web Service"
3. Search for and select **"studybuddy"** repository
4. Click "Connect"

### Step 3: Configure Service
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | study-buddy |
| **Region** | Oregon (or your preference) |
| **Branch** | main |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Step 4: Environment Variables
Add these environment variables:

```
FLASK_ENV=production
ANTHROPIC_API_KEY=[Your Anthropic API key if you have one]
```

**How to add env variables:**
- In the Render dashboard, scroll to "Environment"
- Click "Add Environment Variable"
- Add each variable

### Step 5: Create & Deploy
1. Click "Create Web Service"
2. Render automatically starts building
3. Wait for "Live" status (2-5 minutes)
4. Your app is live! 🎉

---

## 📱 Access Your App

Once deployed, Render gives you a URL like:
```
https://study-buddy.onrender.com
```

Your app is **automatically accessible on the internet!**

---

## 🔄 How Auto-Deploy Works

With Render:
1. You push code to GitHub main branch
2. Render automatically detects the push
3. Rebuilds and deploys your app
4. Takes ~2-5 minutes
5. New version is live!

**No GitHub Secrets needed!** (unlike SSH deployment)

---

## 📊 Database Considerations

### SQLite on Render
Your app uses SQLite (study_buddy.db). On Render:
- ✅ Works fine for small apps
- ❌ Data resets when service restarts
- ❌ Not persistent across deployments

### Solution 1: Use Render Postgres (Recommended for production)
1. Add Postgres database service in Render
2. Update app.py to use Postgres
3. Data persists across restarts

### Solution 2: Keep SQLite (For now)
- Works for testing/learning
- Data resets on redeploy (not ideal for production)
- Fine for MVP/prototype

### Solution 3: External Database
- Use cloud database service
- Better for production

**For Study Buddy MVP, SQLite is fine for testing!**

---

## 🔑 Important Settings

### Build & Start Commands
- **Build**: `pip install -r requirements.txt`
- **Start**: `gunicorn app:app`

### Python Version
Render auto-detects from requirements.txt

### Memory/CPU
- Free tier: Shared resources, adequate for small app
- Pay tier: Better performance

---

## ✅ Verification Checklist

After deployment:
- [ ] See "Live" status in Render dashboard
- [ ] Click the service URL
- [ ] App homepage loads
- [ ] Can create a topic
- [ ] Can add notes/flashcards
- [ ] Quiz feature works

---

## 🐛 Troubleshooting

### Build Fails
1. Check "Build Logs" in Render dashboard
2. Common issues:
   - Missing dependency in requirements.txt
   - Python version mismatch
   - Syntax error in code

**Fix**: Commit corrected code, push to main, Render rebuilds automatically

### App Won't Start
1. Check "Logs" tab in Render
2. Common issues:
   - Import error
   - Missing environment variable
   - Database issue

**Fix**: Check the error, fix code, push to main

### Can't Connect to App
1. Wait a few minutes after deployment
2. Try refreshing page
3. Check Render dashboard for "Live" status
4. If stuck, restart service in Render dashboard

### Database Issues
1. First deploy: SQLite creates empty database
2. If data not persisting: Normal for SQLite on Render
3. For persistent data: Upgrade to Postgres

---

## 📝 Next Steps

### After Deployment:
1. ✅ Test all features on Render URL
2. ✅ Share URL with friends to try
3. ✅ Make code changes and watch auto-deploy
4. ✅ Monitor logs if issues arise

### To Keep Deploying:
Just push to main branch:
```bash
git add .
git commit -m "your message"
git push origin main
# Render auto-deploys!
```

### To Add Custom Domain (Optional):
In Render dashboard:
1. Go to Settings
2. Custom Domain
3. Add your domain
4. Follow DNS setup instructions

---

## 🎯 Your Deployment Timeline

1. **Now**: Create Render account
2. **5 min**: Connect GitHub repo
3. **2-5 min**: Build and deploy
4. **Your app is live!** 🎉

---

## Quick Links

- **Render Dashboard**: https://dashboard.render.com
- **Render Docs**: https://render.com/docs
- **Study Buddy URL**: https://study-buddy.onrender.com (after deploy)
- **GitHub Repo**: https://github.com/Kofiacheampong/studybuddy

---

## Final Checklist

Before you start:
- [ ] GitHub account (already have it)
- [ ] Render account (create at render.com)
- [ ] GitHub repo authorized (happens during signup)

That's it! Let's go! 🚀

