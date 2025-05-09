import re
import string

def preprocess_ingredients(user_input):
    """
    Extract ingredients from user input
    
    Args:
        user_input (str): User's request including ingredients
        
    Returns:
        list: List of extracted ingredients
    """
    # Clean text
    text = user_input.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Extract ingredients using common patterns
    ingredients = []
    
    # Look for "I have X, Y, and Z"
    have_pattern = r"(?:i have|got|with)(?:[^.?!]*)(?:\.|\?|!|$)"
    have_matches = re.findall(have_pattern, text)
    
    if have_matches:
        # Extract the ingredients after "I have"
        for match in have_matches:
            # Remove the "I have" part
            match = re.sub(r"(?:i have|got|with)\s+", "", match)
            
            # Split by common separators
            items = re.split(r',\s*|\s+and\s+|\s+&\s+', match)
            
            # Clean up and add to the list
            for item in items:
                item = item.strip()
                if item and len(item) > 1 and item not in ['a', 'an', 'the', 'some']:
                    # Remove quantities
                    item = re.sub(r'^\d+\s+', '', item)
                    ingredients.append(item)
    
    # If no ingredients found, try to extract nouns
    if not ingredients:
        # Common food items
        food_items = [
            "rice", "wheat", "flour", "atta", "potato", "aloo", "tomato", "onion", "garlic",
            "ginger", "chicken", "mutton", "fish", "paneer", "tofu", "lentil", "dal",
            "oil", "ghee", "butter", "milk", "cream", "yogurt", "curd", "cheese",
            "sugar", "honey", "vegetable", "spinach", "cauliflower", "carrot",
            "peas", "bean", "nut", "cashew", "almond", "spice", "masala", "chili",
            "cinnamon", "cardamom", "clove", "pepper", "salt", "cumin", "coriander",
            "turmeric", "saffron", "curry", "leaf", "cilantro", "mint", "roti",
            "bread", "naan", "paratha", "chapati", "dosa", "idli", "sambar", "chutney"
        ]
        
        # Look for these food items in the text
        words = text.split()
        for word in words:
            word = word.strip(string.punctuation)
            if word in food_items and word not in ingredients:
                ingredients.append(word)
    
    # If still no ingredients, use some defaults
    if not ingredients:
        ingredients = ["onion", "tomato", "potato", "rice"]
    
    return ingredients

def get_regional_cuisines():
    """
    Get a list of Indian regional cuisines
    
    Returns:
        list: List of regional cuisines
    """
    return [
        "North Indian",
        "South Indian",
        "Bengali",
        "Gujarati",
        "Maharashtrian",
        "Punjabi",
        "Rajasthani",
        "Goan",
        "Kashmiri",
        "Hyderabadi",
        "Kerala",
        "Tamil Nadu",
        "Andhra",
        "Chettinad",
        "Awadhi",
        "Sindhi",
        "Bihari"
    ]

def extract_preferences(user_input):
    """
    Extract preferences from user input
    
    Args:
        user_input (str): User's request
        
    Returns:
        dict: Dictionary of preferences
    """
    text = user_input.lower()
    
    preferences = {}
    
    # Extract spice level
    if "mild" in text or "less spicy" in text:
        preferences["spice_level"] = "Mild"
    elif "very spicy" in text or "extra spicy" in text:
        preferences["spice_level"] = "Very Spicy"
    elif "spicy" in text:
        preferences["spice_level"] = "Spicy"
    
    # Extract cuisine
    cuisines = get_regional_cuisines()
    for cuisine in cuisines:
        if cuisine.lower() in text:
            preferences["cuisine"] = cuisine
            break
    
    # Extract dietary preferences
    dietary = []
    if "vegetarian" in text:
        dietary.append("Vegetarian")
    if "vegan" in text:
        dietary.append("Vegan")
    if "healthy" in text:
        dietary.append("Healthy")
    if "low oil" in text or "less oil" in text:
        dietary.append("Low Oil")
    if "low calorie" in text or "diet" in text:
        dietary.append("Low Calorie")
    
    if dietary:
        preferences["dietary"] = dietary
    
    return preferences
