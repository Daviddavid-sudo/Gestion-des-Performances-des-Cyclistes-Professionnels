import requests
import json

# URL de ton API
API_URL = "http://localhost:8000/performance/create"  

#Token
with open("data.json", "r") as file:  # Remplace "data.json" par le chemin de ton fichier
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

# # En-têtes HTTP
# headers = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Content-Type": "application/json"
# }

# Envoi de la requête POST
response = requests.post(API_URL, json=payload, headers=headers)

# Affichage de la réponse
print(response.status_code, response.json())
