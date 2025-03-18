import sqlite3
from core.security import get_password_hash

## Creation of the database
conn = sqlite3.connect('api.db') # Connexion to the db
cursor = conn.cursor() # creation of a cursor

requete = """CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    password TEXT,
    role TEXT);"""

cursor.execute(requete)

conn.commit()

conn.close()

# Test to fill the database
conn = sqlite3.connect('api.db')
cursor = conn.cursor() 

requete = """INSERT INTO users(firstname, lastname, email, password, role) VALUES (?, ?, ?, ?, ?);""" 

cursor.execute(requete, ('Titi', 'tata', 'tata@mail.com', 'password', 'coach')) # execution of the requete with the values to insert into the db

conn.commit() 
conn.close() 

## Test to modify the db

conn = sqlite3.connect('api.db')
cursor = conn.cursor()

password = get_password_hash('password')

requete = """UPDATE users SET password = ? WHERE id = ?;""" 

cursor.execute(requete, (password, 1))  # Paramètres passés en tuple

conn.commit()
conn.close()
