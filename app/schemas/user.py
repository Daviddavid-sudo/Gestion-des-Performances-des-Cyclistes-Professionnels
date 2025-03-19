import sqlite3

def create_user_table():
    try:
        c.execute("""CREATE TABLE user 
                  (id PRIMARY KEY, 
                  name, 
                  email, 
                  password)""")
    except:
        pass


def create_performance_table():
    try:
        c.execute("""CREATE TABLE performance 
                  (ppo, 
                  vo2)""")
    except:
        pass


def insert_user(x,y,z):
    c.execute("""INSERT INTO user(name,email,password) VALUES (?,?,?)""", (x, y, z))


def insert_performance(x,y):
    c.execute("""INSERT INTO performance(ppo,vo2) VALUES (?,?)""", (x, y))


def update_user(x,y,z):
    c.execute("""UPDATE user SET name = ? WHERE email= ? AND password = ?""",(x,y,z) )


def delete_user(x,y):
    c.execute("""DELETE FROM user WHERE email= ? AND password = ?""",(x,y) )


def select_users():
    sql = "SELECT * FROM user"
    recs = c.execute(sql)
    for row in recs:
        print(row)

def select_user(x):
    sql = "SELECT * FROM user WHERE email = ?"
    recs = c.execute(sql, (x,))
    return recs


def select_performances():
    sql = "SELECT * FROM performance"
    recs = c.execute(sql)
    l = []
    for row in recs:
        print(row)
        l.append(row)
    return l

def select_performance(x):
    sql = "SELECT * FROM performance WHERE vo2 = ?"
    recs = c.execute(sql, (x,))
    for row in recs:
        print(row)


conn = sqlite3.connect('database.db')
c = conn.cursor()
# create_user_table()
# create_performance_table()
# insert_user("David", "do", "45")
# insert_performance(80,90)
# update_user("David3","do","45")
# delete_user("do","45")
select_users()
select_user("do")
select_performances()
select_performance(90)
conn.commit()
c.close()