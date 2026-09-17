import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class SessionsWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Remote Sessions")
        self.window.geometry("1100x600")
        self.window.resizable(True, True)

        self.build_interface()
        self.load_sessions()

    # ==========================================================
    # BUILD INTERFACE
    # ==========================================================

    def build_interface(self):

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        tk.Label(
            self.window,
            text="REMOTE SESSIONS",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        # ------------------------------------------------------
        # TABLE
        # ------------------------------------------------------

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
            "Device",
            "Protocol",
            "Started",
            "Ended",
            "Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Headings
        for column in columns:

            self.table.heading(
                column,
                text=column
            )

        # Column widths
        self.table.column(
            "ID",
            width=70,
            anchor="center"
        )

        self.table.column(
            "User",
            width=150,
            anchor="center"
        )

        self.table.column(
            "Device",
            width=180,
            anchor="center"
        )

        self.table.column(
            "Protocol",
            width=120,
            anchor="center"
        )

        self.table.column(
            "Started",
            width=170,
            anchor="center"
        )

        self.table.column(
            "Ended",
            width=170,
            anchor="center"
        )

        self.table.column(
            "Status",
            width=120,
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

        # ------------------------------------------------------
        # BUTTON FRAME
        # ------------------------------------------------------

        button_frame = tk.Frame(self.window)
        button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Button(
            button_frame,
            text="Start Authorized Session",
            command=self.start_session,
            width=22
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="End Session",
            command=self.end_session,
            width=15
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_sessions,
            width=12
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            width=12
        ).pack(
            side="right",
            padx=5
        )

    # ==========================================================
    # GET CURRENT USER ID
    # ==========================================================

    def get_current_user_id(self):

        # If current_user is a dictionary
        if isinstance(self.current_user, dict):

            return self.current_user.get("user_id")

        # If current_user is an integer
        if isinstance(self.current_user, int):

            return self.current_user

        return None

    # ==========================================================
    # LOAD SESSIONS
    # ==========================================================

    def load_sessions(self):

        # Clear table first
        for item in self.table.get_children():

            self.table.delete(item)

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to the database."
                )

                return

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    rs.session_id,
                    u.username,
                    d.device_name,
                    rs.protocol,
                    rs.started_at,
                    rs.ended_at,
                    rs.status
                FROM remote_sessions rs

                JOIN users u
                    ON rs.user_id = u.user_id

                JOIN devices d
                    ON rs.device_id = d.device_id

                ORDER BY rs.session_id DESC
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
                "Database Error",
                f"Unable to load sessions.\n\n{error}"
            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()

    # ==========================================================
    # START AUTHORIZED SESSION
    # ==========================================================

    def start_session(self):

        # ------------------------------------------------------
        # INFORMATION MESSAGE
        # ------------------------------------------------------

        messagebox.showinfo(
            "Authorized Session",
            "This module records an authorized remote session.\n\n"
            "The actual RDP/SSH/VPN connection should use the "
            "organization's approved remote-access client or gateway."
        )

        # ------------------------------------------------------
        # CREATE DIALOG
        # ------------------------------------------------------

        dialog = tk.Toplevel(self.window)

        dialog.title("Start Authorized Session")
        dialog.geometry("450x400")
        dialog.resizable(False, False)

        dialog.transient(self.window)
        dialog.grab_set()

        # ------------------------------------------------------
        # REQUEST ID
        # ------------------------------------------------------

        tk.Label(
            dialog,
            text="Access Request ID:",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        request_entry = ttk.Entry(
            dialog,
            width=40
        )

        request_entry.pack(
            padx=30,
            pady=5
        )

        # ------------------------------------------------------
        # DEVICE ID
        # ------------------------------------------------------

        tk.Label(
            dialog,
            text="Device ID:",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )

        device_entry = ttk.Entry(
            dialog,
            width=40
        )

        device_entry.pack(
            padx=30,
            pady=5
        )

        # ------------------------------------------------------
        # PROTOCOL
        # ------------------------------------------------------

        tk.Label(
            dialog,
            text="Protocol:",
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )

        protocol_combo = ttk.Combobox(
            dialog,
            values=[
                "RDP",
                "SSH",
                "VNC",
                "VPN",
                "Web",
                "Other"
            ],
            state="readonly",
            width=37
        )

        protocol_combo.pack(
            padx=30,
            pady=5
        )

        protocol_combo.set("RDP")

        # ------------------------------------------------------
        # SAVE SESSION
        # ------------------------------------------------------

        def save_session():

            request_id = request_entry.get().strip()
            device_id = device_entry.get().strip()
            protocol = protocol_combo.get()

            # Validate request ID
            if not request_id:

                messagebox.showwarning(
                    "Missing Request ID",
                    "Enter the Access Request ID.",
                    parent=dialog
                )

                return

            # Validate device ID
            if not device_id:

                messagebox.showwarning(
                    "Missing Device ID",
                    "Enter the Device ID.",
                    parent=dialog
                )

                return

            # Validate numeric IDs
            if not request_id.isdigit():

                messagebox.showwarning(
                    "Invalid Request ID",
                    "Request ID must be a number.",
                    parent=dialog
                )

                return

            if not device_id.isdigit():

                messagebox.showwarning(
                    "Invalid Device ID",
                    "Device ID must be a number.",
                    parent=dialog
                )

                return

            user_id = self.get_current_user_id()

            if not user_id:

                messagebox.showerror(
                    "User Error",
                    "The current user ID could not be determined.",
                    parent=dialog
                )

                return

            connection = None
            cursor = None

            try:

                connection = get_connection()

                if not connection:

                    messagebox.showerror(
                        "Database Error",
                        "Unable to connect to the database.",
                        parent=dialog
                    )

                    return

                cursor = connection.cursor()

                # ------------------------------------------------
                # VERIFY REQUEST
                # ------------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        request_id,
                        requester_id,
                        device_id,
                        status
                    FROM access_requests
                    WHERE request_id = %s
                    """,
                    (int(request_id),)
                )

                request = cursor.fetchone()

                if not request:
                    messagebox.showerror(
                        "Invalid Request",
                        f"Access Request #{request_id} does not exist.",
                        parent=dialog
                    )

                    return

                request_db_id = request[0]
                requester_id = request[1]
                request_device_id = request[2]
                request_status = str(request[3]).upper() if request[3] else ""

                if request_status != "APPROVED":
                    messagebox.showwarning(
                        "Request Not Approved",
                        f"Access Request #{request_id} is currently "
                        f"'{request_status or 'NULL'}'.\n\n"
                        "Only APPROVED access requests can start a remote session.",
                        parent=dialog
                    )

                    return

                if request_device_id != int(device_id):
                    messagebox.showerror(
                        "Device Mismatch",
                        f"Access Request #{request_id} is not for Device #{device_id}.",
                        parent=dialog
                    )

                    return

                # ------------------------------------------------
                # VERIFY DEVICE
                # ------------------------------------------------

                cursor.execute(
                    """
                    SELECT device_id
                    FROM devices
                    WHERE device_id = %s
                    """,
                    (int(device_id),)
                )

                device = cursor.fetchone()

                if not device:

                    messagebox.showerror(
                        "Invalid Device",
                        f"Device #{device_id} does not exist.",
                        parent=dialog
                    )

                    return

                # ------------------------------------------------
                # CREATE SESSION
                # ------------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO remote_sessions (
                        request_id,
                        user_id,
                        device_id,
                        protocol,
                        started_at,
                        status
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        NOW(),
                        'STARTED'
                    )
                    """,
                    (
                        int(request_id),
                        user_id,
                        int(device_id),
                        protocol
                    )
                )

                connection.commit()

                messagebox.showinfo(
                    "Session Started",
                    "Authorized remote session recorded successfully.",
                    parent=dialog
                )

                dialog.destroy()

                self.load_sessions()

            except Exception as error:

                if connection:

                    connection.rollback()

                messagebox.showerror(
                    "Database Error",
                    f"Unable to start session.\n\n{error}",
                    parent=dialog
                )

            finally:

                if cursor:

                    cursor.close()

                if connection:

                    connection.close()

        # ------------------------------------------------------
        # SAVE BUTTON
        # ------------------------------------------------------

        tk.Button(
            dialog,
            text="Start Session",
            command=save_session,
            width=18
        ).pack(
            pady=(25, 10)
        )

        # ------------------------------------------------------
        # CANCEL BUTTON
        # ------------------------------------------------------

        tk.Button(
            dialog,
            text="Cancel",
            command=dialog.destroy,
            width=18
        ).pack()

    # ==========================================================
    # END SESSION
    # ==========================================================

    def end_session(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Session",
                "Please select a session from the table."
            )

            return

        # Get selected row
        values = self.table.item(
            selected[0]
        ).get("values", [])

        if not values:

            messagebox.showwarning(
                "Session",
                "Unable to read the selected session."
            )

            return

        session_id = values[0]
        status = str(values[6]).upper()

        # ------------------------------------------------------
        # Check current status
        # ------------------------------------------------------

        if status == "ENDED":

            messagebox.showinfo(
                "Session Already Ended",
                f"Session #{session_id} has already ended."
            )

            return

        # ------------------------------------------------------
        # Confirm
        # ------------------------------------------------------

        confirm = messagebox.askyesno(
            "End Session",
            f"Are you sure you want to end session #{session_id}?"
        )

        if not confirm:

            return

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to the database."
                )

                return

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE remote_sessions

                SET
                    ended_at = NOW(),
                    status = 'ENDED'

                WHERE session_id = %s
                AND status = 'STARTED'
                """,
                (session_id,)
            )

            if cursor.rowcount == 0:

                connection.rollback()

                messagebox.showwarning(
                    "Session Not Updated",
                    "The session was not updated. "
                    "It may already have ended."
                )

                return

            connection.commit()

            messagebox.showinfo(
                "Session Ended",
                f"Session #{session_id} ended successfully."
            )

            self.load_sessions()

        except Exception as error:

            if connection:

                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to end session.\n\n{error}"
            )

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()