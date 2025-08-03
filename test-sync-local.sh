#!/bin/bash

# 🚀 Local Sync Test Script
# This script allows you to test the sync logic locally before running in GitHub Actions

set -e  # Exit on any error

# Configuration (adjust these for your setup)
SOURCE_REPO="DYAI2025/_1-_MEWT-backend"
DEPLOY_REPO="DYAI2025/ME_CORE_Backend-mar-spar"
SOURCE_BRANCH="main"
DEPLOY_BRANCH="main"
TEST_DIR="/tmp/sync-test-$(date +%s)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up test directory..."
    rm -rf "$TEST_DIR"
}

# Set trap for cleanup
trap cleanup EXIT

main() {
    log_info "🚀 Starting local sync test..."
    log_info "Test directory: $TEST_DIR"
    
    # Create test directory
    mkdir -p "$TEST_DIR"
    cd "$TEST_DIR"
    
    # Step 1: Clone source repository
    log_info "📥 Cloning source repository: $SOURCE_REPO"
    if git clone "https://github.com/$SOURCE_REPO.git" source-repo; then
        log_success "Source repository cloned successfully"
    else
        log_error "Failed to clone source repository"
        exit 1
    fi
    
    cd source-repo
    git checkout "$SOURCE_BRANCH"
    SOURCE_COMMIT=$(git rev-parse HEAD)
    SOURCE_COMMIT_MSG=$(git log -1 --pretty=format:"%s")
    log_info "Source commit: $SOURCE_COMMIT"
    log_info "Latest commit message: $SOURCE_COMMIT_MSG"
    cd ..
    
    # Step 2: Clone deploy repository (read-only test)
    log_info "📥 Cloning deploy repository: $DEPLOY_REPO"
    if git clone "https://github.com/$DEPLOY_REPO.git" deploy-repo; then
        log_success "Deploy repository cloned successfully"
    else
        log_error "Failed to clone deploy repository"
        exit 1
    fi
    
    cd deploy-repo
    git checkout "$DEPLOY_BRANCH"
    DEPLOY_COMMIT=$(git rev-parse HEAD)
    log_info "Deploy commit: $DEPLOY_COMMIT"
    cd ..
    
    # Step 3: Test sync operation
    log_info "🔄 Testing file synchronization..."
    
    # Backup original deploy state
    cp -r deploy-repo deploy-repo-backup
    
    # Perform sync with same exclusions as workflow
    rsync -av --delete \
        --exclude='.git' \
        --exclude='.github' \
        --exclude='node_modules' \
        --exclude='.env*' \
        --exclude='*.log' \
        --exclude='.DS_Store' \
        --exclude='Thumbs.db' \
        --exclude='.vscode' \
        --exclude='.idea' \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='dist' \
        --exclude='build' \
        source-repo/ deploy-repo/
    
    log_success "Sync operation completed"
    
    # Step 4: Check for changes
    cd deploy-repo
    
    if git diff --quiet && git diff --cached --quiet; then
        log_info "No changes detected - repositories are already in sync"
        CHANGES_DETECTED=false
    else
        log_warning "Changes detected!"
        CHANGES_DETECTED=true
        
        echo
        log_info "📋 Summary of changes:"
        git status --porcelain | head -20
        
        if [ $(git status --porcelain | wc -l) -gt 20 ]; then
            log_warning "... and $(( $(git status --porcelain | wc -l) - 20 )) more files"
        fi
        
        echo
        log_info "📊 Statistics:"
        ADDED=$(git status --porcelain | grep '^A' | wc -l)
        MODIFIED=$(git status --porcelain | grep '^.M' | wc -l)
        DELETED=$(git status --porcelain | grep '^.D' | wc -l)
        UNTRACKED=$(git status --porcelain | grep '^??' | wc -l)
        
        echo "  • Added files: $ADDED"
        echo "  • Modified files: $MODIFIED"
        echo "  • Deleted files: $DELETED"
        echo "  • Untracked files: $UNTRACKED"
    fi
    
    cd ..
    
    # Step 5: Generate report
    echo
    log_info "📊 Test Summary Report"
    echo "================================"
    echo "Source Repository: $SOURCE_REPO"
    echo "Deploy Repository: $DEPLOY_REPO"
    echo "Source Branch: $SOURCE_BRANCH"
    echo "Deploy Branch: $DEPLOY_BRANCH"
    echo "Source Commit: $SOURCE_COMMIT"
    echo "Deploy Commit: $DEPLOY_COMMIT"
    echo "Changes Detected: $CHANGES_DETECTED"
    echo "Test Directory: $TEST_DIR"
    echo "Timestamp: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    
    if [ "$CHANGES_DETECTED" = true ]; then
        echo
        log_warning "⚠️  Changes would be synchronized in the actual workflow"
        log_info "Review the changes above to ensure they are expected"
    else
        echo
        log_success "✅ No sync needed - repositories are already synchronized"
    fi
    
    echo
    log_info "🔍 To inspect changes in detail, navigate to:"
    echo "   cd $TEST_DIR/deploy-repo"
    echo "   git diff"
    echo
    log_info "💡 This test was read-only. No changes were pushed to the actual repositories."
}

# Check if rsync is available
if ! command -v rsync &> /dev/null; then
    log_error "rsync is required but not installed. Please install rsync first."
    exit 1
fi

# Check if git is available
if ! command -v git &> /dev/null; then
    log_error "git is required but not installed. Please install git first."
    exit 1
fi

# Run main function
main "$@"