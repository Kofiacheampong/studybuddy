# AWS RDS Setup Guide for StudyBuddy

## Overview

This guide walks you through setting up AWS RDS (PostgreSQL) for persistent database storage.

## Prerequisites

- AWS Account
- AWS CLI installed (optional but recommended)
- Your StudyBuddy app deployed on Render

## Step 1: Create AWS RDS PostgreSQL Instance

### Via AWS Console:

1. **Go to AWS RDS Console**
   - Navigate to https://console.aws.amazon.com/rds/

2. **Create Database**
   - Click "Create database"
   - Choose **PostgreSQL**
   - Template: **Free tier** (if eligible)
   
3. **Settings**:
   - DB instance identifier: `studybuddy-db`
   - Master username: `studybuddy_admin`
   - Master password: (create a strong password - save it!)

4. **Instance Configuration**:
   - DB instance class: `db.t3.micro` (free tier eligible)
   - Storage: 20 GB (free tier eligible)
   - Storage autoscaling: Disabled (for free tier)

5. **Connectivity**:
   - VPC: Default
   - Public access: **Yes** (needed for Render to connect)
   - VPC security group: Create new
   - Security group name: `studybuddy-db-sg`

6. **Additional Configuration**:
   - Initial database name: `studybuddy`
   - Automated backups: 7 days retention
   - Encryption: Enabled

7. **Create Database** - Takes ~5-10 minutes

## Step 2: Configure Security Group

1. Go to **EC2 Console** → **Security Groups**
2. Find `studybuddy-db-sg`
3. Edit **Inbound Rules**
4. Add rule:
   - Type: PostgreSQL
   - Protocol: TCP
   - Port: 5432
   - Source: `0.0.0.0/0` (allows Render to connect)
   - Description: "Allow Render connection"
   
⚠️ **Security Note**: For production, restrict to Render's IP ranges

## Step 3: Get Database Connection URL

1. Go to RDS Console → Databases → `studybuddy-db`
2. Copy the **Endpoint** (e.g., `studybuddy-db.abc123.us-east-1.rds.amazonaws.com`)
3. Create connection URL:
   ```
   postgresql://studybuddy_admin:YOUR_PASSWORD@ENDPOINT:5432/studybuddy
   ```
   
   Example:
   ```
   postgresql://studybuddy_admin:MySecurePass123@studybuddy-db.abc123.us-east-1.rds.amazonaws.com:5432/studybuddy
   ```

## Step 4: Update Render Environment Variables

1. Go to Render Dashboard → Your Service
2. Go to **Environment** tab
3. Add new variable:
   - Key: `DATABASE_URL`
   - Value: (paste your PostgreSQL URL from Step 3)
4. **Save Changes**

## Step 5: Deploy Updated Code

The app now checks for `DATABASE_URL`:
- If present → uses PostgreSQL (AWS RDS)
- If absent → uses SQLite (local dev)

### Update your code:

```bash
git pull origin main  # Get latest changes with RDS support
```

The app will automatically:
- Detect `DATABASE_URL` environment variable
- Connect to AWS RDS PostgreSQL
- Initialize tables on first run
- Migrate from SQLite seamlessly

## Step 6: Verify Connection

1. After deploy, check Render logs for:
   ```
   Initializing PostgreSQL database at: studybuddy-db...rds.amazonaws.com
   Database initialized successfully!
   ```

2. Test the app - create a topic, notes, flashcards
3. Data now persists across deployments! 🎉

## Costs

### Free Tier (12 months):
- db.t3.micro instance: 750 hours/month
- 20 GB storage
- 20 GB backup storage

### After Free Tier:
- ~$15-25/month for db.t3.micro with 20GB storage

## Troubleshooting

### Can't connect to database
- Check security group allows port 5432 from `0.0.0.0/0`
- Verify "Public access" is enabled
- Confirm `DATABASE_URL` format is correct
- Check RDS instance status is "Available"

### Tables not created
- Check Render logs for initialization errors
- Verify PostgreSQL version compatibility (12+)
- Ensure database name in URL matches RDS database name

### Performance issues
- Upgrade instance class (e.g., db.t3.small)
- Enable connection pooling
- Add database indexes for common queries

## Migration from SQLite

Your existing SQLite data won't automatically migrate. Options:

1. **Fresh start** (easiest): Start with empty PostgreSQL database
2. **Manual export/import**: Export SQLite data, import to PostgreSQL
3. **Migration script**: Use custom Python script to copy data

## Best Practices

1. **Backups**: Enable automated backups (7-30 days retention)
2. **Monitoring**: Set up CloudWatch alarms for CPU, storage, connections
3. **Security**: 
   - Use strong passwords
   - Rotate credentials periodically
   - Restrict security group to known IPs when possible
4. **Performance**: Monitor slow queries, add indexes as needed

## Alternative: AWS RDS Free Tier Alternatives

If you want to avoid AWS costs entirely:

- **Supabase** (free tier): Generous PostgreSQL hosting
- **ElephantSQL** (free tier): 20MB limit
- **Render PostgreSQL** (paid): $7/month, integrates well

See `docs/FREE_HOSTING_OPTIONS.md` for comparisons.

## Next Steps

Once RDS is working:
1. Set up automated backups
2. Configure CloudWatch monitoring
3. Consider read replicas for scaling (if needed)
4. Implement connection pooling for better performance

---

**Questions?** Check AWS RDS documentation: https://docs.aws.amazon.com/rds/
