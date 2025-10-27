#!/usr/bin/env python3
"""
Quick start script for P_Web_NoteBook
This script provides easy commands to run the application
"""

import sys
import subprocess
from pathlib import Path

def run_dev():
    """Run in development mode"""
    print("🚀 Starting P_Web_NoteBook in development mode...")
    subprocess.run([sys.executable, "main.py"])

def run_docker():
    """Run with Docker"""
    print("🐳 Starting P_Web_NoteBook with Docker...")
    subprocess.run(["docker-compose", "up", "-d"], cwd="docker")

def stop_docker():
    """Stop Docker containers"""
    print("🛑 Stopping Docker containers...")
    subprocess.run(["docker-compose", "down"], cwd="docker")

def show_help():
    """Show help information"""
    print("""
P_Web_NoteBook - Quick Start

Usage:
    python start.py [command]

Commands:
    dev         Run in development mode (default)
    docker      Start with Docker
    stop        Stop Docker containers
    help        Show this help message

Examples:
    python start.py            # Run in development mode
    python start.py dev        # Run in development mode
    python start.py docker     # Start with Docker
    python start.py stop       # Stop Docker containers

Default login:
    Username: admin
    Password: hello
    TOTP: Use secret 'JBSWY3DPEHPK3PXP' in Google Authenticator
    """)

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "dev":
        run_dev()
    elif sys.argv[1] == "docker":
        run_docker()
    elif sys.argv[1] == "stop":
        stop_docker()
    elif sys.argv[1] == "help":
        show_help()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        show_help()