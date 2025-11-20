import streamlit as st
import httpx
import json
import random
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time

class EnhancedGroqChatbot:
    """Enhanced Groq API-based chatbot with better error handling and styling"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "llama-3.1-8b-instant"
        self.temperature = 0.7
        
    def test_api_connection(self) -> bool:
        """Test if API connection is working"""
        try:
            http_client = httpx.Client(timeout=10.0, follow_redirects=True)
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
            
            return bool(response.choices[0].message.content)
        except Exception as e:
            return False
        
    def get_response(self, user_query: str, system_prompt: str, analysis_context: str = None) -> str:
        """Get response from Groq API with enhanced error handling"""
        try:
            # Create HTTP client with proper timeout and proxy support
            http_client = httpx.Client(timeout=60.0, follow_redirects=True)
            
            # Initialize Groq client
            from groq import Groq
            client = Groq(api_key=self.api_key, http_client=http_client)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self._prepare_user_message(user_query, analysis_context)}
            ]
            
            # Get response
            response = client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                stream=False,
                max_tokens=1000
            )
            
            # Check if response is empty
            if not response.choices[0].message.content:
                return "I apologize, but I received an empty response. Please try rephrasing your question or try again in a moment."
            
            return response.choices[0].message.content
            
        except Exception as e:
            return self._get_fallback_response(user_query, str(e))
    
    def _prepare_user_message(self, user_query: str, analysis_context: str = None) -> str:
        """Prepare user message with context"""
        if analysis_context:
            return f"Context: {analysis_context}\n\nQuestion: {user_query}"
        return user_query
    
    def _get_fallback_response(self, user_query: str, error: str) -> str:
        """Provide fallback response when API fails"""
        return f"""I apologize, but I'm experiencing technical difficulties connecting to my AI service. 
        
**Your Question:** {user_query}

**Error:** {error}

**What I can still help with:**
- Basic agricultural advice based on my knowledge base
- General farming recommendations
- Information about common agricultural practices

Please try rephrasing your question or contact support if the issue persists."""


class AdvancedFoundationalChatbot:
    """Advanced foundational chatbot without API dependencies"""
    
    def __init__(self):
        self.knowledge_base = self._build_comprehensive_knowledge_base()
        self.conversation_history = []
        self.user_profile = {}
        
        # Define trained domain scope
        self.trained_crops = ["maize", "wheat", "rice", "corn", "soybean", "soya bean", "soya"]
        self.trained_topics = [
            "crop health", "monitoring", "nutrient", "deficiency", "disease",
            "pest", "detection", "insect", "control", "management",
            "weed", "herbicide", "weeding",
            "irrigation", "water", "watering", "moisture", "drought"
        ]
        
    def _is_within_domain(self, user_input: str) -> bool:
        """Check if user query is within the trained domain"""
        user_input_lower = user_input.lower()
        
        # Check for greetings and general queries (allow these) - use word boundaries
        import re
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", 
                    "how are you", "what can you do", "help", "what is this", "who are you"]
        if any(re.search(r'\b' + re.escape(greeting.replace(' ', r'\s+')) + r'\b', user_input_lower) for greeting in greetings):
            return True
        
        # Check if query mentions any trained crop (use word boundaries to avoid false matches)
        import re
        has_crop = any(re.search(r'\b' + re.escape(crop) + r'\b', user_input_lower) for crop in self.trained_crops)
        
        # Check if query mentions any trained topic (use word boundaries)
        has_topic = any(re.search(r'\b' + re.escape(topic.replace(' ', r'\s+')) + r'\b', user_input_lower) for topic in self.trained_topics)
        
        # If no crop or topic mentioned, check if it's clearly out of domain
        if not (has_crop or has_topic):
            # Check for obviously out-of-domain keywords
            out_of_domain_keywords = [
                "gold", "silver", "stock", "bitcoin", "crypto",
                "machine learning", "artificial intelligence", "programming",
                "recipe", "cooking", "biryani", "restaurant",
                "movie", "music", "sports", "cricket", "football",
                "politics", "election", "medicine", "doctor"
            ]
            
            # If any out-of-domain keyword found, reject
            if any(keyword in user_input_lower for keyword in out_of_domain_keywords):
                return False
            
            # If no crops, topics, or obvious out-of-domain keywords, still reject
            # (be conservative - only allow if explicitly about our domain)
            return False
        
        # Query mentions crops or topics, so it's in domain
        return True
    
    def _get_out_of_domain_response(self) -> str:
        """Return polite message for out-of-domain queries"""
        return """🤖 **I apologize, but I can only help with specific topics.**

