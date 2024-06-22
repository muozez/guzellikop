import MySQLdb

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="kayit_isletme"
    )
