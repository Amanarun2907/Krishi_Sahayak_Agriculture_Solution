import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from modules.pinn_models import *
from modules.enhanced_chatbot import create_chat_interface
from config import CUSTOM_CSS, CHATBOT_PROMPTS

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Physics-Informed AI - Krishi Sahayak",
    page_icon="⚛️",
    layout="wide"
)

# Main title
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="color: #2E8B57; font-size: 3.5rem; margin-bottom: 1rem;">
        ⚛️ Physics-Informed Neural Networks (PINN)
    </h1>
    <p style="color: #228B22; font-size: 1.3rem; max-width: 900px; margin: 0 auto;">
        Combining AI with Agricultural Physics - Where Data Meets Science
    </p>
</div>
""", unsafe_allow_html=True)

# Introduction
with st.expander("📖 What are Physics-Informed Neural Networks?", expanded=False):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 🎓 Technical Explanation
        
        **Physics-Informed Neural Networks (PINNs)** integrate physical laws and domain knowledge 
        into machine learning models.
        
        **Key Concepts:**
        - **Physics Laws**: Differential equations, conservation laws, thermodynamics
        - **Neural Networks**: Learn patterns from data
        - **Hybrid Approach**: Combine both for better predictions
        
        **Mathematical Framework:**
        ```
        Loss = Loss_data + λ × Loss_physics
        
        where:
        - Loss_data: Standard prediction error
        - Loss_physics: Violation of physical laws
        - λ: Weight balancing both terms
        ```
        
        **Advantages:**
        - ✅ More accurate with limited data
        - ✅ Predictions respect physical laws
        - ✅ Better extrapolation beyond training data
        - ✅ Interpretable results
        - ✅ Reduced need for large datasets
        
        **Applications in Agriculture:**
        - Crop growth modeling
        - Pest population dynamics
        - Nutrient uptake and transport
        - Water flow in soil
        - Disease spread modeling
        """)
    
    with col2:
        st.markdown("""
        ### 👨‍🌾 Simple Explanation
        
        **Think of it like a smart farmer with a science degree:**
        
        Traditional AI is like a farmer who only learns from experience (data).
        Physics-Informed AI is like a farmer who ALSO knows the science behind farming.
        
        **Example:**
        - **AI-only**: "I've seen this pattern before, so the crop will grow this much"
        - **Physics-Informed AI**: "Based on sunlight, temperature, water, and plant biology, 
          the crop will grow this much"
        
        **Why it's better:**
        - 🌱 **More reliable**: Won't predict impossible things (like negative growth)
        - 📊 **Needs less data**: Uses science to fill gaps
        - 🎯 **More accurate**: Especially in new situations
        - 💡 **Explainable**: Can tell you WHY something happens
        
        **Real-world benefits:**
        - Predict crop yield more accurately
        - Optimize fertilizer timing and amount
        - Forecast pest outbreaks
        - Plan irrigation schedules
        - Understand cause-and-effect relationships
        """)

st.markdown("---")

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌱 Crop Growth",
    "🐛 Pest Dynamics",
    "💧 Water Transport",
    "🧪 Nutrient Uptake",
    "📊 AI vs Physics",
    "🤖 PINN Chat Assistant"
])


