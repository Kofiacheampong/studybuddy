#!/bin/bash

# Quick update script for when you make changes
# This script only updates the code without full redeployment

set -e

# Configuration - EDIT THESE VALUES (should match deploy.sh)
SERVER_USER="kofiarcher"
SERVER_HOST="192.168.1.172"
SERVER_PORT="64295"
APP_NAME="oci-study-buddy"
SERVICE_NAME="${APP_NAME}"

# Local and remote paths
LOCAL_DIR="$(pwd)"
REMOTE_DIR="/var/www/${APP_NAME}"

echo "🔄 Updating OCI Study Buddy application..."

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Create update package (exclude database and large files)
print_status "Creating update package..."
tar --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='oci_study.db' \
    --exclude='data/' \
    --exclude='venv/' \
    -czf /tmp/${APP_NAME}-update.tar.gz \
    -C "$LOCAL_DIR" .

# Upload and update
print_status "Uploading changes..."
scp -P $SERVER_PORT /tmp/${APP_NAME}-update.tar.gz $SERVER_USER@$SERVER_HOST:/tmp/

print_status "Applying updates on server..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST << EOF
set -e

cd $REMOTE_DIR
print_status() {
    echo -e "\033[0;32m[REMOTE]\033[0m \$1"
}

print_status "Backing up current version..."
sudo systemctl stop ${SERVICE_NAME}

print_status "Extracting updates..."
tar -xzf /tmp/${APP_NAME}-update.tar.gz
rm /tmp/${APP_NAME}-update.tar.gz

print_status "Installing any new dependencies..."
source venv/bin/activate
pip install -r requirements.txt

print_status "Restarting service..."
sudo systemctl start ${SERVICE_NAME}
sudo systemctl reload nginx

# Check if service started successfully
sleep 2
if sudo systemctl is-active --quiet ${SERVICE_NAME}; then
    print_status "✅ Update completed successfully!"
else
    print_status "❌ Service failed to start. Check logs:"
    sudo journalctl -u ${SERVICE_NAME} --lines=10
fi

EOF

# Cleanup
rm /tmp/${APP_NAME}-update.tar.gz

print_status "🎉 Update completed!"