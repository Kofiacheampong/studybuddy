# Deploy Study Buddy to Render.com - Step by Step

## 🚀 Quick Overview
Render.com is the easiest way to deploy. Your app will be live in ~5 minutes with auto-deploy on every push!

---

## Step 1: Sign Up (2 minutes)

1. Go to https://render.com
2. Click "Sign Up"
3. Choose "Continue with GitHub"
4. Authorize Render to access your GitHub account
5. Done! You're logged in

---

## Step 2: Create Web Service (2 minutes)

1. On Render dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. Choose **"Connect a repository"**
4. Find and select **"studybuddy"**
5. Click **"Connect"**

---

## Step 3: Configure Service (1 minute)

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `study-buddy` |
| **Region** | `Oregon (US West)` (default, fine) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Environment Variables (IMPORTANT!)
Add this environment variable:

Click **"Add Environment Variable"**

| Key | Value |
|-----|-------|
| `ANTHROPIC_API_KEY` | [Your API key from .env] |

If you don't have an Anthropic API key:
- Go to https://console.anthropic.com
- Create account and get free credits
- Copy your API key
- Paste it here

---

## Step 4: Deploy! (1 minute)

1. Scroll down
2. Click **"Create Web Service"**
3. Watch it deploy (you'll see logs)
4. Wait for "Service is live" message
5. Click the URL to view your app

---

## 🎉 Your App is Live!

Render will give you a URL like:
```
https://study-buddy-abc123.onrender.com
```

**Visit your app**: Click the URL!

---

## ✅ Auto-Deploy Enabled

Every time you push to main:
```bash
git add .
git commit -m "your message"
git push origin main
```

Render automatically:
- Pulls your latest code
- Installs dependencies
- Restarts your app
- App is updated! ✨

---

## 📝 Important Notes

### Free Tier Limits
- **Spins down after 15 minutes of inactivity**
  - First request wakes it up (takes 30 seconds)
  - After that, runs normally
  - Good for testing/learning

### If You Need Always-On
- Upgrade to $7/month paid plan
- No spin-downs
- Better performance

### Database
- Your SQLite database `study_buddy.db` is created automatically
- Data persists between deployments
- Data persists during spin-downs

---

## 🔗 Your Custom Domain (Optional)

If you want a custom domain later:

1. On Render dashboard, go to your service
2. Click **"Settings"**
3. Under "Custom Domains", click **"Add"**
4. Enter your domain
5. Follow DNS setup instructions

---

## 📊 Monitor Your App

On Render dashboard:

1. Click your service name
2. **Logs**: See real-time logs
3. **Events**: Deployment history
4. **Metrics**: CPU, memory usage
5. **Settings**: Change configuration

---

## 🐛 Troubleshooting

### App won't start
1. Check logs: Click service → "Logs"
2. Look for error messages
3. Most common: Missing API key or dependencies

### "Connection refused"
1. Make sure your app is running locally first
2. Check `gunicorn app:app` starts successfully locally

### Database errors
1. `study_buddy.db` is created automatically
2. Check file permissions

### Can't see your app
1. Wait 30-60 seconds for first deploy
2. Check build logs for errors
3. Refresh the page

---

## Next: Test Your App

1. **Visit your Render URL**
2. Create a topic
3. Add notes/flashcards
4. Take a quiz
5. Make sure everything works

---

## Then: Test Auto-Deploy

1. Make a small change locally:
   ```bash
   echo "# Deployed to Render" >> README.md
   git add README.md
   git commit -m "test: verify render deployment"
   git push origin main
   ```

2. Watch Render deploy automatically
3. Refresh your app URL
4. See your changes live!

---

## 🎯 You're Done!

Your Study Buddy app is now:
- ✅ Live on the internet
- ✅ Auto-deploying on every push
- ✅ Accessible from anywhere
- ✅ Completely free

Share your URL: `https://study-buddy-abc123.onrender.com`

---

## Common Questions

**Q: Will my app be slow?**
A: Free tier might spin down. First request takes 30 sec, then normal. Upgrade to paid for always-on.

**Q: Can I use my own domain?**
A: Yes, but need to configure DNS. See "Custom Domain" section.

**Q: What if I want HTTPS?**
A: Render gives you free HTTPS automatically! URL is `https://...`

**Q: How much does it cost?**
A: Free tier is free! Paid plans start at $7/month for always-on.

**Q: Can I roll back?**
A: Yes, go to Events tab and click "Deploy Again" on old version.

---

## Next Steps

1. **Right now**: Go to https://render.com
2. **Sign up** with GitHub
3. **Create Web Service**
4. **Fill in the form** (see Step 3)
5. **Click "Create"**
6. **Wait for deploy** (~2 minutes)
7. **Visit your URL**
8. **Test your app**
9. **Share with friends!**

---

**Questions? Check Render docs**: https://docs.render.com

Good luck! 🚀

