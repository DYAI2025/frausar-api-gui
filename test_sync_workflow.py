#!/usr/bin/env python3
"""
Test suite for the Auto-Sync Workflow
Tests workflow file structure and configuration validity
"""

import yaml
import os
import pytest
from pathlib import Path

def test_workflow_file_exists():
    """Test that the workflow file exists"""
    workflow_path = Path('.github/workflows/sync-to-deploy.yml')
    assert workflow_path.exists(), "Workflow file should exist"

def test_workflow_yaml_valid():
    """Test that the workflow YAML is valid"""
    workflow_path = Path('.github/workflows/sync-to-deploy.yml')
    
    with open(workflow_path, 'r') as f:
        try:
            workflow_data = yaml.safe_load(f)
            assert workflow_data is not None, "Workflow YAML should be parseable"
        except yaml.YAMLError as e:
            pytest.fail(f"Workflow YAML is invalid: {e}")

def test_workflow_structure():
    """Test that the workflow has required structure"""
    workflow_path = Path('.github/workflows/sync-to-deploy.yml')
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    # Test basic structure
    assert 'name' in workflow, "Workflow should have a name"
    # 'on' becomes True when parsed by YAML, so check for it as boolean or string
    assert ('on' in workflow) or (True in workflow), "Workflow should have triggers"
    assert 'jobs' in workflow, "Workflow should have jobs"
    
    # Test triggers - handle both 'on' and True key
    triggers = workflow.get('on', workflow.get(True, {}))
    assert 'push' in triggers, "Should trigger on push"
    assert 'workflow_dispatch' in triggers, "Should allow manual trigger"
    assert 'schedule' in triggers, "Should have scheduled trigger"

def test_workflow_environment_variables():
    """Test that required environment variables are defined"""
    workflow_path = Path('.github/workflows/sync-to-deploy.yml')
    
    with open(workflow_path, 'r') as f:
        workflow = yaml.safe_load(f)
    
    assert 'env' in workflow, "Workflow should define environment variables"
    
    env_vars = workflow['env']
    required_vars = ['SOURCE_REPO', 'DEPLOY_REPO', 'DEPLOY_BRANCH']
    
    for var in required_vars:
        assert var in env_vars, f"Environment variable {var} should be defined"

def test_sync_config_file_exists():
    """Test that sync configuration file exists"""
    config_path = Path('.github/sync-config.yml')
    assert config_path.exists(), "Sync config file should exist"

def test_sync_config_valid():
    """Test that sync configuration is valid YAML"""
    config_path = Path('.github/sync-config.yml')
    
    with open(config_path, 'r') as f:
        try:
            config_data = yaml.safe_load(f)
            assert config_data is not None, "Config YAML should be parseable"
        except yaml.YAMLError as e:
            pytest.fail(f"Config YAML is invalid: {e}")

def test_documentation_exists():
    """Test that workflow documentation exists"""
    docs_path = Path('SYNC_WORKFLOW_GUIDE.md')
    assert docs_path.exists(), "Workflow documentation should exist"

def test_test_script_exists():
    """Test that local test script exists and is executable"""
    script_path = Path('test-sync-local.sh')
    assert script_path.exists(), "Test script should exist"
    assert os.access(script_path, os.X_OK), "Test script should be executable"

def test_readme_updated():
    """Test that README mentions the sync workflow"""
    readme_path = Path('README.md')
    
    with open(readme_path, 'r') as f:
        readme_content = f.read()
    
    assert 'Auto-Sync Workflow' in readme_content, "README should mention the sync workflow"
    assert 'SYNC_WORKFLOW_GUIDE.md' in readme_content, "README should reference the guide"

if __name__ == '__main__':
    # Run tests when script is executed directly
    import subprocess
    result = subprocess.run(['python', '-m', 'pytest', __file__, '-v'], 
                          cwd=os.path.dirname(os.path.abspath(__file__)))
    exit(result.returncode)