import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from database import get_connection


class Dashboard:

    # ============================================================
    # COLOUR PALETTE
    # ============================================================

    BG = "#07111F"
    SIDEBAR = "#0B1728"
    HEADER = "#0D1B2E"
    CARD = "#10243A"
    CARD_HOVER = "#15314D"

    WHITE = "#FFFFFF"
    TEXT = "#D9E7F5"
    MUTED = "#8297AD"

    BLUE = "#2196F3"
    CYAN = "#00D4FF"
    GREEN = "#20D67B"
    ORANGE = "#FFB020"
    RED = "#FF4D67"
    PURPLE = "#9B6DFF"

    def __init__(self, root, user):

        self.root = root
        self.user = user

        self.root.title(
            "Remote Access Management System"
        )

        self.root.geometry("1280x760")
        self.root.minsize(1100, 650)

        self.build_interface()
        self.load_statistics()

    # ============================================================
    # MAIN INTERFACE
    # ============================================================

    def build_interface(self):

        self.root.configure(bg=self.BG)

        # Main container
        self.main_container = tk.Frame(
            self.root,
            bg=self.BG
        )

        self.main_container.pack(
            fill="both",
            expand=True
        )

        # ========================================================
        # SIDEBAR
        # ========================================================

        self.sidebar = tk.Frame(
            self.main_container,
            bg=self.SIDEBAR,
            width=235
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # Logo / Brand
        brand_frame = tk.Frame(
            self.sidebar,
            bg=self.SIDEBAR
        )

        brand_frame.pack(
            fill="x",
            padx=18,
            pady=(25, 20)
        )

        # Shield graphic
        shield = tk.Canvas(
            brand_frame,
            width=45,
            height=45,
            bg=self.SIDEBAR,
            highlightthickness=0
        )

        shield.pack(side="left")

        shield.create_oval(
            4, 4, 41, 41,
            fill="#12385A",
            outline=self.CYAN,
            width=2
        )

        shield.create_text(
            22,
            22,
            text="✓",
            fill=self.CYAN,
            font=("Segoe UI", 18, "bold")
        )

        tk.Label(
            brand_frame,
            text="REMOTE\nACCESS",
            bg=self.SIDEBAR,
            fg=self.WHITE,
            font=("Segoe UI", 11, "bold"),
            justify="left"
        ).pack(
            side="left",
            padx=10
        )

        # Separator
        tk.Frame(
            self.sidebar,
            bg="#1A3048",
            height=1
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 20)
        )

        # Navigation title
        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # Navigation buttons
        navigation = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("♟", "Users", self.open_users),
            ("▣", "Devices", self.open_devices),
            ("↗", "Access Requests", self.open_requests),
            ("◉", "Remote Sessions", self.open_sessions),
            ("▤", "Audit Logs", self.open_logs),
            ("▥", "Reports", self.open_reports),
            ("🔐", "MFA Security", self.open_mfa),
        ]

        for icon, text, command in navigation:

            self.create_nav_button(
                icon,
                text,
                command
            )

        # Sidebar bottom
        bottom = tk.Frame(
            self.sidebar,
            bg=self.SIDEBAR
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=20
        )

        tk.Frame(
            bottom,
            bg="#1A3048",
            height=1
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        # User information
        tk.Label(
            bottom,
            text="SIGNED IN AS",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI", 7, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            bottom,
            text=self.user.get(
                "full_name",
                "Administrator"
            ),
            bg=self.SIDEBAR,
            fg=self.WHITE,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        tk.Label(
            bottom,
            text=self.user.get(
                "role",
                "Administrator"
            ),
            bg=self.SIDEBAR,
            fg=self.CYAN,
            font=("Segoe UI", 8)
        ).pack(
            anchor="w"
        )

        # ========================================================
        # CONTENT AREA
        # ========================================================

        self.content = tk.Frame(
            self.main_container,
            bg=self.BG
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ========================================================
        # TOP HEADER
        # ========================================================

        header = tk.Frame(
            self.content,
            bg=self.HEADER,
            height=75
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title_frame = tk.Frame(
            header,
            bg=self.HEADER
        )

        title_frame.pack(
            side="left",
            padx=25
        )

        tk.Label(
            title_frame,
            text="Dashboard",
            bg=self.HEADER,
            fg=self.WHITE,
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Remote Access Security & Operations Center",
            bg=self.HEADER,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )

        # Header right
        right_header = tk.Frame(
            header,
            bg=self.HEADER
        )

        right_header.pack(
            side="right",
            padx=20
        )

        self.time_label = tk.Label(
            right_header,
            text="",
            bg=self.HEADER,
            fg=self.CYAN,
            font=("Segoe UI", 9, "bold")
        )

        self.time_label.pack(
            side="left",
            padx=15
        )

        self.update_clock()

        logout = tk.Button(
            right_header,
            text="  Logout  ",
            command=self.logout,
            bg="#341827",
            fg="#FF6B81",
            activebackground="#522138",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=10,
            pady=7
        )

        logout.pack(
            side="right"
        )

        # ========================================================
        # SCROLLABLE CONTENT
        # ========================================================

        self.body = tk.Frame(
            self.content,
            bg=self.BG
        )

        self.body.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # ========================================================
        # WELCOME + SECURITY STATUS
        # ========================================================

        welcome_frame = tk.Frame(
            self.body,
            bg=self.BG
        )

        welcome_frame.pack(
            fill="x",
            pady=(0, 18)
        )

        welcome_text = (
            f"Welcome back, "
            f"{self.user.get('full_name', 'Administrator')}"
        )

        tk.Label(
            welcome_frame,
            text=welcome_text,
            bg=self.BG,
            fg=self.WHITE,
            font=("Segoe UI", 16, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            welcome_frame,
            text="  ● SYSTEM ONLINE",
            bg=self.BG,
            fg=self.GREEN,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="right"
        )

        # ========================================================
        # STATISTICS CARDS
        # ========================================================

        stats = tk.Frame(
            self.body,
            bg=self.BG
        )

        stats.pack(
            fill="x"
        )

        self.users_card = self.create_stat_card(
            stats,
            "USERS",
            "0",
            self.BLUE,
            "♟",
            0
        )

        self.devices_card = self.create_stat_card(
            stats,
            "DEVICES",
            "0",
            self.CYAN,
            "▣",
            1
        )

        self.requests_card = self.create_stat_card(
            stats,
            "PENDING REQUESTS",
            "0",
            self.ORANGE,
            "↗",
            2
        )

        self.sessions_card = self.create_stat_card(
            stats,
            "ACTIVE SESSIONS",
            "0",
            self.GREEN,
            "◉",
            3
        )

        for i in range(4):
            stats.grid_columnconfigure(
                i,
                weight=1
            )

        # ========================================================
        # LOWER AREA
        # ========================================================

        lower = tk.Frame(
            self.body,
            bg=self.BG
        )

        lower.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        lower.grid_columnconfigure(
            0,
            weight=3
        )

        lower.grid_columnconfigure(
            1,
            weight=2
        )

        lower.grid_rowconfigure(
            0,
            weight=1
        )

        # ========================================================
        # REMOTE ACCESS GRAPHIC
        # ========================================================

        graphic_frame = tk.Frame(
            lower,
            bg=self.CARD,
            highlightbackground="#1B3A56",
            highlightthickness=1
        )

        graphic_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 10)
        )

        tk.Label(
            graphic_frame,
            text="REMOTE ACCESS NETWORK",
            bg=self.CARD,
            fg=self.WHITE,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 0)
        )

        self.create_network_graphic(
            graphic_frame
        )

        # ========================================================
        # SECURITY STATUS PANEL
        # ========================================================

        security = tk.Frame(
            lower,
            bg=self.CARD,
            highlightbackground="#1B3A56",
            highlightthickness=1
        )

        security.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(10, 0)
        )

        tk.Label(
            security,
            text="SECURITY STATUS",
            bg=self.CARD,
            fg=self.WHITE,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 15)
        )

        self.create_status_row(
            security,
            "Database Connection",
            "CONNECTED",
            self.GREEN
        )

        self.create_status_row(
            security,
            "Access Control",
            "ACTIVE",
            self.CYAN
        )

        self.create_status_row(
            security,
            "Session Monitoring",
            "ACTIVE",
            self.GREEN
        )

        self.create_status_row(
            security,
            "Audit Logging",
            "ENABLED",
            self.PURPLE
        )

        self.create_status_row(
            security,
            "Threat Status",
            "NORMAL",
            self.GREEN
        )

        # Quick actions
        tk.Label(
            security,
            text="QUICK ACTIONS",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(25, 8)
        )

        action_frame = tk.Frame(
            security,
            bg=self.CARD
        )

        action_frame.pack(
            fill="x",
            padx=20
        )

        self.create_action_button(
            action_frame,
            "New Access Request",
            self.open_requests
        )

        self.create_action_button(
            action_frame,
            "View Remote Sessions",
            self.open_sessions
        )

        self.create_action_button(
            action_frame,
            "Open Reports",
            self.open_reports
        )

    # ============================================================
    # NAVIGATION BUTTON
    # ============================================================

    def create_nav_button(
        self,
        icon,
        text,
        command
    ):

        button = tk.Button(
            self.sidebar,
            text=f"  {icon}   {text}",
            command=command,
            anchor="w",
            bg=self.SIDEBAR,
            fg=self.TEXT,
            activebackground="#12304A",
            activeforeground=self.CYAN,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=18,
            pady=10
        )

        button.pack(
            fill="x",
            padx=12,
            pady=2
        )

        def on_enter(event):
            button.configure(
                bg="#12304A",
                fg=self.CYAN
            )

        def on_leave(event):
            button.configure(
                bg=self.SIDEBAR,
                fg=self.TEXT
            )

        button.bind(
            "<Enter>",
            on_enter
        )

        button.bind(
            "<Leave>",
            on_leave
        )

    # ============================================================
    # STATISTIC CARD
    # ============================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        accent,
        icon,
        column
    ):

        card = tk.Frame(
            parent,
            bg=self.CARD,
            height=105,
            highlightbackground="#1B3A56",
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew"
        )

        card.grid_propagate(False)

        # Icon
        icon_box = tk.Frame(
            card,
            bg=accent,
            width=48,
            height=48
        )

        icon_box.place(
            x=15,
            y=28
        )

        icon_box.pack_propagate(False)

        tk.Label(
            icon_box,
            text=icon,
            bg=accent,
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(
            expand=True
        )

        # Title
        tk.Label(
            card,
            text=title,
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).place(
            x=78,
            y=22
        )

        # Value
        value_label = tk.Label(
            card,
            text=value,
            bg=self.CARD,
            fg=self.WHITE,
            font=("Segoe UI", 24, "bold")
        )

        value_label.place(
            x=78,
            y=43
        )

        # Accent line
        tk.Frame(
            card,
            bg=accent,
            height=3
        ).pack(
            side="bottom",
            fill="x"
        )

        return value_label

    # ============================================================
    # NETWORK GRAPHIC
    # ============================================================

    def create_network_graphic(self, parent):

        canvas = tk.Canvas(
            parent,
            bg=self.CARD,
            highlightthickness=0,
            height=240
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Central server
        canvas.create_oval(
            190, 65, 270, 145,
            fill="#12385A",
            outline=self.CYAN,
            width=2
        )

        canvas.create_text(
            230,
            90,
            text="SERVER",
            fill=self.WHITE,
            font=("Segoe UI", 9, "bold")
        )

        canvas.create_text(
            230,
            116,
            text="RMS",
            fill=self.CYAN,
            font=("Segoe UI", 13, "bold")
        )

        # Client nodes
        nodes = [
            (55, 35, "ADMIN"),
            (55, 155, "USER"),
            (360, 35, "DEVICE"),
            (360, 155, "TECH"),
        ]

        for x, y, name in nodes:

            # Connection line
            canvas.create_line(
                230,
                105,
                x + 35,
                y + 25,
                fill="#245A7E",
                width=2
            )

            # Node
            canvas.create_rectangle(
                x,
                y,
                x + 70,
                y + 50,
                fill="#102F49",
                outline=self.BLUE,
                width=2
            )

            canvas.create_text(
                x + 35,
                y + 25,
                text=name,
                fill=self.WHITE,
                font=("Segoe UI", 8, "bold")
            )

        # Connection dots
        for x, y in [
            (125, 60),
            (125, 165),
            (335, 60),
            (335, 165)
        ]:

            canvas.create_oval(
                x - 4,
                y - 4,
                x + 4,
                y + 4,
                fill=self.GREEN,
                outline=""
            )

        canvas.create_text(
            230,
            205,
            text="SECURE REMOTE CONNECTIONS",
            fill=self.GREEN,
            font=("Segoe UI", 9, "bold")
        )

    # ============================================================
    # SECURITY STATUS
    # ============================================================

    def create_status_row(
        self,
        parent,
        label,
        status,
        color
    ):

        row = tk.Frame(
            parent,
            bg=self.CARD
        )

        row.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            row,
            text="●",
            bg=self.CARD,
            fg=color,
            font=("Segoe UI", 10)
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=label,
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=8
        )

        tk.Label(
            row,
            text=status,
            bg=self.CARD,
            fg=color,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="right"
        )

    # ============================================================
    # QUICK ACTION BUTTON
    # ============================================================

    def create_action_button(
        self,
        parent,
        text,
        command
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg="#12304A",
            fg=self.TEXT,
            activebackground="#1A4B70",
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2",
            pady=7
        )

        button.pack(
            fill="x",
            pady=3
        )

        def enter(event):
            button.configure(
                bg="#1A4B70",
                fg=self.CYAN
            )

        def leave(event):
            button.configure(
                bg="#12304A",
                fg=self.TEXT
            )

        button.bind(
            "<Enter>",
            enter
        )

        button.bind(
            "<Leave>",
            leave
        )

    # ============================================================
    # CLOCK
    # ============================================================

    def update_clock(self):

        current_time = datetime.now().strftime(
            "%d %b %Y   %I:%M:%S %p"
        )

        self.time_label.config(
            text=current_time
        )

        self.root.after(
            1000,
            self.update_clock
        )

    # ============================================================
    # SHOW DASHBOARD
    # ============================================================

    def show_dashboard(self):
        self.load_statistics()

    # ============================================================
    # LOAD STATISTICS
    # ============================================================

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

    # ============================================================
    # USERS
    # ============================================================

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

    # ============================================================
    # DEVICES
    # ============================================================

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

    # ============================================================
    # ACCESS REQUESTS
    # ============================================================

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

    # ============================================================
    # SESSIONS
    # ============================================================

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

    # ============================================================
    # AUDIT LOGS
    # ============================================================

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

    # ============================================================
    # REPORTS
    # ============================================================

    def open_reports(self):

        try:

            from reports_updated import ReportsWindow

            ReportsWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "Reports",
                f"Unable to open Reports:\n\n{error}"
            )

    # ============================================================
    # MFA SECURITY
    # ============================================================

    def open_mfa(self):

        try:

            from mfa_setup import MFASetupWindow

            MFASetupWindow(
                self.root,
                self.user
            )

        except Exception as error:

            messagebox.showerror(
                "MFA Security",
                f"Unable to open MFA Security:\n\n{error}",
                parent=self.root
            )


    # ============================================================
    # LOGOUT
    # ============================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Do you want to logout?",
            parent=self.root
        )

        if answer:

            self.root.destroy()

            from login import start_login

            start_login()


# ================================================================
# START DASHBOARD
# ================================================================

def start_dashboard(user):

    root = tk.Tk()

    Dashboard(
        root,
        user
    )

    root.mainloop()


# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

if __name__ == "__main__":

    print(
        "Dashboard should be started from login.py"
    )