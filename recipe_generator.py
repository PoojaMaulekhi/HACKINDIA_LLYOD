import os
import json
import cohere
import random
import time
from utils import preprocess_ingredients, get_regional_cuisines

# Initialize Cohere client
co = cohere.Client(os.getenv("COHERE_API_KEY", "default_key"))

def generate_recipe(user_input):
    """
    Generate a recipe based on user input using Cohere API
    
    Args:
        user_input (str): User's request including ingredients and/or preferences
        
    Returns:
        dict: A recipe dictionary with name, ingredients, instructions, etc.
    """
    # Preprocess the input to identify ingredients
    ingredients = preprocess_ingredients(user_input)
    
    # Extract preferences from the request
    spice_preference = "Medium"
    region_preference = "North Indian"
    
    if "spicy" in user_input.lower():
        spice_preference = "Spicy"
    elif "mild" in user_input.lower() or "less spicy" in user_input.lower():
        spice_preference = "Mild"
        
    for region in ["punjabi", "bengali", "south indian", "gujarati", "maharashtrian"]:
        if region in user_input.lower():
            region_preference = region.title()
            
    # Prepare the prompt for Cohere
    prompt = f"""
    You are an expert Indian chef who specializes in traditional recipes from all over India.
    Provide a detailed Indian recipe based on these ingredients: {', '.join(ingredients)}.
    The recipe should have a spice level of {spice_preference} and follow {region_preference} cooking style.
    
    Please respond in the following JSON format:
    {{
        "name": "Recipe Name",
        "cuisine": "Regional Cuisine (e.g., Punjabi, Bengali)",
        "spice_level": "Spice Level (Mild, Medium, Spicy, Very Spicy, Fire!)",
        "ingredients": ["ingredient 1 with quantity", "ingredient 2 with quantity"],
        "instructions": ["step 1", "step 2", "step 3"],
        "calories": estimated calories per serving,
        "nutrition": {{"protein": "amount in g", "carbs": "amount in g", "fat": "amount in g"}},
        "prep_time": "preparation time in minutes",
        "cook_time": "cooking time in minutes",
        "total_time": "total time in minutes",
        "servings": number of servings
    }}
    
    Make sure the recipe is authentic, detailed, and follows traditional Indian cooking methods.
    """
    
    # Call Cohere API
    response = co.generate(
        model="command",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.7,
        k=0,
        stop_sequences=[],
        return_likelihoods="NONE"
    )
    
    try:
        # Parse the response
        response_text = response.generations[0].text
        
        # Extract the JSON portion from the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_string = response_text[json_start:json_end]
        
        recipe = json.loads(json_string)
        
        # Ensure all required fields are present
        required_fields = ["name", "cuisine", "spice_level", "ingredients", "instructions", "calories"]
        for field in required_fields:
            if field not in recipe:
                raise ValueError(f"Missing required field: {field}")
        
        return recipe
        
    except Exception as e:
        # Fallback to a manually constructed recipe if parsing fails
        print(f"Error parsing response: {e}")
        return create_fallback_recipe(ingredients, spice_preference, region_preference)

def generate_recipe_list(spice_level="Medium", cuisine="North Indian", dietary_preferences=None):
    """
    Generate a list of recipe suggestions based on preferences
    
    Args:
        spice_level (str): Preferred spice level
        cuisine (str): Preferred regional cuisine
        dietary_preferences (list): List of dietary preferences
        
    Returns:
        list: List of recipe dictionaries
    """
    if dietary_preferences is None:
        dietary_preferences = ["Healthy"]
        
    prompt = f"""
    You are an expert Indian chef. Provide a list of 3 Indian recipes that match these criteria:
    - Spice level: {spice_level}
    - Regional cuisine: {cuisine}
    - Dietary preferences: {', '.join(dietary_preferences)}
    
    Please respond with a JSON array of 3 recipes in this format:
    [
        {{
            "name": "Recipe Name",
            "cuisine": "{cuisine}",
            "spice_level": "{spice_level}",
            "ingredients": ["ingredient 1 with quantity", "ingredient 2 with quantity"],
            "instructions": ["step 1", "step 2", "step 3"],
            "calories": estimated calories per serving,
            "nutrition": {{"protein": "amount in g", "carbs": "amount in g", "fat": "amount in g"}},
            "prep_time": "preparation time in minutes",
            "cook_time": "cooking time in minutes"
        }},
        // Recipe 2 and 3 with same format
    ]
    """
    
    try:
        # Call Cohere API
        response = co.generate(
            model="command",
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7,
            k=0,
            stop_sequences=[],
            return_likelihoods="NONE"
        )
        
        # Parse the response
        response_text = response.generations[0].text
        
        # Extract the JSON portion from the response
        json_start = response_text.find('[')
        json_end = response_text.rfind(']') + 1
        json_string = response_text[json_start:json_end]
        
        recipes = json.loads(json_string)
        return recipes
        
    except Exception as e:
        # Fallback to manually constructed recipes
        print(f"Error generating recipe list: {e}")
        return create_fallback_recipe_list(spice_level, cuisine, dietary_preferences)

