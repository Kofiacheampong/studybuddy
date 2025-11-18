# Render Deployment - Database Options

## Current Status

Your app is now live on Render! 🎉

### URL
```
https://studybuddy-6b0i.onrender.com
```

## Database Behavior

### SQLite on Render (Current Setup)

**Location**: `/tmp/study_buddy.db` (ephemeral)

**Pros**:
- ✅ No additional configuration needed
- ✅ App works immediately
- ✅ Free tier compatible

**Cons**:
- ❌ Data resets when service restarts
- ❌ Data resets when new code is deployed
- ❌ Not suitable for production

---

## Persistent Data Options

### Option 1: Use Render Postgres (Recommended)

For true production use, upgrade to a PostgreSQL database on Render:

**Steps**:
1. Go to your Render dashboard
2. Click "New +" → "PostgreSQL"
3. Set name to "studybuddy-db"
4. Note the internal database URL
5. Add to your service environment variables as `DATABASE_URL`
6. Update `src/app.py` to use PostgreSQL instead of SQLite

**Code Update Example**:
```python
import psycopg2  # PostgreSQL driver

if os.getenv('FLASK_ENV') == 'production':
    # Use Render Postgres
    db_url = os.getenv('DATABASE_URL')
    # Parse and connect to PostgreSQL
else:
    # Use SQLite locally
    DB = os.path.join(..., 'study_buddy.db')
```

### Option 2: Keep SQLite but Accept Data Loss

Current setup - works for:
- ✅ Learning/prototyping
- ✅ Testing the app
- ✅ Demo purposes

Just accept that data resets on redeploy.

### Option 3: Use External Database Service

Options like:
- **AWS RDS** (free tier available)
- **Cloud SQL** (Google Cloud)
- **Supabase** (Postgres-as-a-service, free tier)
- **PlanetScale** (MySQL-as-a-service)

---

## How to Monitor

Check Render logs:
1. Go to https://dashboard.render.com
2. Select your "study-buddy" service
3. Click "Logs" tab
4. Monitor for errors

---

## Next Steps

**For learning/demo**: You're done! App is live.

**For production data**:
1. Add Postgres database to Render
2. Update app code to use PostgreSQL
3. Redeploy

**Questions?** See original `docs/RENDER_DEPLOYMENT.md`
