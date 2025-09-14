#!/usr/bin/env python3
"""
Test the simple_server imports and basic functionality
"""

try:
    from simple_server import app
    print("✅ Successfully imported app from simple_server")
    
    # Test the FastAPI app
    print(f"✅ App type: {type(app)}")
    print(f"✅ App routes: {len(app.routes)} routes found")
    
    # List routes
    for route in app.routes:
        if hasattr(route, 'path'):
            print(f"  - {route.path}")
            
except Exception as e:
    print(f"❌ Error importing: {e}")
    import traceback
    traceback.print_exc()