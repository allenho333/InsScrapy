import re
import spacy
import subprocess

# Function to load the SpaCy model
async def load_spacy_model():
    try:
        # Try to load the model
        nlp = spacy.load("en_core_web_sm")
        return nlp
    except OSError:
        # If the model is not found, download and install it
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
        return nlp

# Load the model
load_spacy_model()
# Load spacy's small English model
nlp = spacy.load("en_core_web_sm")

# Scraped text
text = """
Chicken, Mushroom, and Leek Risotto✨ This one’s a regular in our household and one of my favourite chook dishes.

It’s super tasty, nutritionally well-balanced, and packed with protein (which is pretty rare for a risotto). Chicken’s such a versatile ingredient—it’s lean, easy to cook, cost-effective and full of protein🙏.

Check out @chickendinnernz for more chicken recipe inspiration!

Here’s the ingredients (method in comments):
500 g boneless chicken thigh
1 tsp dried oregano
1 tsp dried rosemary
Olive oil
1 leek
300 g button mushrooms
1 cup arbioio rice
1 L chicken stock
A few big handfuls of baby spinach
½ cup frozen peas
2 cloves garlic
A big handful of fresh parsley or basil
1 Tbsp butter
¼ cup parmesan cheese, or more to taste
Salt and pepper, to taste
"""

def extract_recipe_details(text):
    # Use spaCy to parse the text and find the recipe title
    doc = nlp(text)
    
    # Recipe name: typically a noun phrase at the beginning of the text
    recipe_name = None
    
    # Define a list of common words that should not be part of a recipe title (e.g., "easy", "quick", etc.)
    common_non_title_words = {"quick", "easy", "ultimate", "delicious", "fakeaway", "dinner"}
    
    for sentence in doc.sents:
        # Try extracting the first few words of the sentence as the recipe title
        potential_title = []
        for token in sentence:
            # If the token is punctuation or a word like "easy", stop capturing the title
            if token.is_punct or token.text.lower() in common_non_title_words:
                break
            # Only capture descriptive words or nouns
            if token.pos_ in {"ADJ", "NOUN"}:
                potential_title.append(token.text)
        
        # If the potential title is a reasonable length (not too short), assume it's the recipe name
        if len(potential_title) > 2:
            recipe_name = " ".join(potential_title)
            break
    
    if not recipe_name:
        # Fallback to the first sentence if extraction failed
        sentences = list(doc.sents)
        recipe_name = sentences[0].text.strip()
    
    # Clean the recipe name further by removing emojis or special characters
    recipe_name = re.split(r'[✨\n]', recipe_name)[0].strip()
    
    # Extracting ingredients
    units = ["g", "kg", "ml", "l", "cup", "tsp", "tbsp", "handful", "cloves", "pinch", "dash", "lb", "oz"]
    ingredients = []
    for token in doc:
        if token.like_num or re.match(r'\d+/\d+', token.text):
            next_token = doc[token.i + 1]
            if next_token.text.lower() in units:
                ingredient = f"{token.text} {next_token.text} " + " ".join([t.text for t in doc[token.i + 2:token.i + 5] if t.pos_ == 'NOUN' or t.pos_ == 'ADJ'])
                ingredients.append(ingredient.strip())
    
    # Fallback to regex if spaCy doesn't work well
    if not ingredients:
        ingredients_pattern = r"(\d+[^a-zA-Z]*\s[a-zA-Z]+[^:\n]*)"
        ingredients = re.findall(ingredients_pattern, text)
    
    return recipe_name, ingredients
