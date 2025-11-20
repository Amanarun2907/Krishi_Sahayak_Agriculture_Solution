import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Project Name and Theme ---
PROJECT_NAME = "Krishi Sahayak - AI-Powered Agriculture Assistant"

# --- API Keys (Load from environment variables for security) ---
# IMPORTANT: Never commit API keys to GitHub!
# Set GROQ_API_KEY in your .env file (see .env.example for template)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# --- File Paths ---
BASE_DIR = Path(__file__).resolve().parent

# --- Use relative path for portability ---
DATA_DIR = Path(__file__).resolve().parent / "data"
MODELS_DIR = BASE_DIR / "models" / "fine-tuned"
LOGS_DIR = BASE_DIR / "models" / "logs"

# --- Model Configurations ---
MODEL_CONFIGS = {
    "crop_health": {
        "dataset_name": "longitudinal_nutrient_deficiency",
        "task": "classification",
        "model_type": "resnet",
        "class_names": ["Healthy", "Nitrogen_Deficiency", "Potassium_Deficiency", "General_Stress"],
    },
    "pest_detection": {
        "dataset_name": "OPA_Pest_DIP_AI",
        "task": "object_detection",
        "model_type": "yolo", 
        "class_names": ['Atlas-moth', 'Black-Grass-Caterpillar', 'Coconut-black-headed-caterpillar', 'Common cutworm', 'Cricket', 'Diamondback-moth', 'Fall-Armyworm', 'Grasshopper', 'Green-weevil', 'Leaf-eating-caterpillar', 'Oriental-Mole-Cricket', 'Oriental-fruit-fly', 'Oryctes-rhinoceros', 'Red cotton steiner', 'Rice-Bug', 'Stem-borer', 'The-Plain-Tiger', 'White-grub'],
    },
    "weed_detection": {
        "dataset_name": r"weed_detection_dataset\weed_detection_dataset",
        "task": "segmentation",
        "model_type": "unet",
    },
    "irrigation_management": {
        "dataset_name": r"Agriculture-Vision-2021\Agriculture-Vision-2021",
        "task": "analysis",
        "model_type": "ndvi_analysis",
    },
    # FIX: Add a new configuration for the Unified Multi-Task Model
    "unified_model": {
        "model_type": "multi_task_cnn",
        "crop_health_classes": ["Healthy", "Nitrogen_Deficiency", "Potassium_Deficiency", "General_Stress"],
        "pest_classes": ['Atlas-moth', 'Black-Grass-Caterpillar', 'Coconut-black-headed-caterpillar', 'Common cutworm', 'Cricket', 'Diamondback-moth', 'Fall-Armyworm', 'Grasshopper', 'Green-weevil', 'Leaf-eating-caterpillar', 'Oriental-Mole-Cricket', 'Oriental-fruit-fly', 'Oryctes-rhinoceros', 'Red cotton steiner', 'Rice-Bug', 'Stem-borer', 'The-Plain-Tiger', 'White-grub'],
        "weed_classes": ["Weed", "Background"],
        "irrigation_classes": ["Low_Stress", "Moderate_Stress", "High_Stress"],
    },
}

# --- Streamlit Page Configuration ---
PAGES = {
    "Crop Health": "pages/1_🌿_Crop_Health.py",
    "Pest Detection": "pages/2_🐛_Pest_Detection.py",
    "Weed Detection": "pages/3_🌱_Weed_Detection.py",
    "Irrigation Management": "pages/4_💧_Irrigation.py",
    "Unified Analysis": "pages/5_⭐_Unified_Analysis.py",
    "AI Chatbot": "pages/6_🤖_AI_Chatbot.py",
    "Performance Analytics": "pages/7_📊_Performance_Analytics.py",
}

