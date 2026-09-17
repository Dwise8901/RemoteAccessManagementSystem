from database import get_connection


connection = get_connection()

if connection:
    cursor = connection.cursor()

    cursor.execute("SELECT DATABASE()")

    print("Python is connected to:")
    print(cursor.fetchone()[0])

    cursor.execute("SHOW COLUMNS FROM devices")

    print("\nDevices table columns:")

    for column in cursor.fetchall():
        print(column)

    cursor.close()
    connection.close()
else:
    print("Unable to connect to MySQL.")