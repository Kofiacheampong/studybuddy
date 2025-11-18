# AWS RDS Integration - Complete ✅

## What Was Done

Successfully migrated Study Buddy to use a database abstraction layer that supports both SQLite (development) and PostgreSQL (AWS RDS production).

### Files Modified

1. **`src/database.py`** - Created database abstraction layer
   - `get_db_connection()`: Returns SQLite or PostgreSQL connection based on DATABASE_URL
   - `init_database()`: Creates tables with correct DDL for each database
   - `get_placeholder()`: Returns correct parameterized query syntax ('?' or '%s')
   - `USE_POSTGRES`: Auto-detects DATABASE_URL environment variable

2. **`src/topics_manager.py`** - Fully migrated (6 routes)
   - All routes now use `get_db_connection()`
   - Compatible with both SQLite and PostgreSQL

3. **`src/app.py`** - Fully migrated (10 routes)
   - All routes now use `get_db()` helper function
   - `get_db()` wrapper calls `get_db_connection()` from database module
   - Compatible with both SQLite and PostgreSQL

4. **`requirements.txt`** - Added PostgreSQL driver
   - `psycopg2-binary==2.9.9` for AWS RDS connection

### Tests Verified

All 10 tests passing with database abstraction layer:
```
✅ test_index_page_loads
✅ test_notes_page_loads  
✅ test_can_create_note
✅ test_flashcards_page_loads
✅ test_can_create_flashcard
✅ test_quiz_page_loads
✅ test_404_for_nonexistent_route
✅ test_404_for_invalid_topic_id
✅ test_list_topics_page
✅ test_create_topic_form
```

## Next Steps: Deploy to Render with AWS RDS

### Step 1: Get Your RDS Connection String

From your AWS RDS console, collect these details:
- **Endpoint**: `studybuddy-db.abc123.us-east-1.rds.amazonaws.com` (example)
- **Port**: `5432` (default PostgreSQL)
- **Database name**: `studybuddy` (what you created)
- **Username**: `studybuddy_admin` (or whatever you chose)
- **Password**: (the password you set)

Build your DATABASE_URL:
```
postgresql://username:password@endpoint:5432/database_name
```

**Example:**
```
postgresql://studybuddy_admin:MySecurePass123@studybuddy-db.abc123.us-east-1.rds.amazonaws.com:5432/studybuddy
```

### Step 2: Add DATABASE_URL to Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your **studybuddy** web service
3. Go to **Environment** tab in the left sidebar
4. Click **Add Environment Variable**
5. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Your complete PostgreSQL connection string from Step 1
6. Click **Save Changes**

**Important**: Render will automatically redeploy when you add the environment variable.

### Step 3: Verify RDS Security Group

Ensure your RDS security group allows connections from Render:

1. Go to AWS RDS Console → Your database → Security group
2. Check **Inbound rules**
3. Should have:
   - **Type**: PostgreSQL
   - **Protocol**: TCP
   - **Port**: 5432
   - **Source**: `0.0.0.0/0` (public access) OR Render IP ranges

If you need tighter security, Render provides static IP addresses on paid plans. For free tier, use `0.0.0.0/0`.

### Step 4: Deploy Code Changes

Commit and push the database abstraction layer:

```bash
git add -A
git commit -m "feat: Add AWS RDS PostgreSQL support with database abstraction layer"
git push origin main
```

Render will automatically deploy the new code.

### Step 5: Monitor Deployment

1. Watch Render logs during deployment:
   ```
   Initializing PostgreSQL database...
   Database initialized successfully
   ```

2. Look for successful PostgreSQL connection messages

3. Check for any errors related to:
   - Connection refused → Check security group
   - Authentication failed → Verify DATABASE_URL credentials
   - Database does not exist → Ensure database name is correct

### Step 6: Test Your App

1. Visit: https://studybuddy-6b0i.onrender.com/study
2. Create a test topic
3. Add notes to the topic
4. Create flashcards
5. Take a quiz

### Step 7: Verify Data Persistence

1. Make changes (create notes, topics, etc.)
2. Trigger a redeploy on Render:
   - Go to **Manual Deploy** → **Clear build cache & deploy**
3. After redeployment, verify your data is still there
4. ✅ Data persists = AWS RDS working correctly!

## How It Works

### Development (Your Local Machine)
- No `DATABASE_URL` environment variable set
- App uses SQLite: `/home/kofi/studybuddy/data/study_buddy.db`
- Fast, simple, perfect for development

### Production (Render with AWS RDS)
- `DATABASE_URL` environment variable set
- App detects PostgreSQL connection string
- Uses AWS RDS PostgreSQL database
- Data persists across deployments

### Code Pattern
```python
from database import get_db_connection

def my_route():
    conn = get_db_connection()  # Returns SQLite OR PostgreSQL
    c = conn.cursor()
    c.execute('SELECT * FROM notes')
    # ... rest of code works the same!
```

The abstraction layer handles all differences between SQLite and PostgreSQL automatically.

## Troubleshooting

### Error: "Connection refused"
- **Cause**: RDS security group blocking connections
- **Fix**: Add inbound rule for port 5432 from `0.0.0.0/0`

### Error: "Database does not exist"
- **Cause**: Database name in DATABASE_URL doesn't match RDS
- **Fix**: Verify database name: `psql -h endpoint -U username -l`

### Error: "Authentication failed"
- **Cause**: Wrong username or password in DATABASE_URL
- **Fix**: Reset password in RDS console, update DATABASE_URL

### Tables Not Created
- **Cause**: Init database might have failed
- **Fix**: Check Render logs for initialization errors

### Data Still Lost After Redeploy
- **Cause**: DATABASE_URL not set or app still using SQLite
- **Fix**: Verify environment variable in Render dashboard

## Cost Monitoring

**AWS RDS Free Tier** (first 12 months):
- 750 hours/month of db.t3.micro
- 20 GB storage
- 20 GB backups

**After free tier or exceeding limits:**
- db.t3.micro: ~$15/month
- Storage: $0.115/GB/month
- Backups: $0.095/GB/month

**Estimated cost**: $15-20/month after free tier

## Backup Strategy

### Automated Backups (AWS RDS)
- Already enabled by default
- 7-day retention
- Daily snapshots at maintenance window

### Manual Backup
```bash
# Export to SQL file
pg_dump -h your-endpoint -U username -d studybuddy > backup.sql

# Restore
psql -h your-endpoint -U username -d studybuddy < backup.sql
```

## Success Checklist

- [ ] DATABASE_URL added to Render environment variables
- [ ] Code committed and pushed to GitHub
- [ ] Render deployment successful (check logs)
- [ ] App accessible at studybuddy-6b0i.onrender.com/study
- [ ] Can create and view topics
- [ ] Can create and view notes
- [ ] Can create and view flashcards
- [ ] Can take quiz
- [ ] Data persists after manual redeploy

## Questions?

Refer to `docs/AWS_RDS_SETUP.md` for detailed AWS RDS setup instructions.

Good luck! 🚀
