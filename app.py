import streamlit as st
import os
from recipe_generator import generate_recipe, generate_recipe_list
from voice_input import process_voice_input
from nutrition import get_nutrition_info
from data_handler import save_recipe, get_saved_recipes
import base64
import io
import tempfile
from utils import preprocess_ingredients, get_regional_cuisines

# Page configuration
st.set_page_config(
    page_title="AI Rasoi: Recipe GPT with a Desi Twist",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if 'saved_recipes' not in st.session_state:
    st.session_state.saved_recipes = get_saved_recipes()

if 'current_recipe' not in st.session_state:
    st.session_state.current_recipe = None

# Display logo and header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.svg", width=100)
with col2:
    st.title("AI Rasoi: Recipe GPT with a Desi Twist")
    st.subheader("Your Indian Recipe Assistant")

st.markdown("---")

# Sidebar for saved recipes
with st.sidebar:
    st.header("Your Recipe Collection")
    if not st.session_state.saved_recipes:
        st.info("Your saved recipes will appear here")
    else:
        for i, recipe in enumerate(st.session_state.saved_recipes):
            with st.expander(recipe['name']):
                st.write(f"**Cuisine**: {recipe['cuisine']}")
                st.write(f"**Spice Level**: {recipe['spice_level']}")
                st.write(f"**Calories**: {recipe['calories']} kcal")
                if st.button("Load Recipe", key=f"load_{i}"):
                    st.session_state.current_recipe = recipe
                    st.rerun()

# Input tabs
tab1, tab2 = st.tabs(["Text Input", "Voice Input"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_area(
            "Tell me what's in your kitchen or ask for a specific dish:",
            placeholder="I have 2 onions, 1 tomato, and some leftover roti. Now what?",
            height=100
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("Generate Recipe", key="generate_text_recipe"):
            if user_input:
                with st.spinner("Thinking of the perfect dish..."):
                    ingredients = preprocess_ingredients(user_input)
                    st.session_state.current_recipe = generate_recipe(user_input)
                    st.rerun()
            else:
                st.error("Please enter some ingredients or a recipe request")

with tab2:
    st.write("Click the button below and speak your ingredients or recipe request")
    if st.button("Start Recording", key="start_recording"):
        with st.spinner("Listening..."):
            audio_bytes = process_voice_input()
            
            # Save audio to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile:
                tmpfile.write(audio_bytes)
                audio_path = tmpfile.name
            
            # Display the audio for playback
            st.audio(audio_bytes, format='audio/wav')
            
            # Process the audio with Cohere
            from voice_input import transcribe_audio
            transcription = transcribe_audio(audio_path)
            os.unlink(audio_path)  # Delete the temporary file
            
            st.text_area("Transcribed text:", transcription, height=100)
            
            if st.button("Generate Recipe from Voice", key="generate_voice_recipe"):
                with st.spinner("Thinking of the perfect dish..."):
                    st.session_state.current_recipe = generate_recipe(transcription)
                    st.rerun()

# Customization options
st.markdown("### Customize Your Recipe")
col1, col2, col3 = st.columns(3)

with col1:
    spice_level = st.select_slider(
        "Spice Level",
        options=["Mild", "Medium", "Spicy", "Very Spicy", "Fire!"],
        value="Medium"
    )

with col2:
    regional_cuisines = get_regional_cuisines()
    cuisine_preference = st.selectbox(
        "Regional Preference",
        options=regional_cuisines,
        index=0
    )

with col3:
    dietary_preference = st.multiselect(
        "Dietary Preferences",
        options=["Vegetarian", "Vegan", "Healthy", "Low Oil", "Low Calorie", "High Protein"],
        default=["Healthy"]
    )

# Generate a recipe list based on customization
if st.button("Suggest Recipes Based on Preferences"):
    with st.spinner("Finding perfect matches..."):
        recipe_suggestions = generate_recipe_list(
            spice_level=spice_level,
            cuisine=cuisine_preference,
            dietary_preferences=dietary_preference
        )
        
        st.subheader("Recipe Suggestions")
        recipe_cols = st.columns(3)
        for i, recipe in enumerate(recipe_suggestions):
            with recipe_cols[i % 3]:
                st.markdown(f"**{recipe['name']}**")
                st.write(f"Spice level: {recipe['spice_level']}")
                st.write(f"Calories: {recipe['calories']} kcal")
                if st.button("View Recipe", key=f"view_{i}"):
                    st.session_state.current_recipe = recipe
                    st.rerun()

# Display current recipe
if st.session_state.current_recipe:
    st.markdown("---")
    recipe = st.session_state.current_recipe
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header(recipe['name'])
        st.subheader(f"{recipe['cuisine']} Cuisine | Spice Level: {recipe['spice_level']}")
        
        st.markdown("### Ingredients")
        for ingredient in recipe['ingredients']:
            st.markdown(f"- {ingredient}")
        
        st.markdown("### Instructions")
        for i, step in enumerate(recipe['instructions'], 1):
            st.markdown(f"{i}. {step}")
    
    with col2:
        st.markdown("### Nutrition Info")
        st.markdown(f"**Calories:** {recipe['calories']} kcal")
        if 'nutrition' in recipe:
            for nutrient, value in recipe['nutrition'].items():
                st.markdown(f"**{nutrient}:** {value}")
        
        if st.button("Save Recipe"):
            save_recipe(recipe)
            st.session_state.saved_recipes = get_saved_recipes()
            st.success(f"Recipe '{recipe['name']}' saved to your collection!")
        
        if st.button("Get a Different Recipe"):
            st.session_state.current_recipe = None
            st.rerun()

# About and Help sections
with st.expander("About AI Rasoi"):
    st.write("""
    **AI Rasoi** is your personal Indian recipe assistant that suggests dishes based on 
    ingredients you have. Customize recipes by spice level, regional preferences, and dietary needs.
    
    Built with ❤️ using Streamlit, Cohere API, and culinary expertise from across India.
    """)

with st.expander("How to Use"):
    st.write("""
    1. **Enter ingredients** - List what you have in your kitchen
    2. **Customize** - Set your spice level and regional preferences
    3. **Generate** - Get personalized recipe recommendations
    4. **Save** - Store your favorite recipes for later
    5. **Voice Input** - Speak to AI Rasoi just like you would to your mom!
    """)

# Footer
st.markdown("---")
st.markdown("AI Rasoi: Recipe GPT with a Desi Twist | Made with Streamlit and Cohere")
