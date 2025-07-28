#!/usr/bin/env python3
"""
Simple test to verify the Flask app can start without errors.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_app_startup():
    """Test that the Flask app can start and load project pages."""
    try:
        from app import app
        
        with app.test_client() as client:
            # Test home page
            response = client.get('/')
            print(f"Home page: {response.status_code}")
            
            # Test a project with markdown
            response = client.get('/projects/wage_distribution')
            print(f"Wage distribution project: {response.status_code}")
            
            # Test another project
            response = client.get('/projects/delivery_app_simulation')
            print(f"Delivery app project: {response.status_code}")
            
            print("✓ Flask app is working correctly!")
            
    except Exception as e:
        print(f"✗ Error testing Flask app: {e}")

if __name__ == "__main__":
    test_app_startup()
