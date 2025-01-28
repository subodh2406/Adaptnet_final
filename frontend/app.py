# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import requests
# import streamlit as st

# # Configure page
# st.set_page_config(
#     page_title="AdaptNet™ Climate Adaptation Recommendation System",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for styling
# st.markdown("""
# <style>
#     .main {
#         background-color: #1E1E1E;
#         color: #FFFFFF;
#     }
#     .stSlider {
#         background-color: #2D2D2D;
#     }
#     .stTextInput {
#         background-color: #2D2D2D;
#     }
#     .section-header {
#         color: #4FD1C5;
#         font-size: 1.2em;
#         font-weight: bold;
#         margin-bottom: 1em;
#     }
#     .subsection {
#         background-color: #2D2D2D;
#         padding: 1em;
#         border-radius: 5px;
#         margin-bottom: 1em;
#     }
# </style>
# """, unsafe_allow_html=True)

# # API endpoint
# API_URL = "http://127.0.0.1:8000/predict"

# # Title and description
# st.title("AdaptNet™ Climate Adaptation Recommendation System")
# st.markdown("Welcome to AdaptNet™, your comprehensive climate adaptation planning assistant. Get detailed recommendations for adaptation measures based on your local conditions.")
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# Configure page
st.set_page_config(
    page_title="AdaptNet™ Climate Adaptation Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stSlider {
        background-color: #2D2D2D;
    }
    .stTextInput {
        background-color: #2D2D2D;
    }
    .section-header {
        color: #4FD1C5;
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 1em;
    }
    .subsection {
        background-color: #2D2D2D;
        padding: 1em;
        border-radius: 5px;
        margin-bottom: 1em;
    }
