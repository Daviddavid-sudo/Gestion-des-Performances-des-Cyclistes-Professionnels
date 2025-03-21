import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()


def create_user_table():
    """
    Creates the 'user' table in the database if it does not already exist.

    The table has the following columns:
    - id: INTEGER, primary key, auto-incremented
    - name: TEXT, the name of the user
    - email: TEXT, the email address of the user
    - password: TEXT, the password of the user
    - role: TEXT, the role of the user

    If the table creation fails, the exception is caught and passed.
    """

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
    """
    Creates the 'athlete' table in the database if it does not already exist.
    
    The table includes the following columns:
    - athlete_id: INTEGER, primary key, auto-incremented
    - age: INTEGER, age of the athlete
    - weight: INTEGER, weight of the athlete
    - height: INTEGER, height of the athlete
    
    The athlete_id column is a foreign key that references the id column in the 'user' table.
    
    If the table creation fails, the exception is caught and passed.
    """
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
    """
    Creates the 'performance' table in the SQLite database if it does not exist.

    The table includes the following columns:
    - performance_id: INTEGER, primary key, auto-incremented
    - athlete_id: INTEGER, foreign key referencing athlete (athlete_id)
    - vo2max: INTEGER, VO2 max value
    - hr: INTEGER, heart rate
    - rf: INTEGER, respiratory frequency
    - cadence: INTEGER, cycling cadence
    - ppo: INTEGER, peak power output
    - completion_date: str, date of performance completion

    If the table already exists, the function does nothing.
    """
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
    """
    Inserts a new user into the user table in the database.

    Args:
        name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The password for the user.
        role (str): The role of the user.

    Returns:
        None
    """

    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("""INSERT INTO user(name, email, password, role) VALUES (?,?,?,?)""", (name, email, password, role))
    conn.commit()
    c.close()


def select_user(email):
    """
    Retrieve a user record from the database based on the provided email.

    Args:
        email (str): The email address of the user to be selected.

    Returns:
        tuple: A tuple containing the user's information if found, otherwise None.
    """
    conn = sqlite3.connect('database.db', check_same_thread=False)
    c = conn.cursor()

    sql = "SELECT * FROM user WHERE email = ?"
    recs = c.execute(sql, (email,))
    recs=c.fetchone()
    c.close()
    return recs


def insert_athlete(athlete_id, age, weight, height):
    """
    Inserts a new athlete into the athlete table in the database.

    Args:
        athlete_id (int): The unique identifier for the athlete.
        age (int): The age of the athlete.
        weight (float): The weight of the athlete in kilograms.
        height (float): The height of the athlete in centimeters.

    Returns:
        None
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""INSERT INTO athlete(athlete_id, age, weight, height) VALUES (?,?,?,?)""", (athlete_id, age, weight, height))
    conn.commit()
    c.close()


def select_athlete(athlete_id):
    """
    Retrieve an athlete's record from the database based on the athlete's ID.

    Args:
        athlete_id (int): The ID of the athlete to be selected.

    Returns:
        tuple: A tuple containing the athlete's record if found, otherwise None.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT * FROM athlete WHERE athlete_id = ?"
    recs = c.execute(sql, (athlete_id,))
    recs=c.fetchone()
    c.close()
    return recs

def delete_athlete(athlete_id):
    """
    Deletes an athlete from the database based on the provided athlete_id.

    Args:
        athlete_id (int): The ID of the athlete to be deleted.

    Raises:
        sqlite3.OperationalError: If there is an error executing the SQL command.

    Example:
        delete_athlete(123)
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    try:
        sql = "DELETE FROM athlete WHERE athlete_id = ?"
        c.execute(sql, (athlete_id,))
        conn.commit()
    except sqlite3.OperationalError as e:
        print("Error Sqlite :", e)
    finally:
        c.close()

