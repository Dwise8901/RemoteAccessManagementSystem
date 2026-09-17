import tkinter as tk
from tkinter import messagebox

from database import get_connection
from security import verify_password


class Login(tk.Tk):

    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Remote Access Management System")
        self.geometry("500x400")
        self.resizable(False, False)

        # =========================
        # TITLE
        # =========================
        tk.Label(
            self,
            text="Remote Access Management System",
            font=("Arial", 20, "bold")
        ).pack(pady=30)

        # =========================
        # USERNAME
        # =========================
        tk.Label(
            self,
            text="Username",
            font=("Arial", 12)
        ).pack()

        self.username = tk.Entry(
            self,
            width=35,
            font=("Arial", 12)
        )
        self.username.pack(pady=5)

        # =========================
        # PASSWORD
        # =========================
        tk.Label(
            self,
            text="Password",
            font=("Arial", 12)
        ).pack()

        self.password = tk.Entry(
            self,
            width=35,
            font=("Arial", 12),
            show="*"
        )
        self.password.pack(pady=5)

        # =========================
        # LOGIN BUTTON
        # =========================
        tk.Button(
            self,
            text="Login",
            width=20,
            font=("Arial", 11, "bold"),
            command=self.login
        ).pack(pady=25)

        # Allow pressing ENTER to login
        self.bind("<Return>", lambda event: self.login())

    # =========================
    # LOGIN FUNCTION
    # =========================
    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        # Check empty fields
        if not username or not password:
            messagebox.showwarning(
                "Login",
                "Please enter your username and password."
            )
            return

        # Connect to MySQL
        connection = get_connection()

        if not connection:
            messagebox.showerror(
                "Database Error",
                "Unable to connect to MySQL."
            )
            return

        try:

            cursor = connection.cursor(dictionary=True)

            # Get user account
            query = """
                SELECT *
                FROM users
                WHERE username = %s
                AND status = 'ACTIVE'
            """

            cursor.execute(query, (username,))

            user = cursor.fetchone()

            # Close database resources
            cursor.close()
            connection.close()

            # =========================
            # VERIFY LOGIN
            # =========================
            if user:

                password_hash = user.get("password_hash")

                if password_hash and verify_password(
                    password,
                    password_hash
                ):

                    messagebox.showinfo(
                        "Login Successful",
                        f"Welcome {user['username']}!"
                    )

                    # Close login window
                    self.destroy()

                    # Open dashboard
                    import dashboard
                    dashboard.start_dashboard(user)

                    return

            # Invalid login
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

        except Exception as error:

            # Close connection if an error occurs
            try:
                connection.close()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"An error occurred:\n\n{error}"
            )


# =========================
# START LOGIN APPLICATION
# =========================
def start_login():

    app = Login()
    app.mainloop()


# =========================
# PROGRAM ENTRY POINT
# =========================
if __name__ == "__main__":
    start_login()