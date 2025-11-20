import streamlit as st
import httpx
import json
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time

# ============================================================================
# MULTILINGUAL SUPPORT - ISSUE 3 FIX
# ============================================================================

TRANSLATIONS = {
    "English": {
        "chat_title": "Krishi Sahayak Assistant",
        "specialized_in": "Specialized in",
        "ask_anything": "Ask me anything!",
        "status": "Status",
        "connected": "Connected",
        "fallback_mode": "Fallback Mode",
        "foundational_mode": "Foundational Mode",
        "messages": "Messages",
        "no_messages": "No messages yet. Type a message below to get started!",
        "you": "You",
        "thinking": "Thinking...",
        "type_question": "Type your question here...",
        "send": "Send",
        "clear_chat": "Clear Chat",
        "export_chat": "Export Chat",
        "switch_language": "Switch Language",
        "chat_cleared": "Chat cleared!",
        "download_chat": "Download Chat",
        "quick_actions": "Quick Actions",
        "api_error": "API Error. Using foundational chatbot...",
        "error_processing": "I apologize, but I encountered an error while processing your question",
        "try_again": "Please try again or contact support if the issue persists."
    },
    "Hindi": {
        "chat_title": "कृषि सहायक सहायक",
        "specialized_in": "विशेषज्ञता",
        "ask_anything": "मुझसे कुछ भी पूछें!",
        "status": "स्थिति",
        "connected": "जुड़ा हुआ",
        "fallback_mode": "फॉलबैक मोड",
        "foundational_mode": "मूल मोड",
        "messages": "संदेश",
        "no_messages": "अभी तक कोई संदेश नहीं। शुरू करने के लिए नीचे एक संदेश टाइप करें!",
        "you": "आप",
        "thinking": "सोच रहा हूँ...",
        "type_question": "अपना प्रश्न यहाँ टाइप करें...",
        "send": "भेजें",
        "clear_chat": "चैट साफ़ करें",
        "export_chat": "चैट निर्यात करें",
        "switch_language": "भाषा बदलें",
        "chat_cleared": "चैट साफ़ हो गई!",
        "download_chat": "चैट डाउनलोड करें",
        "quick_actions": "त्वरित क्रियाएं",
        "api_error": "API त्रुटि। मूल चैटबॉट का उपयोग कर रहे हैं...",
        "error_processing": "मुझे खेद है, लेकिन आपके प्रश्न को संसाधित करते समय मुझे एक त्रुटि का सामना करना पड़ा",
        "try_again": "कृपया पुनः प्रयास करें या यदि समस्या बनी रहती है तो सहायता से संपर्क करें।"
    }
}

def get_text(key: str, language: str = "English") -> str:
    """Get translated text"""
    return TRANSLATIONS.get(language, TRANSLATIONS["English"]).get(key, key)

# ============================================================================
# ENHANCED GROQ CHATBOT - ISSUE 3 FIX (ROBUST API)
# ============================================================================

