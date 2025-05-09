import json
import os
import streamlit as st

# File to store saved recipes
RECIPES_FILE = "saved_recipes.json"

def load_datasets():
    """
    Load recipe datasets for suggestions
    
    Returns:
        dict: Dictionary containing datasets
    """
    # In a real implementation, this would load actual datasets
    # For now, we'll return empty datasets
    return {
        "tarla_dalal": [],
        "indian_food_101": []
    }

def save_recipe(recipe):
    """
    Save a recipe to the saved recipes file
    
    Args:
        recipe (dict): Recipe to save
    """
    # Load existing recipes
    saved_recipes = get_saved_recipes()
    
    # Add the new recipe if it's not already saved
    recipe_names = [r["name"] for r in saved_recipes]
    if recipe["name"] not in recipe_names:
        saved_recipes.append(recipe)
    
    # Save to session state
    st.session_state.saved_recipes = saved_recipes
    
    # Save to file
    try:
        with open(RECIPES_FILE, "w") as f:
            json.dump(saved_recipes, f)
    except Exception as e:
        print(f"Error saving recipes: {e}")

def get_saved_recipes():
    """
    Get saved recipes from file
    
    Returns:
        list: List of saved recipes
    """
    try:
        if os.path.exists(RECIPES_FILE):
            with open(RECIPES_FILE, "r") as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        print(f"Error loading recipes: {e}")
        return []

def search_recipes_by_ingredients(ingredients, dataset):
    """
    Search for recipes by ingredients
    
    Args:
        ingredients (list): List of ingredients
        dataset (str): Dataset to search in
        
    Returns:
        list: List of matching recipes
    """
    # This would search through the actual dataset
    # For now, we'll return empty results
    return []

def filter_recipes_by_preferences(recipes, preferences):
    """
    Filter recipes by user preferences
    
    Args:
        recipes (list): List of recipes
        preferences (dict): User preferences
        
    Returns:
        list: Filtered list of recipes
    """
    filtered_recipes = []
    
    for recipe in recipes:
        # Check spice level
        if preferences.get("spice_level") and recipe["spice_level"] != preferences["spice_level"]:
            continue
            
        # Check cuisine
        if preferences.get("cuisine") and recipe["cuisine"] != preferences["cuisine"]:
            continue
            
        # Check dietary preferences
        if preferences.get("dietary"):
            dietary = preferences["dietary"]
            if "Vegetarian" in dietary and any(i in recipe["ingredients"].lower() for i in ["chicken", "mutton", "fish", "meat"]):
                continue
            if "Vegan" in dietary and any(i in recipe["ingredients"].lower() for i in ["milk", "paneer", "ghee", "curd", "yogurt"]):
                continue
                
        filtered_recipes.append(recipe)
    
    return filtered_recipes
