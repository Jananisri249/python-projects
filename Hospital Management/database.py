import json 
from pathlib import Path 
 
DB_FILE = Path("data.json") 
 
DEFAULT_DB = { 
    "admins": [{"user_id": 1, "name": "Admin", "role": "admin", "password": "admin123"}], 
    "doctors": [], 
    "patients": [], 
    "appointments": [], 
    "next_ids": {"doctor": 1, "patient": 1, "appointment": 1} 
} 
 
def read_db(): 
    if not DB_FILE.exists(): 
        write_db(DEFAULT_DB) 
    with open(DB_FILE, "r") as f: 
        return json.load(f) 
 
def write_db(data): 
    with open(DB_FILE, "w") as f: 
        json.dump(data, f, indent=4) 