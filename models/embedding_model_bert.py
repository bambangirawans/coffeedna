import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize the SBERT model
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')  # A lightweight SBERT model suitable for embedding similarity

def load_coffee_data():
    """Load coffee profile data from CSV."""
    try:
        return pd.read_csv('data/coffee_profiles.csv')
    except (UnicodeDecodeError, FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        print(f"Error loading coffee data: {e}")
        return pd.DataFrame()

def generate_coffee_embeddings(coffee_profiles):
    """Generate SBERT embeddings for each coffee profile."""
    try:
        return sbert_model.encode(coffee_profiles, convert_to_tensor=False)
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

def get_user_embedding(user_preferences):
    """Generate an embedding for the user preferences."""
    preferences_text = f"{user_preferences.get('flavor_profile', '')} {user_preferences.get('coffee_types', '')}"
    try:
        return sbert_model.encode([preferences_text])[0]  # Single embedding in array format
    except Exception as e:
        print(f"Error generating user embedding: {e}")
        return None

def recommend_coffees(user_preferences, coffee_data):
    """Generate top coffee recommendations based on user preferences."""
    if coffee_data.empty:
        print("Error: Coffee data is empty.")
        return []

    # Prepare text descriptions for embeddings
    coffee_data['coffee_profile'] = coffee_data.apply(
        lambda row: f"{row['coffee_type']} with a {row['flavor_profile']} flavor available at {row['store']} - {row['url']}", 
        axis=1
    )
    coffee_profiles = coffee_data["coffee_profile"].tolist()

    # Generate coffee profile embeddings
    coffee_embeddings = generate_coffee_embeddings(coffee_profiles)
    user_embedding = get_user_embedding(user_preferences)

    if user_embedding is None or not coffee_embeddings:
        print("Error: Embedding generation failed.")
        return []

    # Use FAISS for efficient similarity searching
    embedding_dim = len(user_embedding)
    index = faiss.IndexFlatL2(embedding_dim)  # L2 distance (can also use IndexFlatIP for cosine similarity approximation)
    index.add(np.array(coffee_embeddings).astype('float32'))  # Add coffee embeddings to the FAISS index

    # Perform the search to get top 5 similar coffees
    user_embedding = np.array([user_embedding]).astype('float32')
    distances, indices = index.search(user_embedding, k=5)  # Retrieve top 5 matches
    recommended_indices = indices[0]

    # Retrieve recommended coffee information
    recommended_coffees = coffee_data.iloc[recommended_indices][["coffee_type", "store", "url"]]
    return recommended_coffees.to_dict(orient="records")