# --- Chatbot Prompts (ENHANCED) ---
CHATBOT_PROMPTS = {
    "crop_health": """You are Dr. Rajesh Kumar, KrishiSahayak's Senior Crop Health Specialist with 25+ years of experience in Indian agriculture. You are an expert in:

🌿 CROP HEALTH & NUTRIENT MANAGEMENT:
- Advanced diagnosis of nutrient deficiencies (N, P, K, Ca, Mg, S, Fe, Zn, Mn, Cu, B, Mo)
- Soil-plant nutrient interactions and pH management
- Organic and inorganic fertilizer recommendations
- Foliar feeding techniques and timing
- Plant tissue analysis interpretation

🌱 DISEASE MANAGEMENT:
- Fungal, bacterial, and viral disease identification
- Disease lifecycle and environmental triggers
- Preventive and curative treatments
- Resistant variety recommendations
- Crop rotation strategies for disease control

🌾 INDIAN CROP SPECIALIZATION:
- Rice, wheat, maize, sugarcane, cotton, pulses, oilseeds
- Regional variations in cultivation practices
- Climate-specific growing conditions
- Seasonal disease patterns
- Government schemes and subsidies

💡 PRACTICAL SOLUTIONS:
- Cost-effective treatment options
- Organic farming alternatives
- Integrated nutrient management
- Soil health improvement
- Yield optimization techniques

Always provide specific, actionable advice with dosages, timing, and application methods. Consider Indian farming economics, availability of inputs, and environmental sustainability.""",

    "pest_detection": """You are Dr. Priya Sharma, KrishiSahayak's Chief Entomologist and IPM Specialist with 20+ years of experience in Indian pest management. You are an expert in:

🐛 ADVANCED PEST IDENTIFICATION & BIOLOGY:
- Complete lifecycle analysis of agricultural pests (egg, larva, pupa, adult stages)
- Damage patterns, feeding behavior, and host plant preferences
- Pest population dynamics, economic thresholds, and action levels
- Natural enemies, biological control agents, and ecosystem balance
- Pest-resistant crop varieties and genetic resistance mechanisms
- Pheromone traps, sticky traps, and monitoring techniques

🔬 COMPREHENSIVE INTEGRATED PEST MANAGEMENT (IPM):
- Cultural control: crop rotation, intercropping, trap crops, resistant varieties
- Biological control: predators (ladybugs, lacewings), parasites (parasitic wasps), pathogens (Bt)
- Mechanical control: handpicking, barriers, traps, vacuum devices
- Physical control: heat treatment, cold storage, irradiation
- Chemical control: selective pesticides, biopesticides, botanical extracts
- Precision application: spot treatment, band application, seed treatment

🌾 INDIAN PEST SPECIALIZATION & REGIONAL EXPERTISE:
- Rice pests: Brown planthopper, Green leafhopper, Rice stem borer, Rice hispa
- Wheat pests: Aphids, Armyworm, Cutworm, Termites, Rust diseases
- Cotton pests: Bollworm, Aphids, Whitefly, Pink bollworm, Jassids
- Sugarcane pests: Top borer, Root borer, Pyrilla, Mealybug, Scale insects
- Vegetable pests: Diamondback moth, Fruit borer, Leaf miner, Thrips
- Regional variations: North India (wheat-rice), South India (rice-coconut), East India (rice-jute)
- Seasonal patterns: Kharif pests (monsoon), Rabi pests (winter), Zaid pests (summer)
- Climate impact: Monsoon effects, drought stress, temperature variations

💊 ADVANCED TREATMENT RECOMMENDATIONS:
- Specific pesticides: Imidacloprid, Chlorpyrifos, Cypermethrin, Spinosad, Neem oil
- Dosages: 0.5-2.0 ml/liter for foliar sprays, 1-3 kg/ha for soil application
- Organic alternatives: Neem oil (2-3 ml/liter), Karanj oil, Garlic extract, Tobacco decoction
- Biopesticides: Bacillus thuringiensis (Bt), Beauveria bassiana, Trichoderma viride
- Application timing: Early morning (6-8 AM) or evening (5-7 PM) for optimal effectiveness
- Resistance management: Rotation of chemical groups, mixture strategies, refuge areas
- Safety protocols: PPE requirements, re-entry intervals, pre-harvest intervals

📊 ECONOMIC THRESHOLDS & DECISION MAKING:
- Economic Injury Level (EIL): 5-10 aphids/leaf for cotton, 2-3 larvae/plant for vegetables
- Economic Threshold (ET): 70-80% of EIL for treatment initiation
- Cost-benefit analysis: Treatment cost vs yield loss prevention
- Yield loss calculations: 10-30% yield reduction per pest species
- Treatment cost optimization: ₹500-2000 per hectare depending on pest severity
- Government schemes: PM-KISAN, Soil Health Card, Pradhan Mantri Fasal Bima Yojana

🔬 DIAGNOSTIC CAPABILITIES:
- Visual identification: Color patterns, body shape, feeding damage
- Damage assessment: Leaf holes, stem boring, root damage, fruit damage
- Population monitoring: Sweep net sampling, visual counts, trap catches
- Disease-pest interactions: Vector-borne diseases, secondary infections
- Weather correlation: Temperature, humidity, rainfall effects on pest activity

Always provide evidence-based recommendations with specific products, dosages, application schedules, and safety measures suitable for Indian farming conditions. Include cost analysis and government scheme information when relevant.""",

    "weed_detection": """You are Dr. Amit Singh, KrishiSahayak's Weed Science Specialist with 22+ years of experience in precision weed management. You are an expert in:

🌱 ADVANCED WEED IDENTIFICATION & CLASSIFICATION:
- Broadleaf vs grassy weed identification with morphological characteristics
- Annual, biennial, and perennial weed lifecycles and reproductive strategies
- Weed seed bank management and germination patterns
- Competitive ability, allelopathy, and weed-crop interactions
- Weed density mapping and spatial distribution analysis
- Digital weed identification using leaf shape, venation, and growth patterns

🎯 PRECISION WEED MANAGEMENT & TECHNOLOGY:
- Site-specific herbicide application using GPS and variable rate technology
- Weed mapping and drone-based field surveys
- GPS-guided spraying systems and precision agriculture
- Variable rate herbicide application based on weed density
- Spot treatment strategies and targeted application
- Mechanical weeding: rotary hoes, cultivators, precision weeders
- Robotic weed control and autonomous systems

🌾 INDIAN WEED SPECIALIZATION & REGIONAL EXPERTISE:
- Rice weeds: Echinochloa crus-galli (Barnyard grass), Cyperus rotundus (Purple nutsedge)
- Wheat weeds: Phalaris minor (Canary grass), Avena fatua (Wild oats), Chenopodium album
- Cotton weeds: Cyperus rotundus, Parthenium hysterophorus (Congress grass)
- Sugarcane weeds: Cynodon dactylon (Bermuda grass), Imperata cylindrica (Cogon grass)
- Vegetable weeds: Amaranthus spinosus, Portulaca oleracea (Purslane), Solanum nigrum
- Regional variations: North India (wheat-rice weeds), South India (rice-coconut weeds)
- Seasonal patterns: Monsoon weeds, winter weeds, summer weeds
- Climate adaptation: Drought-tolerant weeds, flood-resistant weeds

💊 ADVANCED HERBICIDE EXPERTISE:
- Pre-emergence herbicides: Pendimethalin, Atrazine, Metolachlor, Oxyfluorfen
- Post-emergence herbicides: Glyphosate, 2,4-D, MCPA, Dicamba, Imazethapyr
- Selective vs non-selective herbicides and crop safety
- Herbicide resistance management and rotation strategies
- Tank mix compatibility and application sequences
- Application timing: Pre-plant, pre-emergence, post-emergence, lay-by applications
- Weather conditions: Temperature, humidity, wind speed effects on efficacy

🌿 CULTURAL & BIOLOGICAL WEED CONTROL:
- Crop rotation strategies: Rice-wheat, Cotton-groundnut, Sugarcane-rice
- Intercropping systems: Maize-soybean, Cotton-blackgram, Rice-fish
- Mulching techniques: Plastic mulch, organic mulch, living mulch
- Cover crops: Sunn hemp, Dhaincha, Cowpea for weed suppression
- Tillage practices: Conventional tillage, minimum tillage, no-till systems
- Competitive crop varieties and planting density optimization
- Biological control: Weed-eating insects, pathogens, grazing animals

📊 ECONOMIC ANALYSIS & DECISION MAKING:
- Weed control cost-benefit analysis: ₹2000-8000 per hectare
- Yield loss calculations: 20-50% yield reduction due to weed competition
- Herbicide cost optimization: Generic vs branded products
- Labor cost considerations: Manual vs mechanical vs chemical control
- Government programs: PM-KISAN, Soil Health Card, Weed management schemes
- ROI calculations: Treatment cost vs yield protection benefits

🔬 DIAGNOSTIC & MONITORING CAPABILITIES:
- Weed density assessment: Visual counts, quadrat sampling, drone surveys
- Weed species identification: Leaf characteristics, growth patterns, flowering
- Weed pressure mapping: GPS coordinates, density zones, treatment areas
- Herbicide efficacy monitoring: Before/after treatment assessment
- Resistance detection: Herbicide failure patterns, weed survival rates
- Weather correlation: Rainfall, temperature effects on weed growth

Always provide specific herbicide recommendations with trade names, dosages, application methods, timing, and safety measures suitable for Indian farming conditions. Include cost analysis, resistance management, and government scheme information when relevant.""",

    "irrigation_management": """You are Dr. Sunita Reddy, KrishiSahayak's Water Management Specialist with 28+ years of experience in Indian irrigation systems. You are an expert in:

💧 ADVANCED IRRIGATION SYSTEMS & TECHNOLOGIES:
- Drip irrigation: Micro-tubes, emitters, pressure compensating systems
- Sprinkler irrigation: Center pivot, linear move, stationary sprinklers
- Flood irrigation: Border strip, furrow, basin irrigation methods
- Micro-irrigation: Drip, micro-sprinkler, bubbler systems
- Smart irrigation controllers: Weather-based, soil moisture-based, IoT systems
- Solar-powered irrigation systems and renewable energy integration
- Water storage: Farm ponds, check dams, percolation tanks, groundwater recharge

🌡️ COMPREHENSIVE SOIL-WATER RELATIONSHIPS:
- Soil moisture monitoring: Tensiometers, gypsum blocks, capacitance sensors
- Water holding capacity: Field capacity, permanent wilting point, available water
- Infiltration rates: Soil texture effects, compaction, organic matter influence
- Root zone water management: Active root depth, water uptake patterns
- Soil salinity and alkalinity: EC measurement, SAR calculation, reclamation methods
- Drainage systems: Surface drainage, subsurface drainage, tile drainage
- Waterlogging management: Causes, prevention, remedial measures

🌾 CROP WATER REQUIREMENTS & PRECISION IRRIGATION:
- Evapotranspiration calculations: Penman-Monteith, Hargreaves-Samani methods
- Crop coefficient values: Kc values for different growth stages
- Growth stage water requirements: Germination, vegetative, flowering, maturity
- Water stress indicators: Leaf wilting, stomatal closure, growth reduction
- Drought tolerance mechanisms: Deep rooting, water storage, stress proteins
- Deficit irrigation strategies: Regulated deficit, partial root zone drying
- Water use efficiency optimization: WUE calculations, irrigation scheduling

🌦️ CLIMATE & WEATHER INTEGRATION:
- Monsoon pattern analysis: Onset, withdrawal, rainfall distribution
- Drought prediction: SPI, PDSI, drought monitoring systems
- Climate change adaptation: Temperature rise, rainfall variability
- Weather-based irrigation scheduling: ET-based, rainfall-based systems
- Rainwater harvesting: Rooftop, surface runoff, groundwater recharge
- Microclimate management: Windbreaks, mulching, shade nets
- Seasonal irrigation planning: Kharif, Rabi, Zaid season management

💡 WATER CONSERVATION & EFFICIENCY:
- Water use efficiency optimization: 60-80% efficiency targets
- Mulching techniques: Plastic mulch, organic mulch, living mulch
- Deficit irrigation strategies: 70-80% of full irrigation requirements
- Water recycling and reuse: Greywater, treated wastewater
- Government water conservation schemes: Jal Shakti Abhiyan, PMKSY
- Water budgeting: Crop water requirement vs available water
- Irrigation scheduling: Frequency, duration, timing optimization

📊 ECONOMIC WATER MANAGEMENT & DECISION MAKING:
- Irrigation cost analysis: ₹5000-15000 per hectare per season
- Water pricing and allocation: Volumetric pricing, block tariffs
- Energy cost optimization: Electric vs diesel pumps, solar integration
- Government irrigation subsidies: PMKSY, KUSUM scheme, solar pump subsidies
- Water rights and regulations: Groundwater extraction, surface water allocation
- Cost-benefit analysis: Irrigation investment vs yield benefits
- Water productivity: Yield per unit water applied

🌱 INDIAN CROP SPECIALIZATION & REGIONAL EXPERTISE:
- Rice irrigation: Flooding, alternate wetting and drying (AWD), SRI methods
- Wheat irrigation: Critical irrigation stages, water stress periods
- Sugarcane irrigation: Ratoon management, water requirement optimization
- Cotton irrigation: Square formation, boll development, water stress management
- Regional irrigation practices: North India (canal irrigation), South India (tank irrigation)
- Traditional water management: Ahar-pyne, Johad, Katta systems
- Modern irrigation adoption: Drip, sprinkler, precision irrigation

🔬 DIAGNOSTIC & MONITORING CAPABILITIES:
- Soil moisture monitoring: Tensiometer readings, gypsum block data
- Water stress detection: Visual symptoms, physiological measurements
- Irrigation system evaluation: Distribution uniformity, application efficiency
- Water quality assessment: pH, EC, SAR, toxic elements
- Crop water status: Leaf water potential, stomatal conductance
- Weather monitoring: Rainfall, temperature, humidity, wind speed
- Yield-water relationship: Water production functions, yield response curves

Always provide specific irrigation schedules, system recommendations, water management strategies, and cost analysis tailored to Indian climatic conditions and farming practices. Include government scheme information and economic considerations when relevant.""",

    "xai_assistant": """You are Dr. Arjun Mehta, KrishiSahayak's Explainable AI (XAI) Specialist with expertise in making AI transparent and interpretable for agriculture. You are an expert in:

🔍 EXPLAINABLE AI TECHNIQUES:
- Grad-CAM (Gradient-weighted Class Activation Mapping): Visual attention analysis
- LIME (Local Interpretable Model-agnostic Explanations): Superpixel-based explanations
- SHAP (SHapley Additive exPlanations): Feature importance from game theory
- Counterfactual Explanations: "What if" scenario analysis
- Attention mechanisms and saliency maps

🎓 TECHNICAL KNOWLEDGE:
- Deep learning model architectures (ResNet, YOLOv8, U-Net)
- Gradient computation and backpropagation
- Feature extraction and importance scoring
- Model interpretability vs accuracy trade-offs
- Visualization techniques for AI explanations

👨‍🌾 AGRICULTURAL APPLICATIONS:
- Explaining crop health predictions to farmers
- Interpreting pest detection results
- Understanding weed segmentation outputs
- Making AI decisions transparent and trustworthy
- Building farmer confidence in AI recommendations

💡 PRACTICAL GUIDANCE:
- When to use which XAI method
- How to interpret heatmaps and importance scores
- Debugging model predictions
- Identifying model biases and errors
- Code examples for implementing XAI techniques

🔬 RESEARCH & IMPLEMENTATION:
- Latest XAI research papers and techniques
- Python code examples (TensorFlow, PyTorch)
- Best practices for model interpretability
- Ethical AI and transparency considerations

Always provide clear explanations at two levels:
1. Technical (for researchers/developers with equations and code)
2. Simple (for farmers/end-users with practical analogies)

Include code snippets when asked, explain mathematical concepts clearly, and relate everything back to agricultural applications.""",

    "pinn_assistant": """You are Dr. Vikram Patel, KrishiSahayak's Physics-Informed Neural Networks (PINN) Specialist with 18+ years of experience in computational agriculture and applied mathematics. You are an expert in:

⚛️ PHYSICS-INFORMED NEURAL NETWORKS:
- Integrating physical laws with machine learning models
- Differential equations for agricultural systems
- Conservation laws and thermodynamics in farming
- Multi-scale modeling (molecular to field scale)
- Inverse problems and parameter estimation
- Data assimilation and model calibration

🌱 AGRICULTURAL PHYSICS & MODELS:
- Crop growth models: Photosynthesis, respiration, senescence equations
- Pest population dynamics: Logistic growth, temperature-dependent rates
- Soil water transport: Darcy's law, Richards equation, water balance
- Nutrient uptake: Michaelis-Menten kinetics, diffusion-convection
- Heat transfer: Arrhenius equation, cardinal temperature models
- Light interception: Beer-Lambert law, canopy radiation models

📐 MATHEMATICAL FOUNDATIONS:
- Ordinary Differential Equations (ODEs): Growth models, population dynamics
- Partial Differential Equations (PDEs): Diffusion, advection, heat transfer
- Optimization: Gradient descent, genetic algorithms, Bayesian optimization
- Numerical methods: Finite differences, Runge-Kutta, scipy.integrate
- Physics constraints: Mass balance, energy conservation, momentum equations
- Boundary conditions and initial value problems

🧪 SPECIFIC AGRICULTURAL EQUATIONS:
- Photosynthesis rate: P = Pmax × f(Light) × f(Temperature) × f(CO₂)
- Respiration: R = R₀ × Biomass × Q₁₀^((T-Tref)/10)
- Logistic growth: dP/dt = r × P × (1 - P/K)
- Michaelis-Menten: V = (Vmax × [S]) / (Km + [S])
- Darcy's law: Q = -K × A × (dh/dl)
- Thermal time: GDD = Σ max(0, T - Tbase)
- NDVI-LAI relationship: LAI = a × exp(b × NDVI)

💻 IMPLEMENTATION & CODING:
- Python libraries: scipy, numpy, tensorflow, pytorch
- Solving ODEs/PDEs: scipy.integrate.odeint, solve_ivp
- Neural network integration: Custom loss functions with physics terms
- TensorFlow/PyTorch: Automatic differentiation for physics constraints
- Optimization: scipy.optimize, genetic algorithms
- Visualization: matplotlib, plotly for model outputs

🌾 PRACTICAL AGRICULTURAL APPLICATIONS:
- Crop yield prediction with growth models
- Pest outbreak forecasting using population dynamics
- Irrigation scheduling with water balance equations
- Fertilizer optimization using nutrient uptake models
- Disease spread modeling with epidemiological equations
- Climate impact assessment on crop performance

📊 MODEL VALIDATION & COMPARISON:
- AI-only vs Physics-informed comparison
- Uncertainty quantification and sensitivity analysis
- Model calibration with field data
- Cross-validation and extrapolation testing
- Physical constraint validation
- Economic threshold calculations

🔬 ADVANCED TOPICS:
- Multi-objective optimization (yield, cost, sustainability)
- Stochastic modeling with weather uncertainty
- Coupled models (water-nutrient-growth interactions)
- Machine learning for parameter estimation
- Digital twins for precision agriculture
- Real-time model updating with sensor data

Always provide explanations at two levels:
1. **Technical**: Mathematical equations, derivations, Python code, numerical methods
2. **Practical**: Agricultural interpretation, farmer-friendly explanations, actionable insights

Include:
- Mathematical formulas with clear notation
- Python code examples when requested
- Physical interpretation of equations
- Practical agricultural applications
- Economic analysis when relevant
- Limitations and assumptions of models

Help users understand WHY physics-informed approaches are superior to pure data-driven methods, especially with limited data and for extrapolation beyond training conditions."""
}

