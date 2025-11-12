# Render Deployment - Important Configuration

## 🔧 What Render.com Provides

When you deploy to Render, your app runs at:
```
https://study-buddy-abc123.onrender.com/
```

NOT at `/study/` subdirectory like your home server!

---

## Fix for Render Deployment

Your app currently has subdirectory middleware for `/study`. We need to disable this for Render.

### Option 1: Update app.py (Recommended)

The good news: Your app already handles this!

In `app.py`, line 35:
```python
if os.getenv('FLASK_ENV') != 'development':
    app.wsgi_app = SubdirectoryMiddleware(app.wsgi_app)
```

**For Render, don't set FLASK_ENV to 'production'**

### Option 2: Environment Variables in Render

When you create the service, set:
```
FLASK_ENV = development
```

This tells the app NOT to use the subdirectory middleware.

---

## Database Location on Render

On Render:
- Your app runs in `/app` directory
- Database should be in `/app/study_buddy.db` (local)
- Render provides ephemeral storage (persists but can be wiped)

The code already handles this:
```python
if os.getenv('FLASK_ENV') == 'production':
    DB = '/var/www/study-buddy/data/study_buddy.db'
else:
    DB = 'study_buddy.db'
```

Since we won't set `FLASK_ENV=production`, it will use `study_buddy.db` - perfect!

---

## Steps to Deploy to Render

Follow **DEPLOY_RENDER_STEP_BY_STEP.md**, but when configuring:

### Service Configuration

| Field | Value |
|-------|-------|
| **Name** | `study-buddy` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Environment Variables

Add these 2 variables:

| Key | Value |
|-----|-------|
| `ANTHROPIC_API_KEY` | [Your API key] |
| `FLASK_ENV` | `development` |

---

## ✅ Your App is Render-Ready!

No code changes needed! Your app will:
- ✅ Load from home page `/`
- ✅ Create database at `study_buddy.db`
- ✅ Work with Gunicorn WSGI server
- ✅ Handle all Flask routes correctly

---

## Quick Checklist Before Deploying

- [ ] You have GitHub account
- [ ] You signed up for Render.com
- [ ] Your study-buddy repo is on GitHub
- [ ] You have Anthropic API key (or skip for now)
- [ ] You're ready to click deploy!

---

## After Deployment

Your app will be at:
```
https://study-buddy-xxxxxxxx.onrender.com
```

All features work:
- ✅ Create topics
- ✅ Add notes
- ✅ Create flashcards
- ✅ Take quizzes
- ✅ AI summaries (if API key set)

---

Ready to deploy? Follow DEPLOY_RENDER_STEP_BY_STEP.md!

