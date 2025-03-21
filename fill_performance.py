import requests
import json
from models.models import insert_performance
import sqlite3



#Token
with open("json_file/bonus_sbj.json", "r") as file:  # Remplace "data.json" par le chemin de ton fichier
    json_data = json.load(file)

# Extract the values
payload = {
    "vo2max": int(json_data["vo2.max"]),
    "hr": int(json_data["hr.max"]),
    "rf": int(json_data["rf.max"]),
    "cadence": int(json_data["cadence.max"]),
    "ppo": int(json_data["power.max"]),
    "completion_date": "2025-03-21"  # to adapt
}

# # Envoi de la requête POST
# response = requests.post(API_URL, json=payload, headers=headers)

# # Affichage de la réponse
# print(response.status_code, response.json())


# Insert users and athlete
conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
insert_performance(athlete_id=8,completion_date="03/01/2025",vo2max=payload["vo2max"],
                       hr=payload["hr"],cadence=payload["cadence"],ppo=payload['ppo'],rf=payload['rf'])

print("1 performance created!")

conn.close()