import mysql.connector


def connDatabase():
    return mysql.connector.connect(
        host="localhost",
        user="username",
        password="password",
        database="database"
    )