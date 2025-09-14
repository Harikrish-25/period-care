#!/usr/bin/env python3
"""
Simple server startup script for Period Care Backend
"""
import uvicorn
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    print("🚀 Starting Period Care Backend Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    print("-" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=[str(current_dir)],
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Installed all dependencies: pip install -r requirements.txt")
        print("  2. Firebase credentials configured (optional for basic testing)")
        sys.exit(1)

if __name__ == "__main__":
    main()