def modify_athlete(athlete_id, **kwargs):
    """
    Modify the details of an athlete in the database.

    Args:
        athlete_id (int): The ID of the athlete to be modified.
        **kwargs: Arbitrary keyword arguments representing the fields to be updated and their new values.

    Returns:
        dict: A dictionary containing a success message if the update was successful, 
              or an error message if an exception occurred.

    Example:
        modify_athlete(1, name="John Doe", age=30, team="Team A")
    """
    conn = sqlite3.connect('database.db')
    c =conn.cursor()

    fields= ", ".join(f"{key} = ?" for key in kwargs.keys())
    values = list(kwargs.values()) + [athlete_id]
    sql = f"UPDATE athlete SET {fields} WHERE athlete_id = ?"

    try:
        c.execute(sql, values)
        conn.commit()
        return {"message": "Athlete updated successfully"}
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        c.close()

def modify_user(id: int, **kwargs):
    """
    Modify a user's information in the database.

    Args:
        id (int): The ID of the user to be modified.
        **kwargs: Arbitrary keyword arguments representing the fields to be updated and their new values.

    Returns:
        dict: A dictionary containing a success message if the update was successful, 
              or an error message if an exception occurred.
    """
    conn = sqlite3.connect('database.db')
    c =conn.cursor()

    fields= ", ".join(f"{key} = ?" for key in kwargs.keys())
    values = list(kwargs.values()) + [id]
    sql = f"UPDATE user SET {fields} WHERE id = ?"

    try:
        c.execute(sql, values)
        conn.commit()
        return {"message": "user updated successfully"}
    except sqlite3.Error as e:
        return {"error": str(e)}
    finally:
        c.close()

def select_performance(athlete_id):
    """
    Retrieve performance records for a specific athlete from the database.

    Args:
        athlete_id (int): The ID of the athlete whose performance records are to be retrieved.

    Returns:
        list[dict]: A list of dictionaries where each dictionary represents a performance record.
                    The keys of the dictionary are the column names of the performance table.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT * FROM performance WHERE athlete_id = ?"
    recs = c.execute(sql, (athlete_id,))
    columns = [desc[0] for desc in c.description]
    recs = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return recs 


def select_all_performance():
    """
    Retrieve all records from the 'performance' table in the database.

    This function connects to the 'database.db' SQLite database, executes a 
    SQL query to select all records from the 'performance' table, and returns 
    the results as a list of dictionaries where each dictionary represents a 
    row with column names as keys.

    Returns:
        list of dict: A list of dictionaries, each containing the data of a 
        row from the 'performance' table with column names as keys.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT * FROM performance"
    recs = c.execute(sql)
    columns = [desc[0] for desc in c.description]
    recs = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return recs 


