import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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

                session_id = cursor.lastrowid
                connection.commit()

                # Keep the session dialog from flashing away.
                dialog.destroy()
                self.load_sessions()

                # Show the connection interface.
                self.show_connection_window(
                    session_id=session_id,
                    device_id=int(device_id),
                    protocol=protocol
                )

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
    # REMOTE CONNECTION INTERFACE
    # ==========================================================

    def show_connection_window(self, session_id, device_id, protocol):
        """
        Display a connection-status interface for the authorized
        remote session.

        This interface represents the connection workflow. The actual
        RDP/SSH/VPN connection should be launched through the
        organization's approved remote-access client or gateway.
        """

        connection_window = tk.Toplevel(self.window)
        connection_window.title("Remote Session - Connecting")
        connection_window.geometry("650x520")
        connection_window.resizable(False, False)
        connection_window.transient(self.window)
        connection_window.protocol(
            "WM_DELETE_WINDOW",
            connection_window.destroy
        )

        # -----------------------------
        # Header
        # -----------------------------
        header = tk.Frame(
            connection_window,
            bg="#1f2937",
            height=85
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="REMOTE SESSION",
            bg="#1f2937",
            fg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(12, 0))

        tk.Label(
            header,
            text=f"Session #{session_id}  •  {protocol}",
            bg="#1f2937",
            fg="#d1d5db",
            font=("Segoe UI", 10)
        ).pack()

        # -----------------------------
        # Main content
        # -----------------------------
        content = tk.Frame(connection_window, bg="white")
        content.pack(fill="both", expand=True, padx=35, pady=25)

        tk.Label(
            content,
            text=f"Connecting to Device #{device_id}",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 17, "bold")
        ).pack(pady=(0, 5))

        tk.Label(
            content,
            text="Authorized remote-access connection",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 20))

        # -----------------------------
        # Status card
        # -----------------------------
        status_card = tk.Frame(
            content,
            bg="#f3f4f6",
            bd=1,
            relief="solid"
        )
        status_card.pack(fill="x", pady=5)

        status_label = tk.Label(
            status_card,
            text="●  INITIALIZING CONNECTION",
            bg="#f3f4f6",
            fg="#b45309",
            font=("Segoe UI", 13, "bold")
        )
        status_label.pack(pady=(18, 5))

        detail_label = tk.Label(
            status_card,
            text="Preparing authorized remote session...",
            bg="#f3f4f6",
            fg="#4b5563",
            font=("Segoe UI", 10)
        )
        detail_label.pack(pady=(0, 18))

        # -----------------------------
        # Progress bar
        # -----------------------------
        progress = ttk.Progressbar(
            content,
            orient="horizontal",
            length=570,
            mode="determinate",
            maximum=100
        )
        progress.pack(pady=(20, 8))

        percentage_label = tk.Label(
            content,
            text="0%",
            bg="white",
            fg="#374151",
            font=("Segoe UI", 10, "bold")
        )
        percentage_label.pack()

        # -----------------------------
        # Connection steps
        # -----------------------------
        steps_frame = tk.Frame(content, bg="white")
        steps_frame.pack(fill="x", pady=20)

        step_labels = []

        steps = [
            "Establishing secure connection",
            "Authenticating authorized request",
            "Verifying target device",
            "Starting remote session"
        ]

        for step in steps:
            label = tk.Label(
                steps_frame,
                text="○  " + step,
                anchor="w",
                bg="white",
                fg="#6b7280",
                font=("Segoe UI", 10)
            )
            label.pack(fill="x", pady=3)
            step_labels.append(label)

        # -----------------------------
        # Footer
        # -----------------------------
        footer = tk.Frame(connection_window, bg="#f9fafb")
        footer.pack(fill="x", side="bottom")

        cancel_button = tk.Button(
            footer,
            text="Cancel Connection",
            width=20,
            font=("Segoe UI", 10, "bold"),
            command=connection_window.destroy
        )
        cancel_button.pack(pady=15)

        connection_window.update_idletasks()

        # -----------------------------
        # Connection animation
        # -----------------------------
        stages = [
            (15, 0, "●  CONNECTING", "Establishing connection to the target device..."),
            (35, 1, "●  AUTHENTICATING", "Checking the approved access request..."),
            (60, 2, "●  VERIFYING DEVICE", "Verifying the target device and protocol..."),
            (85, 3, "●  STARTING SESSION", "Preparing the authorized remote session..."),
            (100, None, "●  SESSION READY", "Remote session is ready to be opened.")
        ]

        def update_stage(index=0):
            if not connection_window.winfo_exists():
                return

            if index >= len(stages):
                return

            percent, active_step, status_text, detail_text = stages[index]

            progress["value"] = percent
            percentage_label.config(text=f"{percent}%")
            status_label.config(text=status_text)
            detail_label.config(text=detail_text)

            for i, label in enumerate(step_labels):
                if active_step is not None and i < active_step:
                    label.config(
                        text="✓  " + steps[i],
                        fg="#15803d"
                    )
                elif active_step is not None and i == active_step:
                    label.config(
                        text="●  " + steps[i],
                        fg="#b45309"
                    )
                elif percent == 100:
                    label.config(
                        text="✓  " + steps[i],
                        fg="#15803d"
                    )
                else:
                    label.config(
                        text="○  " + steps[i],
                        fg="#6b7280"
                    )

            if percent == 100:
                status_label.config(fg="#15803d")
                cancel_button.config(
                    text="Close",
                    command=connection_window.destroy
                )

                # Refresh the session table so the recorded STARTED
                # session remains visible.
                self.load_sessions()

                return

            connection_window.after(
                1200,
                lambda: update_stage(index + 1)
            )

        update_stage()

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