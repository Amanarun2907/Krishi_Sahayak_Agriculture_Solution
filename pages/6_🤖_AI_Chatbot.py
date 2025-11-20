import streamlit as st
import re
import random
from datetime import datetime
from config import CUSTOM_CSS
from modules.enhanced_chatbot import AdvancedFoundationalChatbot, create_chat_interface

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="AI Chatbot Assistant - Krishi Sahayak",
    page_icon="🤖",
    layout="wide"
)

def get_topic_insights(topic):
    """Get detailed insights and information for each topic"""
    insights = {
        "Crop Health & Nutrient Deficiency": {
            "title": "🌿 Crop Health & Nutrient Deficiency",
            "description": "Comprehensive guide to identifying and managing crop health issues",
            "key_points": [
                "🔍 **Visual Symptoms**: Yellowing leaves indicate nitrogen deficiency, brown edges suggest potassium deficiency",
                "🧪 **Soil Testing**: Test soil every 2-3 years for pH, NPK, and micronutrients",
                "💊 **Treatment**: Apply urea for nitrogen, MOP for potassium, DAP for phosphorus",
                "📊 **Monitoring**: Regular field visits help detect problems early",
                "🌱 **Prevention**: Balanced fertilization, crop rotation, organic matter addition"
            ],
            "quick_tips": [
                "Take photos of affected plants for better diagnosis",
                "Check soil moisture levels before applying fertilizers",
                "Use foliar sprays for quick nutrient delivery",
                "Monitor weather conditions affecting nutrient uptake"
            ],
            "common_issues": [
                "Nitrogen Deficiency: Yellowing of older leaves, stunted growth",
                "Potassium Deficiency: Brown scorching on leaf edges, weak stems",
                "Phosphorus Deficiency: Purple/reddish leaves, delayed flowering",
                "Iron Deficiency: Yellow leaves with green veins (interveinal chlorosis)"
            ],
            "cost_info": "Soil testing: ₹500-1000 per sample, saves ₹5000-10000 in fertilizer costs"
        },
        "Pest Management & Control": {
            "title": "🐛 Pest Management & Control",
            "description": "Integrated Pest Management strategies for effective pest control",
            "key_points": [
                "🔄 **IPM Approach**: Cultural → Biological → Chemical control methods",
                "🕷️ **Natural Predators**: Encourage ladybugs, lacewings, parasitic wasps",
                "🌿 **Biological Control**: Use Bt for caterpillars, neem oil for sucking pests",
                "⏰ **Timing**: Apply pesticides early morning (6-8 AM) or evening (5-7 PM)",
                "🔄 **Rotation**: Rotate chemical groups to prevent resistance"
            ],
            "quick_tips": [
                "Use pheromone traps for monitoring pest populations",
                "Avoid broad-spectrum pesticides to protect beneficial insects",
                "Implement crop rotation to break pest cycles",
                "Monitor weather conditions affecting pest activity"
            ],
            "common_issues": [
                "Aphids: Sucking pests causing yellowing and stunting",
                "Whiteflies: Transmit viral diseases, use yellow sticky traps",
                "Stem Borer: Major pest of rice and maize, use pheromone traps",
                "Bollworm: Affects cotton and vegetables, use Bt cotton varieties"
            ],
            "cost_info": "IPM reduces pesticide costs by 30-50% while maintaining effective control"
        },
        "Weed Control Strategies": {
            "title": "🌱 Weed Control Strategies",
            "description": "Effective weed management techniques for different farming scenarios",
            "key_points": [
                "⏰ **Early Intervention**: Weed management should be done early in crop cycle",
                "🧪 **Herbicide Selection**: Pre-emergence prevents germination, post-emergence targets growing weeds",
                "🌾 **Cultural Control**: Crop rotation, intercropping, mulching suppress weeds",
                "👥 **Manual Weeding**: Most effective for small farms, weed when soil is moist",
                "📊 **Monitoring**: Regular field scouting to identify weed species and density"
            ],
            "quick_tips": [
                "Weed when soil is moist - easier to pull and reduces soil disturbance",
                "Use proper herbicide timing for maximum effectiveness",
                "Implement mulching with organic materials to suppress weeds",
                "Choose competitive crop varieties and optimal plant density"
            ],
            "common_issues": [
                "Broadleaf Weeds: Use 2,4-D in cereals, MCPA in broadleaf crops",
                "Grassy Weeds: Use selective herbicides, proper crop rotation",
                "Perennial Weeds: Require repeated treatments, deep cultivation",
                "Herbicide Resistance: Rotate herbicide modes of action"
            ],
            "cost_info": "Manual weeding: ₹2000-3000/hectare, herbicides: ₹1000-2000/hectare"
        },
        "Irrigation & Water Management": {
            "title": "💧 Irrigation & Water Management",
            "description": "Smart irrigation strategies for water conservation and crop optimization",
            "key_points": [
                "💧 **Drip Irrigation**: Saves 30-50% water, ideal for vegetables and fruits",
                "⏰ **Scheduling**: Water based on crop growth stage, critical periods are flowering and fruiting",
                "🌡️ **Water Stress**: Symptoms include wilting, leaf curling, reduced growth",
                "📊 **Monitoring**: Use tensiometers or soil moisture sensors for accurate timing",
                "🌧️ **Conservation**: Mulching, cover crops, proper drainage management"
            ],
            "quick_tips": [
                "Use a simple tensiometer to monitor soil moisture levels accurately",
                "Check soil moisture 2-3 inches deep before irrigation",
                "Avoid overwatering to prevent root diseases",
                "Schedule irrigation based on weather forecasts"
            ],
            "common_issues": [
                "Overwatering: Causes root diseases, nutrient leaching",
                "Underwatering: Stunts growth, reduces yield quality",
                "Poor Drainage: Leads to waterlogging and root rot",
                "Salinity: Affects water uptake, requires leaching"
            ],
            "cost_info": "Drip irrigation: ₹50,000-80,000/hectare, saves 30-50% water and increases yield by 20-30%"
        },
        "Soil Health & Fertility": {
            "title": "🌍 Soil Health & Fertility",
            "description": "Building and maintaining healthy soil for sustainable agriculture",
            "key_points": [
                "🌱 **Organic Matter**: Healthy soil contains 3-5% organic matter",
                "📊 **Soil Testing**: Test every 2-3 years for pH, nutrients, organic matter",
                "🪱 **Biological Activity**: Encourage earthworms and beneficial microbes",
                "⚖️ **pH Management**: Most crops prefer pH 6.0-7.0, use lime or sulfur",
                "🌿 **Cover Crops**: Improve soil structure, add organic matter"
            ],
            "quick_tips": [
                "Test soil every 2-3 years to track changes in fertility and pH",
                "Add compost or farmyard manure regularly to improve soil structure",
                "Avoid excessive tillage to preserve soil structure",
                "Use crop rotation to maintain soil fertility"
            ],
            "common_issues": [
                "Low Organic Matter: Add compost, farmyard manure, cover crops",
                "Acidic Soil: Apply lime to raise pH, improve nutrient availability",
                "Alkaline Soil: Use sulfur, organic matter to lower pH",
                "Compacted Soil: Deep tillage, organic matter addition"
            ],
            "cost_info": "Soil health improvement: ₹10,000-15,000/hectare annually, improves yield by 15-25%"
        },
        "Crop Selection & Planning": {
            "title": "🌾 Crop Selection & Planning",
            "description": "Strategic crop selection and planning for maximum profitability",
            "key_points": [
                "🌱 **Selection Criteria**: Soil type, climate, water availability, market demand",
                "🔄 **Crop Rotation**: Break pest cycles, improve soil fertility",
                "💰 **Profitability**: High-value crops require more management",
                "📅 **Seasonal Planning**: Kharif (June-October), Rabi (October-March), Zaid (March-June)",
                "🌍 **Climate Adaptation**: Choose varieties suitable for local conditions"
            ],
            "quick_tips": [
                "Visit local markets to understand demand and pricing before choosing crops",
                "Consider your soil and water resources when selecting crops",
                "Start with crops you're familiar with, gradually diversify",
                "Plan crop rotation to maximize soil health and profitability"
            ],
            "common_issues": [
                "Poor Market Prices: Research market demand before planting",
                "Climate Mismatch: Choose varieties suitable for local weather",
                "Soil Incompatibility: Match crops to soil type and fertility",
                "Water Shortage: Select drought-tolerant varieties"
            ],
            "cost_info": "High-value crops: ₹50,000-100,000/hectare investment, 200-400% ROI potential"
        },
        "Weather & Climate Impact": {
            "title": "🌧️ Weather & Climate Impact",
            "description": "Understanding and adapting to weather patterns and climate change",
            "key_points": [
                "🌧️ **Monsoon Management**: Plan cropping calendar around monsoon patterns",
                "🌡️ **Climate Adaptation**: Use drought-resistant varieties, water conservation",
                "📊 **Weather Monitoring**: Track temperature, rainfall, humidity patterns",
                "🌱 **Stress Management**: Protect crops from extreme weather events",
                "📅 **Seasonal Planning**: Adjust planting dates based on weather forecasts"
            ],
            "quick_tips": [
                "Keep a weather diary to track patterns and plan farming activities",
                "Use weather apps for accurate forecasts and planning",
                "Monitor temperature changes during critical growth stages",
                "Implement climate-smart agriculture practices"
            ],
            "common_issues": [
                "Drought: Use drought-resistant varieties, water conservation",
                "Floods: Choose flood-tolerant varieties, improve drainage",
                "Heat Stress: Provide shade, increase irrigation frequency",
                "Cold Damage: Use frost protection, select cold-tolerant varieties"
            ],
            "cost_info": "Climate adaptation: ₹20,000-40,000/hectare investment, reduces weather-related losses by 30-50%"
        },
        "Government Schemes & Subsidies": {
            "title": "🏛️ Government Schemes & Subsidies",
            "description": "Accessing government support and financial assistance for farmers",
            "key_points": [
                "💰 **PM Kisan**: ₹6,000 per year to small and marginal farmers",
                "📋 **Soil Health Card**: Free soil testing every 3 years",
                "🛡️ **Crop Insurance**: PMFBY protects against weather-related losses",
                "🌱 **Fertilizer Subsidies**: Available through government channels",
                "💧 **Irrigation Schemes**: KUSUM for solar irrigation, PMKSY for water management"
            ],
            "quick_tips": [
                "Visit your local Krishi Vigyan Kendra (KVK) for latest scheme information",
                "Keep all documents ready for scheme applications",
                "Apply for schemes well before deadlines",
                "Join farmer groups for better access to schemes"
            ],
            "common_issues": [
                "Documentation: Keep land records, bank details, Aadhaar ready",
                "Application Process: Visit agriculture office for guidance",
                "Eligibility: Check income and landholding criteria",
                "Timing: Apply during specified periods for each scheme"
            ],
            "cost_info": "PM Kisan: ₹6,000/year, Soil Health Card: Free, Crop Insurance: 1.5-2% premium"
        },
        "General Farming Advice": {
            "title": "🌾 General Farming Advice",
            "description": "Essential farming practices and sustainable agriculture principles",
            "key_points": [
                "🌱 **Sustainable Practices**: Crop rotation, organic fertilizers, IPM",
                "📊 **Record Keeping**: Track inputs, yields, costs for better decisions",
                "🤝 **Farmer Networks**: Join cooperatives for better prices and knowledge",
                "🔬 **Technology Adoption**: Use modern tools and techniques",
                "📚 **Continuous Learning**: Stay updated with latest agricultural practices"
            ],
            "quick_tips": [
                "Network with other farmers in your area to share knowledge",
                "Keep detailed records of all farming activities",
                "Attend agricultural workshops and training programs",
                "Use mobile apps for farm management and weather updates"
            ],
            "common_issues": [
                "Low Productivity: Improve soil health, use quality seeds",
                "High Input Costs: Bulk purchasing through cooperatives",
                "Market Access: Direct marketing, value addition",
                "Knowledge Gap: Regular training, extension services"
            ],
            "cost_info": "Sustainable farming: 20-30% higher initial investment, 40-60% better long-term profitability"
        }
    }
    
    return insights.get(topic, {
        "title": topic,
        "description": "General agricultural information",
        "key_points": ["General farming advice"],
        "quick_tips": ["General tips"],
        "common_issues": ["Common issues"],
        "cost_info": "Cost information"
    })