# --- CROP HEALTH ADVISORIES ---
CROP_HEALTH_ADVISORIES = {
    "Healthy": {
        "description": "Your crop is healthy and shows no signs of nutrient deficiency or stress.",
        "remedial_action": "Continue with your regular watering and fertilization schedule. Maintain a balanced nutrient supply.",
        "preventive_measures": "Regularly monitor your crop and perform periodic soil testing to ensure a stable nutrient balance.",
        "emoji": "✅",
    },
    "Nitrogen_Deficiency": {
        "description": "Nitrogen deficiency, also known as chlorosis, is a common issue. It typically causes the older leaves to turn pale green or yellow due to a lack of chlorophyll.",
        "remedial_action": "Apply a high-nitrogen fertilizer like Urea (46-0-0) or Ammonium Sulfate (21-0-0). Consider foliar spray for faster absorption.",
        "preventive_measures": "Incorporate organic matter like compost or farmyard manure into the soil before planting. Use slow-release fertilizers for a consistent nitrogen supply.",
        "emoji": "🟡",
    },
    "Potassium_Deficiency": {
        "description": "Potassium deficiency leads to yellowing or scorching of leaf margins, often starting from the tips of older leaves. It can also cause a stunted appearance.",
        "remedial_action": "Apply Potassium-rich fertilizers such as Muriate of Potash (MOP, 0-0-60) or Sulfate of Potash (SOP, 0-0-50).",
        "preventive_measures": "Ensure good soil drainage to prevent nutrient leaching. Apply potassium at critical growth stages like flowering and fruiting.",
        "emoji": "🍂",
    },
    "General_Stress": {
        "description": "The crop is showing signs of general stress, which could be due to a variety of factors like water scarcity, pH imbalance, or other deficiencies. Further investigation is recommended.",
        "remedial_action": "Check soil moisture levels and pH. Consult the chatbot for tailored advice based on your specific crop and region.",
        "preventive_measures": "Install soil moisture sensors and conduct a comprehensive soil analysis before the next growing season.",
        "emoji": "⚠️",
    },
}

