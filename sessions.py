import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import subprocess

from database import get_connection


class SessionsWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title(
            "Remote Sessions - Virtual System Access Control"
        )
        self.window.geometry("1250x720")
        self.window.minsize(1050, 650)
        self.window.configure(bg="#f1f5f9")

        self.build_interface()
        self.load_sessions()

    # ==========================================================
    # BUILD INTERFACE
    # ==========================================================

    def build_interface(self):

        self.colors = {
            "navy": "#172554",
            "blue": "#2563eb",
            "light_blue": "#dbeafe",
            "green": "#16a34a",
            "light_green": "#dcfce7",
            "red": "#dc2626",
            "light_red": "#fee2e2",
            "orange": "#ea580c",
            "light_orange": "#ffedd5",
            "purple": "#7c3aed",
            "light_purple": "#ede9fe",
            "cyan": "#0891b2",
            "light_cyan": "#cffafe",
            "white": "#ffffff",
            "background": "#f1f5f9",
            "text": "#0f172a",
            "muted": "#64748b",
            "border": "#cbd5e1"
        }

        # ------------------------------------------------------
        # TREEVIEW STYLE
        # ------------------------------------------------------

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Session.Treeview",
            background="white",
            foreground="#0f172a",
            fieldbackground="white",
            rowheight=38,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Session.Treeview.Heading",
            background="#172554",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Session.Treeview",
            background=[
                ("selected", "#bfdbfe")
            ],
            foreground=[
                ("selected", "#172554")
            ]
        )

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            self.window,
            bg=self.colors["navy"],
            height=90
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="◉",
            font=("Segoe UI", 28, "bold"),
            fg="#60a5fa",
            bg=self.colors["navy"]
        ).pack(
            side="left",
            padx=(25, 10)
        )

        title_frame = tk.Frame(
            header,
            bg=self.colors["navy"]
        )

        title_frame.pack(
            side="left",
            pady=15
        )

        tk.Label(
            title_frame,
            text="REMOTE SESSIONS",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=self.colors["navy"]
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Monitor authorized remote-access connections",
            font=("Segoe UI", 10),
            fg="#bfdbfe",
            bg=self.colors["navy"]
        ).pack(anchor="w")

        # ------------------------------------------------------
        # SUMMARY CARDS
        # ------------------------------------------------------

        summary = tk.Frame(
            self.window,
            bg=self.colors["background"]
        )

        summary.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        self.total_value = self.create_summary_card(
            summary,
            "TOTAL SESSIONS",
            "0",
            self.colors["blue"]
        )

        self.active_value = self.create_summary_card(
            summary,
            "ACTIVE SESSIONS",
            "0",
            self.colors["green"]
        )

        self.ended_value = self.create_summary_card(
            summary,
            "ENDED SESSIONS",
            "0",
            self.colors["red"]
        )

        self.protocol_value = self.create_summary_card(
            summary,
            "PROTOCOLS USED",
            "0",
            self.colors["purple"]
        )

        # ------------------------------------------------------
        # CONTROL BAR
        # ------------------------------------------------------

        controls = tk.Frame(
            self.window,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            controls,
            text="Search:",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["text"],
            bg="white"
        ).pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.search_entry = tk.Entry(
            controls,
            width=30,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=self.colors["text"],
            relief="flat"
        )

        self.search_entry.pack(
            side="left",
            ipady=7,
            padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        tk.Label(
            controls,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["text"],
            bg="white"
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.status_filter = ttk.Combobox(
            controls,
            values=[
                "ALL",
                "STARTED",
                "ENDED"
            ],
            state="readonly",
            width=13
        )

        self.status_filter.set("ALL")

        self.status_filter.pack(
            side="left",
            padx=5
        )

        self.status_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        # ------------------------------------------------------
        # EXPORT BUTTON
        # ------------------------------------------------------

        tk.Button(
            controls,
            text="↓ Export",
            command=self.export_sessions,
            bg=self.colors["green"],
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=5,
            pady=7
        )

        # ------------------------------------------------------
        # REPORT BUTTON
        # ------------------------------------------------------

        tk.Button(
            controls,
            text="▣ Session Report",
            command=self.show_session_report,
            bg=self.colors["purple"],
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=5,
            pady=7
        )

        # ------------------------------------------------------
        # REFRESH BUTTON
        # ------------------------------------------------------

        tk.Button(
            controls,
            text="↻ Refresh",
            command=self.load_sessions,
            bg=self.colors["blue"],
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=5,
            pady=7
        )

        # ------------------------------------------------------
        # TABLE CARD
        # ------------------------------------------------------

        table_card = tk.Frame(
            self.window,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        table_container = tk.Frame(
            table_card,
            bg="white"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=10,
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
            table_container,
            columns=columns,
            show="headings",
            style="Session.Treeview",
            selectmode="browse"
        )

        widths = {
            "ID": 70,
            "User": 140,
            "Device": 180,
            "Protocol": 110,
            "Started": 180,
            "Ended": 180,
            "Status": 120
        }

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=widths[column],
                minwidth=70,
                anchor="center"
            )

        # ------------------------------------------------------
        # TABLE ROW COLORS
        # ------------------------------------------------------

        self.table.tag_configure(
            "started",
            background="#ecfdf5",
            foreground="#166534"
        )

        self.table.tag_configure(
            "ended",
            background="#fef2f2",
            foreground="#991b1b"
        )

        self.table.tag_configure(
            "rdp",
            background="#eff6ff",
            foreground="#1d4ed8"
        )

        self.table.tag_configure(
            "ssh",
            background="#f0fdf4",
            foreground="#15803d"
        )

        self.table.tag_configure(
            "vnc",
            background="#fff7ed",
            foreground="#c2410c"
        )

        self.table.tag_configure(
            "vpn",
            background="#f5f3ff",
            foreground="#6d28d9"
        )

        # ------------------------------------------------------
        # SCROLLBARS
        # ------------------------------------------------------

        vertical = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.table.yview
        )

        horizontal = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set
        )

        self.table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_container.grid_rowconfigure(
            0,
            weight=1
        )

        table_container.grid_columnconfigure(
            0,
            weight=1
        )

        self.table.bind(
            "<Double-1>",
            self.show_session_details
        )

        # ------------------------------------------------------
        # ACTION BUTTONS
        # ------------------------------------------------------

        action_frame = tk.Frame(
            self.window,
            bg=self.colors["background"]
        )

        action_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        tk.Button(
            action_frame,
            text="▶ Start Authorized Session",
            command=self.start_session,
            bg=self.colors["blue"],
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            action_frame,
            text="■ End Selected Session",
            command=self.end_session,
            bg=self.colors["red"],
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=9
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            action_frame,
            text="Close",
            command=self.window.destroy,
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=9
        ).pack(
            side="right",
            padx=5
        )

        # ------------------------------------------------------
        # FOOTER
        # ------------------------------------------------------

        footer = tk.Frame(
            self.window,
            bg=self.colors["navy"],
            height=32
        )

        footer.pack(
            fill="x"
        )

        footer.pack_propagate(False)

        self.footer_label = tk.Label(
            footer,
            text="Session monitoring active",
            font=("Segoe UI", 9),
            fg="#bfdbfe",
            bg=self.colors["navy"]
        )

        self.footer_label.pack(
            side="left",
            padx=20
        )

    # ==========================================================
    # SUMMARY CARD
    # ==========================================================

    def create_summary_card(
        self,
        parent,
        title,
        value,
        color
    ):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        tk.Frame(
            card,
            bg=color,
            width=6
        ).pack(
            side="left",
            fill="y"
        )

        content = tk.Frame(
            card,
            bg="white"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        tk.Label(
            content,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"],
            bg="white"
        ).pack(
            anchor="w"
        )

        value_label = tk.Label(
            content,
            text=value,
            font=("Segoe UI", 20, "bold"),
            fg=color,
            bg="white"
        )

        value_label.pack(
            anchor="w"
        )

        return value_label

    # ==========================================================
    # GET CURRENT USER ID
    # ==========================================================

    def get_current_user_id(self):

        if isinstance(self.current_user, dict):
            return self.current_user.get("user_id")

        if isinstance(self.current_user, int):
            return self.current_user

        return None

    # ==========================================================
    # LOAD SESSIONS
    # ==========================================================

    def load_sessions(self):

        if not hasattr(self, "table"):
            return

        for item in self.table.get_children():
            self.table.delete(item)

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if not connection:

                messagebox.showerror(
                    "Database Error",
                    "Unable to connect to the database.",
                    parent=self.window
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

            self.all_sessions = cursor.fetchall()

            self.apply_filters()
            self.update_statistics()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                f"Unable to load sessions.\n\n{error}",
                parent=self.window
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================================
    # FILTER
    # ==========================================================

    def apply_filters(self):

        if not hasattr(self, "all_sessions"):
            return

        search = self.search_entry.get().strip().lower()
        selected_status = self.status_filter.get().upper()

        for item in self.table.get_children():
            self.table.delete(item)

        count = 0

        for row in self.all_sessions:

            user = str(row[1] or "").lower()
            device = str(row[2] or "").lower()
            protocol = str(row[3] or "").lower()
            status = str(row[6] or "").upper()

            searchable = (
                user
                + " "
                + device
                + " "
                + protocol
                + " "
                + status
            )

            if search and search not in searchable:
                continue

            if selected_status != "ALL" and status != selected_status:
                continue

            tag = self.get_session_tag(
                protocol,
                status
            )

            self.table.insert(
                "",
                tk.END,
                values=row,
                tags=(tag,)
            )

            count += 1

        self.footer_label.config(
            text=(
                f"Showing {count} of "
                f"{len(self.all_sessions)} session(s)"
            )
        )

    # ==========================================================
    # SESSION TAG
    # ==========================================================

    def get_session_tag(self, protocol, status):

        status = str(status).upper()
        protocol = str(protocol).upper()

        # Status takes priority.
        if status == "STARTED":
            return "started"

        if status == "ENDED":
            return "ended"

        if protocol == "RDP":
            return "rdp"

        if protocol == "SSH":
            return "ssh"

        if protocol == "VNC":
            return "vnc"

        if protocol == "VPN":
            return "vpn"

        return "ended"

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def update_statistics(self):

        if not hasattr(self, "all_sessions"):
            return

        total = len(self.all_sessions)

        active = 0
        ended = 0
        protocols = set()

        for row in self.all_sessions:

            status = str(row[6] or "").upper()
            protocol = str(row[3] or "").upper()

            if status == "STARTED":
                active += 1

            elif status == "ENDED":
                ended += 1

            if protocol:
                protocols.add(protocol)

        self.total_value.config(
            text=str(total)
        )

        self.active_value.config(
            text=str(active)
        )

        self.ended_value.config(
            text=str(ended)
        )

        self.protocol_value.config(
            text=str(len(protocols))
        )

    # ==========================================================
    # START AUTHORIZED SESSION
    # ==========================================================

    def start_session(self):

        dialog = tk.Toplevel(
            self.window
        )

        dialog.title(
            "Start Authorized Session"
        )

        dialog.geometry(
            "460x450"
        )

        dialog.resizable(
            False,
            False
        )

        dialog.configure(
            bg="#f1f5f9"
        )

        dialog.transient(
            self.window
        )

        dialog.grab_set()

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            dialog,
            bg="#172554",
            height=75
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="START REMOTE SESSION",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#172554"
        ).pack(
            pady=(12, 0)
        )

        tk.Label(
            header,
            text="Only approved access requests are allowed",
            font=("Segoe UI", 9),
            fg="#bfdbfe",
            bg="#172554"
        ).pack()

        # ------------------------------------------------------
        # FORM
        # ------------------------------------------------------

        form = tk.Frame(
            dialog,
            bg="white"
        )

        form.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Request ID
        tk.Label(
            form,
            text="Access Request ID",
            font=("Segoe UI", 10, "bold"),
            fg="#334155",
            bg="white"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        request_entry = ttk.Entry(form)

        request_entry.pack(
            fill="x",
            ipady=5
        )

        # Device ID
        tk.Label(
            form,
            text="Device ID",
            font=("Segoe UI", 10, "bold"),
            fg="#334155",
            bg="white"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        device_entry = ttk.Entry(form)

        device_entry.pack(
            fill="x",
            ipady=5
        )

        # Protocol
        tk.Label(
            form,
            text="Remote Protocol",
            font=("Segoe UI", 10, "bold"),
            fg="#334155",
            bg="white"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        protocol_combo = ttk.Combobox(
            form,
            values=[
                "RDP",
                "SSH",
                "VNC",
                "VPN",
                "Web",
                "Other"
            ],
            state="readonly"
        )

        protocol_combo.set("RDP")

        protocol_combo.pack(
            fill="x"
        )

        # ------------------------------------------------------
        # SAVE SESSION
        # ------------------------------------------------------

        def save_session():

            request_id = request_entry.get().strip()
            device_id = device_entry.get().strip()
            protocol = protocol_combo.get().strip()

            if not request_id:

                messagebox.showwarning(
                    "Missing Request ID",
                    "Enter the Access Request ID.",
                    parent=dialog
                )

                return

            if not device_id:

                messagebox.showwarning(
                    "Missing Device ID",
                    "Enter the Device ID.",
                    parent=dialog
                )

                return

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
                    "Current user ID could not be determined.",
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
                        "Unable to connect to database.",
                        parent=dialog
                    )

                    return

                cursor = connection.cursor()

                # ----------------------------------------------
                # VERIFY ACCESS REQUEST
                # ----------------------------------------------

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

                request_device_id = request[2]

                request_status = (
                    str(request[3]).upper()
                    if request[3]
                    else ""
                )

                if request_status != "APPROVED":

                    messagebox.showwarning(
                        "Request Not Approved",
                        (
                            f"Access Request #{request_id} is "
                            f"'{request_status or 'NULL'}'.\n\n"
                            "Only APPROVED requests can start sessions."
                        ),
                        parent=dialog
                    )

                    return

                if request_device_id != int(device_id):

                    messagebox.showerror(
                        "Device Mismatch",
                        (
                            f"Request #{request_id} is not for "
                            f"Device #{device_id}."
                        ),
                        parent=dialog
                    )

                    return

                # ----------------------------------------------
                # GET DEVICE INFORMATION
                # ----------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        device_id,
                        device_name,
                        hostname,
                        ip_address
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

                device_name = device[1]
                hostname = device[2]
                ip_address = device[3]

                # Use hostname first, otherwise IP address.
                target = hostname or ip_address

                if not target:

                    messagebox.showerror(
                        "Missing Connection Target",
                        (
                            f"Device #{device_id} has no hostname "
                            "or IP address configured.\n\n"
                            "Open Devices and add a hostname or IP address "
                            "before starting a remote session."
                        ),
                        parent=dialog
                    )

                    return

                # ----------------------------------------------
                # CREATE REMOTE SESSION
                # ----------------------------------------------

                cursor.execute(
                    """
                    INSERT INTO remote_sessions
                    (
                        request_id,
                        user_id,
                        device_id,
                        protocol,
                        started_at,
                        status
                    )
                    VALUES
                    (
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

                dialog.destroy()

                self.load_sessions()

                # ----------------------------------------------
                # OPEN CONNECTION WINDOW
                # ----------------------------------------------

                self.show_connection_window(
                    session_id,
                    int(device_id),
                    device_name,
                    target,
                    protocol
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
        # BUTTONS
        # ------------------------------------------------------

        button_frame = tk.Frame(
            dialog,
            bg="#f1f5f9"
        )

        button_frame.pack(
            fill="x",
            pady=(0, 20)
        )

        tk.Button(
            button_frame,
            text="▶ Start Session",
            command=save_session,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=9
        ).pack(
            side="left",
            padx=(80, 5)
        )

        tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#64748b",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(
            side="left",
            padx=5
        )

    # ==========================================================
    # CONNECTION WINDOW
    # ==========================================================

    def show_connection_window(
        self,
        session_id,
        device_id,
        device_name,
        target,
        protocol
    ):

        connection_window = tk.Toplevel(
            self.window
        )

        connection_window.title(
            "Remote Session - Connecting"
        )

        connection_window.geometry(
            "700x650"
        )

        connection_window.resizable(
            False,
            False
        )

        connection_window.configure(
            bg="white"
        )

        connection_window.transient(
            self.window
        )

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            connection_window,
            bg="#172554",
            height=95
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="◉  REMOTE CONNECTION",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#172554"
        ).pack(
            pady=(13, 0)
        )

        tk.Label(
            header,
            text=f"Session #{session_id}  •  {protocol}",
            font=("Segoe UI", 10),
            fg="#bfdbfe",
            bg="#172554"
        ).pack()

        # ------------------------------------------------------
        # MAIN CONTENT
        # ------------------------------------------------------

        content = tk.Frame(
            connection_window,
            bg="white"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=20
        )

        tk.Label(
            content,
            text=f"Connecting to {device_name}",
            font=("Segoe UI", 17, "bold"),
            fg="#111827",
            bg="white"
        ).pack()

        tk.Label(
            content,
            text=f"Target: {target}",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg="white"
        ).pack(
            pady=(5, 2)
        )

        tk.Label(
            content,
            text="Authorized remote-access connection",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg="white"
        ).pack(
            pady=(0, 18)
        )

        # ------------------------------------------------------
        # STATUS CARD
        # ------------------------------------------------------

        status_card = tk.Frame(
            content,
            bg="#f8fafc",
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )

        status_card.pack(
            fill="x"
        )

        status_label = tk.Label(
            status_card,
            text="● INITIALIZING",
            font=("Segoe UI", 13, "bold"),
            fg="#ea580c",
            bg="#f8fafc"
        )

        status_label.pack(
            pady=(15, 5)
        )

        detail_label = tk.Label(
            status_card,
            text="Preparing authorized session...",
            font=("Segoe UI", 10),
            fg="#64748b",
            bg="#f8fafc"
        )

        detail_label.pack(
            pady=(0, 15)
        )

        # ------------------------------------------------------
        # PROGRESS
        # ------------------------------------------------------

        progress = ttk.Progressbar(
            content,
            orient="horizontal",
            length=600,
            mode="determinate",
            maximum=100
        )

        progress.pack(
            pady=(18, 5)
        )

        percent_label = tk.Label(
            content,
            text="0%",
            font=("Segoe UI", 10, "bold"),
            fg="#334155",
            bg="white"
        )

        percent_label.pack()

        # ------------------------------------------------------
        # STEPS
        # ------------------------------------------------------

        steps_frame = tk.Frame(
            content,
            bg="white"
        )

        steps_frame.pack(
            fill="x",
            pady=15
        )

        steps = [
            "Establishing secure connection",
            "Authenticating access request",
            "Verifying target device",
            "Starting remote client"
        ]

        step_labels = []

        for step in steps:

            label = tk.Label(
                steps_frame,
                text="○  " + step,
                font=("Segoe UI", 10),
                fg="#64748b",
                bg="white",
                anchor="w"
            )

            label.pack(
                fill="x",
                pady=3
            )

            step_labels.append(label)

        # ------------------------------------------------------
        # CLOSE / CANCEL BUTTON
        # ------------------------------------------------------

        close_button = tk.Button(
            connection_window,
            text="Cancel Connection",
            command=connection_window.destroy,
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8
        )

        close_button.pack(
            pady=(0, 20)
        )

        # ------------------------------------------------------
        # LAUNCH REMOTE CLIENT
        # ------------------------------------------------------

        def launch_remote_connection():

            try:

                protocol_upper = str(protocol).upper()

                # ----------------------------------------------
                # RDP
                # ----------------------------------------------

                if protocol_upper == "RDP":

                    subprocess.Popen(
                        [
                            "mstsc.exe",
                            f"/v:{target}"
                        ]
                    )

                    return True, (
                        f"Windows Remote Desktop launched for {target}."
                    )

                # ----------------------------------------------
                # SSH
                # ----------------------------------------------

                elif protocol_upper == "SSH":

                    subprocess.Popen(
                        [
                            "cmd",
                            "/c",
                            "start",
                            "cmd",
                            "/k",
                            "ssh",
                            str(target)
                        ]
                    )

                    return True, (
                        f"SSH terminal launched for {target}."
                    )

                # ----------------------------------------------
                # VNC
                # ----------------------------------------------

                elif protocol_upper == "VNC":

                    return False, (
                        "VNC was selected, but no VNC client is "
                        "configured on this computer."
                    )

                # ----------------------------------------------
                # VPN
                # ----------------------------------------------

                elif protocol_upper == "VPN":

                    return False, (
                        "VPN was selected, but no VPN client "
                        "has been configured."
                    )

                # ----------------------------------------------
                # WEB
                # ----------------------------------------------

                elif protocol_upper == "WEB":

                    try:

                        import webbrowser

                        url = str(target)

                        if not (
                            url.startswith("http://")
                            or url.startswith("https://")
                        ):
                            url = "http://" + url

                        webbrowser.open(url)

                        return True, (
                            f"Web connection opened for {url}."
                        )

                    except Exception as error:

                        return False, str(error)

                # ----------------------------------------------
                # OTHER
                # ----------------------------------------------

                else:

                    return False, (
                        f"No remote client is configured for "
                        f"protocol '{protocol_upper}'."
                    )

            except FileNotFoundError:

                if str(protocol).upper() == "RDP":

                    return False, (
                        "Windows Remote Desktop (mstsc.exe) "
                        "could not be found."
                    )

                return False, (
                    f"The client required for {protocol} "
                    "could not be started."
                )

            except Exception as error:

                return False, str(error)

        # ------------------------------------------------------
        # ANIMATION
        # ------------------------------------------------------

        stages = [
            (
                20,
                0,
                "● CONNECTING",
                "Preparing connection to target device..."
            ),
            (
                45,
                1,
                "● AUTHENTICATING",
                "Checking approved access request..."
            ),
            (
                70,
                2,
                "● VERIFYING",
                f"Verifying {device_name}..."
            ),
            (
                90,
                3,
                "● STARTING CLIENT",
                f"Preparing {protocol} remote client..."
            )
        ]

        def finish_connection():

            if not connection_window.winfo_exists():
                return

            progress["value"] = 100

            percent_label.config(
                text="100%"
            )

            for label, step in zip(step_labels, steps):

                label.config(
                    text="✓  " + step,
                    fg="#15803d"
                )

            success, message = launch_remote_connection()

            if success:

                status_label.config(
                    text="● SESSION READY",
                    fg="#15803d"
                )

                detail_label.config(
                    text=message
                )

                close_button.config(
                    text="Close",
                    command=connection_window.destroy,
                    bg="#16a34a",
                    activebackground="#15803d"
                )

                self.footer_label.config(
                    text=f"Session #{session_id} is ready"
                )

            else:

                status_label.config(
                    text="● CONNECTION NOT LAUNCHED",
                    fg="#dc2626"
                )

                detail_label.config(
                    text=message
                )

                close_button.config(
                    text="Close",
                    command=connection_window.destroy,
                    bg="#dc2626",
                    activebackground="#b91c1c"
                )

                # ----------------------------------------------
                # END SESSION IF CLIENT DID NOT LAUNCH
                # ----------------------------------------------

                self.mark_session_ended(
                    session_id
                )

                self.footer_label.config(
                    text=f"Session #{session_id} was not launched"
                )

            self.load_sessions()

        def update_stage(index=0):

            if not connection_window.winfo_exists():
                return

            if index >= len(stages):

                finish_connection()

                return

            percent, active, status, detail = stages[index]

            progress["value"] = percent

            percent_label.config(
                text=f"{percent}%"
            )

            status_label.config(
                text=status,
                fg="#ea580c"
            )

            detail_label.config(
                text=detail
            )

            for i, label in enumerate(step_labels):

                if i < active:

                    label.config(
                        text="✓  " + steps[i],
                        fg="#15803d"
                    )

                elif i == active:

                    label.config(
                        text="●  " + steps[i],
                        fg="#ea580c"
                    )

                else:

                    label.config(
                        text="○  " + steps[i],
                        fg="#64748b"
                    )

            connection_window.after(
                1000,
                lambda: update_stage(index + 1)
            )

        update_stage()

    # ==========================================================
    # MARK SESSION ENDED
    # ==========================================================

    def mark_session_ended(self, session_id):

        connection = None
        cursor = None

        try:

            connection = get_connection()

            if not connection:
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

            connection.commit()

        except Exception:

            if connection:
                connection.rollback()

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================================
    # END SESSION
    # ==========================================================

    def end_session(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Session",
                "Please select a session first.",
                parent=self.window
            )

            return

        values = self.table.item(
            selected[0],
            "values"
        )

        if not values:
            return

        session_id = values[0]
        status = str(values[6]).upper()

        if status == "ENDED":

            messagebox.showinfo(
                "Session Already Ended",
                f"Session #{session_id} has already ended.",
                parent=self.window
            )

            return

        confirm = messagebox.askyesno(
            "End Remote Session",
            f"End remote session #{session_id}?",
            parent=self.window
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
                    "Unable to connect to database.",
                    parent=self.window
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
                    "The session may already have ended.",
                    parent=self.window
                )

                return

            connection.commit()

            messagebox.showinfo(
                "Session Ended",
                f"Session #{session_id} ended successfully.",
                parent=self.window
            )

            self.load_sessions()

        except Exception as error:

            if connection:
                connection.rollback()

            messagebox.showerror(
                "Database Error",
                f"Unable to end session.\n\n{error}",
                parent=self.window
            )

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # ==========================================================
    # SESSION DETAILS
    # ==========================================================

    def show_session_details(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        if not values:
            return

        details = tk.Toplevel(
            self.window
        )

        details.title(
            "Remote Session Details"
        )

        details.geometry(
            "620x480"
        )

        details.configure(
            bg="#f1f5f9"
        )

        header = tk.Frame(
            details,
            bg="#172554",
            height=80
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="SESSION DETAILS",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#172554"
        ).pack(
            pady=20
        )

        card = tk.Frame(
            details,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        fields = [
            ("Session ID", values[0]),
            ("User", values[1]),
            ("Device", values[2]),
            ("Protocol", values[3]),
            ("Started", values[4]),
            ("Ended", values[5] or "Still Active"),
            ("Status", values[6])
        ]

        for index, (label, value) in enumerate(fields):

            tk.Label(
                card,
                text=label + ":",
                font=("Segoe UI", 10, "bold"),
                fg="#64748b",
                bg="white"
            ).grid(
                row=index,
                column=0,
                sticky="w",
                padx=20,
                pady=9
            )

            value_label = tk.Label(
                card,
                text=str(value),
                font=("Segoe UI", 10, "bold"),
                fg="#0f172a",
                bg="white"
            )

            value_label.grid(
                row=index,
                column=1,
                sticky="w",
                padx=20,
                pady=9
            )

            if label == "Status":

                if str(value).upper() == "STARTED":

                    value_label.config(
                        fg="#16a34a"
                    )

                else:

                    value_label.config(
                        fg="#dc2626"
                    )

        card.columnconfigure(
            1,
            weight=1
        )

        tk.Button(
            details,
            text="Close",
            command=details.destroy,
            bg="#172554",
            fg="white",
            activebackground="#1e3a8a",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=25,
            pady=8
        ).pack(
            pady=(0, 20)
        )

    # ==========================================================
    # SESSION REPORT
    # ==========================================================

    def show_session_report(self):

        if not hasattr(self, "all_sessions"):
            return

        if not self.all_sessions:

            messagebox.showinfo(
                "Session Report",
                "There are currently no session records.",
                parent=self.window
            )

            return

        report = tk.Toplevel(
            self.window
        )

        report.title(
            "Remote Session Operation Report"
        )

        report.geometry(
            "800x620"
        )

        report.configure(
            bg="#f1f5f9"
        )

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            report,
            bg="#172554",
            height=90
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="REMOTE SESSION REPORT",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#172554"
        ).pack(
            pady=(15, 0)
        )

        tk.Label(
            header,
            text="Virtual System Access Control",
            font=("Segoe UI", 10),
            fg="#bfdbfe",
            bg="#172554"
        ).pack()

        # ------------------------------------------------------
        # STATISTICS
        # ------------------------------------------------------

        total = len(self.all_sessions)

        started = 0
        ended = 0
        protocols = {}

        for row in self.all_sessions:

            status = str(row[6] or "").upper()

            protocol = str(
                row[3] or "UNKNOWN"
            ).upper()

            if status == "STARTED":
                started += 1

            elif status == "ENDED":
                ended += 1

            protocols[protocol] = (
                protocols.get(protocol, 0) + 1
            )

        body = tk.Frame(
            report,
            bg="#f1f5f9"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # ------------------------------------------------------
        # SUMMARY
        # ------------------------------------------------------

        summary = tk.Frame(
            body,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )

        summary.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            summary,
            text=f"Total Sessions\n{total}",
            font=("Segoe UI", 12, "bold"),
            fg="#2563eb",
            bg="white",
            justify="center"
        ).pack(
            side="left",
            expand=True,
            pady=15
        )

        tk.Label(
            summary,
            text=f"Active\n{started}",
            font=("Segoe UI", 12, "bold"),
            fg="#16a34a",
            bg="white",
            justify="center"
        ).pack(
            side="left",
            expand=True
        )

        tk.Label(
            summary,
            text=f"Ended\n{ended}",
            font=("Segoe UI", 12, "bold"),
            fg="#dc2626",
            bg="white",
            justify="center"
        ).pack(
            side="left",
            expand=True
        )

        # ------------------------------------------------------
        # PROTOCOL REPORT
        # ------------------------------------------------------

        tk.Label(
            body,
            text="Session Operations by Protocol",
            font=("Segoe UI", 12, "bold"),
            fg="#172554",
            bg="#f1f5f9"
        ).pack(
            anchor="w",
            pady=(5, 8)
        )

        report_table = ttk.Treeview(
            body,
            columns=(
                "Protocol",
                "Sessions",
                "Percentage"
            ),
            show="headings",
            height=12
        )

        report_table.heading(
            "Protocol",
            text="Protocol"
        )

        report_table.heading(
            "Sessions",
            text="Number of Sessions"
        )

        report_table.heading(
            "Percentage",
            text="Percentage"
        )

        report_table.column(
            "Protocol",
            width=220,
            anchor="center"
        )

        report_table.column(
            "Sessions",
            width=220,
            anchor="center"
        )

        report_table.column(
            "Percentage",
            width=220,
            anchor="center"
        )

        report_table.pack(
            fill="both",
            expand=True
        )

        for protocol, count in sorted(
            protocols.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            percentage = (
                count / total
            ) * 100

            report_table.insert(
                "",
                tk.END,
                values=(
                    protocol,
                    count,
                    f"{percentage:.1f}%"
                )
            )

        # ------------------------------------------------------
        # CLOSE REPORT
        # ------------------------------------------------------

        tk.Button(
            report,
            text="Close Report",
            command=report.destroy,
            bg="#172554",
            fg="white",
            activebackground="#1e3a8a",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=25,
            pady=9
        ).pack(
            pady=(0, 20)
        )

    # ==========================================================
    # EXPORT SESSIONS
    # ==========================================================

    def export_sessions(self):

        if not hasattr(self, "all_sessions"):
            return

        if not self.all_sessions:

            messagebox.showinfo(
                "Export",
                "There are no sessions to export.",
                parent=self.window
            )

            return

        file_path = filedialog.asksaveasfilename(
            parent=self.window,
            title="Export Session Report",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ],
            initialfile="remote_session_report.csv"
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Session ID",
                    "User",
                    "Device",
                    "Protocol",
                    "Started",
                    "Ended",
                    "Status"
                ])

                writer.writerows(
                    self.all_sessions
                )

            messagebox.showinfo(
                "Export Successful",
                (
                    "Remote session report exported successfully.\n\n"
                    + file_path
                ),
                parent=self.window
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error),
                parent=self.window
            )