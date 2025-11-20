"""
Physics-Informed Neural Network Models
Implements agricultural physics equations and simulations
"""

import numpy as np
from scipy.integrate import odeint
import streamlit as st

# ==================== CROP GROWTH MODELS ====================

def photosynthesis_rate(light_intensity, temperature, co2_concentration, 
                       Pmax=30, Km_light=500, T_opt=25, CO2_opt=400):
    """
    Calculate photosynthesis rate based on environmental factors
    
    Args:
        light_intensity: Light intensity (μmol/m²/s)
        temperature: Temperature (°C)
        co2_concentration: CO₂ concentration (ppm)
        Pmax: Maximum photosynthesis rate
        Km_light: Half-saturation constant for light
        T_opt: Optimal temperature
        CO2_opt: Optimal CO₂ concentration
    
    Returns:
        P: Photosynthesis rate (μmol CO₂/m²/s)
    """
    # Light response (Michaelis-Menten)
    f_light = light_intensity / (light_intensity + Km_light)
    
    # Temperature response (cardinal temperature model)
    T_min, T_max = 10, 40
    if temperature < T_min or temperature > T_max:
        f_temp = 0
    else:
        f_temp = ((temperature - T_min) * (T_max - temperature)) / \
                 ((T_opt - T_min) * (T_max - T_opt))
    
    # CO₂ response
    f_co2 = co2_concentration / (co2_concentration + CO2_opt)
    
    # Combined photosynthesis rate
    P = Pmax * f_light * f_temp * f_co2
    
    return P


def respiration_rate(temperature, biomass, R0=2.0, Q10=2.0, T_ref=20):
    """
    Calculate respiration rate using Q10 rule
    
    Args:
        temperature: Temperature (°C)
        biomass: Current biomass (kg/ha)
        R0: Base respiration rate
        Q10: Temperature coefficient
        T_ref: Reference temperature
    
    Returns:
        R: Respiration rate
    """
    R = R0 * biomass * (Q10 ** ((temperature - T_ref) / 10))
    return R


def crop_growth_model(state, t, params):
    """
    Differential equation for crop growth
    
    Args:
        state: Current state [biomass]
        t: Time (days)
        params: Dictionary of parameters
    
    Returns:
        dB_dt: Rate of biomass change
    """
    biomass = state[0]
    
    # Extract parameters
    light = params['light_intensity']
    temp = params['temperature']
    co2 = params['co2_concentration']
    water = params['water_availability']
    
    # Photosynthesis
    P = photosynthesis_rate(light, temp, co2)
    
    # Respiration
    R = respiration_rate(temp, biomass)
    
    # Senescence (age-dependent)
    senescence = 0.01 * biomass * (t / 100)
    
    # Water stress factor
    water_stress = water / 100.0
    
    # Net growth
    dB_dt = (P - R - senescence) * water_stress * 10  # Scaling factor
    
    return [dB_dt]


def simulate_crop_growth_pinn(time_days, light_intensity, temperature, 
                              co2_concentration, water_availability, initial_biomass):
    """
    Run PINN simulation for crop growth
    
    Args:
        time_days: Array of time points
        light_intensity: Light intensity
        temperature: Temperature
        co2_concentration: CO₂ concentration
        water_availability: Water availability (%)
        initial_biomass: Initial biomass (kg/ha)
    
    Returns:
        biomass: Array of biomass over time
    """
    params = {
        'light_intensity': light_intensity,
        'temperature': temperature,
        'co2_concentration': co2_concentration,
        'water_availability': water_availability
    }
    
    # Solve ODE
    solution = odeint(crop_growth_model, [initial_biomass], time_days, args=(params,))
    biomass = solution[:, 0]
    
    # Ensure non-negative
    biomass = np.maximum(biomass, 0)
    
    return biomass


# ==================== NDVI & BIOMASS MODELS ====================

def calculate_lai_from_ndvi(ndvi, a=0.5, b=2.0):
    """
    Estimate Leaf Area Index from NDVI using empirical relationship
    
    Args:
        ndvi: NDVI value (-1 to 1)
        a, b: Empirical coefficients
    
    Returns:
        LAI: Leaf Area Index
    """
    # Clip NDVI to valid range
    ndvi = np.clip(ndvi, -1, 1)
    
    # Empirical relationship
    LAI = a * np.exp(b * ndvi)
    
    return LAI


