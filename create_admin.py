from database import get_connection
from security import hash_password


USERNAME = "admin"
PASSWORD = "Admin@123"
FULL_NAME = "System Administrator"
EMAIL = "admin@example.com"


def create_admin():

    connection = get_connection()

    if not connection:
        print("Unable to connect to MySQL.")
        return

    cursor = connection.cursor()

    try:
        password_hash = hash_password(PASSWORD)

        sql = """
        INSERT INTO users
        (
            username,
            password_hash,
            full_name,
            email,
            role,
            status
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            'ADMIN',
            'ACTIVE'
        )
        """

        cursor.execute(
            sql,
            (
                USERNAME,
                password_hash,
                FULL_NAME,
                EMAIL
            )
        )

        connection.commit()

        print("Administrator account created.")
        print("Username:", USERNAME)
        print("Password:", PASSWORD)

    except Exception as error:

        connection.rollback()

        print("Error:", error)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    create_admin()