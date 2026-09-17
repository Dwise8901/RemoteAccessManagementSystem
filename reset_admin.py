from database import get_connection
from security import hash_password


USERNAME = "admin"
NEW_PASSWORD = "Admin@123"


def reset_admin_password():

    connection = get_connection()

    if not connection:
        print("Unable to connect to MySQL.")
        return

    cursor = connection.cursor()

    try:
        password_hash = hash_password(NEW_PASSWORD)

        sql = """
        UPDATE users
        SET password_hash = %s,
            status = 'ACTIVE',
            role = 'ADMIN'
        WHERE username = %s
        """

        cursor.execute(
            sql,
            (
                password_hash,
                USERNAME
            )
        )

        if cursor.rowcount == 0:
            print("Admin user was not found.")
            return

        connection.commit()

        print("================================")
        print("ADMIN PASSWORD RESET SUCCESSFUL")
        print("================================")
        print("Username:", USERNAME)
        print("Password:", NEW_PASSWORD)

    except Exception as error:

        connection.rollback()
        print("Error:", error)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    reset_admin_password()