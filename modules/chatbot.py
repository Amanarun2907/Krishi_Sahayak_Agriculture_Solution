import streamlit as st
from groq import Groq
from config import CHATBOT_PROMPTS, GROQ_API_KEY
import time
import os
import httpx
import json
import random
from datetime import datetime
from modules.enhanced_chatbot import create_chat_interface

def get_chatbot_response(user_query, sector_name, analysis_result=None):
    """
    Enhanced chatbot response function with better error handling
    """
    try:
        # Create HTTP client with proper configuration
        http_client = httpx.Client(
            trust_env=False, 
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY, http_client=http_client)
        
        # Get system prompt
        system_prompt = CHATBOT_PROMPTS.get(sector_name, "You are a helpful agricultural assistant.")
        
        # Prepare user message with context
        if analysis_result:
            context = f"Based on the image analysis: {analysis_result}\n\n"
            user_query = context + "Question: " + user_query
        
        # Create chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            stream=False,
            max_tokens=1000
        )
        
        response = chat_completion.choices[0].message.content
        return response
        
    except Exception as e:
        # Enhanced error handling with fallback response
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            return """🔑 **API Key Issue Detected**

It seems there's an issue with the API key configuration. Please check:

1. **API Key Setup**: Ensure your Groq API key is properly configured
2. **Key Validity**: Verify the API key is active and has sufficient credits
3. **Network Access**: Check your internet connection

**Fallback Response**: While we resolve this, here's some general advice:
- For crop health issues, check soil pH and nutrient levels
- For pest problems, consider Integrated Pest Management (IPM)
- For weed control, timing of herbicide application is crucial
- For irrigation, monitor soil moisture levels regularly

Please contact support if the issue persists."""
        
        elif "timeout" in error_msg.lower():
            return """⏱️ **Connection Timeout**

The chatbot service is taking longer than expected to respond. This could be due to:

1. **Network Issues**: Check your internet connection
2. **Server Load**: The service might be experiencing high traffic
3. **Query Complexity**: Try breaking down your question into smaller parts

**Please try again in a moment.** If the issue continues, consider rephrasing your question or contacting support."""
        
        else:
            return f"""⚠️ **Service Temporarily Unavailable**

I'm experiencing technical difficulties: {error_msg}

**What you can do:**
1. Try rephrasing your question
2. Check your internet connection
3. Try again in a few minutes

**Emergency Agricultural Advice:**
- For urgent crop health issues, contact your local agricultural extension officer
- For pest emergencies, consult with a local agricultural expert
- For irrigation problems, check soil moisture and weather conditions

I apologize for the inconvenience and will be back online shortly."""

def display_chat_interface(sector_name, analysis_result=None, unique_key=None):
    """
    Enhanced chat interface with better styling and functionality
    """
    # Use the enhanced chat interface
    create_chat_interface(sector_name, analysis_result, use_api=True, unique_key=unique_key)

def display_foundational_chat_interface(sector_name, analysis_result=None, unique_key=None):
    """
    Display foundational chatbot interface (no API required)
    """
    # Use the enhanced chat interface in foundational mode
    create_chat_interface(sector_name, analysis_result, use_api=False, unique_key=unique_key)

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.title("Enhanced Chatbot Module Test")
    
    # Test both API and foundational chatbots
    test_mode = st.sidebar.selectbox("Select Chatbot Mode", ["API-Powered", "Foundational AI"])
    test_sector = st.sidebar.selectbox("Select Sector", list(CHATBOT_PROMPTS.keys()))
    
    if test_mode == "API-Powered":
        display_chat_interface(test_sector)
    else:
        display_foundational_chat_interface(test_sector)