# Tech Stack:

- FastAPI for the web framework implementation.
- SQLite for database management. 
- Ollama for local llm inference.
- (requirements.txt included)

# List of files:

## 4some_users.csv

I cleaned the user data that was shared with me to match few of the user characteristics mentioned in the documentation (I'm aware that most of the logic here is obviously not ideal, just wanted a basic data representation to come up with a matching logic to test if the tool call is working.):

1. `User_ID`

    Same as submission id in the original file (hence, did not use `AUTOINCREMENT` in db schema).

3. `Personality`
   
    For now, I used the `How do you typically interact in new settings?` field to tag the user as Introvert/Extrovert.

5. `AgeRange`
   
    Same as `Which age range do you fall into?` field

7. `Interests`
   
    `Creative Arts & DIY (Street Art, Thrifting, Photography)`, `Sports & Outdoor Community (Hiking, Skating, Surfing)` and `Music lovers / concert-goers` seemed to be the most common amongst the users, so I filled them in, in a cyclic fashion. 

9. `Location`
    
    Same as the original file, but retained only the city name. 

11. `WillingnessToTravelToDiffCity`
    
    Used `How far are you willing to travel for a meetup?` field for this.
    - 1-2 hour (different city for the really adventurous, open for it) --> Yes
    - 30-60 min (different area of the city/state) --> No
    - 10-30 min (same city) --> No

13. `GenderPreference`
    
    Used `What’s your preferred friend group composition?` field. 
        Values were mapped to No Preference, LGBTQ+, Women.
    
I've only used the first 11 entries to create .csv file.

## match_logic.py

This code implements a very rudimentary matching logic.

Step 1: Filters those users that are in the same city as the user to be matched with, or are willing to travel to another city for a meet-up. 

Step 2: Selects 3 users at random from this subset. (Step 1 and 2 implemented in `matching_logic()`)

Step 3: Depending on whether the user is satisfied with the matches or not, the LLM Agent decides whether `matching_logic()` must be called again, or if matching can be terminated. (implemeted in `ask_llm()`)

## py_schemas.py

Pydantic schemas for data validation.

## create_db.py

Database schema to store user information.

## session_store.py

In-memory session management for the application.

## app.py

I re-implemented the CRUD operaions from typescript to python, so you can interact with the application and database if you'd like :). 

- `POST /users/` - Create a new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Data Import
- `POST /import_csv/` - Import user data from CSV file

### Matching System
- `POST /start_match/` - Start a new matching session
- `POST /submit_feedback/` - Submit feedback and get new suggestions

# To run the application:

1. Execute either
    `python -m uvicorn app:app --reload` or
    `uvicorn app:app --reload`

2. Go to [http://127.0.0.1:8000/docs] to use SwaggerUI to interact with the various endpoints.

3. Aside from the python import, Ollama should also be installed on your device ([https://ollama.com/]). For the purposes of this app, I am using `qwen2.5:7b` (also must be separately downloaded through Ollama - [https://ollama.com/library/qwen2.5]) but you can use a bigger model for better reliability if your device allows for it. In this case, only the model name (line 8 in `match_logic.py`) would change, nothing else. 

4. Of course, if you have access to the OpenAI api, or any other llm, you can plug that in instead.

## Sample Input-Output



# TO DOs/Improvements:

Once we have a more robust rule based logic for matching, ideally, I would implement an LLM sql agent using `LangChain`. This means, the agent will receive `user feedback + rules for matching` and generate an SQL query. This query will be queried against the db to generate the new matches. 
