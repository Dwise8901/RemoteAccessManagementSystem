import tkinter as tk
from tkinter import messagebox

from database import get_connection


class Dashboard:

    def __init__(self, root, user):

        self.root = root
        self.user = user

        self.root.title(
            "Remote Access Management System"
        )

        self.root.geometry("1200x700")

        self.root.minsize(1000, 600)

        self.build_interface()

        self.load_statistics()

    def build_interface(self):

        # ==========================================
        # HEADER
        # ==========================================

        header = tk.Frame(
            self.root,
            bg="#172554",
            height=80
        )

        header.pack(
            fill="x"
        )

        tk.Label(
            header,
            text="REMOTE ACCESS MANAGEMENT SYSTEM",
            bg="#172554",
            fg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(
            side="left",
            padx=25,
            pady=20
        )

        tk.Button(
            header,
            text="Logout",
            command=self.logout
        ).pack(
            side="right",
            padx=25
        )

        # ==========================================
        # WELCOME MESSAGE
        # ==========================================

        welcome = tk.Label(
            self.root,
            text=(
                f"Welcome, {self.user['full_name']} "
                f"({self.user['role']})"
            ),
            font=("Segoe UI", 13, "bold")
        )

        welcome.pack(
            anchor="w",
            padx=30,
            pady=25
        )

        # ==========================================
        # STATISTICS CARDS
        # ==========================================

        cards = tk.Frame(
            self.root
        )

        cards.pack(
            fill="x",
            padx=30
        )

        self.users_card = self.create_card(
            cards,
            "USERS",
            0
        )

        self.devices_card = self.create_card(
            cards,
            "DEVICES",
            1
        )

        self.requests_card = self.create_card(
            cards,
            "PENDING REQUESTS",
            2
        )

        self.sessions_card = self.create_card(
            cards,
            "ACTIVE SESSIONS",
            3
        )

        # ==========================================
        # MENU
        # ==========================================

        menu = tk.Frame(
            self.root
        )

        menu.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=35
        )

        buttons = [
            ("Users", self.open_users),
            ("Devices", self.open_devices),
            ("Access Requests", self.open_requests),
            ("Sessions", self.open_sessions),
            ("Audit Logs", self.open_logs),
            ("Reports", self.open_reports),
        ]

        for index, (text, command) in enumerate(buttons):

            row = index // 3
            column = index % 3

            button = tk.Button(
                menu,
                text=text,
                font=("Segoe UI", 12, "bold"),
                width=25,
                height=3,
                command=command
            )

            button.grid(
                row=row,
                column=column,
                padx=10,
                pady=10,
                sticky="nsew"
            )

        for column in range(3):

            menu.grid_columnconfigure(
                column,
                weight=1
            )

        for row in range(2):

            menu.grid_rowconfigure(
                row,
                weight=1
            )

    # ==========================================
    # CREATE STATISTICS CARD
    # ==========================================

    def create_card(self, parent, title, column):

        frame = tk.Frame(
            parent,
            bd=1,
            relief="solid",
            padx=30,
            pady=20
        )

        frame.grid(
            row=0,
            column=column,
            padx=8,
            pady=5,
            sticky="nsew"
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 10, "bold")
        ).pack()

        value = tk.Label(
            frame,
            text="0",
            font=("Segoe UI", 25, "bold")
        )

        value.pack(
            pady=5
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        return value

    # ==========================================
    # LOAD STATISTICS
    # ==========================================

    def load_statistics(self):

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            # USERS
            cursor.execute(
                "SELECT COUNT(*) FROM users"
            )

            result = cursor.fetchone()

            if result:
                self.users_card.config(
                    text=str(result[0])
                )

            # DEVICES
            cursor.execute(
                "SELECT COUNT(*) FROM devices"
            )

            result = cursor.fetchone()

            if result:
                self.devices_card.config(
                    text=str(result[0])
                )

            # PENDING REQUESTS
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM access_requests
                WHERE status = 'PENDING'
                """
            )

            result = cursor.fetchone()

            if result:
                self.requests_card.config(
                    text=str(result[0])
                )

            # ACTIVE SESSIONS
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM remote_sessions
                WHERE status = 'STARTED'
                """
            )

            result = cursor.fetchone()

            if result:
                self.sessions_card.config(
                    text=str(result[0])
                )

        except Exception as error:

            print(
                "Statistics error:",
                error
            )

        finally:

            cursor.close()
            connection.close()

    # ==========================================
    # USERS
    # ==========================================

    def open_users(self):

        try:

            from users import UsersWindow

            UsersWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Users",
                f"Unable to open Users:\n\n{error}"
            )

    # ==========================================
    # DEVICES
    # ==========================================

    def open_devices(self):

        try:

            from devices import DevicesWindow

            DevicesWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Devices",
                f"Unable to open Devices:\n\n{error}"
            )

    # ==========================================
    # ACCESS REQUESTS
    # ==========================================

    def open_requests(self):

        try:

            from access_requests import AccessRequestsWindow

            AccessRequestsWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Access Requests",
                f"Unable to open Access Requests:\n\n{error}"
            )

    # ==========================================
    # SESSIONS
    # ==========================================

    def open_sessions(self):

        try:

            from sessions import SessionsWindow

            SessionsWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Sessions",
                f"Unable to open Sessions:\n\n{error}"
            )

    # ==========================================
    # AUDIT LOGS
    # ==========================================

    def open_logs(self):

        try:

            from audit_logs import AuditLogsWindow

            AuditLogsWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Audit Logs",
                f"Unable to open Audit Logs:\n\n{error}"
            )

    # ==========================================
    # REPORTS
    # ==========================================

    def open_reports(self):

        try:

            from reports import ReportsWindow

            ReportsWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Reports",
                f"Unable to open Reports:\n\n{error}"
            )

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?"
        )

        if answer:

            self.root.destroy()

            from login import start_login

            start_login()


# ==============================================
# START DASHBOARD
# ==============================================

def start_dashboard(user):

    root = tk.Tk()

    Dashboard(
        root,
        user
    )

    root.mainloop()


# ==============================================
# PROGRAM ENTRY POINT
# ==============================================

if __name__ == "__main__":

    # This section is mainly for testing.
    # Normally dashboard.py is started from login.py.

    print(
        "Dashboard should be started from login.py"
    )