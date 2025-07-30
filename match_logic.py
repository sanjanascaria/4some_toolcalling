# match_logic.py
import random
import ollama
from fastapi import HTTPException

from create_db import get_conn

model = 'qwen2.5:7b'

# function that implements the basic match logic 
def matching_logic(user_id):
    with get_conn() as conn:
        cur = conn.cursor()
        # selecting informaiton of the user for whom matches must be generated
        cur.execute("SELECT * from users WHERE id = ?;", (user_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"User not found. Please enter a valid id.")
        user_details = dict(zip([column[0] for column in cur.description], row))
    with get_conn() as conn:
        cur = conn.cursor()
        # selecting users who reside in the same city or are willing to travel to the city
        cur.execute("SELECT * from users where id != ? and location = ? or willing_to_travel = ?;", (user_details['id'], user_details['location'], 'Yes'))
        rows = cur.fetchall()
    columns = [column[0] for column in cur.description]
    same_city_users = [dict(zip(columns, row)) for row in rows] 
    return random.sample(same_city_users, 3)

# assigning matching_logic() as a tool the llm can access
tools = [
    {
        'type': 'function',
        'function': {
            'name': 'matching_logic',
            'description': 'Suggest new users based on location.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'}
                },
                'required': ['user_id']
            }
        }
    }
]

system_prompt = {
    "role": "system",
    "content": (
        "You are a match assistant. Present user suggestions and ask if the user is happy. "
        "If they are not, call the matching_logic tool again."
    )
}

# function that interacts with the LLM Agent
def ask_llm(user_input, match_suggestions, chat_history, user_id):
    messages = chat_history + [
        system_prompt,
        {
            "role": "assistant",
            "content": f"Here are your suggested matches: {match_suggestions}"
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = ollama.chat(
        model=model,
        messages=messages,
        tools=tools
    )

    return dict(response['message'])
