"""
AgriGPT - AI Agent for Farmers
A Streamlit web application for farmer assistance
"""

import streamlit as st
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AgriGPT - AI Agent for Farmers",
    page_icon="🌾",
    layout="wide"
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Government Schemes Database
GOVT_SCHEMES = {
    "PM-KISAN": {
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "description": "Income support of ₹6000 per year to farmer families",
        "eligibility": "All landholding farmer families",
        "benefits": "₹6000 per year in 3 installments"
    },
    "PMFBY": {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "description": "Crop insurance scheme for farmers",
        "eligibility": "All farmers including sharecroppers and tenant farmers",
        "benefits": "Low premium rates (2% for Kharif, 1.5% for Rabi)"
    },
    "KCC": {
        "name": "Kisan Credit Card (KCC) Scheme",
        "description": "Credit facility for farmers at subsidized rates",
        "eligibility": "All farmers - individual/joint borrowers",
        "benefits": "Credit limit up to ₹3 lakh at concessional interest rate"
    },
    "SMAM": {
        "name": "Sub-Mission on Agricultural Mechanization (SMAM)",
        "description": "Promotion of agricultural mechanization",
        "eligibility": "Small and marginal farmers",
        "benefits": "Subsidy on agricultural machinery up to 50%"
    },
    "PKVY": {
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "description": "Organic farming promotion",
        "eligibility": "Farmers interested in organic farming",
        "benefits": "₹20,000 per hectare for 3 years"
    }
}

# Crop recommendations based on region and season
CROP_RECOMMENDATIONS = {
    "North India": {
        "Kharif": ["Rice", "Maize", "Cotton", "Soybean", "Sugarcane"],
        "Rabi": ["Wheat", "Barley", "Mustard", "Chickpea", "Peas"],
        "Zaid": ["Watermelon", "Muskmelon", "Cucumber", "Green Fodder"]
    },
    "South India": {
        "Kharif": ["Rice", "Maize", "Groundnut", "Cotton", "Sugarcane"],
        "Rabi": ["Wheat", "Chickpea", "Sunflower", "Mustard"],
        "Zaid": ["Watermelon", "Cucumber", "Tomato", "Green Chillies"]
    },
    "East India": {
        "Kharif": ["Rice", "Maize", "Jute", "Sugarcane", "Turmeric"],
        "Rabi": ["Wheat", "Mustard", "Lentil", "Potato"],
        "Zaid": ["Watermelon", "Muskmelon", "Summer Rice"]
    },
    "West India": {
        "Kharif": ["Cotton", "Groundnut", "Soybean", "Maize", "Sugarcane"],
        "Rabi": ["Wheat", "Mustard", "Chickpea", "Onion"],
        "Zaid": ["Watermelon", "Muskmelon", "Green Fodder"]
    },
    "Central India": {
        "Kharif": ["Soybean", "Maize", "Cotton", "Rice", "Pulses"],
        "Rabi": ["Wheat", "Mustard", "Chickpea", "Linseed"],
        "Zaid": ["Watermelon", "Muskmelon", "Cucumber"]
    }
}

