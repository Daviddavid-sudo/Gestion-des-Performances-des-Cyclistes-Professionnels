from models.models import select_user, insert_user, insert_athlete
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

cyclistes = [
    {"name": "Thomas Dupont", "email": "thomas@mail.com", "password": "password1", "role": "athlete", "age": 25, "weight": 70, "height": 175},
    {"name": "Emma Lefebvre", "email": "emma@mail.com", "password": "password2", "role": "athlete", "age": 22, "weight": 60, "height": 168},
    {"name": "Lucas Morel", "email": "lucas@mail.com", "password": "password3", "role": "athlete", "age": 30, "weight": 75, "height": 180},
    {"name": "Sophie Bernard", "email": "sophie@mail.com", "password": "password4", "role": "athlete", "age": 28, "weight": 65, "height": 170},
    {"name": "Julien Martin", "email": "julien@mail.com", "password": "password5", "role": "athlete", "age": 26, "weight": 68, "height": 172},
    {"name": "Camille Robert", "email": "camille@mail.com", "password": "password6", "role": "athlete", "age": 24, "weight": 62, "height": 166},
    {"name": "Antoine Girard", "email": "antoine@mail.com", "password": "password7", "role": "athlete", "age": 27, "weight": 72, "height": 178},
]

# Insert users and athlete
for cycliste in cyclistes:
    insert_user(cycliste["name"], cycliste["email"], cycliste["password"], cycliste["role"])
    
    c.execute("SELECT id FROM user WHERE email = ?", (cycliste["email"],))
    user_id = c.fetchone()[0]
    insert_athlete(user_id, cycliste["age"], cycliste["weight"], cycliste["height"])

print("7 cyclists created!")

conn.close()