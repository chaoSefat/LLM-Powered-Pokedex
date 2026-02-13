"""
AI Pokédex - A Streamlit web app for identifying Pokémon from images.

Requirements:
- streamlit
- openai
- requests
- Pillow

Usage: streamlit run app.py
"""

import streamlit as st
import requests
import base64
import os
from typing import Optional, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# PAGE CONFIG & SESSION INITIALIZATION
# ============================================================================

st.set_page_config(
    page_title="AI Pokédex",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "pokemon_data" not in st.session_state:
    st.session_state.pokemon_data = None
if "captured_image" not in st.session_state:
    st.session_state.captured_image = None
if "detection_failed" not in st.session_state:
    st.session_state.detection_failed = False


# ============================================================================
# BUSINESS LOGIC - Image Processing & API Calls
# ============================================================================

def encode_image(image_bytes: bytes) -> str:
    """
    Convert image bytes to base64 string.
    
    Args:
        image_bytes: Raw image bytes
    
    Returns:
        Base64 encoded string
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def clean_name(raw_prediction: str) -> str:
    """
    Clean Pokémon name prediction for API query.
    
    Args:
        raw_prediction: Raw name from OpenAI
    
    Returns:
        Cleaned name (lowercase, hyphenated)
    """
    return raw_prediction.strip().lower().replace(" ", "-")


def predict_pokemon(base64_image: str) -> Optional[str]:
    """
    Use OpenAI Vision to identify Pokémon in image.
    
    Args:
        base64_image: Base64 encoded image string
    
    Returns:
        Pokémon name or None if error
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Error: OPENAI_API_KEY not set")
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Pokémon identifier. Respond with ONLY the Pokémon name in lowercase."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What Pokémon is this?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=20,
            temperature=0
        )
        
        name = response.choices[0].message.content.strip()
        
        # Filter out invalid responses
        if not name or name.lower() in ["none", "unknown", "not a pokemon", "no pokemon", "unable to identify"]:
            return None
        
        return name
        
    except Exception as e:
        return None


@st.cache_data(ttl=3600)
def fetch_pokemon_data(pokemon_name: str) -> Optional[Dict]:
    """
    Fetch comprehensive Pokémon data from PokéAPI.
    Results are cached for 1 hour.
    
    Args:
        pokemon_name: Pokémon name (will be cleaned)
    
    Returns:
        Dict with Pokémon details or None if not found
    """
    if not pokemon_name:
        return None
    
    clean = clean_name(pokemon_name)
    
    try:
        response = requests.get(
            f"https://pokeapi.co/api/v2/pokemon/{clean}",
            timeout=5
        )
        
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        # Extract relevant data
        pokemon_data = {
            "name": data["name"].capitalize(),
            "official_sprite": data["sprites"]["other"]["official-artwork"]["front_default"],
            "types": [t["type"]["name"].capitalize() for t in data["types"]],
            "height": data["height"] * 0.1,  # Convert to meters
            "weight": data["weight"] * 0.1,  # Convert to kg
            "stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]},
            "abilities": [a["ability"]["name"].capitalize() for a in data["abilities"][:3]],
        }
        
        return pokemon_data
        
    except Exception:
        return None


# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_pokemon_info(data: Dict) -> None:
    """
    Render Pokémon information with stats.
    
    Args:
        data: Pokémon data dict from fetch_pokemon_data()
    """
    if not data:
        st.error("No data to display")
        return
    
    # Name header
    st.write(f"## {data['name']}")
    
    # Sprite and basics
    col1, col2 = st.columns(2)
    
    with col1:
        if data["official_sprite"]:
            st.image(data["official_sprite"], width=300)
    
    with col2:
        # Types
        type_str = ", ".join(data["types"])
        st.write(f"**Types:** {type_str}")
        
        # Key metrics
        st.write(f"**Height:** {data['height']:.1f}m")
        st.write(f"**Weight:** {data['weight']:.1f}kg")
        
        # Abilities
        abilities_str = ", ".join(data['abilities'])
        st.write(f"**Abilities:** {abilities_str}")
    
    # Stats
    st.subheader("Base Stats")
    
    stat_names = {
        "hp": "HP",
        "attack": "Attack",
        "defense": "Defense",
        "special-attack": "Sp. Atk",
        "special-defense": "Sp. Def",
        "speed": "Speed"
    }
    
    for stat_key, stat_label in stat_names.items():
        stat_val = data["stats"].get(stat_key, 0)
        normalized = min(stat_val / 255, 1.0)
        st.write(f"{stat_label}: {stat_val}")
        st.progress(normalized)


def render_help_card() -> None:
    """Render instructions card."""
    st.info(
        "📸 **How to Use:**\n"
        "1. Click 'Take a Picture' to capture an image\n"
        "2. Click 'Capture & Analyze' to identify the Pokémon\n"
        "3. View stats and information"
    )


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main app layout and logic."""
    
    # ---- TITLE ----
    st.markdown("<h1 style='text-align: center; margin-bottom: 1rem;'>🔴 AI POKÉDEX 🔴</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray; margin-bottom: 2rem;'>Identify Pokémon with AI Vision</p>", 
                unsafe_allow_html=True)
    
    # Camera input
    st.subheader("📸 Capture Image")
    captured_image = st.camera_input("Take a picture", key="pokemon_camera")
    
    render_help_card()
    
    # Store captured image and create analyze button
    if captured_image is not None:
        st.session_state.captured_image = captured_image
    
    col1, col2, col3 = st.columns(3)
    with col2:
        analyze_button = st.button("Capture & Analyze")
    
    # Process image when button clicked
    if analyze_button and st.session_state.captured_image is not None:
        with st.spinner("Analyzing image..."):
            # Convert image to bytes
            image_bytes = st.session_state.captured_image.getvalue()
            
            # Encode to base64
            base64_image = encode_image(image_bytes)
            
            # Predict Pokémon
            with st.spinner("Identifying Pokémon..."):
                pokemon_name = predict_pokemon(base64_image)
            
            # Only proceed if we got a valid pokemon name
            if pokemon_name:
                # Fetch data
                with st.spinner("Fetching data from PokéAPI..."):
                    pokemon_data = fetch_pokemon_data(pokemon_name)
                
                if pokemon_data:
                    st.session_state.pokemon_data = pokemon_data
                    st.session_state.detection_failed = False
                else:
                    # Pokemon detected but not found in database
                    st.session_state.detection_failed = True
            else:
                # No pokemon detected
                st.session_state.detection_failed = True
    
    # Display results
    if st.session_state.pokemon_data:
        st.write("---")
        render_pokemon_info(st.session_state.pokemon_data)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("Start Over"):
                st.session_state.pokemon_data = None
                st.session_state.captured_image = None
                st.session_state.detection_failed = False
                st.experimental_rerun()
    elif st.session_state.detection_failed:
        st.write("---")
        st.info("No Pokémon found. Please try with a clear image of a Pokémon.")
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("Start Over"):
                st.session_state.pokemon_data = None
                st.session_state.captured_image = None
                st.session_state.detection_failed = False
                st.experimental_rerun()


if __name__ == "__main__":
    main()