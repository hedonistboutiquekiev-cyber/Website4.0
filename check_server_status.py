#!/usr/bin/env python3
"""
Check for potential model-viewer issues on production server
"""

import os
import subprocess
import sys

def check_server_cors():
    """Check if server has CORS headers configured"""
    try:
        # Try to check CORS headers
        result = subprocess.run(
            ['curl', '-I', 'https://albaspace.com.tr/assets/models/imece.glb'],
            capture_output=True,
            timeout=10,
            text=True
        )
        
        print("=== CORS Headers Check ===")
        print(result.stdout)
        
        # Check for critical headers
        if 'Access-Control-Allow-Origin' in result.stdout:
            print("✓ CORS headers found")
        else:
            print("⚠ No CORS headers detected (may be needed for GL resources)")
            
    except Exception as e:
        print(f"⚠ Could not check server CORS: {e}")


def check_model_viewer_cdn():
    """Verify CDN is accessible"""
    try:
        result = subprocess.run(
            ['curl', '-I', 'https://ajax.googleapis.com/ajax/libs/model-viewer/3.0.0/model-viewer.min.js'],
            capture_output=True,
            timeout=10,
            text=True
        )
        
        print("\n=== CDN Accessibility ===")
        if '200' in result.stdout or '304' in result.stdout:
            print("✓ Google CDN is accessible")
        else:
            print("✗ Google CDN may have issues:")
            print(result.stdout[:200])
            
    except Exception as e:
        print(f"⚠ Could not check CDN: {e}")


def check_page_on_server():
    """Check the actual HTTP page"""
    try:
        result = subprocess.run(
            ['curl', '-s', 'https://albaspace.com.tr/imece/', '--head'],
            capture_output=True,
            timeout=10,
            text=True
        )
        
        print("\n=== Page Server Check ===")
        if '200' in result.stdout:
            print("✓ Page is accessible (HTTP 200)")
        else:
            print("Page status check result:")
            print(result.stdout[:300])
            
    except Exception as e:
        print(f"⚠ Could not check page: {e}")


if __name__ == '__main__':
    print("Checking model-viewer / 3D display issues...\n")
    check_server_cors()
    check_model_viewer_cdn()
    check_page_on_server()
    
    print("\n=== Summary ===")
    print("If 3D models still not showing:")
    print("1. Check browser console (F12 → Console tab)")
    print("2. Look for CORS errors or network failures")
    print("3. Check if model-viewer custom element loaded")
    print("4. Verify GLB file downloads successfully")