class EnhancedGroqChatbot:
    """Enhanced Groq API-based chatbot with robust error handling"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "llama-3.1-8b-instant"
        self.temperature = 0.7
        self.max_retries = 3
        self.timeout = 30.0
        
    def test_api_connection(self) -> bool:
        """Test if API connection is working with retry logic"""
        for attempt in range(self.max_retries):
            try:
                http_client = httpx.Client(
                    trust_env=False, 
                    timeout=10.0,
                    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
                )
                from groq import Groq
                client = Groq(api_key=self.api_key, http_client=http_client)
                
                # Simple test query
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": "Hello"}],
                    model=self.model,
                    temperature=0.1,
                    stream=False,
                    max_tokens=10
                )
                
                http_client.close()
                return bool(response.choices[0].message.content)
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)  # Wait before retry
                    continue
                return False
        return False
        
    def get_response(self, user_query: str, system_prompt: str, analysis_context: str = None, language: str = "English") -> str:
        """Get response from Groq API with robust error handling and retry logic"""
        
        for attempt in range(self.max_retries):
            try:
                # Create HTTP client with proper configuration
                http_client = httpx.Client(
                    trust_env=False, 
                    timeout=self.timeout,
                    limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
                )
                
                # Initialize Groq client
                from groq import Groq
                client = Groq(api_key=self.api_key, http_client=http_client)
                
                # Prepare user message with context and language instruction
                if analysis_context:
                    context_message = f"Based on the image analysis: {analysis_context}\n\nUser Question: {user_query}"
                else:
                    context_message = user_query
                
                # Add language instruction
                if language == "Hindi":
                    system_prompt += "\n\nIMPORTANT: Please respond in Hindi (हिंदी) language. Use Devanagari script."
                    context_message += "\n\n(कृपया हिंदी में उत्तर दें)"
                
                # Get response
                response = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context_message}
                    ],
                    model=self.model,
                    temperature=self.temperature,
                    stream=False,
                    max_tokens=1500
                )
                
                http_client.close()
                
                # Check if response is valid
                if response and response.choices and response.choices[0].message.content:
                    return response.choices[0].message.content
                else:
                    raise Exception("Empty response from API")
                    
            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                # Return error message in appropriate language
                if language == "Hindi":
                    return f"मुझे खेद है, लेकिन API से कनेक्ट करने में समस्या हो रही है: {str(e)}\n\nकृपया पुनः प्रयास करें।"
                else:
                    return f"I apologize, but I'm experiencing technical difficulties connecting to my AI service: {str(e)}\n\nPlease try again."
        
        return "Unable to get response after multiple attempts. Please try again later."

# ============================================================================
# ADVANCED FOUNDATIONAL CHATBOT (NO CHANGES NEEDED - ALREADY GOOD)
# ============================================================================

class AdvancedFoundationalChatbot:
    """Advanced foundational chatbot without API dependencies"""
    
    def __init__(self):
        self.knowledge_base = self._build_comprehensive_knowledge_base()
        self.conversation_history = []
        self.user_profile = {}
        
    def _build_comprehensive_knowledge_base(self) -> Dict:
        """Build comprehensive knowledge base for Indian agriculture"""
        return {
            "crop_health": {
                "keywords": [
                    "crop health", "nutrient deficiency", "nitrogen", "potassium", "phosphorus", 
                    "chlorosis", "yellowing", "stunted growth", "leaf drop", "necrosis", 
                    "micronutrient", "iron", "zinc", "manganese", "copper", "boron", "molybdenum"
                ],
                "responses": [
                    "🌿 **Crop Health Analysis:** Yellowing leaves typically indicate nitrogen deficiency. Apply urea (46-0-0) at 50-100 kg/hectare. For potassium deficiency (brown leaf edges), use muriate of potash (0-0-60) at 40-60 kg/hectare.",
                    "🔬 **Nutrient Management:** Regular soil testing every 2-3 years is crucial. Most Indian soils are deficient in zinc and boron. Apply zinc sulfate (21% Zn) at 25 kg/hectare and borax at 10-15 kg/hectare.",
                    "🌱 **Organic Solutions:** Use farmyard manure (FYM) at 10-15 tonnes/hectare annually. Compost tea and vermicompost improve soil health and nutrient availability naturally."
                ],
                "detailed_info": {
                    "nitrogen_deficiency": "Yellowing starts from older leaves, stunted growth, reduced tillering in cereals",
                    "potassium_deficiency": "Brown scorching on leaf edges, weak stems, poor fruit quality",
                    "phosphorus_deficiency": "Purple/reddish leaves, delayed flowering, poor root development",
                    "iron_deficiency": "Yellow leaves with green veins (interveinal chlorosis), common in alkaline soils",
                    "zinc_deficiency": "Small leaves, short internodes, white spots on leaves"
                }
            },
            "pest_management": {
                "keywords": [
                    "pest", "insect", "aphid", "whitefly", "caterpillar", "borer", "mite", 
                    "thrips", "jassid", "mealybug", "scale", "control", "pesticide", "IPM",
                    "biological control", "natural enemies", "resistance"
                ],
                "responses": [
                    "🐛 **Integrated Pest Management (IPM):** Start with cultural practices (crop rotation, resistant varieties), then biological control (natural enemies), and finally chemical control if needed. This reduces pesticide resistance and environmental impact.",
                    "🌿 **Biological Control:** Encourage natural predators like ladybugs, lacewings, and parasitic wasps. Use Bacillus thuringiensis (Bt) for caterpillar control and neem-based products for sucking pests.",
                    "⚗️ **Chemical Control:** Use selective pesticides with proper timing. Apply early morning (6-8 AM) or evening (5-7 PM) for better efficacy. Rotate chemical groups to prevent resistance."
                ],
                "detailed_info": {
                    "aphids": "Sucking pests causing yellowing and stunting. Control with imidacloprid 0.3ml/liter or neem oil 2-3ml/liter",
                    "whiteflies": "Transmit viral diseases. Use yellow sticky traps and spray with acetamiprid 0.5g/liter",
                    "stem_borer": "Major pest of rice and maize. Use pheromone traps and spray with chlorantraniliprole 0.4ml/liter",
                    "bollworm": "Affects cotton and vegetables. Use Bt cotton varieties and spray with spinosad 0.5ml/liter"
                }
            },
            "weed_management": {
                "keywords": [
                    "weed", "herbicide", "weeding", "manual", "chemical", "mulching", 
                    "crop competition", "pre-emergence", "post-emergence", "resistance",
                    "broadleaf", "grassy", "sedges", "perennial"
                ],
                "responses": [
                    "🌱 **Weed Management Strategy:** Early intervention is key. Manual weeding is most effective for small farms, while herbicides work well for larger areas. Combine cultural, mechanical, and chemical methods.",
                    "🧪 **Herbicide Selection:** Pre-emergence herbicides (pendimethalin, atrazine) prevent weed germination. Post-emergence herbicides (glyphosate, 2,4-D) target growing weeds. Always follow label instructions.",
                    "🌾 **Cultural Control:** Crop rotation breaks weed cycles. Intercropping and mulching suppress weeds. Use competitive crop varieties and optimal plant density."
                ],
                "detailed_info": {
                    "pre_emergence": "Apply before crop and weed emergence. Pendimethalin 1-1.5 kg/hectare for rice and wheat",
                    "post_emergence": "Apply when weeds are actively growing. Glyphosate 1-2 kg/hectare for non-selective control",
                    "selective_herbicides": "2,4-D for broadleaf weeds in cereals, MCPA for grassy weeds in broadleaf crops"
                }
            },
            "irrigation": {
                "keywords": [
                    "irrigation", "watering", "drip", "sprinkler", "flood", "water stress", 
                    "drought", "moisture", "scheduling", "efficiency", "conservation"
                ],
                "responses": [
                    "💧 **Irrigation Efficiency:** Drip irrigation saves 30-50% water compared to flood irrigation. It's ideal for vegetables, fruits, and cash crops. Maintain soil moisture at 60-80% of field capacity.",
                    "⏰ **Irrigation Scheduling:** Water based on crop growth stage. Critical periods are flowering and fruit development. Use tensiometers or soil moisture sensors for accurate timing.",
                    "🌡️ **Water Stress Management:** Symptoms include wilting, leaf curling, and reduced growth. Check soil moisture 2-3 inches deep. Avoid overwatering to prevent root diseases."
                ],
                "detailed_info": {
                    "drip_irrigation": "Saves water, reduces weeds, improves yield. Cost: ₹50,000-80,000/hectare",
                    "sprinkler_irrigation": "Good for cereals and vegetables. Uniform water distribution, reduces labor",
                    "flood_irrigation": "Traditional method for rice. High water use but simple to implement"
                }
            },
            "general_farming": {
                "keywords": [
                    "farming", "agriculture", "farmer", "crop", "yield", "profit", 
                    "income", "sustainability", "organic", "precision", "technology"
                ],
                "responses": [
                    "🌱 **Sustainable Farming:** Use crop rotation, organic fertilizers, and integrated pest management. These practices improve long-term profitability and environmental health.",
                    "📊 **Record Keeping:** Track inputs, yields, and costs to identify profitable practices. Use farm management apps or simple spreadsheets for better decision-making.",
                    "🤝 **Farmer Networks:** Join farmer groups or cooperatives to share knowledge, access better prices, and reduce input costs through bulk purchasing."
                ],
                "detailed_info": {
                    "sustainable_practices": "Crop rotation, organic farming, water conservation, biodiversity",
                    "record_keeping": "Track inputs, outputs, weather, pest incidence, yields",
                    "farmer_cooperatives": "Better prices, bulk purchasing, knowledge sharing, access to credit"
                }
            }
        }
    
    def find_best_category(self, user_input: str) -> Tuple[str, float]:
        """Find the best matching category with confidence score"""
        user_input_lower = user_input.lower()
        best_category = "general_farming"
        best_score = 0
        
        for category, data in self.knowledge_base.items():
            score = sum(1 for keyword in data["keywords"] if keyword in user_input_lower)
            if score > best_score:
                best_score = score
                best_category = category
        
        confidence = min(best_score / len(self.knowledge_base[best_category]["keywords"]), 1.0)
        return best_category, confidence
    
    def generate_response(self, user_input: str, language: str = "English") -> str:
        """Generate comprehensive response based on user input"""
        category, confidence = self.find_best_category(user_input)
        
        # Get base response
        responses = self.knowledge_base[category]["responses"]
        base_response = random.choice(responses)
        
        # Combine all parts
        response_parts = [base_response]
        
        # Add confidence indicator
        if confidence > 0.7:
            response_parts.append(f"\n✅ **Confidence Level:** High ({confidence:.0%})")
        elif confidence > 0.4:
            response_parts.append(f"\n⚠️ **Confidence Level:** Medium ({confidence:.0%})")
        else:
            response_parts.append(f"\n❓ **Confidence Level:** Low ({confidence:.0%}) - Please provide more specific details")
        
        response = "\n".join(response_parts)
        
        # Translate to Hindi if needed (basic translation for key terms)
        if language == "Hindi":
            response = self._translate_to_hindi(response)
        
        return response
    
    def _translate_to_hindi(self, text: str) -> str:
        """Basic translation of key agricultural terms to Hindi"""
        translations = {
            "Crop Health": "फसल स्वास्थ्य",
            "Nitrogen": "नाइट्रोजन",
            "Potassium": "पोटैशियम",
            "Phosphorus": "फास्फोरस",
            "Pest": "कीट",
            "Weed": "खरपतवार",
            "Irrigation": "सिंचाई",
            "Soil": "मिट्टी",
            "Fertilizer": "उर्वरक",
            "High": "उच्च",
            "Medium": "मध्यम",
            "Low": "निम्न",
            "Confidence Level": "विश्वास स्तर"
        }
        
        for eng, hindi in translations.items():
            text = text.replace(eng, f"{eng} ({hindi})")
        
        return text

# ============================================================================
# MAIN CHAT INTERFACE - ALL ISSUES FIXED
# ============================================================================

def create_chat_interface(sector_name: str, analysis_context: str = None, use_api: bool = True, unique_key: str = None):
    """
    Create enhanced chat interface with ALL ISSUES FIXED:
    - Issue 1: Preserves uploaded image state
    - Issue 2: Separate chat history for home vs analysis
    - Issue 3: Robust API + Multilingual support
    """
    
    # ========================================================================
    # FIX ISSUE 2: Use completely different chat keys for home vs analysis
    # ========================================================================
    if unique_key:
        chat_key = f"chat_history_{unique_key}"  # Unique for each instance
    else:
        chat_key = f"chat_history_{sector_name}_default"
    
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    
    # Initialize language preference
    lang_key = f"language_{unique_key or sector_name}"
    if lang_key not in st.session_state:
        st.session_state[lang_key] = "English"
    
    current_language = st.session_state[lang_key]
    
    # ========================================================================
    # FIX ISSUE 3: Robust API initialization with proper error handling
    # ========================================================================
    if use_api:
        try:
            from config import GROQ_API_KEY
            chatbot = EnhancedGroqChatbot(GROQ_API_KEY)
            
            # Test API connection with retry logic
            api_working = chatbot.test_api_connection()
            
            if not api_working:
                st.warning(get_text("api_error", current_language))
                use_api = False
        except Exception as e:
            st.warning(f"{get_text('api_error', current_language)}: {str(e)}")
            use_api = False
    
    if not use_api:
        if f"foundational_chatbot_{sector_name}" not in st.session_state:
            st.session_state[f"foundational_chatbot_{sector_name}"] = AdvancedFoundationalChatbot()
        chatbot = st.session_state[f"foundational_chatbot_{sector_name}"]
        chatbot_type = get_text("foundational_mode", current_language)
        chatbot_icon = "🧠"
    else:
        chatbot_type = "API-Powered"
        chatbot_icon = "🤖"
    
    # Chat interface styling
    status_color = "#2E8B57" if "API" in chatbot_type else "#6C757D"
    
    # Language selector in header
    col_lang1, col_lang2 = st.columns([4, 1])
    with col_lang2:
        new_language = st.selectbox(
            "🌐",
            ["English", "Hindi"],
            index=0 if current_language == "English" else 1,
            key=f"lang_select_{unique_key or sector_name}",
            label_visibility="collapsed"
        )
        if new_language != current_language:
            st.session_state[lang_key] = new_language
            st.rerun()
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 1.5rem; border-radius: 15px; margin: 1rem 0; 
                border: 2px solid {status_color}; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <h3 style="color: {status_color}; margin-bottom: 1rem; text-align: center;">
            {chatbot_icon} {get_text("chat_title", current_language)} - {chatbot_type}
        </h3>
        <p style="text-align: center; color: #666; margin-bottom: 1rem;">
            {get_text("specialized_in", current_language)} {sector_name.replace('_', ' ').title()} - {get_text("ask_anything", current_language)}
        </p>
        <p style="text-align: center; color: {status_color}; font-size: 0.9rem; margin: 0;">
            {get_text("status", current_language)}: {'🟢 ' + get_text("connected", current_language) if 'API' in chatbot_type else '🔵 ' + get_text("foundational_mode", current_language)} | {get_text("messages", current_language)}: {len(st.session_state[chat_key])}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if len(st.session_state[chat_key]) == 0:
            st.info(f"💬 {get_text('no_messages', current_language)}")
        else:
            for i, message in enumerate(st.session_state[chat_key]):
                if message['role'] == 'user':
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                                padding: 1rem; border-radius: 15px; margin: 0.5rem 0; 
                                border-left: 4px solid #2196f3; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <strong style="color: #0d47a1;">👤 {get_text("you", current_language)}:</strong><br>
                        <span style="color: #2d2d2d;">{message['content']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f0fff0 0%, #c8e6c9 100%); 
                                padding: 1rem; border-radius: 15px; margin: 0.5rem 0; 
                                border-left: 4px solid #4caf50; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <strong style="color: #1b5e20;">{chatbot_icon} Krishi Sahayak:</strong><br>
                        <div style="color: #2d2d2d; line-height: 1.6;">{message['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FIX ISSUE 1: Use callback to prevent page reload and preserve state
    # ========================================================================
    
    def handle_message_submit():
        """Callback function to handle message submission without page reload"""
        user_input = st.session_state.get(f"user_input_{unique_key or sector_name}", "")
        
        if user_input and user_input.strip():
            # Add user message
            st.session_state[chat_key].append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now()
            })
            
            # Generate response
            try:
                if use_api:
                    from config import CHATBOT_PROMPTS
                    system_prompt = CHATBOT_PROMPTS.get(sector_name, "You are a helpful agricultural assistant.")
                    response = chatbot.get_response(user_input, system_prompt, analysis_context, current_language)
                else:
                    response = chatbot.generate_response(user_input, current_language)
                
                # Check if response is valid
                if not response or response.strip() == "":
                    response = f"{get_text('error_processing', current_language)}: '{user_input}'. {get_text('try_again', current_language)}"
                    
            except Exception as e:
                response = f"{get_text('error_processing', current_language)}: {str(e)}. {get_text('try_again', current_language)}"
            
            # Add bot response
            st.session_state[chat_key].append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now()
            })
            
            # Clear input
            st.session_state[f"user_input_{unique_key or sector_name}"] = ""
    
    # Input form with callback (prevents page reload)
    st.text_input(
        get_text("type_question", current_language),
        key=f"user_input_{unique_key or sector_name}",
        on_change=handle_message_submit,
        placeholder=get_text("type_question", current_language)
    )
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"🗑️ {get_text('clear_chat', current_language)}", use_container_width=True, key=f"clear_{unique_key or sector_name}"):
            st.session_state[chat_key] = []
            st.success(f"✅ {get_text('chat_cleared', current_language)}")
            st.rerun()
    
    with col2:
        if len(st.session_state[chat_key]) > 0:
            chat_export = {
                "sector": sector_name,
                "chatbot_type": chatbot_type,
                "language": current_language,
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state[chat_key]
            }
            st.download_button(
                label=f"📄 {get_text('download_chat', current_language)}",
                data=json.dumps(chat_export, indent=2, default=str),
                file_name=f"chat_export_{sector_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key=f"download_{unique_key or sector_name}"
            )
    
    with col3:
        if st.button(f"🌐 {get_text('switch_language', current_language)}", use_container_width=True, key=f"switch_lang_{unique_key or sector_name}"):
            st.session_state[lang_key] = "Hindi" if current_language == "English" else "English"
            st.rerun()