def beer_lambert_law(I0, LAI, k=0.5):
    """
    Calculate light transmission through canopy using Beer-Lambert Law
    
    Args:
        I0: Incident light intensity
        LAI: Leaf Area Index
        k: Extinction coefficient
    
    Returns:
        I: Transmitted light intensity
    """
    I = I0 * np.exp(-k * LAI)
    return I


def estimate_biomass_from_ndvi(ndvi, a=1000, b=1.5):
    """
    Estimate biomass from NDVI
    
    Args:
        ndvi: NDVI value
        a, b: Empirical coefficients
    
    Returns:
        biomass: Estimated biomass (kg/ha)
    """
    LAI = calculate_lai_from_ndvi(ndvi)
    biomass = a * (LAI ** b)
    return biomass


# ==================== PEST POPULATION DYNAMICS ====================

def logistic_growth(P, t, r, K):
    """
    Logistic growth model for pest population
    
    Args:
        P: Current population
        t: Time
        r: Growth rate
        K: Carrying capacity
    
    Returns:
        dP_dt: Rate of population change
    """
    dP_dt = r * P * (1 - P / K)
    return dP_dt


def temperature_dependent_growth_rate(temperature, r0=0.5, a=0.05):
    """
    Calculate temperature-dependent growth rate
    
    Args:
        temperature: Temperature (°C)
        r0: Base growth rate
        a: Temperature coefficient
    
    Returns:
        r: Growth rate at given temperature
    """
    r = r0 * np.exp(a * temperature)
    return r


def simulate_pest_population(time_days, initial_population, growth_rate, carrying_capacity):
    """
    Simulate pest population dynamics
    
    Args:
        time_days: Array of time points
        initial_population: Initial pest count
        growth_rate: Population growth rate
        carrying_capacity: Maximum sustainable population
    
    Returns:
        population: Array of population over time
    """
    solution = odeint(logistic_growth, initial_population, time_days, 
                     args=(growth_rate, carrying_capacity))
    population = solution[:, 0]
    
    return population


def calculate_economic_threshold(pest_population, damage_per_pest=0.5, 
                                control_cost=1000, crop_value=50000):
    """
    Calculate economic threshold for pest control
    
    Args:
        pest_population: Current pest population
        damage_per_pest: Yield loss per pest (%)
        control_cost: Cost of control measure (₹/ha)
        crop_value: Value of crop (₹/ha)
    
    Returns:
        threshold: Economic threshold
        should_treat: Boolean indicating if treatment is needed
    """
    # Calculate potential loss
    potential_loss = (pest_population * damage_per_pest / 100) * crop_value
    
    # Economic threshold
    threshold = (control_cost / crop_value) * (100 / damage_per_pest)
    
    should_treat = pest_population > threshold
    
    return threshold, should_treat, potential_loss


# ==================== NUTRIENT UPTAKE MODELS ====================

def michaelis_menten_uptake(concentration, Vmax=10, Km=1.0):
    """
    Michaelis-Menten kinetics for nutrient uptake
    
    Args:
        concentration: Nutrient concentration in soil
        Vmax: Maximum uptake rate
        Km: Michaelis constant (half-saturation)
    
    Returns:
        V: Uptake rate
    """
    V = (Vmax * concentration) / (Km + concentration)
    return V


def nutrient_balance_model(state, t, params):
    """
    Nutrient balance in soil-plant system
    
    Args:
        state: [soil_N, plant_N]
        t: Time
        params: Parameters dictionary
    
    Returns:
        derivatives: [dN_soil/dt, dN_plant/dt]
    """
    soil_N, plant_N = state
    
    # Uptake rate
    uptake = michaelis_menten_uptake(soil_N, params['Vmax'], params['Km'])
    
    # Leaching (simplified)
    leaching = params['leaching_rate'] * soil_N
    
    # Fertilizer application (if any)
    fertilizer = params.get('fertilizer_rate', 0)
    
    # Soil nitrogen change
    dN_soil_dt = fertilizer - uptake - leaching
    
    # Plant nitrogen change
    dN_plant_dt = uptake
    
    return [dN_soil_dt, dN_plant_dt]


def optimize_fertilizer_dosage(target_yield, crop_efficiency=0.6, N_content=0.02):
    """
    Calculate optimal fertilizer dosage
    
    Args:
        target_yield: Target yield (kg/ha)
        crop_efficiency: Nutrient use efficiency
        N_content: Nitrogen content in crop (fraction)
    
    Returns:
        fertilizer_needed: Fertilizer requirement (kg N/ha)
    """
    # Nitrogen requirement
    N_required = target_yield * N_content
    
    # Account for efficiency
    fertilizer_needed = N_required / crop_efficiency
    
    return fertilizer_needed


