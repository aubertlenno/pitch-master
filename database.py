import mysql.connector

def get_db_connection():
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        database='pitch-master'
    )
    return mydb