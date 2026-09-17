import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from security import hash_password


class UsersWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)

        self.window.title("User Management")

        self.window.geometry("1000x600")

        self.build_interface()

        self.load_users()

    def build_interface(self):

        title = tk.Label(
            self.window,
            text="USER MANAGEMENT",
            font=("Segoe UI", 18, "bold")
        )

        title.pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            form,
            text="Username"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.username = tk.Entry(form)

        self.username.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            form,
            text="Password"
        ).grid(row=0, column=2)

        self.password = tk.Entry(
            form,
            show="*"
        )

        self.password.grid(
            row=0,
            column=3
        )

        tk.Label(
            form,
            text="Full Name"
        ).grid(row=1, column=0)

        self.full_name = tk.Entry(form)

        self.full_name.grid(
            row=1,
            column=1
        )

        tk.Label(
            form,
            text="Email"
        ).grid(row=1, column=2)

        self.email = tk.Entry(form)

        self.email.grid(
            row=1,
            column=3
        )

        tk.Label(
            form,
            text="Role"
        ).grid(row=2, column=0)

        self.role = ttk.Combobox(
            form,
            values=[
                "ADMIN",
                "MANAGER",
                "TECHNICIAN",
                "USER"
            ],
            state="readonly"
        )

        self.role.set("USER")

        self.role.grid(
            row=2,
            column=1
        )

        tk.Button(
            form,
            text="Add User",
            command=self.add_user
        ).grid(
            row=2,
            column=3,
            pady=15
        )

        columns = (
            "ID",
            "Username",
            "Full Name",
            "Email",
            "Role",
            "Status"
        )

        self.table = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=140
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def add_user(self):

        username = self.username.get().strip()

        password = self.password.get()

        full_name = self.full_name.get().strip()

        email = self.email.get().strip()

        role = self.role.get()

        if not username or not password or not full_name:

            messagebox.showwarning(
                "Missing Information",
                "Username, password and full name are required."
            )

            return

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            password_hash = hash_password(password)

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password_hash,
                    full_name,
                    email,
                    role
                )
                VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    username,
                    password_hash,
                    full_name,
                    email,
                    role
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "User created successfully."
            )

            self.username.delete(0, tk.END)
            self.password.delete(0, tk.END)
            self.full_name.delete(0, tk.END)
            self.email.delete(0, tk.END)

            self.load_users()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    def load_users(self):

        for item in self.table.get_children():

            self.table.delete(item)

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                full_name,
                email,
                role,
                status
            FROM users
            ORDER BY user_id DESC
            """
        )

        for row in cursor.fetchall():

            self.table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()
        connection.close()