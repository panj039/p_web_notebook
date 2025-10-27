#!/usr/bin/env python3
"""
P_Web_NoteBook - Personal Knowledge Base
Main entry point for the application
"""

import sys
from pathlib import Path

# Add current directory to Python path for app imports
sys.path.insert(0, str(Path(__file__).parent))

from app.server import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)