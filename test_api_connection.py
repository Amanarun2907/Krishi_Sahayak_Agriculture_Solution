#!/usr/bin/env python3
"""
Test script to verify Groq API connection is working
Run this to test if the API connection fix is successful
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_connection():
    """Test if Groq API connection works"""
    
    print("=" * 60)
    print("🧪 Testing Groq API Connection")
    print("=" * 60)
    
    # Step 1: Check API key
    print("\n1️⃣ Checking API Key...")
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment")
        print("💡 Create a .env file with: GROQ_API_KEY=your_key_here")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Step 2: Test httpx import
    print("\n2️⃣ Testing httpx import...")
    try:
        import httpx
        print(f"✅ httpx version: {httpx.__version__}")
    except ImportError:
        print("❌ httpx not installed")
        print("💡 Run: pip install httpx")
        return False
    
    # Step 3: Test Groq import
    print("\n3️⃣ Testing Groq import...")
    try:
        from groq import Groq
        print("✅ Groq library imported successfully")
    except ImportError:
        print("❌ groq not installed")
        print("💡 Run: pip install groq")
        return False
    
    # Step 4: Test connection
    print("\n4️⃣ Testing API connection...")
    try:
        # Create HTTP client with fixed configuration
        http_client = httpx.Client(
            timeout=60.0,
            follow_redirects=True,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        # Initialize Groq client
        client = Groq(api_key=api_key, http_client=http_client)
        
        print("✅ Client initialized successfully")
        
        # Step 5: Test API call
        print("\n5️⃣ Testing API call...")
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": "Say 'Hello from Krishi Sahayak!' in one sentence."}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        # Step 6: Test with agricultural context
        print("\n6️⃣ Testing agricultural query...")
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an agricultural expert."},
                {"role": "user", "content": "What is nitrogen deficiency in crops? Answer in one sentence."}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        print(f"✅ Agricultural Response: {result}")
        
        print("\n" + "=" * 60)
        print("🎉 All tests passed! API connection is working!")
        print("=" * 60)
        return True
        
    except httpx.ConnectError as e:
        print(f"❌ Connection Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Check your internet connection")
        print("   - Check if you're behind a proxy")
        print("   - Try: export HTTP_PROXY=http://proxy:port")
        return False
        
    except httpx.TimeoutException as e:
        print(f"❌ Timeout Error: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Check your internet speed")
        print("   - Try again in a moment")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Error type: {type(e).__name__}")
        
        error_msg = str(e).lower()
        if "api key" in error_msg or "401" in error_msg:
            print("\n💡 Troubleshooting:")
            print("   - Check if your API key is valid")
            print("   - Get a new key from: https://console.groq.com")
        elif "rate limit" in error_msg or "429" in error_msg:
            print("\n💡 Troubleshooting:")
            print("   - You've hit the rate limit")
            print("   - Wait a few minutes and try again")
        
        return False

if __name__ == "__main__":
    print("\n🌾 Krishi Sahayak - API Connection Test\n")
    
    success = test_api_connection()
    
    if success:
        print("\n✅ Your chatbots should now work properly!")
        print("🚀 Run: streamlit run app.py")
        sys.exit(0)
    else:
        print("\n❌ Please fix the issues above and try again")
        sys.exit(1)
