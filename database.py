import mysql.connector
from mysql.connector import Error

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            database="remote_access_management",
            user="remote_app",
            password="Pemisire@8901!"
        )

        return connection

    except mysql.connector.Error as error:
        print(f"Database connection error: {error}")
        return None

def test_connection():
    connection = get_connection()

    if connection:
        print("MySQL connection successful")
        connection.close()
        return True

    print("MySQL connection failed")
    return False

if __name__ == "__main__":
    test_connection()