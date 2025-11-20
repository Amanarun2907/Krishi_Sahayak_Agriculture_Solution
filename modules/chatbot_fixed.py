# FIXED CHATBOT - Use this to replace the chat interface function in enhanced_chatbot.py

def create_chat_interface_fixed(sector_name: str, analysis_context: str = None, use_api: bool = True, unique_key: str = None):
    """
    FIXED: Create chat interface that doesn't reload the page
    """
    import streamlit as st
    from datetime import datetime
    import json
    
    # Initialize session state
    chat_key = f"chat_history_{sector_name}_{unique_key or 'default'}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    
    # Chatbot initialization
    if use_api:
        from config import GROQ_API_KEY
        chatbot_type = "API-Powered"
        chatbot_icon = "🤖"
    else:
        from modules.enhanced_chatbot import AdvancedFoundationalChatbot
        if f"foundational_chatbot_{sector_name}" not in st.session_state:
            st.session_state[f"foundational_chatbot_{sector_name}"] = AdvancedFoundationalChatbot()
        chatbot_type = "Foundational AI"
        chatbot_icon = "🧠"
    
    # Chat interface styling
    status_color = "#2E8B57" if "API" in chatbot_type else "#6C757D"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                border: 2px solid {status_color}; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <h3 style="color: {status_color}; margin-bottom: 1rem; text-align: center;">
            {chatbot_icon} Krishi Sahayak {chatbot_type} Assistant
        </h3>
        <p style="text-align: center; color: #666; margin-bottom: 1rem;">
            Specialized in {sector_name.replace('_', ' ').title()} - Ask me anything!
        </p>
        <p style="text-align: center; color: {status_color}; font-size: 0.9rem; margin: 0;">
            Status: 🟢 Ready | Messages: {len(st.session_state[chat_key])}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    if len(st.session_state[chat_key]) == 0:
        st.info("💬 No messages yet. Type a message below to get started!")
    else:
        for message in st.session_state[chat_key]:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                            padding: 1rem; border-radius: 15px; margin: 0.5rem 0; 
                            border-left: 4px solid #2196f3;">
                    <strong style="color: #0d47a1;">👤 You:</strong><br>
                    <span style="color: #2d2d2d;">{message['content']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f0fff0 0%, #c8e6c9 100%); 
                            padding: 1rem; border-radius: 15px; margin: 0.5rem 0; 
                            border-left: 4px solid #4caf50;">
                    <strong style="color: #1b5e20;">{chatbot_icon} Krishi Sahayak:</strong><br>
                    <div style="color: #2d2d2d; line-height: 1.6;">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input with callback
    def handle_submit():
        user_input = st.session_state.get(f"chat_input_{unique_key or sector_name}", "").strip()
        if not user_input:
            return
        
        # Add user message
        st.session_state[chat_key].append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now()
        })
        
        # Generate response
        try:
            if use_api:
                from config import CHATBOT_PROMPTS, GROQ_API_KEY
                import httpx
                from groq import Groq
                
                system_prompt = CHATBOT_PROMPTS.get(sector_name, "You are a helpful agricultural assistant.")
                http_client = httpx.Client(trust_env=False, timeout=30.0)
                client = Groq(api_key=GROQ_API_KEY, http_client=http_client)
                
                context_message = f"Analysis: {analysis_context}\n\nQuestion: {user_input}" if analysis_context else user_input
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context_message}
                    ],
                    model="llama-3.1-8b-instant",
                    temperature=0.7,
                    max_tokens=1500
                )
                
                response = chat_completion.choices[0].message.content
            else:
                from modules.enhanced_chatbot import AdvancedFoundationalChatbot
                if f"foundational_chatbot_{sector_name}" not in st.session_state:
                    st.session_state[f"foundational_chatbot_{sector_name}"] = AdvancedFoundationalChatbot()
                chatbot = st.session_state[f"foundational_chatbot_{sector_name}"]
                response = chatbot.generate_response(user_input)
        except Exception as e:
            response = f"Error: {str(e)}. Please try again."
        
        # Add response
        st.session_state[chat_key].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
        # Clear input
        st.session_state[f"chat_input_{unique_key or sector_name}"] = ""
    
    # Input field
    st.text_input(
        "💬 Type your question...",
        key=f"chat_input_{unique_key or sector_name}",
        on_change=handle_submit,
        placeholder="Ask anything about agriculture..."
    )
    
    # Control buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", key=f"clear_{unique_key or sector_name}"):
            st.session_state[chat_key] = []
            st.rerun()
    with col2:
        if st.button("📋 Export", key=f"export_{unique_key or sector_name}"):
            data = json.dumps(st.session_state[chat_key], indent=2, default=str)
            st.download_button("📄 Download", data, f"chat_{sector_name}.json", "application/json")
