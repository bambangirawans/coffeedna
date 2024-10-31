import json
import os

history_file_path = os.path.join('data', 'chat_history.json')  # Adjust the path as necessary

def load_history(user_id):
    if not os.path.exists(history_file_path):
        return []
    
    with open(history_file_path, 'r') as file:
        history = json.load(file)
    
    return history.get(user_id, [])

def save_history(user_id, message):
    if not os.path.exists(history_file_path):
        with open(history_file_path, 'w') as file:
            json.dump({}, file)

    with open(history_file_path, 'r') as file:
        history = json.load(file)

    if user_id not in history:
        history[user_id] = []

    history[user_id].append(message)

    with open(history_file_path, 'w') as file:
        json.dump(history, file)
