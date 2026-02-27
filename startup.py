"""
Startup file for Azure App Service
"""
import uvicorn
import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app import app
    print("✅ App imported successfully")
except ImportError as e:
    print(f"❌ Error importing app: {e}")
    sys.exit(1)

if __name__ == "__main__":
    # Azure App Service uses PORT environment variable
    port = int(os.environ.get("PORT", os.environ.get("SERVER_PORT", 8000)))
    
    print(f"🚀 Starting server on port {port}")
    print(f"📱 App will be available at: http://0.0.0.0:{port}")
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info",
        access_log=True,
        reload=False  # Disable reload in production
    )