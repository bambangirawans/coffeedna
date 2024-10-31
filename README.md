```markdown
# CoffeeDNA ☕

**Discover Your Coffee DNA – Personalized Brews, Perfectly Matched**

CoffeeDNA is an interactive, AI-driven chat application that personalizes coffee recommendations based on users' unique flavor profiles and preferences. The app allows users to set preferences such as language, tone, detail level, and desired coffee characteristics to receive the perfect coffee match tailored just for them.

## Table of Contents
- [Features](#features)
- [Screenshots](#screenshots)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Personalized Coffee Recommendations**: Users receive tailored coffee suggestions based on their input,  preference settings, analyze sentiment, similarity using  langchain OpenAIEmbeddings
- **Customizable Preferences**: Language, tone, and level of detail can be set to match each user’s style.
- **Flavor Profile Matching**: Unique flavor preferences, including bean type and coffee strength, refine recommendations.
- **Chat History with Message Re-Selection**: Users can select previous messages to use as new input, expanding upon earlier conversations.

## Getting Started

### Prerequisites
- **Python 3.7+**: Ensure you have Python installed on your machine.
- **Streamlit**: Install Streamlit for the web interface.
- Other dependencies can be found in `requirements.txt`.

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/bambangirawans/coffeedna.git
   cd coffeedna
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenAI API Key**:
   - Create a `.env` file in the root directory:
     ```bash
     touch .env
     ```
   - Add your `OPENAI_API_KEY` to the `.env` file:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   This key is required for accessing OpenAI’s API to generate coffee recommendations.

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

6. Open [http://localhost:8501](http://localhost:8501) in your browser to access the application.

## Usage

1. **Set Preferences**: Use the sidebar to select language, tone, detail level, and specify your coffee preferences (e.g., flavor profile and bean type).
2. **Chat**: Enter your coffee preference query in the chat box and click "Send." The AI will respond with a tailored coffee recommendation.
3. **Re-use Previous Messages**: Click "Use as Input" on any previous message to modify and send it as a new query, enhancing the conversation.

## Environment Variables
The following environment variable is required for CoffeeDNA to work correctly:
- `OPENAI_API_KEY`: The API key to access OpenAI’s API. Set this in the `.env` file as described in the [Getting Started](#getting-started) section.

## Contributing
We welcome contributions to make CoffeeDNA even better! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your fork and create a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- CoffeeDNA is inspired by the love for personalized coffee experiences.
- Special thanks to all contributors and users who make this project possible.

## Contact
For questions or feedback, feel free to reach out or open an issue on this repository!

---

Happy brewing with CoffeeDNA! ☕
```

This update includes a new section, **Environment Variables**, explaining how to add the `OPENAI_API_KEY` in a `.env` file, which will be securely accessed by your application.