def create_fallback_recipe(ingredients, spice_level, region_preference):
    """Create a fallback recipe if the API response can't be parsed"""
    
    # Basic mapping for common ingredients to recipes
    staple_dishes = {
        "rice": "Pulao",
        "lentils": "Dal",
        "potato": "Aloo Curry",
        "tomato": "Tomato Chutney",
        "onion": "Pyaaz Paratha",
        "paneer": "Paneer Tikka",
        "chicken": "Chicken Curry"
    }
    
    # Choose a dish based on ingredients
    dish_name = "Mixed Vegetable Curry"  # Default
    for ing in ingredients:
        for key, value in staple_dishes.items():
            if key in ing.lower():
                dish_name = value
                break
    
    # Add regional prefix
    region_map = {
        "North Indian": "Punjabi",
        "South Indian": "Tamil",
        "Bengali": "Bengali",
        "Gujarati": "Gujarati",
        "Maharashtrian": "Maharashtrian"
    }
    
    region = region_map.get(region_preference, "Indian")
    full_name = f"{region} {dish_name}"
    
    # Create a complete recipe
    return {
        "name": full_name,
        "cuisine": region_preference,
        "spice_level": spice_level,
        "ingredients": [f"{ing}" for ing in ingredients] + ["Salt to taste", "Cooking oil", "Spices as per taste"],
        "instructions": [
            "Prepare all ingredients by washing and chopping as needed.",
            f"Heat oil in a pan and add the spices according to {region} style.",
            "Add the main ingredients and cook until tender.",
            "Season with salt and garnish as desired.",
            "Serve hot with rice or bread."
        ],
        "calories": random.randint(200, 400),
        "nutrition": {"protein": f"{random.randint(5, 15)}g", "carbs": f"{random.randint(20, 40)}g", "fat": f"{random.randint(8, 20)}g"},
        "prep_time": f"{random.randint(10, 20)}",
        "cook_time": f"{random.randint(20, 40)}",
        "total_time": f"{random.randint(30, 60)}",
        "servings": random.randint(2, 4)
    }

def create_fallback_recipe_list(spice_level, cuisine, dietary_preferences):
    """Create a fallback recipe list if the API response can't be parsed"""
    
    recipes = []
    dish_names = ["Vegetable Biryani", "Paneer Butter Masala", "Chole Bhature"]
    
    for name in dish_names:
        recipes.append({
            "name": name,
            "cuisine": cuisine,
            "spice_level": spice_level,
            "ingredients": [
                "2 cups main ingredient",
                "1 onion, chopped",
                "2 tomatoes, pureed",
                "1 tbsp ginger-garlic paste",
                "Spices as needed",
                "Salt to taste",
                "Fresh herbs for garnish"
            ],
            "instructions": [
                "Prepare all ingredients by washing and chopping as needed.",
                "Cook the main ingredients with spices as per recipe.",
                "Simmer until the flavors meld together.",
                "Garnish with fresh herbs and serve hot."
            ],
            "calories": random.randint(300, 600),
            "nutrition": {
                "protein": f"{random.randint(10, 20)}g", 
                "carbs": f"{random.randint(30, 60)}g", 
                "fat": f"{random.randint(10, 25)}g"
            },
            "prep_time": f"{random.randint(15, 30)}",
            "cook_time": f"{random.randint(20, 45)}"
        })
    
    return recipes
