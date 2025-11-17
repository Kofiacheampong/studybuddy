#!/bin/bash

# OCI Study Buddy Deployment Script
# This script deploys the Flask app to your Ubuntu server

set -e  # Exit on any error

# Configuration - EDIT THESE VALUES
SERVER_USER="kofiarcher"  # Your SSH username
SERVER_HOST="192.168.1.172"  # Your server's IP address or hostname
SERVER_PORT="64295"
APP_NAME="oci-study-buddy"
DOMAIN_NAME="192.168.1.172"  # Using IP for now, change to domain if you have one
APP_PORT="5001"  # Port for this app (make sure it's unique on your server)

# Local and remote paths
LOCAL_DIR="$(pwd)"
REMOTE_DIR="/var/www/${APP_NAME}"
SERVICE_NAME="${APP_NAME}"

echo "🚀 Starting deployment of OCI Study Buddy..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found! Please create it with your ANTHROPIC_API_KEY"
    exit 1
fi

# Check SSH connection
print_status "Testing SSH connection..."
if ! ssh -p $SERVER_PORT -o ConnectTimeout=10 -o BatchMode=yes $SERVER_USER@$SERVER_HOST exit 2>/dev/null; then
    print_error "Cannot connect to server. Please check your SSH configuration."
    exit 1
fi

print_status "✅ SSH connection successful"

# Create deployment package
print_status "Creating deployment package..."
tar --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='oci_study.db' \
    -czf /tmp/${APP_NAME}-deploy.tar.gz \
    -C "$LOCAL_DIR" .

print_status "✅ Deployment package created"

# Upload files to server
print_status "Uploading files to server..."
scp -P $SERVER_PORT /tmp/${APP_NAME}-deploy.tar.gz $SERVER_USER@$SERVER_HOST:/tmp/

# Execute deployment on server
print_status "Executing deployment on server..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST << EOF
set -e

# Colors for remote output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "\${GREEN}[REMOTE]${NC} \$1"
}

print_status "Starting server-side deployment..."

# Create application directory
sudo mkdir -p $REMOTE_DIR
sudo chown $SERVER_USER:$SERVER_USER $REMOTE_DIR

# Extract files
cd $REMOTE_DIR
print_status "Extracting application files..."
tar -xzf /tmp/${APP_NAME}-deploy.tar.gz
rm /tmp/${APP_NAME}-deploy.tar.gz

# Install system dependencies if needed
print_status "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nginx

# Create virtual environment
print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server

# Create systemd service file
print_status "Creating systemd service..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null << EOL
[Unit]
Description=OCI Study Buddy Flask App
After=network.target

[Service]
Type=notify
User=$SERVER_USER
Group=$SERVER_USER
WorkingDirectory=$REMOTE_DIR
Environment=PATH=$REMOTE_DIR/venv/bin
ExecStart=$REMOTE_DIR/venv/bin/gunicorn --bind 127.0.0.1:$APP_PORT --workers 2 --timeout 60 --keep-alive 5 --max-requests 1000 --preload app:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Create nginx configuration
print_status "Creating nginx configuration..."
sudo tee /etc/nginx/sites-available/${APP_NAME} > /dev/null << EOL
server {
    listen 80;
    server_name $DOMAIN_NAME;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # Static files
    location /static {
        alias $REMOTE_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Main application
    location / {
        proxy_pass http://127.0.0.1:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:$APP_PORT/;
        access_log off;
    }
}
EOL

# Enable nginx site
sudo ln -sf /etc/nginx/sites-available/${APP_NAME} /etc/nginx/sites-enabled/
sudo nginx -t  # Test nginx configuration

# Set up database directory with proper permissions
mkdir -p $REMOTE_DIR/data
chmod 755 $REMOTE_DIR/data

# Reload systemd and start services
print_status "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl restart ${SERVICE_NAME}
sudo systemctl reload nginx

# Check service status
sleep 3
if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
    print_status "✅ ${SERVICE_NAME} service is running"
else
    echo -e "\${RED}❌ Service failed to start. Checking logs...${NC}"
    sudo systemctl status ${SERVICE_NAME}
    sudo journalctl -u ${SERVICE_NAME} --lines=20
    exit 1
fi

print_status "✅ Deployment completed successfully!"
print_status "Your app should be available at: http://$DOMAIN_NAME"
print_status "To check logs: sudo journalctl -u ${SERVICE_NAME} -f"
print_status "To restart: sudo systemctl restart ${SERVICE_NAME}"

EOF

# Cleanup local temp files
rm /tmp/${APP_NAME}-deploy.tar.gz

print_status "🎉 Deployment completed!"
print_status ""
print_status "Next steps:"
print_status "1. Point your domain '$DOMAIN_NAME' to your server IP"
print_status "2. Consider setting up SSL with Let's Encrypt:"
print_status "   sudo apt install certbot python3-certbot-nginx"
print_status "   sudo certbot --nginx -d $DOMAIN_NAME"
print_status ""
print_status "Useful commands:"
print_status "- Check app status: ssh $SERVER_USER@$SERVER_HOST 'sudo systemctl status $SERVICE_NAME'"
print_status "- View logs: ssh $SERVER_USER@$SERVER_HOST 'sudo journalctl -u $SERVICE_NAME -f'"
print_status "- Restart app: ssh $SERVER_USER@$SERVER_HOST 'sudo systemctl restart $SERVICE_NAME'"