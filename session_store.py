# session_store.py
from uuid import uuid4

sessions = {}

def create_session(user_id, initial_matches):
    session_id = str(uuid4())
    sessions[session_id] = {
        "user_id": user_id,
        "matches": initial_matches,
        "chat_history": []
    }
    return session_id

def get_session(session_id):
    return sessions.get(session_id)

def update_session(session_id, key, value):
    if session_id in sessions:
        sessions[session_id][key] = value
