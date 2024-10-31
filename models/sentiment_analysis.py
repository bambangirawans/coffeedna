from transformers import pipeline

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(user_input):
    return sentiment_analyzer(user_input)[0]