def display_topic_insights(topic):
    """Display detailed insights for selected topic"""
    insights = get_topic_insights(topic)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0; 
                border: 2px solid #2E8B57; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <h2 style="color: #2E8B57; margin-bottom: 1rem; text-align: center;">
            {insights['title']}
        </h2>
        <p style="text-align: center; color: #666; margin-bottom: 2rem; font-size: 1.1rem;">
            {insights['description']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Points
    st.markdown("### 🔑 Key Points")
    for point in insights['key_points']:
        st.markdown(f"• {point}")
    
    # Quick Tips
    st.markdown("### 💡 Quick Tips")
    col1, col2 = st.columns(2)
    for i, tip in enumerate(insights['quick_tips']):
        with col1 if i % 2 == 0 else col2:
            st.markdown(f"""
            <div style="background: #f0fff0; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        border-left: 4px solid #4caf50;">
                {tip}
            </div>
            """, unsafe_allow_html=True)
    
    # Common Issues
    st.markdown("### ⚠️ Common Issues & Solutions")
    for issue in insights['common_issues']:
        st.markdown(f"""
        <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                    border-left: 4px solid #ffc107;">
            {issue}
        </div>
        """, unsafe_allow_html=True)
    
    # Cost Information
    st.markdown("### 💰 Cost Information")
    st.markdown(f"""
    <div style="background: #d1ecf1; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                border-left: 4px solid #17a2b8;">
        <strong>💡 Investment Insight:</strong> {insights['cost_info']}
    </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Ask About This Topic", use_container_width=True):
            st.session_state.current_query = f"Tell me more about {topic.lower()}"
            st.rerun()
    
    with col2:
        if st.button("📚 Get Detailed Guide", use_container_width=True):
            st.session_state.show_detailed_guide = topic
            st.rerun()
    
    with col3:
        if st.button("🔄 Back to Topics", use_container_width=True):
            st.session_state.show_topic_insights = None
            st.rerun()

def display_detailed_guide(topic):
    """Display detailed guide for selected topic"""
    insights = get_topic_insights(topic)
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0; 
                border: 2px solid #2196f3; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
        <h2 style="color: #1976d2; margin-bottom: 1rem; text-align: center;">
            📚 Detailed Guide: {insights['title']}
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Step-by-step guide based on topic
    if "Crop Health" in topic:
        st.markdown("### 📋 Step-by-Step Crop Health Management")
        steps = [
            "**Step 1: Visual Inspection** - Walk through your field and observe plant appearance",
            "**Step 2: Symptom Identification** - Note specific symptoms like yellowing, wilting, or spots",
            "**Step 3: Soil Testing** - Collect soil samples and send for laboratory analysis",
            "**Step 4: Diagnosis** - Compare symptoms with nutrient deficiency charts",
            "**Step 5: Treatment Planning** - Calculate required fertilizer dosages",
            "**Step 6: Application** - Apply treatments following safety guidelines",
            "**Step 7: Monitoring** - Track crop response and adjust treatments as needed"
        ]
    elif "Pest Management" in topic:
        st.markdown("### 📋 Step-by-Step Pest Management")
        steps = [
            "**Step 1: Pest Identification** - Identify pest species and damage patterns",
            "**Step 2: Population Assessment** - Count pests and assess infestation level",
            "**Step 3: Economic Threshold** - Determine if treatment is economically justified",
            "**Step 4: Control Method Selection** - Choose cultural, biological, or chemical control",
            "**Step 5: Treatment Application** - Apply control measures at optimal timing",
            "**Step 6: Effectiveness Monitoring** - Assess treatment success and pest resurgence",
            "**Step 7: Prevention Planning** - Implement preventive measures for next season"
        ]
    elif "Weed Control" in topic:
        st.markdown("### 📋 Step-by-Step Weed Management")
        steps = [
            "**Step 1: Weed Identification** - Identify weed species and growth stage",
            "**Step 2: Density Assessment** - Calculate weed density and coverage percentage",
            "**Step 3: Competition Analysis** - Assess impact on crop growth and yield",
            "**Step 4: Control Strategy** - Choose manual, mechanical, or chemical control",
            "**Step 5: Treatment Timing** - Apply treatments at optimal growth stage",
            "**Step 6: Application** - Follow herbicide labels and safety guidelines",
            "**Step 7: Follow-up** - Monitor control effectiveness and plan prevention"
        ]
    else:
        st.markdown("### 📋 Step-by-Step Implementation Guide")
        steps = [
            "**Step 1: Assessment** - Evaluate current situation and identify needs",
            "**Step 2: Planning** - Develop comprehensive management plan",
            "**Step 3: Resource Allocation** - Allocate budget, time, and resources",
            "**Step 4: Implementation** - Execute planned activities systematically",
            "**Step 5: Monitoring** - Track progress and measure effectiveness",
            "**Step 6: Evaluation** - Assess results and identify improvements",
            "**Step 7: Adaptation** - Modify approach based on results and learning"
        ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                    border-left: 4px solid #6c757d;">
            <strong>Step {i}:</strong> {step}
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Resources
    st.markdown("### 📖 Additional Resources")
    resources = [
        "📱 **Mobile Apps**: Krishi Vigyan Kendra apps, weather apps, pest identification apps",
        "🌐 **Websites**: ICAR, KVK websites, agricultural extension services",
        "📚 **Publications**: Agricultural magazines, research papers, extension bulletins",
        "👥 **Experts**: Local agricultural officers, KVK scientists, experienced farmers",
        "🎓 **Training**: Farmer training programs, workshops, field demonstrations"
    ]
    
    for resource in resources:
        st.markdown(f"• {resource}")
    
    # Back button
    if st.button("🔙 Back to Topic Overview", use_container_width=True):
        st.session_state.show_detailed_guide = None
        st.rerun()

def main():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;">
            🤖 Krishi Sahayak AI Assistant
        </h1>
        <p style="color: #228B22; font-size: 1.2rem; max-width: 700px; margin: 0 auto;">
            Your intelligent agriculture companion - No API keys required! 
            Ask me anything about farming, crop management, pest control, and more.
        </p>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin: 1.5rem auto; max-width: 700px;">
            <p style="color: white; font-size: 1rem; margin: 0;">
                🌾 <strong>Specialized Training:</strong> Expert knowledge on 
                <strong>Maize, Wheat, Rice, Corn & Soybean</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if 'foundational_chatbot' not in st.session_state:
        st.session_state.foundational_chatbot = AdvancedFoundationalChatbot()
    
    chatbot = st.session_state.foundational_chatbot
    
    # Initialize session state variables
    if 'show_topic_insights' not in st.session_state:
        st.session_state.show_topic_insights = None
    if 'show_detailed_guide' not in st.session_state:
        st.session_state.show_detailed_guide = None
    if 'current_query' not in st.session_state:
        st.session_state.current_query = None
    
    # Sidebar with quick topics
    st.sidebar.markdown("### 🌾 Quick Topics")
    quick_topics = [
        "Crop Health & Nutrient Deficiency",
        "Pest Management & Control",
        "Weed Control Strategies", 
        "Irrigation & Water Management",
        "Soil Health & Fertility",
        "Crop Selection & Planning",
        "Weather & Climate Impact",
        "Government Schemes & Subsidies",
        "General Farming Advice"
    ]
    
    # Handle topic button clicks
    for topic in quick_topics:
        if st.sidebar.button(topic, use_container_width=True):
            st.session_state.show_topic_insights = topic
            st.session_state.show_detailed_guide = None
            st.rerun()
    
    # Display topic insights if selected
    if st.session_state.show_topic_insights:
        display_topic_insights(st.session_state.show_topic_insights)
        return
    
    # Display detailed guide if selected
    if st.session_state.show_detailed_guide:
        display_detailed_guide(st.session_state.show_detailed_guide)
        return
    
    # Main chat interface using enhanced version
    create_chat_interface("general_farming", None, use_api=False)
    
    # Features section
    st.markdown("---")
    st.markdown("### 🌟 What I Can Help You With")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4>🌿 Crop Health</h4>
            <p>Nutrient deficiency diagnosis, soil health, and crop monitoring advice</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h4>🐛 Pest Control</h4>
            <p>Integrated pest management, pesticide recommendations, and biological control</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4>🌱 Weed Management</h4>
            <p>Herbicide selection, manual weeding techniques, and weed prevention</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h4>💧 Irrigation</h4>
            <p>Water management, irrigation scheduling, and drought management</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="custom-card">
            <h4>🌾 Crop Planning</h4>
            <p>Crop selection, rotation planning, and seasonal farming advice</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h4>🏛️ Government Schemes</h4>
            <p>Information about subsidies, loans, insurance, and agricultural schemes</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Specialized Crops Section
    st.markdown("---")
    st.markdown("### 🌾 Specialized Crop Knowledge")
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <p style="color: #2E8B57; font-size: 1.1rem; margin-bottom: 1rem;">
            <strong>This AI chatbot has been specially trained with comprehensive knowledge about:</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    crop_col1, crop_col2, crop_col3, crop_col4, crop_col5 = st.columns(5)
    
    with crop_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFA500 0%, #FF8C00 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0; font-size: 2rem;">🌽</h2>
            <h4 style="margin: 0.5rem 0; color: white;">Maize</h4>
            <p style="font-size: 0.85rem; margin: 0;">Cultivation, pests, diseases, harvesting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with crop_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #DAA520 0%, #B8860B 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0; font-size: 2rem;">🌾</h2>
            <h4 style="margin: 0.5rem 0; color: white;">Wheat</h4>
            <p style="font-size: 0.85rem; margin: 0;">Varieties, irrigation, fertilization</p>
        </div>
        """, unsafe_allow_html=True)
    
    with crop_col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #90EE90 0%, #32CD32 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0; font-size: 2rem;">🌾</h2>
            <h4 style="margin: 0.5rem 0; color: white;">Rice</h4>
            <p style="font-size: 0.85rem; margin: 0;">Paddy management, water needs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with crop_col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0; font-size: 2rem;">🌽</h2>
            <h4 style="margin: 0.5rem 0; color: white;">Corn</h4>
            <p style="font-size: 0.85rem; margin: 0;">Growth stages, pest control</p>
        </div>
        """, unsafe_allow_html=True)
    
    with crop_col5:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #8FBC8F 0%, #556B2F 100%); 
                    padding: 1.5rem; border-radius: 10px; text-align: center; color: white;">
            <h2 style="margin: 0; font-size: 2rem;">🫘</h2>
            <h4 style="margin: 0.5rem 0; color: white;">Soybean</h4>
            <p style="font-size: 0.85rem; margin: 0;">Nitrogen fixing, rotation</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #e8f5e9; padding: 1rem; border-radius: 10px; margin: 1.5rem 0; border-left: 4px solid #4caf50;">
        <p style="color: #2E8B57; margin: 0;">
            💡 <strong>Ask me anything about these crops:</strong> Planting schedules, fertilizer requirements, 
            pest management, disease control, harvesting techniques, market prices, and best practices!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Advanced Features Section
    st.markdown("---")
    st.markdown("### 🚀 Advanced Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4>🧠 Intelligent Analysis</h4>
            <p>Advanced pattern recognition and contextual understanding</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h4>📊 Confidence Scoring</h4>
            <p>Get confidence levels for all recommendations and advice</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4>💡 Pro Tips</h4>
            <p>Expert-level tips and best practices for each topic</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h4>🔄 Context Awareness</h4>
            <p>Remembers conversation context for better responses</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h4>🤖 Krishi Sahayak AI Assistant</h4>
        <p>Powered by foundational AI - No external API keys required!</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Farmers | Always learning, always helping!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()