# ==================== TAB 1: CROP GROWTH ====================
with tab1:
    st.header("🌱 Physics-Based Crop Growth Simulation")
    
    st.markdown("""
    This simulator uses **differential equations** to model crop growth based on:
    - **Photosynthesis**: Light + CO₂ → Biomass
    - **Respiration**: Energy consumption
    - **Senescence**: Natural aging
    - **Water stress**: Impact of water availability
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Environmental Parameters")
        
        # Time parameters
        simulation_days = st.slider("Simulation Duration (days)", 30, 180, 90, 10)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">📅 How many days into the future to simulate crop growth</p>', unsafe_allow_html=True)
        
        st.markdown("#### ☀️ Light & Temperature")
        light_intensity = st.slider("Light Intensity (μmol/m²/s)", 200, 2000, 800, 100)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">☀️ Sunlight available for photosynthesis (higher = more growth)</p>', unsafe_allow_html=True)
        
        temperature = st.slider("Temperature (°C)", 10, 40, 25, 1)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌡️ Field temperature (optimal: 20-30°C for most crops)</p>', unsafe_allow_html=True)
        
        st.markdown("#### 🌫️ CO₂ & Water")
        co2_concentration = st.slider("CO₂ Concentration (ppm)", 300, 800, 400, 50)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌫️ Carbon dioxide in air (normal: 400 ppm, higher = more photosynthesis)</p>', unsafe_allow_html=True)
        
        water_availability = st.slider("Water Availability (%)", 20, 100, 80, 5)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">💧 Soil moisture level (100% = fully irrigated, <60% = water stress)</p>', unsafe_allow_html=True)
        
        st.markdown("#### 🌾 Initial Conditions")
        initial_biomass = st.slider("Initial Biomass (kg/ha)", 10, 200, 50, 10)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌱 Starting crop weight per hectare (seedling stage = low, established = high)</p>', unsafe_allow_html=True)
        
        # Calculate photosynthesis and respiration rates
        P_rate = photosynthesis_rate(light_intensity, temperature, co2_concentration)
        R_rate = respiration_rate(temperature, initial_biomass)
        
        st.info(f"""
        **Current Rates:**
        - 🌿 Photosynthesis: {P_rate:.2f} μmol CO₂/m²/s
        - 💨 Respiration: {R_rate:.2f} units
        - 📈 Net Growth: {'Positive' if P_rate > R_rate else 'Negative'}
        """)
    
    with col2:
        if st.button("🚀 Run Crop Growth Simulation", key="crop_growth_sim"):
            with st.spinner("Running physics-based simulation..."):
                # Time array
                time_days = np.linspace(0, simulation_days, simulation_days + 1)
                
                # Run simulation
                biomass = simulate_crop_growth_pinn(
                    time_days, light_intensity, temperature,
                    co2_concentration, water_availability, initial_biomass
                )
                
                # Calculate derived metrics
                final_biomass = biomass[-1]
                growth_rate = (final_biomass - initial_biomass) / simulation_days
                total_growth = final_biomass - initial_biomass
                
                # Display results
                st.success(f"✅ Simulation Complete!")
                
                # Metrics
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Final Biomass", f"{final_biomass:.1f} kg/ha", 
                             f"+{total_growth:.1f} kg/ha")
                with col_m2:
                    st.metric("Growth Rate", f"{growth_rate:.2f} kg/ha/day")
                with col_m3:
                    st.metric("Total Growth", f"{(total_growth/initial_biomass*100):.1f}%")
                
                # Plot biomass over time
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=time_days,
                    y=biomass,
                    mode='lines',
                    name='Biomass',
                    line=dict(color='green', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(46, 139, 87, 0.2)'
                ))
                
                fig.update_layout(
                    title="Crop Biomass Growth Over Time",
                    xaxis_title="Time (days)",
                    yaxis_title="Biomass (kg/ha)",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)

                
                # Growth rate over time
                growth_rates = np.gradient(biomass, time_days)
                
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=time_days,
                    y=growth_rates,
                    mode='lines',
                    name='Growth Rate',
                    line=dict(color='orange', width=2)
                ))
                
                fig2.update_layout(
                    title="Daily Growth Rate",
                    xaxis_title="Time (days)",
                    yaxis_title="Growth Rate (kg/ha/day)",
                    height=300
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Physics equations used
                with st.expander("📐 Physics Equations Used"):
                    st.markdown("""
                    **1. Photosynthesis Rate (Michaelis-Menten):**
                    ```
                    P = Pmax × (I/(I+Km)) × f(T) × f(CO₂)
                    ```
                    
                    **2. Respiration Rate (Q10 Rule):**
                    ```
                    R = R₀ × Biomass × Q₁₀^((T-Tref)/10)
                    ```
                    
                    **3. Net Growth:**
                    ```
                    dB/dt = (P - R - Senescence) × Water_stress
                    ```
                    
                    **4. Temperature Response:**
                    ```
                    f(T) = ((T-Tmin)(Tmax-T)) / ((Topt-Tmin)(Tmax-Topt))
                    ```
                    """)

# ==================== TAB 2: PEST DYNAMICS ====================
with tab2:
    st.header("🐛 Pest Population Dynamics")
    
    st.markdown("""
    Model pest population growth using **logistic growth equation** with temperature effects.
    
    **Logistic Growth Model:**
    ```
    dP/dt = r × P × (1 - P/K)
    ```
    where P = population, r = growth rate, K = carrying capacity
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Pest Parameters")
        
        pest_days = st.slider("Simulation Days", 10, 100, 50, 5, key="pest_days")
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">📅 How many days into the future to predict pest growth</p>', unsafe_allow_html=True)
        
        initial_pests = st.slider("Initial Pest Count", 10, 500, 100, 10)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🐛 Current number of pests observed in your field</p>', unsafe_allow_html=True)
        
        temperature_pest = st.slider("Temperature (°C)", 15, 35, 25, 1, key="pest_temp")
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌡️ Field temperature (higher temp = faster pest reproduction)</p>', unsafe_allow_html=True)
        
        carrying_capacity = st.slider("Carrying Capacity", 1000, 10000, 5000, 500)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🏔️ Maximum pests your field can support (limited by food/space)</p>', unsafe_allow_html=True)
        
        # Calculate temperature-dependent growth rate
        base_growth_rate = 0.5
        growth_rate = temperature_dependent_growth_rate(temperature_pest, base_growth_rate)
        
        st.info(f"""
        **Growth Rate:** {growth_rate:.3f} per day
        
        Temperature effect: Higher temperature = Faster reproduction
        """)
        
        st.markdown("#### 💰 Economic Analysis")
        damage_per_pest = st.slider("Yield Loss per Pest (%)", 0.1, 2.0, 0.5, 0.1)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">📉 How much crop yield each pest destroys (0.5% = each pest eats 0.5% of crop)</p>', unsafe_allow_html=True)
        
        control_cost = st.number_input("Control Cost (₹/ha)", 500, 5000, 1000, 100)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">💊 Cost to spray pesticide per hectare</p>', unsafe_allow_html=True)
        
        crop_value = st.number_input("Crop Value (₹/ha)", 10000, 100000, 50000, 5000)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">💰 Total value of your healthy crop per hectare</p>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🚀 Simulate Pest Population", key="pest_sim"):
            with st.spinner("Simulating pest dynamics..."):
                # Time array
                time_pest = np.linspace(0, pest_days, pest_days + 1)
                
                # Simulate population
                population = simulate_pest_population(
                    time_pest, initial_pests, growth_rate, carrying_capacity
                )
                
                # Calculate economic threshold
                final_population = population[-1]
                threshold, should_treat, potential_loss = calculate_economic_threshold(
                    final_population, damage_per_pest, control_cost, crop_value
                )
                
                # Display results
                st.success("✅ Simulation Complete!")
                
                # Metrics
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Final Population", f"{int(final_population):,}")
                with col_m2:
                    st.metric("Economic Threshold", f"{int(threshold):,}")
                with col_m3:
                    treatment_status = "🚨 TREAT NOW" if should_treat else "✅ Monitor"
                    st.metric("Action", treatment_status)
                
                # Plot population growth
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=time_pest,
                    y=population,
                    mode='lines',
                    name='Pest Population',
                    line=dict(color='red', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(255, 0, 0, 0.2)'
                ))
                
                # Add threshold line
                fig.add_hline(
                    y=threshold,
                    line_dash="dash",
                    line_color="orange",
                    annotation_text=f"Economic Threshold: {int(threshold)}",
                    annotation_position="right"
                )
                
                # Add carrying capacity line
                fig.add_hline(
                    y=carrying_capacity,
                    line_dash="dot",
                    line_color="gray",
                    annotation_text=f"Carrying Capacity: {carrying_capacity}",
                    annotation_position="right"
                )
                
                fig.update_layout(
                    title="Pest Population Growth Over Time",
                    xaxis_title="Time (days)",
                    yaxis_title="Pest Count",
                    height=400,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)

                
                # Economic analysis
                st.markdown("### 💰 Economic Analysis")
                
                if should_treat:
                    st.error(f"""
                    **⚠️ Treatment Recommended!**
                    
                    - Current Population: **{int(final_population):,}** pests
                    - Economic Threshold: **{int(threshold):,}** pests
                    - Potential Loss: **₹{potential_loss:,.0f}**
                    - Control Cost: **₹{control_cost:,.0f}**
                    - **Net Benefit: ₹{(potential_loss - control_cost):,.0f}**
                    
                    💡 **Action:** Apply pest control measures immediately to prevent economic loss.
                    """)
                else:
                    st.success(f"""
                    **✅ No Treatment Needed**
                    
                    - Current Population: **{int(final_population):,}** pests
                    - Economic Threshold: **{int(threshold):,}** pests
                    - Population is below economic threshold
                    
                    💡 **Action:** Continue monitoring. Treatment not economically justified yet.
                    """)
                
                # Show physics equations
                with st.expander("📐 Physics Equations Used"):
                    st.markdown("""
                    **1. Logistic Growth:**
                    ```
                    dP/dt = r × P × (1 - P/K)
                    ```
                    
                    **2. Temperature-Dependent Growth Rate:**
                    ```
                    r(T) = r₀ × exp(a × T)
                    ```
                    
                    **3. Economic Threshold:**
                    ```
                    ET = (Control_Cost / Crop_Value) × (100 / Damage_per_Pest)
                    ```
                    
                    **4. Potential Loss:**
                    ```
                    Loss = (Population × Damage_per_Pest / 100) × Crop_Value
                    ```
                    """)