# ==================== WATER TRANSPORT MODELS ====================

def darcy_law(K, A, dh, dl):
    """
    Darcy's Law for water flow through soil
    
    Args:
        K: Hydraulic conductivity (cm/day)
        A: Cross-sectional area (cm²)
        dh: Hydraulic head difference (cm)
        dl: Flow path length (cm)
    
    Returns:
        Q: Water flow rate (cm³/day)
    """
    Q = -K * A * (dh / dl)
    return Q


def soil_water_balance(state, t, params):
    """
    Soil water balance model
    
    Args:
        state: [soil_moisture]
        t: Time
        params: Parameters
    
    Returns:
        dθ_dt: Rate of moisture change
    """
    theta = state[0]
    
    # Inputs
    irrigation = params.get('irrigation', 0)
    rainfall = params.get('rainfall', 0)
    
    # Outputs
    ET = params['evapotranspiration']
    drainage = params['drainage_rate'] * max(0, theta - params['field_capacity'])
    
    # Water balance
    dtheta_dt = irrigation + rainfall - ET - drainage
    
    return [dtheta_dt]


def calculate_irrigation_requirement(ET, rainfall, efficiency=0.8):
    """
    Calculate irrigation water requirement
    
    Args:
        ET: Evapotranspiration (mm/day)
        rainfall: Rainfall (mm/day)
        efficiency: Irrigation efficiency
    
    Returns:
        irrigation_needed: Irrigation requirement (mm/day)
    """
    net_requirement = max(0, ET - rainfall)
    irrigation_needed = net_requirement / efficiency
    
    return irrigation_needed


# ==================== TEMPERATURE EFFECTS ====================

def arrhenius_equation(temperature, A=1e6, Ea=50000, R=8.314):
    """
    Arrhenius equation for temperature effect on reaction rates
    
    Args:
        temperature: Temperature (°C)
        A: Pre-exponential factor
        Ea: Activation energy (J/mol)
        R: Gas constant (J/mol/K)
    
    Returns:
        k: Rate constant
    """
    T_kelvin = temperature + 273.15
    k = A * np.exp(-Ea / (R * T_kelvin))
    return k


def cardinal_temperature_response(temperature, T_min=10, T_opt=25, T_max=40):
    """
    Cardinal temperature model for crop growth
    
    Args:
        temperature: Current temperature (°C)
        T_min: Minimum temperature
        T_opt: Optimal temperature
        T_max: Maximum temperature
    
    Returns:
        f_T: Temperature response factor (0-1)
    """
    if temperature < T_min or temperature > T_max:
        return 0.0
    
    f_T = ((temperature - T_min) * (T_max - temperature)) / \
          ((T_opt - T_min) * (T_max - T_opt))
    
    return max(0, f_T)


def calculate_thermal_time(temperature, T_base=10):
    """
    Calculate thermal time (growing degree days)
    
    Args:
        temperature: Daily temperature (°C)
        T_base: Base temperature
    
    Returns:
        GDD: Growing degree days
    """
    GDD = max(0, temperature - T_base)
    return GDD


# ==================== UTILITY FUNCTIONS ====================

def validate_physics_constraints(predictions, constraints):
    """
    Check if predictions violate physical constraints
    
    Args:
        predictions: Model predictions
        constraints: Dictionary of constraints
    
    Returns:
        violations: List of constraint violations
    """
    violations = []
    
    for key, (min_val, max_val) in constraints.items():
        if key in predictions:
            value = predictions[key]
            if value < min_val:
                violations.append(f"{key} below minimum: {value} < {min_val}")
            if value > max_val:
                violations.append(f"{key} above maximum: {value} > {max_val}")
    
    return violations


def compare_ai_vs_physics(ai_prediction, physics_prediction):
    """
    Compare AI-only vs Physics-informed predictions
    
    Args:
        ai_prediction: Prediction from AI model
        physics_prediction: Prediction from physics-informed model
    
    Returns:
        comparison: Dictionary of comparison metrics
    """
    difference = abs(ai_prediction - physics_prediction)
    relative_error = difference / (physics_prediction + 1e-10) * 100
    
    comparison = {
        'ai_prediction': float(ai_prediction),
        'physics_prediction': float(physics_prediction),
        'absolute_difference': float(difference),
        'relative_error_percent': float(relative_error),
        'agreement': 'Good' if relative_error < 10 else 'Moderate' if relative_error < 25 else 'Poor'
    }
    
    return comparison
