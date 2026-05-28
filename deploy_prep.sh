#!/bin/bash
# LiversegAI Deployment Preparation Script
# This script packages the application securely for production deployment.
# It ensures sensitive files and development environments are NOT included in the final archive.

echo "Preparing LiversegAI for Production Deployment..."

RELEASE_DIR="liverseg_release"
RELEASE_ZIP="liverseg_production.zip"

# Clean previous build if it exists
rm -rf $RELEASE_DIR
rm -f $RELEASE_ZIP

# Create release directory
mkdir $RELEASE_DIR

# Copy all files except those matched by rsync excludes
# This explicitly ignores .env, .git, node_modules, and python venv
echo "Copying source files..."
rsync -av --progress ./ ./$RELEASE_DIR \
  --exclude node_modules \
  --exclude dist \
  --exclude .git \
  --exclude backend/venv \
  --exclude backend/__pycache__ \
  --exclude .env \
  --exclude .env.production \
  --exclude .DS_Store \
  --exclude liverseg_release \
  --exclude liverseg_production.zip

echo "Creating secure production zip..."
cd $RELEASE_DIR
zip -r ../$RELEASE_ZIP .
cd ..

# Cleanup temporary directory
rm -rf $RELEASE_DIR

echo "========================================================="
echo "✅ Deployment Package Ready: $RELEASE_ZIP"
echo "⚠️  REMINDER: Do NOT upload your .env files publicly."
echo "   You must create a secure .env file on your production server."
echo "========================================================="
