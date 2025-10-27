"""
Configuration settings for P_Web_NoteBook
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add util to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))
from util.paths import (
    get_project_root, get_config_dir, get_data_dir, 
    get_templates_dir, get_static_dir, get_users_config_file
)

# Load environment variables from .env file
project_root = Path(__file__).parent.parent
env_file = project_root / '.env'
if env_file.exists():
    load_dotenv(env_file)

# Base directories using unified path management
BASE_DIR = get_project_root()
CONFIG_DIR = get_config_dir()
DATA_DIR = get_data_dir()
TEMPLATES_DIR = get_templates_dir()
STATIC_DIR = get_static_dir()

# Application settings
APP_NAME = os.getenv("APP_NAME", "P_Web_NoteBook")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Personal Knowledge Base")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", None)  # Will be generated if None
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))

# File settings
ALLOWED_EXTENSIONS = {'.txt', '.md', '.markdown'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Security settings
SESSION_TIMEOUT = 24 * 60 * 60  # 24 hours in seconds
TOTP_VALIDITY_WINDOW = 1  # Allow 1 step window for TOTP

# Users configuration file
USERS_CONFIG_FILE = get_users_config_file()