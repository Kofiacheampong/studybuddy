# OCI Study Buddy - Production Deployment Guide

This guide will help you deploy the OCI Study Buddy application to your Ubuntu server.

## Prerequisites

- Ubuntu server with SSH access
- Domain name or subdomain pointing to your server
- Root or sudo access on the server

## Quick Deployment

### 1. Configure Deployment Settings

Edit the configuration variables in `deploy.sh`:

```bash
# Configuration - EDIT THESE VALUES
SERVER_USER="your_username"           # Your SSH username
SERVER_HOST="your.server.ip"          # Your server IP address
SERVER_PORT="22"                      # SSH port (usually 22)
APP_NAME="oci-study-buddy"            # App name (used for directories)
DOMAIN_NAME="study.yourdomain.com"    # Your domain/subdomain
APP_PORT="5001"                       # Unique port for this app
```

### 2. Run Deployment

```bash
./deploy.sh
```

The script will:
- Test SSH connection
- Create deployment package
- Upload files to server
- Install dependencies (Python, nginx, etc.)
- Configure systemd service
- Set up nginx reverse proxy
- Start the application

### 3. Set up SSL (Recommended)

After deployment, secure your app with Let's Encrypt:

```bash
ssh your_username@your.server.ip
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d study.yourdomain.com
```

## Architecture

The deployment sets up:

- **Flask App**: Runs on `127.0.0.1:5001` (or your chosen port)
- **Gunicorn**: Production WSGI server with 2 workers
- **Nginx**: Reverse proxy handling public traffic
- **Systemd**: Service management and auto-restart
- **Database**: SQLite stored in `/var/www/oci-study-buddy/data/`

## File Structure on Server

```
/var/www/oci-study-buddy/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
├── static/               # CSS, JS, images
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── venv/                 # Python virtual environment
└── data/                 # Database and uploads
    └── oci_study.db      # SQLite database
```

## Management Commands

### Check Application Status
```bash
ssh your_username@your.server.ip 'sudo systemctl status oci-study-buddy'
```

### View Application Logs
```bash
ssh your_username@your.server.ip 'sudo journalctl -u oci-study-buddy -f'
```

### Restart Application
```bash
ssh your_username@your.server.ip 'sudo systemctl restart oci-study-buddy'
```

### Update Application Code

For quick updates without full redeployment:

```bash
./update-app.sh
```

This script:
- Uploads only changed files
- Installs new dependencies
- Restarts the service
- Much faster than full deployment

## Nginx Configuration

The nginx configuration includes:

- **Reverse Proxy**: Routes traffic to Flask app
- **Static Files**: Serves CSS/JS directly for better performance  
- **Security Headers**: Basic security improvements
- **Gzip Compression**: Reduces bandwidth usage
- **Health Checks**: Monitoring endpoint

## Systemd Service

The systemd service configuration provides:

- **Auto-restart**: Restarts if the app crashes
- **Process Management**: Proper signal handling
- **Resource Limits**: Memory and timeout controls
- **Security**: Runs with limited privileges

## Troubleshooting

### Service Won't Start

Check logs:
```bash
sudo journalctl -u oci-study-buddy --lines=50
```

Common issues:
- Missing `.env` file with `ANTHROPIC_API_KEY`
- Port already in use
- Permission issues with database directory

### Nginx Errors

Test nginx configuration:
```bash
sudo nginx -t
```

Check nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

### Database Issues

Ensure database directory has proper permissions:
```bash
sudo chown -R your_username:your_username /var/www/oci-study-buddy/data/
chmod 755 /var/www/oci-study-buddy/data/
```

### Port Conflicts

If the chosen port is already in use, update both:
1. `APP_PORT` in `deploy.sh`
2. Re-run deployment

### SSL Certificate Issues

Renew certificates:
```bash
sudo certbot renew --dry-run
```

## Security Considerations

1. **Firewall**: Ensure only necessary ports (80, 443, SSH) are open
2. **SSH Keys**: Use SSH keys instead of passwords
3. **Regular Updates**: Keep server and dependencies updated
4. **Monitoring**: Set up log monitoring for unusual activity
5. **Backups**: Regular database backups

## Monitoring and Maintenance

### Database Backup

Create a backup script:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /var/www/oci-study-buddy/data/oci_study.db \
   /var/www/oci-study-buddy/backups/oci_study_${DATE}.db
```

### Log Rotation

Logs are automatically rotated by systemd, but you can check:
```bash
sudo journalctl --disk-usage
sudo journalctl --vacuum-time=30d  # Keep only 30 days
```

### Performance Monitoring

Monitor resource usage:
```bash
htop
sudo systemctl status oci-study-buddy
```

## Environment Variables

Required in `.env` file:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Optional production variables:
```
FLASK_ENV=production
DATABASE_PATH=/var/www/oci-study-buddy/data/oci_study.db
```

## Multiple App Deployment

To deploy multiple apps on the same server:

1. Use different `APP_NAME` and `APP_PORT` for each
2. Use different `DOMAIN_NAME` or subdomains
3. Each app gets its own systemd service and nginx site

Example for second app:
```bash
APP_NAME="app2-name"
APP_PORT="5002"
DOMAIN_NAME="app2.yourdomain.com"
```

This deployment setup is production-ready and handles multiple applications gracefully on the same server.