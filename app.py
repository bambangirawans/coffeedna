import streamlit as st
from backend.chat_logic import get_coffee_recommendation

st.set_page_config(page_title="CoffeeDNA Chat", page_icon="☕", layout="centered")

# Sidebar 
with st.sidebar:
    st.image("images/logo.png", width=120)
    st.title("Personalize Your Brew")
    st.markdown("Set your preferences to customize recommendations:")
    language = st.selectbox("🌐 Language", ["English", "Bahasa Indonesia"], key="language")
    tone = st.selectbox("🎭 Tone", ["Friendly", "Professional"], key="tone")
    detail_level = st.selectbox("🔍 Detail Level", ["Concise", "Detailed"], key="detail_level")
    flavor_profile = st.text_input("🍫 Flavor Profile", "e.g., strong, bold", key="flavor_profile")
    bean_type = st.text_input("☕ Bean Type", "e.g., Arabica", key="bean_type")

# Header 
st.title("☕ Welcome to CoffeeDNA Chat!")
st.markdown("### Discover Your Perfect Coffee Match!")
st.write("**Tell us what you're in the mood for, and let CoffeeDNA craft your ideal coffee recommendation!**")
st.write("---")

# Initialize Session State for User ID, Chat History, and Clear Flag
if 'user_id' not in st.session_state:
    st.session_state.user_id = "U001"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'clear_chat' not in st.session_state:
    st.session_state.clear_chat = False

# Chat Function
def chat():
    st.markdown("**Start a conversation with CoffeeDNA:**")
    user_input = st.text_input("Type your message here...", key="user_input", 
                               placeholder="e.g., Suggest a smooth, rich coffee with low acidity",
                               help="Describe your coffee preferences or ask for a specific recommendation.")
    
    # Check for "clear all chat" command
    if user_input.lower().strip() == "clear all chat":
        st.session_state.chat_history = []
        st.session_state.clear_chat = True  # Set flag to true to indicate a clear request

    # Chat Button with Feedback and Animated Spinner
    if st.button("Send") and user_input:
        # Ignore "clear all chat" as an input message
        if st.session_state.clear_chat:
            st.session_state.clear_chat = False  # Reset flag after clearing
            st.success("Chat history cleared! Start a new conversation.")
        else:
            # Display a loading spinner for interaction feedback
            with st.spinner("Brewing up your perfect match..."):
                # Collect user preferences
                user_preferences = {
                    "language": language,
                    "tone": tone,
                    "detail_level": detail_level,
                    "flavor_profile": flavor_profile,
                    "bean_type": bean_type
                }
                
                # Retrieve Coffee Recommendation
                response = get_coffee_recommendation(st.session_state.user_id, user_input, user_preferences)
                
                # Append to Chat History
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "assistant", "content": response})

            # Visual Separator for Each Conversation
            st.write("---")
            
            # Display Chat History with Expanders
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    with st.expander(f"👤 You: {message['content'][:30]}..."):
                        st.markdown(f"**You:** {message['content']}")
                else:
                    with st.expander(f"🤖 CoffeeDNA: {message['content'][:30]}..."):
                        st.markdown(f"**CoffeeDNA:** {message['content']}")

# Execute Chat Function
chat()

# Footer
st.write("---")
st.caption("💡 Tip: Type 'clear all chat' to start a new conversation. Adjust your preferences on the sidebar to fine-tune recommendations. Enjoy your coffee journey with CoffeeDNA!")
