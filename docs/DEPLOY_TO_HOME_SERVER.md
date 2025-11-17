# Deploy Study Buddy to Your Home Server

## Your Server Details
- **IP**: 192.168.1.172
- **SSH Port**: 64295
- **SSH User**: kofiarcher
- **Status**: Already configured for deployment

---

## Step 1: Verify Server is Ready

### Check SSH Access
```bash
ssh -p 64295 kofiarcher@192.168.1.172 "echo Server is reachable"
```

If this works, your SSH access is good. Continue to Step 2.

If it fails:
- Make sure your server is on
- Make sure SSH port 64295 is open
- Make sure your SSH key is in server's `~/.ssh/authorized_keys`

### Setup SSH Key on Server (if needed)
```bash
# On your local machine:
ssh-copy-id -p 64295 -i ~/.ssh/id_rsa kofiarcher@192.168.1.172
```

---

## Step 2: Run Initial Deployment Script

This sets up everything on the server:

```bash
cd /home/kofi/studybuddy
./deploy.sh
```

This will:
- ✅ Create `/var/www/study-buddy` directory
- ✅ Install Python, nginx, gunicorn
- ✅ Set up systemd service
- ✅ Configure nginx as reverse proxy
- ✅ Start the Flask app
- ✅ Make it accessible at `http://192.168.1.172`

---

## Step 3: Set GitHub Secrets

For auto-deployment, add these 4 secrets to GitHub:

**Go to**: https://github.com/Kofiacheampong/studybuddy/settings/secrets/actions

Add:
| Secret | Value |
|--------|-------|
| `SERVER_HOST` | `192.168.1.172` |
| `SERVER_USER` | `kofiarcher` |
| `SERVER_PORT` | `64295` |
| `SSH_PRIVATE_KEY` | [Content of `~/.ssh/id_rsa`] |

---

## Step 4: Test Auto-Deployment

Make a test commit:
```bash
echo "# Auto-deploy test" >> README.md
git add README.md
git commit -m "test: verify auto-deployment"
git push origin main
```

Then:
1. Go to: https://github.com/Kofiacheampong/studybuddy/actions
2. Watch the workflow run
3. If successful, deployment happens automatically
4. Check your app: `http://192.168.1.172`

---

## Step 5: Access Your App

Once deployed:

### From Your Network
```
http://192.168.1.172
```

### From Outside Your Network
You'll need to:
1. Port forward 192.168.1.172:80 on your router to the outside
2. Get your external IP
3. Access via `http://your-external-ip`

Or use a domain name (requires DNS setup)

---

## Verify Deployment

### Check if Service is Running
```bash
ssh -p 64295 kofiarcher@192.168.1.172 "sudo systemctl status study-buddy"
```

### View Recent Logs
```bash
ssh -p 64295 kofiarcher@192.168.1.172 "sudo journalctl -u study-buddy -n 20"
```

### Check Nginx Config
```bash
ssh -p 64295 kofiarcher@192.168.1.172 "sudo nginx -t"
```

### Restart Application
```bash
ssh -p 64295 kofiarcher@192.168.1.172 "sudo systemctl restart study-buddy"
```

---

## Manual Deployment (Without CI/CD)

If you want to deploy without GitHub Secrets:

```bash
# 1. SSH to server
ssh -p 64295 kofiarcher@192.168.1.172

# 2. Navigate to app directory
cd /var/www/study-buddy

# 3. Pull latest code
git pull origin main

# 4. Activate virtualenv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Restart app
sudo systemctl restart study-buddy

# 7. Check status
sudo systemctl status study-buddy
```

---

## Troubleshooting

### Deployment Job Fails
1. Check SSH secrets are correct
2. Verify SSH access works: `ssh -p 64295 kofiarcher@192.168.1.172`
3. Check `/var/www/study-buddy` exists on server
4. View GitHub Actions logs for error messages

### App Won't Start
1. Check logs: `sudo journalctl -u study-buddy -n 50`
2. Verify dependencies: `pip install -r requirements.txt`
3. Check database: `ls -la /var/www/study-buddy/data/`

### Port Already in Use
1. Check what's running on port 80: `sudo netstat -tlnp | grep 80`
2. If nginx is old: `sudo systemctl restart nginx`
3. Choose different port in deploy.sh

### Can't Access from Outside Network
1. Check your router port forwarding settings
2. Verify external firewall allows traffic
3. Use domain name instead of IP (more reliable)

---

## What Gets Auto-Deployed

When you push to main:
1. **Tests run** on GitHub (Python 3.10/3.11/3.12)
2. **Linting checks** (code quality)
3. **Security scan** (vulnerabilities)
4. **If all pass** → Automatic deployment:
   - SSH to 192.168.1.172
   - `cd /var/www/study-buddy`
   - `git pull origin main`
   - `pip install -r requirements.txt`
   - `sudo systemctl restart study-buddy`
   - App is live ✅

---

## Next Steps

1. **Verify SSH access**: `ssh -p 64295 kofiarcher@192.168.1.172`
2. **Run deployment**: `./deploy.sh`
3. **Add GitHub Secrets** (see Step 3)
4. **Make test commit** to verify auto-deployment
5. **Access your app**: `http://192.168.1.172`

---

## Questions?

- **Can't SSH?** → Check SSH key and port settings
- **Deploy script fails?** → Run it manually to see errors
- **Auto-deploy not working?** → Check GitHub Actions logs
- **App not starting?** → Check service logs with journalctl

Good luck! 🚀
