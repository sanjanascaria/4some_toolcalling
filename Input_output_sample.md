# Sample Input-Outputs


## Endpoints

### Start Matching Session
**POST** `/start_match/`

Initiates a matching session for a user and returns initial matches.

**Sample Input:**
```
{"user_id": 6206263409739149989}
```

**Sample Output:**
```json
{
  "session_id": "bfd5f213-45b1-4227-8134-cade69c849b5",
  "matches": [
    {
      "id": 6216601095024764000,
      "personality_type": "Extrovert",
      "age_range": "26-35",
      "interest": "Music lovers / concert-goers",
      "location": "Berlin",
      "willing_to_travel": "No",
      "gender_pref": "Women",
      "feedback": ""
    },
    {
      "id": 6234120196571613000,
      "personality_type": "Introvert",
      "age_range": "21-25",
      "interest": "Creative Arts & DIY (Street Art, Thrifting, Photography)",
      "location": "Berlin",
      "willing_to_travel": "No",
      "gender_pref": "No Preference ",
      "feedback": ""
    },
    {
      "id": 6226949581992483000,
      "personality_type": "Introvert",
      "age_range": "45-59",
      "interest": "Sports & Outdoor Community (Hiking, Skating, Surfing)",
      "location": "Berlin",
      "willing_to_travel": "No",
      "gender_pref": "LGBTQ+",
      "feedback": ""
    }
  ]
}
```

---

### Submit Feedback
**POST** `/submit_feedback/`

User submits feedback on the matches at this endpoint.

**Sample Input:**
```json
{
  "session_id": "bfd5f213-45b1-4227-8134-cade69c849b5",
  "user_input": "I am not happy with these matches. Can I get new suggestions?"
}
```

**Sample Output:**
```json
{
  "matches": [
    {
      "id": 6228817592647750000,
      "personality_type": "Extrovert",
      "age_range": "26-35",
      "interest": "Music lovers / concert-goers",
      "location": "Berlin",
      "willing_to_travel": "Yes",
      "gender_pref": "Women",
      "feedback": ""
    },
    {
      "id": 6206263409739150000,
      "personality_type": "Introvert",
      "age_range": "26-35",
      "interest": "Creative Arts & DIY (Street Art, Thrifting, Photography)",
      "location": "Berlin",
      "willing_to_travel": "Yes",
      "gender_pref": "No Preference ",
      "feedback": ""
    },
    {
      "id": 6216601095024764000,
      "personality_type": "Extrovert",
      "age_range": "26-35",
      "interest": "Music lovers / concert-goers",
      "location": "Berlin",
      "willing_to_travel": "No",
      "gender_pref": "Women",
      "feedback": ""
    }
  ],
  "llm_decision": "New matches generated. Are you happy with this selection?"
}
```

**Sample Input:**
```json
{
  "session_id": "bfd5f213-45b1-4227-8134-cade69c849b5",
  "user_input": "I like the new matches, thank you."
}
```

**Sample Output:**
```json
{
  "message": "Glad you're happy with the matches!"
}
```

---

