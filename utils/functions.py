import bcrypt
from .database import connDatabase 


def verifyEmail(email):
    sql = "SELECT email FROM data"
    dbs = connDatabase()
    cursor = dbs.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    return False if res == [] else email in [x[0] for x in res]

def getSalt(email):
    sql = "SELECT salt FROM data WHERE email = %s"
    dbs = connDatabase()
    cursor = dbs.cursor()
    cursor.execute(sql, (email,))
    return cursor.fetchone()[0].encode()

def hashPass(password, salt):
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode()

def writePass(email, password):
    salt = bcrypt.gensalt()
    hashed = hashPass(password, salt)
    sql = "INSERT INTO data (email, pass, salt) VALUES (%s, %s, %s)"
    dbs = connDatabase()
    dbs.cursor().execute(sql, (email, hashed, salt.decode()))
    dbs.commit()
    pass

def verifyPass(email, password):
    if verifyEmail(email):
        salt = getSalt(email)
        hashed = hashPass(password, salt)
        sql = "SELECT pass FROM data WHERE email = %s"
        dbs = connDatabase()
        cursor = dbs.cursor()
        cursor.execute(sql, (email,))
        res = cursor.fetchone()
        return False if res == None else res[0] == hashed 
    else:
        return False

def resetPass(email, password):
    salt = bcrypt.gensalt()
    hashed = hashPass(password, salt)
    sql = "UPDATE data SET pass = %s, salt = %s WHERE email = %s"
    dbs = connDatabase()
    cursor = dbs.cursor()
    cursor.execute(sql, (hashed, salt.decode(), email))
    dbs.commit()
