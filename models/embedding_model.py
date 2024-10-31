import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")
llm = OpenAI(api_key=api_key)  
embedder = OpenAIEmbeddings(api_key=api_key)  


def load_coffee_data():
    try:
        return pd.read_csv('data/coffee_profiles.csv')
    except (UnicodeDecodeError, FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error loading coffee data: {e}")
        return pd.DataFrame()


def generate_coffee_embeddings(coffee_profiles):
    if hasattr(embedder, 'embed_text'):
        return [embedder.embed_text(profile) for profile in coffee_profiles]
    else:
        print("Error: embed_text function is missing in OpenAIEmbeddings.")
        return []

def get_user_embedding(user_preferences):
    preferences_text = f"{user_preferences.get('flavor_profile', '')} {user_preferences.get('coffee_types', '')}"
    if hasattr(embedder, 'embed_text'):
        return embedder.embed_text(preferences_text)
    else:
        print("Error: embed_text function is missing in OpenAIEmbeddings.")
        return None

def recommend_coffees(user_preferences, coffee_data):
    if coffee_data.empty:
        print("Error: Coffee data is empty.")
        return []

    coffee_data['coffee_profile'] = coffee_data.apply(
        lambda row: f"{row['coffee_type']} with a {row['flavor_profile']} flavor available at {row['store']} - {row['url']}", 
        axis=1
    )
    coffee_profiles = coffee_data["coffee_profile"].tolist()
    coffee_embeddings = generate_coffee_embeddings(coffee_profiles)
    user_embedding = get_user_embedding(user_preferences)

    if user_embedding is None or not coffee_embeddings:
        print("Error: Embedding generation failed.")
        return []

    if hasattr(embedder, 'similarity'):
        similarity_scores = [embedder.similarity(user_embedding, coffee_emb) for coffee_emb in coffee_embeddings]
        coffee_data['similarity'] = similarity_scores
    else:
        print("Error: similarity function is missing in OpenAIEmbeddings.")
        return []

    recommended_coffees = coffee_data.sort_values(by="similarity", ascending=False).head(5)
    return recommended_coffees[["coffee_type", "store", "url"]].to_dict(orient="records")

