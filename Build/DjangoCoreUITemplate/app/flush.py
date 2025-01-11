#!/usr/bin/env python

"""
Script to clear all Django sessions.
Run this script from the command line: python clear_sessions.py
"""

import os
import sys
import django
from datetime import datetime

def setup_django():
    """Setup Django environment"""
    # Add your project directory to the sys.path
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app'))
    sys.path.append(project_path)
    
    # Set the Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    
    # Initialize Django
    django.setup()

def clear_sessions():
    """Clear all sessions from the database"""
    from django.contrib.sessions.models import Session
    
    try:
        # Get current session count
        initial_count = Session.objects.count()
        
        # Delete all sessions
        Session.objects.all().delete()
        
        # Print results
        print(f"Session cleanup completed at {datetime.now()}")
        print(f"Deleted {initial_count} sessions")
        print("All sessions have been cleared successfully!")
        
    except Exception as e:
        print(f"Error clearing sessions: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Starting session cleanup...")
    
    # Setup Django environment
    try:
        setup_django()
    except Exception as e:
        print(f"Error setting up Django environment: {e}")
        sys.exit(1)
    
    # Clear sessions
    success = clear_sessions()
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)