def get_weather(city: str, api_key: str) -> dict:
    """Fetch weather data from OpenWeatherMap API"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def get_ai_response(prompt: str) -> str:
    """Get AI response from OpenAI"""
    try:
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
            return "⚠️ API Key not configured. Please add your OpenAI API key in the .env file."
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are AgriGPT, an AI assistant specifically designed to help farmers with agricultural advice. Provide helpful, accurate, and practical information about farming, crops, weather, and government schemes. Keep responses clear and simple."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Sidebar navigation
st.sidebar.title("🌾 AgriGPT")
st.sidebar.markdown("---")
page = st.sidebar.radio("Select Feature:", 
    ["🏠 Home", "🌱 Crop Recommendation", "🌤️ Weather Updates", "📋 Govt Schemes", "💬 AI Assistant"])

# Home Page
if page == "🏠 Home":
    st.title("🌾 Welcome to AgriGPT")
    st.subheader("Your AI Assistant for Smart Farming")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🌱 Crop Recommendation\nGet personalized crop suggestions based on your region and season")
    
    with col2:
        st.info("### 🌤️ Weather Updates\nStay informed with real-time weather forecasts")
    
    with col3:
        st.info("### 📋 Govt Schemes\nLearn about government schemes and subsidies")
    
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    1. Select a feature from the sidebar
    2. Enter your location/region details
    3. Get AI-powered recommendations and information
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ API Configuration")
    st.warning("""
    To use AI features, please configure your API keys:
    - **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
    - **Weather API Key**: Get from [OpenWeatherMap](https://openweathermap.org/api)
    
    Add these to the `.env` file in the project directory.
    """)

# Crop Recommendation Page
elif page == "🌱 Crop Recommendation":
    st.title("🌱 Crop Recommendation")
    st.markdown("Get personalized crop suggestions based on your region and season")
    
    col1, col2 = st.columns(2)
    
    with col1:
        region = st.selectbox("Select Your Region", 
            ["North India", "South India", "East India", "West India", "Central India"])
    
    with col2:
        season = st.selectbox("Select Season", ["Kharif", "Rabi", "Zaid"])
    
    if st.button("Get Crop Recommendations"):
        st.markdown("### 🌾 Recommended Crops for Your Region")
        
        crops = CROP_RECOMMENDATIONS.get(region, {}).get(season, [])
        
        if crops:
            for crop in crops:
                st.success(f"✅ {crop}")
            
            st.markdown("---")
            st.markdown("### 💡 AI Advice for Your Crops")
            
            advice_prompt = f"Give me farming tips for {region} during {season} season. The recommended crops are: {', '.join(crops)}. Provide advice on soil preparation, irrigation, and harvest timing."
            with st.spinner("Getting AI advice..."):
                advice = get_ai_response(advice_prompt)
                st.info(advice)
        else:
            st.error("No recommendations available for this combination")

# Weather Updates Page
elif page == "🌤️ Weather Updates":
    st.title("🌤️ Weather Updates")
    st.markdown("Get real-time weather information for your location")
    
    city = st.text_input("Enter City Name", placeholder="e.g., Delhi, Mumbai, Chennai")
    
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    
    if st.button("Get Weather Update"):
        if not city:
            st.error("Please enter a city name")
        elif not api_key or api_key == "your_openweathermap_api_key_here":
            st.error("⚠️ Weather API Key not configured. Please add your OpenWeatherMap API key in the .env file")
        else:
            with st.spinner("Fetching weather data..."):
                weather = get_weather(city, api_key)
                
                if "error" in weather:
                    st.error(f"Error fetching weather: {weather['error']}")
                else:
                    st.markdown(f"### Weather in {city.title()}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Temperature", f"{weather['main']['temp']}°C")
                    
                    with col2:
                        st.metric("Humidity", f"{weather['main']['humidity']}%")
                    
                    with col3:
                        st.metric("Wind Speed", f"{weather['wind']['speed']} m/s")
                    
                    with col4:
                        st.metric("Pressure", f"{weather['main']['pressure']} hPa")
                    
                    st.markdown(f"**Condition:** {weather['weather'][0]['description'].title()}")
                    
                    st.markdown("---")
                    st.markdown("### 💡 Farming Advice Based on Weather")
                    
                    advice_prompt = f"Give farming advice for current weather in {city}: Temperature {weather['main']['temp']}°C, Humidity {weather['main']['humidity']}%, Wind {weather['wind']['speed']} m/s, Condition: {weather['weather'][0]['description']}"
                    with st.spinner("Getting AI advice..."):
                        advice = get_ai_response(advice_prompt)
                        st.info(advice)

# Government Schemes Page
elif page == "📋 Govt Schemes":
    st.title("📋 Government Schemes for Farmers")
    st.markdown("Learn about various government schemes and subsidies available")
    
    scheme = st.selectbox("Select a Scheme", list(GOVT_SCHEMES.keys()))
    
    if scheme:
        scheme_info = GOVT_SCHEMES[scheme]
        
        st.markdown(f"### {scheme_info['name']}")
        st.markdown(f"**Description:** {scheme_info['description']}")
        st.markdown(f"**Eligibility:** {scheme_info['eligibility']}")
        st.markdown(f"**Benefits:** {scheme_info['benefits']}")
        
        st.markdown("---")
        
        if st.button(f"Get More Details about {scheme}"):
            advice_prompt = f"Provide detailed information about {scheme_info['name']}, including how to apply, required documents, and important dates."
            with st.spinner("Getting detailed information..."):
                details = get_ai_response(advice_prompt)
                st.info(details)
    
    st.markdown("---")
    st.markdown("### 🔍 Search Schemes")
    
    search_query = st.text_input("Search for schemes", placeholder="Enter keywords...")
    
    if search_query:
        st.markdown("### Search Results:")
        for key, scheme_info in GOVT_SCHEMES.items():
            if (search_query.lower() in scheme_info['name'].lower() or 
                search_query.lower() in scheme_info['description'].lower()):
                st.markdown(f"**{key}:** {scheme_info['name']}")

# AI Assistant Page
elif page == "💬 AI Assistant":
    st.title("💬 AgriGPT AI Assistant")
    st.markdown("Ask any question about farming, crops, weather, or government schemes")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask your farming question..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt)
                st.markdown(response)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("🌾 **AgriGPT** - Empowering Farmers with AI | Version 1.0")