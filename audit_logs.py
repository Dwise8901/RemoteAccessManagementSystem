import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class AuditLogsWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Audit Logs")
        self.window.geometry("1100x600")
        self.window.resizable(True, True)

        self.build_interface()
        self.load_logs()

    def build_interface(self):

        title = tk.Label(
            self.window,
            text="AUDIT LOGS",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=15)

        # Table frame
        table_frame = tk.Frame(self.window)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "User",
            "Action",
            "Description",
            "IP Address",
            "Created"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Column headings and widths
        column_widths = {
            "ID": 70,
            "User": 130,
            "Action": 130,
            "Description": 350,
            "IP Address": 140,
            "Created": 180
        }

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=column_widths[column],
                anchor="center"
            )

        # Vertical scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.load_logs
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy
        ).pack(
            side="left",
            padx=5
        )

    def load_logs(self):

        # Clear existing records
        for item in self.table.get_children():
            self.table.delete(item)

        connection = get_connection()

        if not connection:
            messagebox.showerror(
                "Database Error",
                "Could not connect to the database.",
                parent=self.window
            )
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    al.log_id,
                    COALESCE(u.username, ''),
                    al.action,
                    COALESCE(al.description, ''),
                    COALESCE(al.ip_address, ''),
                    al.created_at
                FROM audit_logs al
                LEFT JOIN users u
                    ON al.user_id = u.user_id
                ORDER BY al.log_id DESC
                """
            )

            rows = cursor.fetchall()

            for row in rows:

                self.table.insert(
                    "",
                    tk.END,
                    values=row
                )

        except Exception as error:

            messagebox.showerror(
                "Error Loading Audit Logs",
                str(error),
                parent=self.window
            )

        finally:

            cursor.close()
            connection.close()