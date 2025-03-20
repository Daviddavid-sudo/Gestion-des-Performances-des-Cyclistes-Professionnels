import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
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
                  height INTEGER,
                  FOREIGN KEY (athlete_id) REFERENCES user (id))""")
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
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""INSERT INTO user(name, email, password, role) VALUES (?,?,?,?)""", (name, email, password, role))
    conn.commit()
    c.close()


def select_user(email):
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()

    sql = "SELECT * FROM user WHERE email = ?"
    recs = c.execute(sql, (email,))
    recs=c.fetchone()
    c.close()
    return recs


def insert_athlete(athlete_id, age, weight, height):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""INSERT INTO athlete(athlete_id, age, weight, height) VALUES (?,?,?,?)""", (athlete_id, age, weight, height))
    conn.commit()
    c.close()


def select_athlete(athlete_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT * FROM athlete WHERE athlete_id = ?"
    recs = c.execute(sql, (athlete_id,))
    recs=c.fetchone()
    c.close()
    return recs


def select_performance(athlete_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT * FROM performance WHERE athlete_id = ?"
    recs = c.execute(sql, (athlete_id,))
    columns = [desc[0] for desc in c.description]
    recs = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return recs 


def select_all_performance():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT * FROM performance"
    recs = c.execute(sql)
    columns = [desc[0] for desc in c.description]
    recs = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return recs 


def select_avg_power():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT athlete_id, avg(ppo) FROM performance ORDER BY ppo DESC")
    row = c.fetchone()
    conn.close()
    return {
        "athlete_id": row[0],
        "average ppo": row[1]
    } if row else {}


def select_max_vo2():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT performance.athlete_id, performance.vo2max FROM performance JOIN athlete ON performance.athlete_id = performance.athlete_id ORDER BY vo2max DESC")
    row = c.fetchone()
    conn.close()
    return {
        "athlete_id": row[0],
        "vo2max": row[1]
    } if row else {}


def select_max_weight_power_ratio():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
                SELECT performance.athlete_id, athlete.weight, performance.ppo,
                (performance.ppo / athlete.weight) AS power_ratio 
                FROM performance 
                JOIN athlete ON performance.athlete_id = athlete.athlete_id
                ORDER BY ppo/weight DESC""")
    row = c.fetchone()
    conn.close()
    return {
        "athlete_id": row[0],
        "weight": row[1],
        "ppo": row[2],
        "power_ratio": row[3]
    } if row else {}


def insert_performance(athlete_id, vo2max, hr, rf, cadence, ppo, completion_date):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""INSERT INTO performance(athlete_id, vo2max, hr, rf, cadence, ppo, completion_date) VALUES (?,?,?,?,?,?,?)""", (athlete_id,vo2max, hr, rf, cadence, ppo, completion_date))
    conn.commit()
    c.close()


def modify_performance(performance_id, athlete_id, vo2max, hr, rf, cadence, ppo, completion_date):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """UPDATE performance SET athlete_id = ?, vo2max = ?, hr= ?, rf= ?, cadence= ?, ppo= ?, completion_date= ? WHERE performance_id = ?"""
    c.execute(sql, (athlete_id,vo2max, hr, rf, cadence, ppo, completion_date, performance_id))
    conn.commit()
    c.close()


def delete_performance(performance_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """DELETE FROM performance WHERE performance_id = ?"""
    c.execute(sql, (performance_id,))
    conn.commit()
    c.close()


def get_role(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT role FROM user WHERE id = ?"
    recs = c.execute(sql, (id,))
    columns = [desc[0] for desc in c.description]
    recs = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return recs 