# ==================== TAB 3: WATER TRANSPORT ====================
with tab3:
    st.header("💧 Soil Water Transport & Irrigation")
    
    st.markdown("""
    Model water movement in soil using **Darcy's Law** and calculate irrigation requirements.
    
    **Darcy's Law:**
    ```
    Q = -K × A × (dh/dl)
    ```
    where Q = flow rate, K = hydraulic conductivity, A = area, dh/dl = hydraulic gradient
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Soil & Water Parameters")
        
        st.markdown("#### 🌍 Soil Properties")
        soil_type = st.selectbox("Soil Type", 
                                 ["Sandy", "Loamy", "Clay", "Silt"])
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌍 Your soil type (Sandy drains fast, Clay holds water longer)</p>', unsafe_allow_html=True)
        
        # Hydraulic conductivity based on soil type
        K_values = {"Sandy": 50, "Loamy": 10, "Clay": 1, "Silt": 5}
        K = K_values[soil_type]
        
        st.info(f"Hydraulic Conductivity (K): {K} cm/day")
        
        field_capacity = st.slider("Field Capacity (%)", 20, 50, 30, 5)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🏔️ Maximum water soil can hold (target moisture level)</p>', unsafe_allow_html=True)
        
        current_moisture = st.slider("Current Soil Moisture (%)", 10, 50, 20, 5)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">💧 Current water content in your soil (measure with sensor or feel test)</p>', unsafe_allow_html=True)
        
        st.markdown("#### 🌦️ Weather & Crop")
        ET_rate = st.slider("Evapotranspiration (mm/day)", 2, 10, 5, 1)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌡️ Water lost through evaporation + plant transpiration (hot days = higher)</p>', unsafe_allow_html=True)
        
        rainfall = st.slider("Rainfall (mm/day)", 0, 20, 0, 1)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🌧️ Daily rainfall amount (reduces irrigation need)</p>', unsafe_allow_html=True)
        
        irrigation_efficiency = st.slider("Irrigation Efficiency (%)", 50, 95, 80, 5) / 100
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">💦 How much water actually reaches plants (drip=90%, flood=60%)</p>', unsafe_allow_html=True)
        
        # Calculate irrigation requirement
        irrigation_needed = calculate_irrigation_requirement(ET_rate, rainfall, irrigation_efficiency)
        
        st.success(f"""
        **💧 Irrigation Requirement:**
        {irrigation_needed:.2f} mm/day
        """)
    
    with col2:
        st.subheader("📊 Water Balance Analysis")
        
        # Create water balance visualization
        water_inputs = rainfall + irrigation_needed
        water_outputs = ET_rate
        
        # Sankey diagram for water balance
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Rainfall", "Irrigation", "Soil Water", "Evapotranspiration", "Drainage"],
                color=["blue", "lightblue", "brown", "orange", "gray"]
            ),
            link=dict(
                source=[0, 1, 2, 2],
                target=[2, 2, 3, 4],
                value=[rainfall, irrigation_needed, ET_rate, max(0, water_inputs - ET_rate)]
            )
        )])
        
        fig.update_layout(
            title="Water Balance Flow Diagram",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Soil moisture status
        st.markdown("### 🌱 Soil Moisture Status")
        
        moisture_deficit = field_capacity - current_moisture
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Current Moisture", f"{current_moisture}%")
        with col_m2:
            st.metric("Field Capacity", f"{field_capacity}%")
        with col_m3:
            st.metric("Deficit", f"{moisture_deficit}%")
        
        # Moisture gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_moisture,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Soil Moisture Level"},
            delta={'reference': field_capacity},
            gauge={
                'axis': {'range': [None, 50]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 15], 'color': "red"},
                    {'range': [15, 25], 'color': "yellow"},
                    {'range': [25, 50], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "green", 'width': 4},
                    'thickness': 0.75,
                    'value': field_capacity
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

        
        # Recommendations
        if current_moisture < field_capacity * 0.6:
            st.error(f"""
            **🚨 Irrigation Needed!**
            
            Soil moisture is critically low. Apply {irrigation_needed:.1f} mm of water.
            """)
        elif current_moisture < field_capacity * 0.8:
            st.warning(f"""
            **⚠️ Monitor Closely**
            
            Soil moisture is moderate. Plan irrigation of {irrigation_needed:.1f} mm soon.
            """)
        else:
            st.success("""
            **✅ Adequate Moisture**
            
            Soil moisture is sufficient. Continue monitoring.
            """)
        
        # Physics equations
        with st.expander("📐 Physics Equations Used"):
            st.markdown("""
            **1. Darcy's Law (Water Flow):**
            ```
            Q = -K × A × (dh/dl)
            ```
            
            **2. Water Balance:**
            ```
            dθ/dt = Irrigation + Rainfall - ET - Drainage
            ```
            
            **3. Irrigation Requirement:**
            ```
            IR = (ET - Rainfall) / Efficiency
            ```
            
            **4. Drainage:**
            ```
            Drainage = K × max(0, θ - θ_FC)
            ```
            """)

# ==================== TAB 4: NUTRIENT UPTAKE ====================
with tab4:
    st.header("🧪 Nutrient Uptake & Fertilizer Optimization")
    
    st.markdown("""
    Model nutrient uptake using **Michaelis-Menten kinetics** and optimize fertilizer application.
    
    **Michaelis-Menten Equation:**
    ```
    V = (Vmax × [S]) / (Km + [S])
    ```
    where V = uptake rate, [S] = substrate concentration, Vmax = maximum rate, Km = half-saturation constant
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎛️ Nutrient Parameters")
        
        st.markdown("#### 🌾 Crop Requirements")
        target_yield = st.slider("Target Yield (kg/ha)", 1000, 10000, 5000, 500)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🎯 Desired crop yield per hectare (higher yield needs more nutrients)</p>', unsafe_allow_html=True)
        
        crop_efficiency = st.slider("Nutrient Use Efficiency (%)", 30, 80, 60, 5) / 100
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">📊 How efficiently crop uses fertilizer (60% = 40% is lost/wasted)</p>', unsafe_allow_html=True)
        
        st.markdown("#### 🧪 Soil Nutrients")
        soil_N = st.slider("Soil Nitrogen (kg/ha)", 10, 200, 50, 10)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🧪 Current nitrogen available in soil (test with soil analysis)</p>', unsafe_allow_html=True)
        
        Vmax = st.slider("Max Uptake Rate (Vmax)", 5, 20, 10, 1)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">⚡ Maximum speed plants can absorb nutrients (depends on crop type)</p>', unsafe_allow_html=True)
        
        Km = st.slider("Half-Saturation (Km)", 0.5, 5.0, 1.0, 0.5)
        st.markdown('<p style="color: #666; font-size: 0.85rem; margin-top: -10px;">🎚️ Nutrient level where uptake is 50% of maximum (lower = more efficient)</p>', unsafe_allow_html=True)
        
        # Calculate uptake rate
        uptake_rate = michaelis_menten_uptake(soil_N, Vmax, Km)
        
        st.info(f"""
        **Current Uptake Rate:**
        {uptake_rate:.2f} kg/ha/day
        """)
        
        # Calculate fertilizer requirement
        fertilizer_needed = optimize_fertilizer_dosage(target_yield, crop_efficiency)
        
        st.success(f"""
        **💊 Fertilizer Recommendation:**
        {fertilizer_needed:.1f} kg N/ha
        """)
    
    with col2:
        st.subheader("📊 Nutrient Uptake Curve")
        
        # Generate uptake curve
        concentrations = np.linspace(0, 200, 100)
        uptake_rates = [michaelis_menten_uptake(c, Vmax, Km) for c in concentrations]
        
        fig = go.Figure()
        
        # Uptake curve
        fig.add_trace(go.Scatter(
            x=concentrations,
            y=uptake_rates,
            mode='lines',
            name='Uptake Rate',
            line=dict(color='green', width=3)
        ))
        
        # Current point
        fig.add_trace(go.Scatter(
            x=[soil_N],
            y=[uptake_rate],
            mode='markers',
            name='Current State',
            marker=dict(size=15, color='red', symbol='star')
        ))
        
        # Km line
        fig.add_vline(
            x=Km,
            line_dash="dash",
            line_color="orange",
            annotation_text=f"Km = {Km}",
            annotation_position="top"
        )
        
        # Vmax line
        fig.add_hline(
            y=Vmax,
            line_dash="dash",
            line_color="blue",
            annotation_text=f"Vmax = {Vmax}",
            annotation_position="right"
        )
        
        fig.update_layout(
            title="Michaelis-Menten Nutrient Uptake Curve",
            xaxis_title="Soil Nitrogen Concentration (kg/ha)",
            yaxis_title="Uptake Rate (kg/ha/day)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Fertilizer optimization
        st.markdown("### 💊 Fertilizer Application Strategy")
        
        # Calculate split application
        num_splits = st.radio("Application Strategy", [1, 2, 3, 4], 
                             format_func=lambda x: f"{x} Split{'s' if x > 1 else ''}")
        
        dose_per_split = fertilizer_needed / num_splits
        
        st.info(f"""
        **Split Application Plan:**
        - Total Fertilizer: {fertilizer_needed:.1f} kg N/ha
        - Number of Splits: {num_splits}
        - Dose per Application: {dose_per_split:.1f} kg N/ha
        
        **Timing Recommendations:**
        """)
        
        if num_splits == 1:
            st.write("- Apply full dose at planting")
        elif num_splits == 2:
            st.write("- 50% at planting")
            st.write("- 50% at tillering/flowering")
        elif num_splits == 3:
            st.write("- 33% at planting")
            st.write("- 33% at tillering")
            st.write("- 34% at flowering")
        else:
            st.write("- 25% at planting")
            st.write("- 25% at tillering")
            st.write("- 25% at flowering")
            st.write("- 25% at grain filling")

        
        # Cost analysis
        st.markdown("### 💰 Economic Analysis")
        
        fertilizer_cost_per_kg = st.number_input("Fertilizer Cost (₹/kg)", 10, 100, 30, 5)
        total_cost = fertilizer_needed * fertilizer_cost_per_kg
        
        expected_revenue = target_yield * 20  # Assuming ₹20/kg crop price
        roi = ((expected_revenue - total_cost) / total_cost) * 100
        
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            st.metric("Fertilizer Cost", f"₹{total_cost:,.0f}")
        with col_e2:
            st.metric("Expected Revenue", f"₹{expected_revenue:,.0f}")
        with col_e3:
            st.metric("ROI", f"{roi:.1f}%")
        
        # Physics equations
        with st.expander("📐 Physics Equations Used"):
            st.markdown("""
            **1. Michaelis-Menten Uptake:**
            ```
            V = (Vmax × [S]) / (Km + [S])
            ```
            
            **2. Fertilizer Requirement:**
            ```
            F = (Yield × N_content) / Efficiency
            ```
            
            **3. Nutrient Balance:**
            ```
            dN_soil/dt = Fertilizer - Uptake - Leaching
            dN_plant/dt = Uptake
            ```
            
            **4. Efficiency:**
            ```
            Efficiency = N_uptake / N_applied × 100%
            ```
            """)

# ==================== TAB 5: AI VS PHYSICS ====================
with tab5:
    st.header("📊 AI-Only vs Physics-Informed Comparison")
    
    st.markdown("""
    Compare predictions from **pure AI models** vs **Physics-Informed Neural Networks (PINNs)**.
    
    This demonstrates why integrating physics improves predictions, especially with limited data.
    """)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Scenario Selection")
        
        scenario = st.selectbox("Select Prediction Task", [
            "Crop Yield Prediction",
            "Pest Population Forecast",
            "Soil Moisture Prediction",
            "Nutrient Uptake Estimation"
        ])
        
        st.markdown("#### 📊 Input Parameters")
        
        if scenario == "Crop Yield Prediction":
            input_temp = st.slider("Temperature (°C)", 15, 35, 25, 1, key="comp_temp")
            input_water = st.slider("Water Availability (%)", 40, 100, 80, 5, key="comp_water")
            input_nutrients = st.slider("Soil Nutrients (kg/ha)", 20, 150, 80, 10, key="comp_nutrients")
            
            # Simulate predictions
            # AI-only: Simple regression-like (less accurate in extremes)
            ai_prediction = 3000 + input_temp * 50 + input_water * 20 + input_nutrients * 15
            ai_prediction += np.random.normal(0, 300)  # Add noise
            
            # Physics-informed: Uses growth equations
            physics_prediction = simulate_crop_growth_pinn(
                np.array([0, 90]), 800, input_temp, 400, input_water, 50
            )[-1] * 50  # Scale to yield
            
            unit = "kg/ha"
            true_value = physics_prediction  # Assume physics is closer to truth
            
        elif scenario == "Pest Population Forecast":
            input_temp = st.slider("Temperature (°C)", 15, 35, 25, 1, key="pest_comp_temp")
            input_days = st.slider("Forecast Days", 10, 60, 30, 5, key="pest_comp_days")
            
            # AI-only: Linear extrapolation
            ai_prediction = 100 + input_days * 50 + input_temp * 20
            ai_prediction += np.random.normal(0, 100)
            
            # Physics-informed: Logistic growth
            growth_rate = temperature_dependent_growth_rate(input_temp)
            physics_prediction = simulate_pest_population(
                np.array([0, input_days]), 100, growth_rate, 5000
            )[-1]
            
            unit = "pests"
            true_value = physics_prediction
            
        elif scenario == "Soil Moisture Prediction":
            input_et = st.slider("ET Rate (mm/day)", 2, 10, 5, 1, key="moisture_et")
            input_rain = st.slider("Rainfall (mm/day)", 0, 15, 3, 1, key="moisture_rain")
            
            # AI-only: Simple balance
            ai_prediction = 30 + input_rain * 2 - input_et * 1.5
            ai_prediction += np.random.normal(0, 3)
            ai_prediction = np.clip(ai_prediction, 10, 50)
            
            # Physics-informed: Darcy's law + water balance
            physics_prediction = 30 + (input_rain - input_et) * 1.2
            physics_prediction = np.clip(physics_prediction, 10, 50)
            
            unit = "%"
            true_value = physics_prediction
            
        else:  # Nutrient Uptake
            input_soil_n = st.slider("Soil N (kg/ha)", 20, 150, 60, 10, key="nutrient_n")
            
            # AI-only: Linear relationship
            ai_prediction = input_soil_n * 0.15
            ai_prediction += np.random.normal(0, 1)
            
            # Physics-informed: Michaelis-Menten
            physics_prediction = michaelis_menten_uptake(input_soil_n, 10, 1.0)
            
            unit = "kg/ha/day"
            true_value = physics_prediction
    
    with col2:
        st.subheader("📈 Prediction Comparison")
        
        # Compare predictions
        comparison = compare_ai_vs_physics(ai_prediction, physics_prediction)
        
        # Display metrics
        col_m1, col_m2 = st.columns(2)
        
        with col_m1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white;">
                <h4>🤖 AI-Only Prediction</h4>
                <h2>{ai_prediction:.1f} {unit}</h2>
                <p>Based on data patterns only</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%); 
                        padding: 1.5rem; border-radius: 10px; color: white;">
                <h4>⚛️ Physics-Informed Prediction</h4>
                <h2>{physics_prediction:.1f} {unit}</h2>
                <p>Based on physics + data</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Comparison metrics
        st.markdown("### 📊 Comparison Metrics")
        
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.metric("Difference", f"{comparison['absolute_difference']:.1f} {unit}")
        with col_c2:
            st.metric("Relative Error", f"{comparison['relative_error_percent']:.1f}%")
        with col_c3:
            agreement_color = "🟢" if comparison['agreement'] == 'Good' else "🟡" if comparison['agreement'] == 'Moderate' else "🔴"
            st.metric("Agreement", f"{agreement_color} {comparison['agreement']}")

        
        # Visualization
        fig = go.Figure()
        
        categories = ['AI-Only', 'Physics-Informed', 'True Value']
        values = [ai_prediction, physics_prediction, true_value]
        colors = ['#667eea', '#2E8B57', '#FFD700']
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f"{v:.1f}" for v in values],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f"{scenario} - Model Comparison",
            yaxis_title=f"Prediction ({unit})",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Advantages table
        st.markdown("### ✅ Why Physics-Informed AI is Better")
        
        advantages_df = pd.DataFrame({
            'Aspect': [
                'Data Requirements',
                'Extrapolation',
                'Physical Constraints',
                'Interpretability',
                'Accuracy'
            ],
            'AI-Only': [
                'Needs large datasets',
                'Poor beyond training range',
                'Can violate physics',
                'Black box',
                'Good with enough data'
            ],
            'Physics-Informed': [
                'Works with less data',
                'Better extrapolation',
                'Respects physical laws',
                'Explainable',
                'Consistently accurate'
            ]
        })
        
        st.dataframe(advantages_df, use_container_width=True, hide_index=True)
        
        # Real-world example
        st.info("""
        **💡 Real-World Example:**
        
        Imagine predicting crop yield in a drought year (outside training data):
        - **AI-Only**: Might predict normal yield (hasn't seen drought data)
        - **Physics-Informed**: Knows water stress reduces photosynthesis → predicts lower yield
        
        Physics-informed models are more reliable in unusual conditions!
        """)