I have been specially trained on **5 crops only:**
1. 🌽 **Maize**
2. 🌾 **Wheat**
3. 🌾 **Rice**
4. 🌽 **Corn**
5. 🫘 **Soybean**

And the following **4 subjects only:**
1. 🌿 **Crop Health & Monitoring** - Nutrient deficiencies, diseases, soil health
2. 🐛 **Pest Detection & Management** - Pest identification, control techniques, IPM
3. 🌱 **Weed Detection & Control** - Weed management, herbicides, manual control
4. 💧 **Irrigation Management** - Water scheduling, irrigation systems, drought management

**Please ask me questions related to these crops and topics, and I'll be happy to help!**

**Example Questions:**
- "How to control pests in wheat?"
- "What are signs of nitrogen deficiency in maize?"
- "Best irrigation schedule for rice?"
- "How to manage weeds in soybean?"
"""
        
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
            "soil_management": {
                "keywords": [
                    "soil", "fertility", "organic matter", "compost", "manure", "pH", 
                    "drainage", "tilth", "structure", "microbes", "earthworms"
                ],
                "responses": [
                    "🌍 **Soil Health:** Healthy soil contains 3-5% organic matter. Add compost or farmyard manure regularly to improve soil structure, fertility, and water retention.",
                    "📊 **Soil Testing:** Test soil every 2-3 years for pH, nutrients, and organic matter. Most crops prefer pH 6.0-7.0. Use lime to raise pH or sulfur to lower it.",
                    "🪱 **Biological Activity:** Encourage earthworms and beneficial microbes by avoiding excessive tillage and using organic amendments. This improves soil structure naturally."
                ],
                "detailed_info": {
                    "soil_ph": "Rice: 5.5-6.5, Wheat: 6.0-7.0, Cotton: 6.0-8.0, Vegetables: 6.0-7.0",
                    "organic_matter": "Target 3-5% in topsoil. Add 10-15 tonnes FYM/hectare annually",
                    "drainage": "Good drainage prevents waterlogging and root diseases. Add organic matter to improve structure"
                }
            },
            "crop_selection": {
                "keywords": [
                    "crop selection", "variety", "season", "climate", "soil type", 
                    "market demand", "profitability", "rotation", "intercropping"
                ],
                "responses": [
                    "🌾 **Crop Selection Criteria:** Choose crops based on soil type, climate, water availability, market demand, and your experience. Rice grows well in clay soils, pulses prefer well-drained soils.",
                    "🔄 **Crop Rotation:** Rotate crops to break pest cycles and improve soil fertility. Good rotations: rice-wheat-pulses, maize-soybean-wheat, cotton-groundnut.",
                    "💰 **Profitability:** High-value crops like vegetables and spices can be profitable but require more management. Start with crops you're familiar with and gradually diversify."
                ],
                "detailed_info": {
                    "kharif_crops": "Rice, maize, cotton, sugarcane, groundnut, soybean (June-October)",
                    "rabi_crops": "Wheat, barley, mustard, chickpea, potato (October-March)",
                    "zaid_crops": "Vegetables, watermelon, cucumber (March-June)"
                }
            },
            "weather_climate": {
                "keywords": [
                    "weather", "climate", "rainfall", "temperature", "monsoon", 
                    "drought", "flood", "season", "climate change", "adaptation"
                ],
                "responses": [
                    "🌧️ **Monsoon Management:** Indian agriculture depends heavily on monsoon rains. Plan cropping calendar around monsoon patterns. Early monsoon crops: rice, maize. Late monsoon crops: wheat, mustard.",
                    "🌡️ **Climate Adaptation:** Climate change affects rainfall patterns. Use drought-resistant varieties, water conservation techniques, and adjust planting dates based on weather forecasts.",
                    "📊 **Weather Monitoring:** Track temperature, rainfall, and humidity. Sudden changes can stress crops, especially during flowering and fruiting stages."
                ],
                "detailed_info": {
                    "monsoon_onset": "Normal onset: June 1st, Early: May 15-31, Late: June 15-30",
                    "drought_tolerance": "Pearl millet, sorghum, chickpea are drought-tolerant crops",
                    "flood_tolerance": "Rice varieties like Swarna Sub-1 are flood-tolerant"
                }
            },
            "government_schemes": {
                "keywords": [
                    "government", "scheme", "subsidy", "loan", "insurance", "PM Kisan", 
                    "soil health card", "fertilizer", "PMFBY", "KUSUM"
                ],
                "responses": [
                    "🏛️ **PM Kisan Scheme:** Provides ₹6,000 per year to small and marginal farmers in three installments. Direct benefit transfer to bank accounts.",
                    "📋 **Soil Health Card:** Free soil testing every 3 years. Provides recommendations for fertilizers and soil amendments. Available at Krishi Vigyan Kendras (KVKs).",
                    "🛡️ **Crop Insurance (PMFBY):** Protects against weather-related losses. Premium subsidized by government. Covers yield loss due to drought, flood, pests, diseases."
                ],
                "detailed_info": {
                    "pm_kisan": "₹6,000/year in 3 installments. Eligibility: Landholding up to 2 hectares",
                    "soil_health_card": "Free every 3 years. Tests pH, NPK, micronutrients, organic matter",
                    "crop_insurance": "Premium: 1.5-2% of sum insured. Covers yield loss and prevented sowing"
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
    
    def generate_response(self, user_input: str) -> str:
        """Generate comprehensive response based on user input"""
        
        # DOMAIN VALIDATION: Check if query is within trained scope
        if not self._is_within_domain(user_input):
            return self._get_out_of_domain_response()
        
        category, confidence = self.find_best_category(user_input)
        
        # Get base response
        responses = self.knowledge_base[category]["responses"]
        base_response = random.choice(responses)
        
        # Add specific information
        specific_info = self._get_specific_information(user_input, category)
        
        # Add contextual advice
        contextual_advice = self._get_contextual_advice(user_input, category)
        
        # Add helpful tips
        tips = self._get_helpful_tips(category)
        
        # Combine all parts
        response_parts = [base_response]
        
        if specific_info:
            response_parts.append(f"\n📋 **Specific Information:**\n{specific_info}")
        
        if contextual_advice:
            response_parts.append(f"\n💡 **Additional Advice:**\n{contextual_advice}")
        
        if tips:
            response_parts.append(f"\n🌟 **Pro Tip:** {tips}")
        
        # Add confidence indicator
        if confidence > 0.7:
            response_parts.append(f"\n✅ **Confidence Level:** High ({confidence:.0%})")
        elif confidence > 0.4:
            response_parts.append(f"\n⚠️ **Confidence Level:** Medium ({confidence:.0%})")
        else:
            response_parts.append(f"\n❓ **Confidence Level:** Low ({confidence:.0%}) - Please provide more specific details")
        
        return "\n".join(response_parts)
    
    def _get_crop_specific_info(self, user_input_lower: str, category: str) -> str:
        """Get crop-specific information for trained crops"""
        crop_info = {
            "maize": {
                "crop_health": "🌽 **Maize Health:** Common issues include nitrogen deficiency (yellowing lower leaves), borer damage (holes in stems), and leaf blight. Apply urea at 120 kg/ha in 2-3 splits.",
                "pest_management": "🌽 **Maize Pests:** Fall armyworm is major pest. Use pheromone traps and spray chlorantraniliprole 0.4ml/L. Stem borer control: Apply carbofuran 1kg/ha at whorl stage.",
                "weed_management": "🌽 **Maize Weeds:** Apply atrazine 1kg/ha pre-emergence. Post-emergence: 2,4-D 1kg/ha at 3-4 leaf stage. Manual weeding at 20-25 days after sowing.",
                "irrigation": "🌽 **Maize Irrigation:** Critical stages: knee-high, tasseling, and grain filling. Apply 5-6 irrigations. Avoid water stress during flowering."
            },
            "wheat": {
                "crop_health": "🌾 **Wheat Health:** Watch for rust diseases (yellow, brown, black). Apply propiconazole 0.1% at first sign. Nitrogen: 120 kg/ha in 3 splits (basal, tillering, jointing).",
                "pest_management": "🌾 **Wheat Pests:** Aphids are common. Spray imidacloprid 0.3ml/L or dimethoate 2ml/L. Termites: Apply chlorpyrifos 2.5L/ha with last plowing.",
                "weed_management": "🌾 **Wheat Weeds:** For Phalaris minor: use sulfosulfuron 25g/ha. Broadleaf weeds: 2,4-D 500g/ha at 30-35 DAS. Pre-emergence: pendimethalin 1kg/ha.",
                "irrigation": "🌾 **Wheat Irrigation:** Critical stages: CRI (20-25 DAS), tillering, jointing, flowering, grain filling. Total 5-6 irrigations. First irrigation at 20-25 days."
            },
            "rice": {
                "crop_health": "🌾 **Rice Health:** Blast disease is serious. Spray tricyclazole 0.6g/L. Bacterial blight: Use copper oxychloride 3g/L. Zinc deficiency common: Apply ZnSO4 25kg/ha.",
                "pest_management": "🌾 **Rice Pests:** Stem borer: Use cartap hydrochloride 2g/L. Brown planthopper: Spray buprofezin 1ml/L. Leaf folder: Apply chlorpyrifos 2ml/L.",
                "weed_management": "🌾 **Rice Weeds:** Pre-emergence: butachlor 2.5L/ha within 3 days of transplanting. Post-emergence: bispyribac sodium 25g/ha at 15-20 DAT.",
                "irrigation": "🌾 **Rice Irrigation:** Maintain 5cm water for first 10 days. Then 2-3cm standing water. Drain 10 days before harvest. AWD method saves 30% water."
            },
            "corn": {
                "crop_health": "🌽 **Corn Health:** Similar to maize. Watch for downy mildew (spray metalaxyl 2g/L). Nitrogen: 150 kg/ha for sweet corn. Boron deficiency: Apply borax 10kg/ha.",
                "pest_management": "🌽 **Corn Pests:** Corn borer: Spray lambda-cyhalothrin 0.5ml/L. Earworm: Apply spinosad 0.5ml/L at silk stage. Aphids: Use imidacloprid 0.3ml/L.",
                "weed_management": "🌽 **Corn Weeds:** Pre-emergence: atrazine 1-1.5kg/ha. Post-emergence: tembotrione 120ml/ha at 2-3 leaf stage. Mulching reduces weeds by 70%.",
                "irrigation": "🌽 **Corn Irrigation:** Sweet corn needs more water. Irrigate at 6-leaf, tasseling, silking, and grain filling. Drip irrigation ideal for sweet corn."
            },
            "soybean": {
                "crop_health": "🫘 **Soybean Health:** Yellow mosaic virus is major issue. Use resistant varieties. Rhizobium inoculation essential: 5g/kg seed. Phosphorus: 60-80 kg P2O5/ha.",
                "pest_management": "🫘 **Soybean Pests:** Girdle beetle: Spray quinalphos 2ml/L. Stem fly: Use carbofuran 1kg/ha. Pod borer: Apply indoxacarb 0.5ml/L at pod formation.",
                "weed_management": "🫘 **Soybean Weeds:** Pre-emergence: pendimethalin 1kg/ha. Post-emergence: imazethapyr 100g/ha at 15-20 DAS. One hand weeding at 30-35 DAS.",
                "irrigation": "🫘 **Soybean Irrigation:** Critical stages: flowering and pod filling. 2-3 irrigations if rainfall insufficient. Avoid waterlogging - ensure good drainage."
            }
        }
        
        # Check which crop is mentioned
        for crop in ["maize", "wheat", "rice", "corn", "soybean", "soya"]:
            if crop in user_input_lower:
                actual_crop = "soybean" if crop in ["soybean", "soya"] else crop
                if actual_crop in crop_info and category in crop_info[actual_crop]:
                    return crop_info[actual_crop][category]
        
        return ""
    
    def _get_specific_information(self, user_input: str, category: str) -> str:
        """Get specific information based on user input"""
        user_input_lower = user_input.lower()
        detailed_info = self.knowledge_base[category].get("detailed_info", {})
        
        # Get crop-specific information for trained crops
        crop_specific_info = self._get_crop_specific_info(user_input_lower, category)
        if crop_specific_info:
            return crop_specific_info
        
        # Check for specific crop mentions (fallback for general info)
        crops = ["rice", "wheat", "maize", "corn", "soybean"]
        mentioned_crops = [crop for crop in crops if crop in user_input_lower]
        
        if mentioned_crops:
            crop_info = {
                "rice": "Requires 2-3 inches standing water, transplanting at 25-30 days, harvest at 30-35% moisture",
                "wheat": "Sow in October-November, requires 4-5 irrigations, harvest when grain moisture is 20-25%",
                "maize": "Plant spacing 60x25 cm, requires 6-8 irrigations, harvest when husk turns brown",
                "cotton": "Plant in April-May, requires 8-10 irrigations, harvest when bolls open 60-70%",
                "sugarcane": "Plant in February-March, requires heavy irrigation, harvest after 12-18 months",
                "vegetable": "Requires frequent irrigation, regular harvesting, use drip irrigation for efficiency"
            }
            return crop_info.get(mentioned_crops[0], "")
        
        # Check for specific issues
        issues = ["nitrogen", "potassium", "phosphorus", "iron", "zinc", "aphid", "whitefly", "borer"]
        mentioned_issues = [issue for issue in issues if issue in user_input_lower]
        
        if mentioned_issues and mentioned_issues[0] in detailed_info:
            return detailed_info[mentioned_issues[0]]
        
        return ""
    
    def _get_contextual_advice(self, user_input: str, category: str) -> str:
        """Get contextual advice based on user input"""
        user_input_lower = user_input.lower()
        
        if "cost" in user_input_lower or "price" in user_input_lower or "expensive" in user_input_lower:
            cost_advice = {
                "crop_health": "Soil testing costs ₹500-1000 per sample but saves ₹5000-10000 in fertilizer costs",
                "pest_management": "IPM reduces pesticide costs by 30-50% while maintaining effective control",
                "weed_management": "Manual weeding costs ₹2000-3000/hectare, herbicides cost ₹1000-2000/hectare",
                "irrigation": "Drip irrigation costs ₹50,000-80,000/hectare but saves 30-50% water and increases yield by 20-30%"
            }
            return cost_advice.get(category, "Consider cost-benefit analysis for all agricultural inputs")
        
        if "organic" in user_input_lower or "natural" in user_input_lower:
            organic_advice = {
                "crop_health": "Use organic fertilizers like compost, vermicompost, and biofertilizers for sustainable soil health",
                "pest_management": "Neem oil, garlic extract, and biological control agents are effective organic pest control methods",
                "weed_management": "Mulching, crop rotation, and manual weeding are effective organic weed control methods",
                "irrigation": "Organic mulching helps conserve soil moisture and reduces irrigation requirements"
            }
            return organic_advice.get(category, "Organic farming practices improve long-term sustainability and soil health")
        
        return ""
    
    def _get_helpful_tips(self, category: str) -> str:
        """Get helpful tips for specific categories"""
        tips = {
            "crop_health": "Take photos of affected plants and soil for better diagnosis. Regular field visits help detect problems early.",
            "pest_management": "Encourage natural predators by avoiding broad-spectrum pesticides. Use pheromone traps for monitoring.",
            "weed_management": "Weed when soil is moist - it's easier to pull and reduces soil disturbance. Use proper herbicide timing.",
            "irrigation": "Use a simple tensiometer or soil moisture probe to monitor soil moisture levels accurately.",
            "soil_management": "Test soil every 2-3 years to track changes in fertility and pH. Keep soil test reports for comparison.",
            "crop_selection": "Visit local markets to understand demand and pricing before choosing crops. Consider your soil and water resources.",
            "weather_climate": "Keep a weather diary to track patterns and plan farming activities. Use weather apps for forecasts.",
            "government_schemes": "Visit your local Krishi Vigyan Kendra (KVK) for the latest information on government schemes and subsidies.",
            "general_farming": "Network with other farmers in your area to share knowledge and experiences. Join farmer groups or cooperatives."
        }
        
        return tips.get(category, "Keep learning and adapting your farming practices based on local conditions and experiences.")


def create_chat_interface(sector_name: str, analysis_context: str = None, use_api: bool = True, unique_key: str = None):
    """
    FIXED VERSION: Create chat interface that doesn't reload the page
    """
    
    # Use unique key to separate different chatbot instances
    if unique_key:
        chat_key = f"chat_history_{unique_key}"
    else:
        chat_key = f"chat_history_{sector_name}"
    
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
    
    # Chatbot initialization
    if use_api:
        from config import GROQ_API_KEY
        chatbot_type = "API-Powered"
        chatbot_icon = "🤖"
    else:
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
    
    # Chat input with callback - NO PAGE RELOAD
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
                
                # Check if API key is available
                if not GROQ_API_KEY or GROQ_API_KEY == "":
                    response = """
                    ❌ **API Key Not Configured**
                    
                    The GROQ API key is not set. To use the AI chatbot:
                    
                    1. Create a `.env` file in the project root
                    2. Add your GROQ API key: `GROQ_API_KEY=your_key_here`
                    3. Get a free API key from: https://console.groq.com
                    
                    For now, you can use the demo mode or other features of the app.
                    """
                else:
                    system_prompt = CHATBOT_PROMPTS.get(sector_name, "You are a helpful agricultural assistant.")
                    # Create HTTP client with proper timeout and proxy support
                    http_client = httpx.Client(timeout=60.0, follow_redirects=True)
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
                if f"foundational_chatbot_{sector_name}" not in st.session_state:
                    st.session_state[f"foundational_chatbot_{sector_name}"] = AdvancedFoundationalChatbot()
                chatbot = st.session_state[f"foundational_chatbot_{sector_name}"]
                response = chatbot.generate_response(user_input)
        except httpx.ConnectError as e:
            response = f"""
            ❌ **Connection Error**
            
            Unable to connect to the Groq API server. This could be due to:
            - Network connectivity issues
            - Firewall blocking the connection
            - Groq API service temporarily unavailable
            
            **What to try:**
            1. Check your internet connection
            2. Try again in a few moments
            3. If on Streamlit Cloud, check if the API key is set in Secrets
            
            **Error details:** {str(e)}
            """
        except httpx.TimeoutException as e:
            response = f"""
            ⏱️ **Request Timeout**
            
            The request took too long to complete. This might be due to:
            - Slow internet connection
            - High server load
            
            **What to try:**
            1. Try asking a simpler question
            2. Wait a moment and try again
            
            **Error details:** {str(e)}
            """
        except Exception as e:
            error_msg = str(e).lower()
            if "api key" in error_msg or "authentication" in error_msg or "401" in error_msg:
                response = f"""
                ❌ **API Authentication Error**
                
                The API key appears to be invalid or expired.
                
                **What to do:**
                1. Check if your GROQ_API_KEY is correct in the `.env` file
                2. Get a new API key from: https://console.groq.com
                3. Make sure the key is properly set in Streamlit Cloud Secrets (if deployed)
                
                **Error details:** {str(e)}
                """
            elif "rate limit" in error_msg or "429" in error_msg:
                response = f"""
                ⚠️ **Rate Limit Exceeded**
                
                You've made too many requests in a short time.
                
                **What to do:**
                1. Wait a few minutes before trying again
                2. Consider upgrading your Groq API plan for higher limits
                
                **Error details:** {str(e)}
                """
            else:
                response = f"""
                ❌ **Unexpected Error**
                
                An error occurred while processing your request.
                
                **Error details:** {str(e)}
                
                **What to try:**
                1. Check your internet connection
                2. Verify your API key is valid
                3. Try again in a few moments
                4. If the problem persists, please report this issue
                """
        
        # Add response
        st.session_state[chat_key].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now()
        })
        
        # Clear input
        st.session_state[f"chat_input_{unique_key or sector_name}"] = ""
    
    # Input field with callback
    st.text_input(
        "💬 Type your question and press Enter...",
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
