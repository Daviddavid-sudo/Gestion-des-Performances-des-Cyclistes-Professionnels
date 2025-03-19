import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


def create_user_table():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS user
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  email TEXT,
                  password TEXT,
                  role TEXT )""")
    except:
        pass

def create_athlete_table():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS athlete
                  (athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  age INTEGER,
                  weight INTEGER,
                  height INTEGER)""")
    except:
        pass

def create_performance_table():
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS performance
                  (performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  athlete_id INTEGER,
                  vo2max INTEGER,
                  hr INTEGER,
                  rf INTEGER,
                  cadence INTEGER,
                  ppo INTEGER,
                  completion_date str,
                  FOREIGN KEY (athlete_id) REFERENCES athlete (athlete_id))""")
    except:
        pass

def insert_user(name, email, password, role):
    c.execute("""INSERT INTO user(name, email, password, role) VALUES (?,?,?,?)""", (name, email, password, role))
    conn.commit()
    c.close()

def select_user(email):
    sql = "SELECT * FROM user WHERE email = ?"
    recs = c.execute(sql, (email,))
    recs=c.fetchone()
    return recs


# if __name__ == "__main__":
#     create_user_table(), create_performance_table(), create_athlete_table()