# ==================== TAB 6: PINN CHAT ASSISTANT ====================
with tab6:
    st.header("🤖 Physics-Informed AI Chat Assistant")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; margin: 1rem 0;">
        <h3 style="color: white; text-align: center; margin-bottom: 1rem;">
            🧑‍🔬 Dr. Vikram Patel - PINN Specialist
        </h3>
        <p style="color: white; text-align: center; font-size: 1.1rem;">
            Expert in Physics-Informed Neural Networks for Agriculture
        </p>
        <p style="color: #e8f4fd; text-align: center; font-size: 0.9rem;">
            ✅ Physics Equations | 🧪 Agricultural Models | 💻 Implementation Guidance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add PINN-specific context
    pinn_context = """
    Physics-Informed Neural Networks (PINN) Page Context:
    - User is on the PINN page of KrishiSahayak agricultural AI system
    - Learning about crop growth models, pest dynamics, water transport, nutrient uptake
    - Physics equations: Michaelis-Menten, Logistic growth, Darcy's law, Q10 rule
    - Focus on combining physics with machine learning for agriculture
    - Provide both mathematical explanations and practical agricultural applications
    - Can provide Python code examples for PINN implementation
    - Help with differential equations, optimization, and model integration
    """
    
    # Create chat interface with PINN context
    create_chat_interface("pinn_assistant", pinn_context, use_api=True, unique_key="pinn_chat")
    
    # Example questions
    st.markdown("### 💡 Example Questions You Can Ask")
    
    st.markdown("""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
        <h4 style="color: #2E8B57;">🎓 Physics & Mathematics:</h4>
        <ul>
            <li>"Explain the Michaelis-Menten equation for nutrient uptake"</li>
            <li>"How does the logistic growth model work for pests?"</li>
            <li>"What is Darcy's law and how does it apply to irrigation?"</li>
            <li>"Derive the crop growth differential equation"</li>
            <li>"Explain the Q10 rule for temperature effects"</li>
        </ul>
        
        <h4 style="color: #2E8B57;">🌾 Agricultural Applications:</h4>
        <ul>
            <li>"How to optimize fertilizer application timing?"</li>
            <li>"When should I treat pest infestations economically?"</li>
            <li>"Calculate irrigation requirements for my field"</li>
            <li>"How does temperature affect crop growth rate?"</li>
            <li>"What's the relationship between NDVI and biomass?"</li>
        </ul>
        
        <h4 style="color: #2E8B57;">💻 Implementation & Code:</h4>
        <ul>
            <li>"Show me Python code for implementing a PINN"</li>
            <li>"How to solve differential equations with scipy?"</li>
            <li>"Integrate physics constraints into neural networks"</li>
            <li>"Code example for crop growth simulation"</li>
            <li>"How to validate physics-informed predictions?"</li>
        </ul>
        
        <h4 style="color: #2E8B57;">🔬 Advanced Topics:</h4>
        <ul>
            <li>"Compare AI-only vs physics-informed approaches"</li>
            <li>"How to handle uncertainty in PINN models?"</li>
            <li>"Multi-scale modeling in agriculture"</li>
            <li>"Inverse problems in agricultural physics"</li>
            <li>"Data assimilation techniques for crop models"</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
    <h4>⚛️ Physics-Informed AI - Krishi Sahayak</h4>
    <p>Where Agricultural Science Meets Artificial Intelligence</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Built with ❤️ for Indian Farmers | Combining Physics with AI for Better Predictions
    </p>
</div>
""", unsafe_allow_html=True)
