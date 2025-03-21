from models.models import insert_user, insert_athlete, insert_performance
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

performances = [
    {"athlete_id": 1, "date": "2021-03-01", "vo2max": 50, "hr": 150, "rf": 20, "cadence": 90, "ppo": 300},
    {"athlete_id": 2, "date": "2021-03-02", "vo2max": 55, "hr": 160, "rf": 22, "cadence": 95, "ppo": 320},
    {"athlete_id": 3, "date": "2021-03-03", "vo2max": 45, "hr": 140, "rf": 18, "cadence": 85, "ppo": 280},
    {"athlete_id": 4, "date": "2021-03-04", "vo2max": 60, "hr": 170, "rf": 24, "cadence": 100, "ppo": 340},
    {"athlete_id": 5, "date": "2021-03-05", "vo2max": 65, "hr": 180, "rf": 26, "cadence": 105, "ppo": 360},
    {"athlete_id": 6, "date": "2021-03-06", "vo2max": 70, "hr": 190, "rf": 28, "cadence": 110, "ppo": 380},
    {"athlete_id": 7, "date": "2021-03-07", "vo2max": 75, "hr": 200, "rf": 30, "cadence": 115, "ppo": 400},
    {"athlete_id": 8, "date": "2021-03-08", "vo2max": 80, "hr": 210, "rf": 32, "cadence": 120, "ppo": 420}
]

# Insert users and athlete
for cycliste in cyclistes:
    insert_user(cycliste["name"], cycliste["email"], cycliste["password"], cycliste["role"])
    
    c.execute("SELECT id FROM user WHERE email = ?", (cycliste["email"],))
    user_id = c.fetchone()[0]
    insert_athlete(user_id, cycliste["age"], cycliste["weight"], cycliste["height"])

# Insert users and athlete
for performance in performances:
    insert_performance(athlete_id=performance["athlete_id"],completion_date=performance["date"],vo2max=performance["vo2max"],
                       hr=performance["hr"],cadence=performance["cadence"],ppo=performance['ppo'],rf=performance['rf'])

print("7 cyclists created!")

conn.close()