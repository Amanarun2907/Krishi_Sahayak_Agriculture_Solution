#!/usr/bin/env python3
"""
Quick test to verify .env file is being loaded correctly
"""

import os
from dotenv import load_dotenv

print("=" * 60)
print("Testing Environment Variable Loading")
print("=" * 60)

# Test 1: Load .env
print("\n1. Loading .env file...")
load_dotenv()
print("✅ load_dotenv() called")

# Test 2: Check if API key exists
print("\n2. Checking GROQ_API_KEY...")
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print(f"✅ API Key found!")
    print(f"   Length: {len(api_key)} characters")
    print(f"   Preview: {api_key[:10]}...{api_key[-4:]}")
    
    if api_key.strip() == "":
        print("⚠️  WARNING: API key is empty or whitespace only!")
    else:
        print("✅ API key has content")
else:
    print("❌ API Key NOT found!")
    print("\n💡 Troubleshooting:")
    print("   1. Check if .env file exists in project root")
    print("   2. Check if GROQ_API_KEY is set in .env")
    print("   3. Make sure there are no extra spaces")
    print("   4. Format should be: GROQ_API_KEY=your_key_here")

# Test 3: Import from config
print("\n3. Testing import from config.py...")
try:
    from config import GROQ_API_KEY as config_key
    
    if config_key:
        print(f"✅ Config loaded API key!")
        print(f"   Length: {len(config_key)} characters")
        print(f"   Preview: {config_key[:10]}...{config_key[-4:]}")
        
        if config_key == api_key:
            print("✅ Keys match!")
        else:
            print("⚠️  Keys don't match!")
    else:
        print("❌ Config API key is empty!")
except Exception as e:
    print(f"❌ Error importing config: {e}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