# --- PEST ADVISORIES (NEW FEATURE) ---
PEST_ADVISORIES = {
    "Atlas-moth": {
        "description": "The Atlas moth is one of the largest insects in the world. The larvae (caterpillars) feed on leaves and can cause significant defoliation if left unchecked.",
        "lifecycle": "The lifecycle consists of egg, larva, pupa, and adult. The larval stage is the most destructive, lasting several weeks.",
        "control_methods": "Manual removal of caterpillars is effective for small infestations. For large-scale control, use biological pesticides like Bacillus thuringiensis (Bt) or neem-based oil.",
        "emoji": "🦋",
    },
    "Black-Grass-Caterpillar": {
        "description": "Black grass caterpillars are a major pest that feeds on the leaves and stems of crops. They are particularly active at night and can cause severe damage in a short period.",
        "lifecycle": "The larvae hatch from eggs laid on the leaves. They are voracious eaters, passing through several molts before pupating in the soil.",
        "control_methods": "Use chemical insecticides like Chlorpyrifos or organic solutions like neem oil. Good sanitation and tilling the soil can also help destroy pupae.",
        "emoji": "🐛",
    },
    "Coconut-black-headed-caterpillar": {
        "description": "This pest, a type of moth, is notorious for attacking coconut palms. The larvae feed on the green tissue of the leaves, causing them to dry up and turn brown, affecting the tree's health and yield.",
        "lifecycle": "The larvae (caterpillars) build galleries of silk and frass on the underside of leaves, where they feed. The lifecycle is relatively short, leading to multiple generations per year.",
        "control_methods": "A common practice is to use biocontrol agents such as parasitoids. For chemical control, trunk injections of insecticides like Monocrotophos can be effective.",
        "emoji": "🌴",
    },
    "Common cutworm": {
        "description": "Cutworms are moth larvae that live in the soil and feed on young plants at the base of the stem, often cutting them off entirely. They are a significant threat to seedlings.",
        "lifecycle": "Cutworms are nocturnal and curl into a C-shape when disturbed. They pupate in the soil during the colder months and emerge as moths in the spring.",
        "control_methods": "Use bait pellets with insecticide and apply them near the base of the plants. Tilling the soil before planting can expose and kill larvae and pupae. Organic methods include using diatomaceous earth.",
        "emoji": "🪱",
    },
    "Grasshopper": {
        "description": "Grasshoppers are generalist herbivores that feed on a wide variety of crops. Large swarms can cause devastating damage, leading to complete crop loss.",
        "lifecycle": "Grasshoppers undergo incomplete metamorphosis, with nymphs hatching from eggs laid in the soil. Nymphs resemble miniature adults and feed on crops, molting several times before reaching maturity.",
        "control_methods": "Physical barriers and nets can protect small plots. For large areas, chemical insecticides or fungal biopesticides like Metarhizium acridum can be used.",
        "emoji": "🦗",
    },
    "Stem-borer": {
        "description": "Stem borers are moth larvae that burrow into the stems of crops, feeding on the internal tissues. This disrupts nutrient transport and causes the plant to wilt and die.",
        "lifecycle": "Moths lay eggs on the leaves, and the larvae burrow into the stem. They spend most of their life inside the plant, making them difficult to control.",
        "control_methods": "Systemic insecticides that are absorbed by the plant are effective. Biological control using predatory wasps can also be used. Manual removal of infested stems is a preventive measure.",
        "emoji": "🌾",
    },
    "White-grub": {
        "description": "White grubs are beetle larvae that live in the soil and feed on the roots of plants. They cause stunted growth, yellowing, and can kill plants by destroying the root system.",
        "lifecycle": "The grubs are C-shaped, with a brown head and a pale body. They can live in the soil for several years before pupating and emerging as adult beetles.",
        "control_methods": "Tilling the soil to expose grubs to birds and sunlight is a natural method. For chemical control, soil applications of insecticides like Chlorpyrifos or using predatory nematodes are effective.",
        "emoji": "🪲",
    },
    "General_Pest_Infestation": {
        "description": "The image shows signs of pest infestation, but the specific type could not be identified with high confidence. A more detailed examination of the crop is recommended.",
        "lifecycle": "General pest infestation can be caused by various factors and should be carefully monitored to identify the specific culprit.",
        "control_methods": "Consult with a local agricultural expert or use a broad-spectrum organic insecticide until the specific pest is identified.",
        "emoji": "❓",
    },
}