</style>
""", unsafe_allow_html=True)

# API endpoint
API_URL = "https://adaptnet-final-j2oc.onrender.com/predict"  # Updated API URL

# Title and description
st.title("AdaptNet™ Climate Adaptation Recommendation System")
st.markdown("Welcome to AdaptNet™, your comprehensive climate adaptation planning assistant. Get detailed recommendations for adaptation measures based on your local conditions.")

def generate_detailed_recommendations(cluster):
    """Generate detailed adaptation recommendations based on cluster"""
    base_recommendations = {
        0: {
            "risk_level": "Low Vulnerability",
            "priority": "Monitor and Maintain",
            "actions": [
                "Implement regular monitoring systems for climate indicators",
                "Develop early warning systems for extreme weather events",
                "Create community awareness programs",
                "Establish baseline data collection protocols"
            ],
            "timeline": "1-2 years",
            "estimated_cost": "Low to Medium"
        },
        1: {
            "risk_level": "Moderate Vulnerability",
            "priority": "Preventive Action",
            "actions": [
                "Upgrade existing infrastructure for climate resilience",
                "Implement water conservation measures",
                "Develop heat action plans",
                "Establish green corridors and urban forests"
            ],
            "timeline": "2-3 years",
            "estimated_cost": "Medium"
        },
        2: {
            "risk_level": "High Vulnerability",
            "priority": "Immediate Action Required",
            "actions": [
                "Develop comprehensive flood management systems",
                "Implement drought-resistant agriculture practices",
                "Establish community cooling centers",
                "Create disaster response protocols"
            ],
            "timeline": "1-2 years",
            "estimated_cost": "High"
        },
        3: {
            "risk_level": "Very High Vulnerability",
            "priority": "Urgent Intervention",
            "actions": [
                "Relocate vulnerable communities from high-risk areas",
                "Implement major infrastructure reinforcement",
                "Develop comprehensive water management systems",
                "Create emergency response centers"
            ],
            "timeline": "Immediate",
            "estimated_cost": "Very High"
        },
        4: {
            "risk_level": "Extreme Vulnerability",
            "priority": "Critical Emergency Response",
            "actions": [
                "Immediate evacuation planning for high-risk areas",
                "Rapid deployment of emergency infrastructure",
                "Implementation of crisis management systems",
                "International aid coordination"
            ],
            "timeline": "Immediate",
            "estimated_cost": "Extremely High"
        }
    }
    return base_recommendations.get(cluster, {})

def display_impact_analysis(features, cluster, recommendations):
    """Display detailed impact analysis visualizations"""
    st.subheader("Vulnerability Assessment")
    
    # Create vulnerability radar chart
    categories = ['Climate Risk', 'Infrastructure', 'Socio-Economic', 'Resource Capacity']
    
    # Calculate vulnerability scores
    climate_risk = (abs(features.get('Temperature_Anomaly', 0)) + 
                   abs(features.get('Precipitation_Change', 0))/100) * 5
    infrastructure = features.get('water_access', 50)/100 * 5
    socio_economic = features.get('poverty_rate', 50)/100 * 5
    resource = min(features.get('adaptation_budget', 1000)/10000 * 5, 5)  # Cap at 5

    values = [climate_risk, infrastructure, socio_economic, resource]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Vulnerability Scores'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False
    )
    
    st.plotly_chart(fig)

    # Cost-Benefit Analysis
    st.subheader("Cost-Benefit Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Costs")
        st.write(f"**Implementation:** {recommendations['estimated_cost']}")
        st.write(f"**Timeline:** {recommendations['timeline']}")
        st.write("**Resource Requirements:** Medium to High")
        st.write("**Training Needs:** Significant")
    
    with col2:
        st.write("#### Benefits")
        st.write("**Risk Reduction:** Significant")
        st.write("**Community Resilience:** Enhanced")
        st.write("**Economic Benefits:** Long-term positive")
        st.write("**Environmental Impact:** Positive")

# Create tabs
tabs = st.tabs(["Data Parameters", "Recommendations", "Impact Analysis"])

with tabs[0]:
    # Create three columns for main sections
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<p class="section-header">🌡️ Climate Parameters</p>', unsafe_allow_html=True)
        with st.container():
            temperature = st.number_input("Temperature Anomaly (°C)", value=0.0, format="%.2f")
            precipitation = st.number_input("Precipitation Change (%)", value=0.0, format="%.2f")
            drought = st.number_input("Drought Index (-4 to 4)", value=0.0, min_value=-4.0, max_value=4.0, format="%.2f")
            relative_humidity = st.number_input("Relative Humidity (%)", value=0.0, format="%.2f")
            average_wind = st.number_input("Average Wind Speed (km/h)", value=0.0, format="%.2f")
            extreme_events = st.number_input("Extreme Events Frequency", value=0.0, format="%.2f")

        st.markdown('<p class="section-header">🌍 Geographic Context</p>', unsafe_allow_html=True)
        with st.container():
            latitude = st.number_input("Latitude", value=0.0, format="%.2f")
            longitude = st.number_input("Longitude", value=0.0, format="%.2f")
            elevation = st.number_input("Elevation (meters)", value=0.0, format="%.2f")
            land_type = st.selectbox("Land Type", 
                ["Coastal", "Inland", "Mountain", "Desert", "Forest"])
            biome = st.selectbox("Biome/Ecosystem", 
                ["Tropical", "Temperate", "Boreal", "Arctic", "Mediterranean"])

    with col2:
        st.markdown('<p class="section-header">👥 Socio-Economic Factors</p>', unsafe_allow_html=True)
        with st.container():
            population = st.number_input("Population Size", value=0, format="%d")
            density = st.number_input("Population Density (per km²)", value=0.0, format="%.2f")
            gdp = st.number_input("GDP per capita (USD)", value=0.0, format="%.2f")
            development = st.selectbox("Development Level",
                ["Low", "Medium", "High", "Very High"])
            poverty_rate = st.number_input("Poverty Rate (%)", value=0.0, format="%.2f")
            literacy = st.number_input("Literacy Rate (%)", value=0.0, format="%.2f")

        st.markdown('<p class="section-header">🏗️ Infrastructure Status</p>', unsafe_allow_html=True)
        with st.container():
            infra_quality = st.select_slider("Infrastructure Quality",
                options=["Poor", "Fair", "Good", "Excellent"])
            water_access = st.number_input("Water Infrastructure Access (%)", value=0.0, format="%.2f")
            energy_access = st.number_input("Energy Infrastructure Access (%)", value=0.0, format="%.2f")

    with col3:
        st.markdown('<p class="section-header">💪 Resource Capacity</p>', unsafe_allow_html=True)
        with st.container():
            adaptation_budget = st.number_input("Adaptation Budget (USD)", value=0, format="%d")
            tech_capacity = st.select_slider("Technical Capacity",
                options=["Low", "Medium", "High"])
            institutional = st.select_slider("Institutional Readiness",
                options=["Limited", "Moderate", "Strong"])

        st.markdown('<p class="section-header">🤝 Community & Governance</p>', unsafe_allow_html=True)
        with st.container():
            governance = st.select_slider("Governance Structure",
                options=["Centralized", "Mixed", "Decentralized"])
            community = st.select_slider("Community Engagement Level",
                options=["Low", "Medium", "High"])
            stakeholder = st.select_slider("Stakeholder Support",
                options=["Limited", "Moderate", "Strong"])

    # Prediction button
    if st.button("Generate Adaptation Recommendations", type="primary"):
        # Prepare input data
        input_data = {
            "Temperature_Anomaly": temperature,
            "Precipitation_Change": precipitation,
            "Drought_Index": drought,
            "Latitude": latitude,
            "Longitude": longitude,
            "Elevation": elevation,
            "Climate_Risk_Level": 2,  # Map from inputs
            "Land_Use_Type": 1,  # Map from land_type
            "water_access": water_access,
            "poverty_rate": poverty_rate,
            "adaptation_budget": adaptation_budget
        }

        try:
            response = requests.post(API_URL, json={"features": input_data})
            if response.status_code == 200:
                result = response.json()
                st.success("Analysis Complete!")
                
                with tabs[1]:
                    st.header("📋 Adaptation Recommendations")
                    cluster = result['prediction']['cluster']
                    recommendations = generate_detailed_recommendations(cluster)
                    
                    # Display risk level and priority
                    st.subheader(f"Risk Level: {recommendations['risk_level']}")
                    st.write(f"**Priority:** {recommendations['priority']}")
                    
                    # Display recommended actions
                    st.subheader("Recommended Actions")
                    for i, action in enumerate(recommendations['actions'], 1):
                        st.write(f"{i}. {action}")
                    
                    # Display timeline and cost
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Implementation Timeline:** {recommendations['timeline']}")
                    with col2:
                        st.write(f"**Estimated Cost Level:** {recommendations['estimated_cost']}")
                
                with tabs[2]:
                    st.header("📊 Impact Analysis")
                    display_impact_analysis(input_data, cluster, recommendations)
                    
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")




