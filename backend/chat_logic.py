import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from transformers import pipeline  
from backend.chat_history import load_history, save_history
from deep_translator import GoogleTranslator
from models.embedding_model import recommend_coffees , load_coffee_data
from models.sentiment_analysis import analyze_sentiment

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=api_key)

def load_stores_data():
    """
    Loads store data from a JSON file located in the 'data' directory.
    :return: List of store dictionaries.
    """
    file_path = os.path.join('data', 'stores_data.json')  # Adjust the path as necessary
    with open(file_path, 'r') as file:
        return json.load(file)

def fetch_online_store_recommendations(user_preferences):
    """
    Fetches online store recommendations based on user preferences.

    :param user_preferences: Dictionary containing user preferences such as coffee type, location, and services desired.
    :return: A list of recommended online stores with additional service information.
    """
    stores_data = load_stores_data()  # Load stores data from JSON

    preferred_types = user_preferences.get("coffee_types", [])
    user_location = user_preferences.get("location", "Global")
    desired_services = user_preferences.get("services", [])

    recommended_stores = []

    for store in stores_data:
        score = 0

        if (any(coffee in store["types"] for coffee in preferred_types) and 
                (store["location"] == user_location or store["location"] == "Global")):
            score += 1  
            
            matching_services = set(store["services"]) & set(desired_services)
            score += len(matching_services) 

            recommended_stores.append({
                "name": store["name"],
                "url": store["url"],
                "services": list(matching_services),
                "score": score  # Store the score for potential future sorting
            })

    recommended_stores.sort(key=lambda x: x['score'], reverse=True)


    if not recommended_stores:
        recommended_stores = [{"name": store["name"], "url": store["url"], "services": store["services"]}
                              for store in stores_data[:3]]

    return recommended_stores

# Fetch coffee image and fun fact based on user preferences
def fetch_coffee_image_and_fact(user_preferences):
    prompt = (
        f"Provide a URL to an image of coffee and a fun, interesting fact about coffee. "
        f"Consider user preferences such as coffee type or flavor profile: {user_preferences}. "
        "The response should include an 'image_url' and a 'fact'."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    
    content = response.choices[0].message.content
    image_url = "sample-coffee.jpg" 
    fact = content.strip() 

    return {
        "image_url": image_url,
        "fact": fact
    }

# Translate the response text if a specific language is required
def translate_response(response_text, target_language):
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(response_text)
        return translation
    except Exception as e:
        print(f"Error during translation: {e}")
        return response_text 


# Main function to get coffee recommendation
def get_coffee_recommendation(user_id, user_input, user_preferences):
    # Save user input to history
    save_history(user_id, {"role": "user", "content": user_input})
    history = load_history(user_id)
    
    # Get user settings from preferences
    language = user_preferences.get("language", "English")
    tone = user_preferences.get("tone", "friendly")
    detail_level = user_preferences.get("detail_level", "concise")
    
    # Analyze sentiment
    user_sentiment = analyze_sentiment(user_input)
    online_store_suggestions = fetch_online_store_recommendations(user_preferences)
    
    # Get machine learning-based recommendations
    coffee_data = load_coffee_data()
    ml_recommendations = recommend_coffees(user_preferences, coffee_data)
    
    # Fetch a coffee image and fact based on preferences
    coffee_image_fact = fetch_coffee_image_and_fact(user_preferences)

    # Compile the recommendation prompt
    recommendation_prompt = (
        f"User preferences: {user_preferences}, language: {language}, tone: {tone}, "
        f"detail level: {detail_level}, sentiment: {user_sentiment}. "
        f"User chat history includes: {history}. Based on these inputs, provide a personalized coffee recommendation."
        f"Highlight recommended coffee types with matching flavor profiles and preferences. "
        f"Include relevant serving images, interesting facts about coffee: '{coffee_image_fact['fact']}', "
        f"and available stores: {online_store_suggestions}. Machine learning recommendations are: {ml_recommendations}. "
        "Craft an engaging response that matches the specified tone and language, detailing each coffee’s unique features and where to buy it."
    )
    
    # Generate response
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": recommendation_prompt}],
    )

    response = completion.choices[0].message.content
    translated_response = translate_response(response, language)
    
    # Save assistant's response to history
    save_history(user_id, {"role": "assistant", "content": translated_response})
    
    return translated_response

