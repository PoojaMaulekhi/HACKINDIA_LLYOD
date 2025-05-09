import os
import json
import requests
import random

def get_nutrition_info(recipe_name, ingredients):
    """
    Get nutrition information for a recipe
    
    Args:
        recipe_name (str): Name of the recipe
        ingredients (list): List of ingredients with quantities
        
    Returns:
        dict: Dictionary containing nutrition information
    """
    # In a real implementation, this would call an external API or use a dataset
    # For now, we'll generate some realistic values
    
    # Estimate calories based on ingredients
    calories = estimate_calories(ingredients)
    
    # Generate other nutrition facts
    nutrition = {
        "calories": calories,
        "protein": f"{random.randint(5, 30)}g",
        "carbs": f"{random.randint(20, 80)}g",
        "fat": f"{random.randint(5, 25)}g",
        "fiber": f"{random.randint(2, 10)}g",
        "sugar": f"{random.randint(1, 15)}g"
    }
    
    return nutrition

def estimate_calories(ingredients):
    """
    Estimate calories based on ingredients
    
    Args:
        ingredients (list): List of ingredients with quantities
        
    Returns:
        int: Estimated calories
    """
    # Map common ingredients to approximate calories per standard serving
    calorie_map = {
        "rice": 200,
        "wheat": 150,
        "flour": 150,
        "potato": 100,
        "tomato": 25,
        "onion": 40,
        "garlic": 5,
        "ginger": 5,
        "chicken": 200,
        "mutton": 250,
        "fish": 150,
        "paneer": 180,
        "tofu": 100,
        "lentil": 120,
        "dal": 120,
        "oil": 120,
        "ghee": 130,
        "butter": 100,
        "milk": 80,
        "cream": 100,
        "yogurt": 60,
        "curd": 60,
        "cheese": 100,
        "sugar": 50,
        "honey": 60,
        "vegetable": 50,
        "spinach": 25,
        "cauliflower": 30,
        "carrot": 35,
        "peas": 40,
        "bean": 40,
        "nut": 180,
        "cashew": 200,
        "almond": 200,
        "spice": 10
    }
    
    # Base calories for any recipe
    base_calories = 150
    
    # Add calories based on ingredients
    additional_calories = 0
    for ingredient in ingredients:
        ingredient_lower = ingredient.lower()
        for key, calories in calorie_map.items():
            if key in ingredient_lower:
                additional_calories += calories
                break
    
    # Adjust for portions - assuming 2-4 servings
    total_calories = base_calories + additional_calories
    per_serving = total_calories // random.randint(2, 4)
    
    # Ensure reasonable range
    if per_serving < 200:
        per_serving = random.randint(200, 300)
    elif per_serving > 800:
        per_serving = random.randint(600, 800)
    
    return per_serving

def get_nutrition_from_huggingface(recipe):
    """
    Get nutrition information using HuggingFace models
    
    Args:
        recipe (dict): Recipe dictionary with name and ingredients
        
    Returns:
        dict: Dictionary containing nutrition information
    """
    # This would use a HuggingFace model to estimate nutrition values
    # For now, we'll use the estimate_calories function
    
    nutrition = {
        "calories": estimate_calories(recipe["ingredients"]),
        "protein": f"{random.randint(5, 30)}g",
        "carbs": f"{random.randint(20, 80)}g",
        "fat": f"{random.randint(5, 25)}g"
    }
    
    return nutrition