def select_avg_power():
    """
    Retrieves the average peak power output (PPO) for the athlete with the highest PPO from the database.

    Connects to the 'database.db' SQLite database, executes a query to join the 'performance' and 'user' tables,
    and selects the athlete ID, name, email, and average PPO, ordered by PPO in descending order. Returns the
    details of the athlete with the highest average PPO.

    Returns:
        dict: A dictionary containing the athlete's ID, name, email, and average PPO if a record is found,
              otherwise an empty dictionary.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT performance.athlete_id, user.name, user.email, avg(performance.ppo) FROM performance JOIN user ON performance.athlete_id = user.id ORDER BY ppo DESC")
    row = c.fetchone()
    conn.close()
    return {
        "athlete_id": row[0],
        "name": row[1],
        "email": row[2],
        "average ppo": row[3]
    } if row else {}


def select_max_vo2():
    """
    Selects the athlete with the maximum VO2 max value from the database.

    Connects to the 'database.db' SQLite database, executes a query to join 
    the 'performance', 'athlete', and 'user' tables, and retrieves the athlete 
    with the highest VO2 max value. The result includes the athlete's ID, name, 
    email, and VO2 max value.

    Returns:
        dict: A dictionary containing the athlete's ID, name, email, and VO2 max 
              value if a row is found, otherwise an empty dictionary.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""SELECT performance.athlete_id, 
    user.name,
    user.email,
    performance.vo2max 
    FROM performance 
    JOIN athlete ON performance.athlete_id = performance.athlete_id 
    JOIN user ON athlete.athlete_id = user.id
    ORDER BY vo2max DESC""")
    row = c.fetchone()
    conn.close()
    return {
        "athlete_id": row[0],
        "name": row[1],
        "email": row[2],
        "vo2max": row[3]
    } if row else {}


def select_max_weight_power_ratio():
    """
    Selects the athlete with the maximum power-to-weight ratio from the database.

    Connects to the SQLite database 'database.db', executes a query to join the 
    performance, athlete, and user tables, and calculates the power-to-weight ratio 
    (performance.ppo / athlete.weight). The results are ordered in descending order 
    by the power-to-weight ratio, and the top result is fetched.

    Returns:
        dict: A dictionary containing the following keys:
            - athlete_id (int): The ID of the athlete.
            - name (str): The name of the athlete.
            - email (str): The email of the athlete.
            - weight (float): The weight of the athlete.
            - ppo (float): The peak power output (PPO) of the athlete.
            - power_ratio (float): The power-to-weight ratio of the athlete.
        If no result is found, an empty dictionary is returned.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""
                SELECT performance.athlete_id,                 
                user.name,
                user.email,
                athlete.weight, 
                performance.ppo,
                (performance.ppo / athlete.weight) AS power_ratio
                FROM performance 
                JOIN athlete ON performance.athlete_id = athlete.athlete_id
                JOIN user ON athlete.athlete_id = user.id
                ORDER BY ppo/weight DESC""")
    row = c.fetchone()
    conn.close()
    return {
        "athlete_id": row[0],
        "name": row[1],
        "email": row[2],
        "weight": row[3],
        "ppo": row[4],
        "power_ratio": row[5]
    } if row else {}


def insert_performance(athlete_id, vo2max, hr, rf, cadence, ppo, completion_date):
    """
    Inserts a new performance record into the performance table in the database.

    Args:
        athlete_id (int): The ID of the athlete.
        vo2max (float): The VO2 max value of the athlete.
        hr (int): The heart rate of the athlete.
        rf (int): The respiratory frequency of the athlete.
        cadence (int): The cadence of the athlete.
        ppo (float): The peak power output of the athlete.
        completion_date (str): The date of the performance completion in YYYY-MM-DD format.

    Returns:
        None
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""INSERT INTO performance(athlete_id, vo2max, hr, rf, cadence, ppo, completion_date) VALUES (?,?,?,?,?,?,?)""", (athlete_id,vo2max, hr, rf, cadence, ppo, completion_date))
    conn.commit()
    c.close()


def modify_performance(performance_id, athlete_id, vo2max, hr, rf, cadence, ppo, completion_date):
    """
    Modify the performance record in the database with the given parameters.

    Args:
        performance_id (int): The ID of the performance record to modify.
        athlete_id (int): The ID of the athlete associated with the performance.
        vo2max (float): The VO2 max value of the performance.
        hr (int): The heart rate value of the performance.
        rf (int): The respiratory frequency value of the performance.
        cadence (int): The cadence value of the performance.
        ppo (float): The peak power output value of the performance.
        completion_date (str): The completion date of the performance in 'YYYY-MM-DD' format.

    Returns:
        None
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """UPDATE performance SET athlete_id = ?, vo2max = ?, hr= ?, rf= ?, cadence= ?, ppo= ?, completion_date= ? WHERE performance_id = ?"""
    c.execute(sql, (athlete_id,vo2max, hr, rf, cadence, ppo, completion_date, performance_id))
    conn.commit()
    c.close()


def delete_performance(performance_id):
    """
    Delete a performance record from the database.

    Args:
        performance_id (int): The ID of the performance record to be deleted.

    Raises:
        sqlite3.DatabaseError: If there is an issue with the database operation.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = """DELETE FROM performance WHERE performance_id = ?"""
    c.execute(sql, (performance_id,))
    conn.commit()
    c.close()


def get_role(id):
    """
    Retrieve the role of a user from the database based on their ID.

    Args:
        id (int): The ID of the user.

    Returns:
        list of dict: A list of dictionaries containing the role of the user.
                      Each dictionary has a single key 'role' with the corresponding value.
    """
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = "SELECT role FROM user WHERE id = ?"
    recs = c.execute(sql, (id,))
    columns = [desc[0] for desc in c.description]
    recs = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return recs 

