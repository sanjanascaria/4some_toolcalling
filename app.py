# app.py
from fastapi import FastAPI, HTTPException
from match_logic import matching_logic, ask_llm
from session_store import create_session, get_session, update_session
from typing import List
import os
import pandas as pd

from create_db import create_table, get_conn, CSV_PATH
from py_schemas import UserCreate, UserRead, UserUpdate, Feedback

create_table()

app = FastAPI()

""" endpoint for importing data from .csv file
    run once to generate 4some_db.db
"""
@app.post("/import_csv/")
def import_csv_to_db(csv_path: str = CSV_PATH):
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail=f"CSV file '{csv_path}' not found.")
    df = pd.read_csv(csv_path)
    with get_conn() as conn:
        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute("""
            INSERT INTO users (id, personality_type, age_range, interest, location, willing_to_travel, gender_pref)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get('User_ID', ''),
                row.get('Personality', ''),
                row.get('AgeRange', ''),
                row.get('Interests', ''),
                row.get('Location', ''),
                row.get('WillingnessToTravelToDiffCity', ''),
                row.get('GenderPreference', '')
            ))
        conn.commit()
    return {"detail": "CSV data imported."}

# --- CRUD Endpoints ---
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (id, personality_type, age_range, interest, location, willing_to_travel, gender_pref)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user.id, user.personality_type, user.age_range, user.interest, user.location, user.willing_to_travel, user.gender_pref))
        user_id = cur.lastrowid
        conn.commit()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return dict(zip([column[0] for column in cur.description], row))
        raise HTTPException(status_code=500, detail="User creation failed")

@app.get("/users/", response_model=List[UserRead])
def list_users():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users;")
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        return [UserRead(**dict(zip(columns, row))) for row in rows]

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        row = cur.fetchone()
        if row:
            return UserRead(**dict(zip([column[0] for column in cur.description], row)))
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate):
    fields = []
    values = []
    for key, value in user_update.dict(exclude_unset=True).items():
        fields.append(f"{key} = ?")
        values.append(value)
    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    values.append(user_id)
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE users SET {', '.join(fields)}
            WHERE id = ?
        """, tuple(values))
        conn.commit()
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return dict(zip([column[0] for column in cur.description], row))
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": f"User {user_id} deleted"}

# endpoint for starting the matching
@app.post("/start_match/")
def start_match(user_id: int):
    initial_matches = matching_logic(user_id)
    session_id = create_session(user_id, initial_matches)
    return {"session_id": session_id, "matches": initial_matches}

# endpoint to receive feedback on the match suggestions from the user
@app.post("/submit_feedback/")
def submit_feedback(feedback: Feedback):
    session = get_session(feedback.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    """ based on the user feedback, the llm agent decides if new matches need to be generated.
        for example, feedback can be "Yes, I am happy with the matches" or "No, I'd like new matches" 
    """
    response = ask_llm(
        user_input=feedback.user_input,
        match_suggestions=session["matches"],
        chat_history=session["chat_history"],
        user_id=session["user_id"]
    )

    update_session(feedback.session_id, "chat_history", session["chat_history"] + [response])

    print(response) # for debugging, can ignore
    
    try:
        # code to execute matching_logic() if the LLM agent decides it is necessary 
        tool_calls = response["tool_calls"]
        for tool in tool_calls:
            if tool["function"]["name"] == "matching_logic":
                new_matches = matching_logic(session["user_id"])
                update_session(feedback.session_id, "matches", new_matches)
                return {"matches": new_matches, "llm_decision": "New matches generated. Are you happy with this selection?"}
    except:
        # if not, matching is terminated.
        return {"message": "Glad you're happy with the matches!"}