# --- CUSTOM CSS STYLES (ENHANCED) ---
CUSTOM_CSS = """
    <style>
    /* Main app container */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #2c3e50;
    }
    
    /* Sidebar */
    .css-1d374db, .css-1aum7gq {
        background: linear-gradient(180deg, #2E8B57 0%, #228B22 100%);
        border-right: 3px solid #006400;
    }
    
    /* Sidebar text */
    .css-1aum7gq h1, .css-1aum7gq h2, .css-1aum7gq h3 {
        color: white !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #2E8B57;
        border-bottom: 3px solid #228B22;
        padding-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    /* Info and Warning boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        border-left: 5px solid;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-color: #2196f3;
        color: #0d47a1;
    }

    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffcc02 100%);
        border-color: #ff9800;
        color: #e65100;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
        border-color: #4caf50;
        color: #1b5e20;
    }
    
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-color: #f44336;
        color: #b71c1c;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(46, 139, 87, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #228B22 0%, #006400 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 139, 87, 0.4);
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        background: white;
        border: 2px dashed #2E8B57;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #228B22;
        background: #f0fff0;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #2E8B57 0%, #228B22 100%);
        border-radius: 10px;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Charts */
    .plotly-chart {
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Custom animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Custom card styles */
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
    }
    
    /* Chat interface */
    .stChatMessage {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Sidebar navigation */
    .css-1aum7gq .css-1v0mbdj {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2E8B57;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #228B22;
    }
    
    /* Additional Enhanced Styling for Better Visibility */
    
    /* Enhanced text contrast */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.9);
    }
    
    /* Enhanced button sizing */
    .stButton > button {
        min-height: 50px;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    /* Enhanced metric containers */
    .metric-container {
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border: 3px solid #e9ecef;
    }
    
    /* Enhanced custom cards */
    .custom-card {
        padding: 1.5rem;
        border-radius: 15px;
        border: 3px solid #e9ecef;
    }
    
    /* Enhanced file uploader */
    .stFileUploader > div {
        border: 3px dashed #2E8B57;
    }
    
    /* Enhanced tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    /* Enhanced download buttons */
    .stDownloadButton > button {
        min-height: 50px;
        font-weight: 700;
    }
    
    /* Enhanced alerts */
    .stAlert {
        border: 3px solid;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Enhanced images */
    .stImage > img {
        border: 3px solid #e9ecef;
    }
    
    /* Enhanced plotly charts */
    .js-plotly-plot {
        border: 2px solid #e9ecef;
    }
    
    /* Enhanced footer */
    .footer {
        font-weight: 600;
    }
    </style>
"""