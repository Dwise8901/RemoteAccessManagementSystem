import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from database import get_connection
from security import verify_password


class Login(tk.Tk):

    # ============================================================
    # COLOURS
    # ============================================================

    BG = "#06101D"
    PANEL = "#0C1B2D"
    PANEL_LIGHT = "#10283E"

    WHITE = "#FFFFFF"
    TEXT = "#D9E7F5"
    MUTED = "#8196AA"

    CYAN = "#00D4FF"
    BLUE = "#2196F3"
    GREEN = "#20D67B"
    RED = "#FF4D67"

    def __init__(self):

        super().__init__()

        # ========================================================
        # WINDOW
        # ========================================================

        self.title(
            "Virtual System Access Control"
        )

        self.geometry(
            "1050x650"
        )

        self.minsize(
            950,
            600
        )

        self.configure(
            bg=self.BG
        )

        # Center window
        self.center_window()

        self.build_interface()

        # ENTER = LOGIN
        self.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ============================================================
    # CENTER WINDOW
    # ============================================================

    def center_window(self):

        self.update_idletasks()

        width = 1050
        height = 650

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (
            screen_width - width
        ) // 2

        y = (
            screen_height - height
        ) // 2

        self.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ============================================================
    # BUILD INTERFACE
    # ============================================================

    def build_interface(self):

        # Main container
        main = tk.Frame(
            self,
            bg=self.BG
        )

        main.pack(
            fill="both",
            expand=True
        )

        main.grid_columnconfigure(
            0,
            weight=3
        )

        main.grid_columnconfigure(
            1,
            weight=2
        )

        main.grid_rowconfigure(
            0,
            weight=1
        )

        # ========================================================
        # LEFT REMOTE ACCESS GRAPHIC
        # ========================================================

        graphic_panel = tk.Frame(
            main,
            bg=self.BG
        )

        graphic_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.create_remote_graphic(
            graphic_panel
        )

        # ========================================================
        # RIGHT LOGIN PANEL
        # ========================================================

        login_panel = tk.Frame(
            main,
            bg=self.PANEL
        )

        login_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=25
        )

        # ========================================================
        # SECURITY ICON
        # ========================================================

        icon = tk.Canvas(
            login_panel,
            width=80,
            height=80,
            bg=self.PANEL,
            highlightthickness=0
        )

        icon.pack(
            pady=(35, 10)
        )

        # Outer circle
        icon.create_oval(
            8,
            8,
            72,
            72,
            outline=self.CYAN,
            width=2
        )

        # Inner circle
        icon.create_oval(
            18,
            18,
            62,
            62,
            fill="#103452",
            outline=self.BLUE,
            width=1
        )

        # Shield
        icon.create_polygon(
            40, 24,
            55, 30,
            52, 49,
            40, 59,
            28, 49,
            25, 30,
            fill=self.CYAN,
            outline=""
        )

        icon.create_text(
            40,
            41,
            text="✓",
            fill=self.BG,
            font=("Segoe UI", 17, "bold")
        )

        # ========================================================
        # TITLE
        # ========================================================

        tk.Label(
            login_panel,
            text="VIRTUAL SYSTEM ACCESS CONTROL",
            bg=self.PANEL,
            fg=self.WHITE,
            font=("Segoe UI", 20, "bold")
        ).pack()

        tk.Label(
            login_panel,
            text="MANAGEMENT SYSTEM",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=(0, 5)
        )

        tk.Label(
            login_panel,
            text="Secure administrator authentication",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            pady=(0, 25)
        )

        # ========================================================
        # SECURE CONNECTION
        # ========================================================

        status = tk.Frame(
            login_panel,
            bg="#09291F"
        )

        status.pack(
            fill="x",
            padx=35,
            pady=(0, 20)
        )

        tk.Label(
            status,
            text="●",
            bg="#09291F",
            fg=self.GREEN,
            font=("Segoe UI", 11)
        ).pack(
            side="left",
            padx=(12, 5),
            pady=8
        )

        tk.Label(
            status,
            text="SECURE CONNECTION",
            bg="#09291F",
            fg=self.GREEN,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left",
            pady=8
        )

        # ========================================================
        # USERNAME
        # ========================================================

        tk.Label(
            login_panel,
            text="USERNAME",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=35
        )

        username_frame = tk.Frame(
            login_panel,
            bg=self.PANEL_LIGHT
        )

        username_frame.pack(
            fill="x",
            padx=35,
            pady=(5, 15)
        )

        tk.Label(
            username_frame,
            text="◉",
            bg=self.PANEL_LIGHT,
            fg=self.CYAN,
            font=("Segoe UI", 12)
        ).pack(
            side="left",
            padx=(12, 5)
        )

        self.username = tk.Entry(
            username_frame,
            bg=self.PANEL_LIGHT,
            fg=self.WHITE,
            insertbackground=self.CYAN,
            relief="flat",
            bd=0,
            font=("Segoe UI", 11)
        )

        self.username.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12),
            pady=11
        )

        # ========================================================
        # PASSWORD
        # ========================================================

        tk.Label(
            login_panel,
            text="PASSWORD",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=35
        )

        password_frame = tk.Frame(
            login_panel,
            bg=self.PANEL_LIGHT
        )

        password_frame.pack(
            fill="x",
            padx=35,
            pady=(5, 20)
        )

        tk.Label(
            password_frame,
            text="◆",
            bg=self.PANEL_LIGHT,
            fg=self.CYAN,
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            padx=(12, 5)
        )

        self.password = tk.Entry(
            password_frame,
            bg=self.PANEL_LIGHT,
            fg=self.WHITE,
            insertbackground=self.CYAN,
            relief="flat",
            bd=0,
            show="●",
            font=("Segoe UI", 11)
        )

        self.password.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12),
            pady=11
        )

        # ========================================================
        # LOGIN BUTTON
        # ========================================================

        self.login_button = tk.Button(
            login_panel,
            text="  CONNECT TO SECURE SYSTEM  ",
            command=self.login,
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.CYAN,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            pady=12
        )

        self.login_button.pack(
            fill="x",
            padx=35
        )

        # Hover effect
        self.login_button.bind(
            "<Enter>",
            self.login_hover_enter
        )

        self.login_button.bind(
            "<Leave>",
            self.login_hover_leave
        )

        # ========================================================
        # FOOTER
        # ========================================================

        tk.Label(
            login_panel,
            text="Authorized personnel only",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(
            pady=(20, 3)
        )

        tk.Label(
            login_panel,
            text="Remote Access Security Gateway",
            bg=self.PANEL,
            fg="#496176",
            font=("Segoe UI", 7)
        ).pack()

        # Focus username
        self.username.focus_set()

    # ============================================================
    # REMOTE ACCESS GRAPHIC
    # ============================================================

    def create_remote_graphic(self, parent):

        canvas = tk.Canvas(
            parent,
            bg=self.BG,
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        # ========================================================
        # HEADER
        # ========================================================

        canvas.create_text(
            45,
            45,
            text="REMOTE ACCESS",
            anchor="w",
            fill=self.WHITE,
            font=("Segoe UI", 25, "bold")
        )

        canvas.create_text(
            45,
            80,
            text="SECURITY GATEWAY",
            anchor="w",
            fill=self.CYAN,
            font=("Segoe UI", 12, "bold")
        )

        canvas.create_text(
            45,
            110,
            text="Securely manage authorized remote connections",
            anchor="w",
            fill=self.MUTED,
            font=("Segoe UI", 9)
        )

        # ========================================================
        # NETWORK CONNECTIONS
        # ========================================================

        # Central server
        server_x = 245
        server_y = 290

        canvas.create_oval(
            server_x - 60,
            server_y - 60,
            server_x + 60,
            server_y + 60,
            fill="#0D2942",
            outline=self.CYAN,
            width=2
        )

        canvas.create_oval(
            server_x - 43,
            server_y - 43,
            server_x + 43,
            server_y + 43,
            fill="#123A5A",
            outline=self.BLUE,
            width=1
        )

        canvas.create_text(
            server_x,
            server_y - 8,
            text="RMS",
            fill=self.WHITE,
            font=("Segoe UI", 18, "bold")
        )

        canvas.create_text(
            server_x,
            server_y + 17,
            text="SERVER",
            fill=self.CYAN,
            font=("Segoe UI", 8, "bold")
        )

        # Client machines
        clients = [
            (80, 200, "ADMIN"),
            (80, 380, "TECHNICIAN"),
            (330, 200, "DEVICE"),
            (330, 380, "USER"),
        ]

        for x, y, name in clients:

            # Connection line
            canvas.create_line(
                x + 45,
                y + 25,
                server_x,
                server_y,
                fill="#245A7E",
                width=2
            )

            # Node
            canvas.create_rectangle(
                x,
                y,
                x + 90,
                y + 50,
                fill="#0D2034",
                outline=self.BLUE,
                width=2
            )

            canvas.create_text(
                x + 45,
                y + 25,
                text=name,
                fill=self.WHITE,
                font=("Segoe UI", 8, "bold")
            )

        # Connection status dots
        dots = [
            (160, 245),
            (160, 360),
            (350, 245),
            (350, 360),
        ]

        for x, y in dots:

            canvas.create_oval(
                x - 4,
                y - 4,
                x + 4,
                y + 4,
                fill=self.GREEN,
                outline=""
            )

        # ========================================================
        # SECURITY MESSAGE
        # ========================================================

        canvas.create_rectangle(
            75,
            475,
            490,
            530,
            fill="#09291F",
            outline="#14583E",
            width=1
        )

        canvas.create_text(
            95,
            492,
            text="●",
            fill=self.GREEN,
            font=("Segoe UI", 11, "bold")
        )

        canvas.create_text(
            115,
            492,
            text="SECURE REMOTE ACCESS ENABLED",
            anchor="w",
            fill=self.GREEN,
            font=("Segoe UI", 8, "bold")
        )

        canvas.create_text(
            115,
            513,
            text="Authentication required before connection",
            anchor="w",
            fill=self.MUTED,
            font=("Segoe UI", 8)
        )

        # ========================================================
        # FOOTER
        # ========================================================

        canvas.create_text(
            45,
            570,
            text="VIRTUAL SYSTEM ACCESS CONTROL",
            anchor="w",
            fill="#496176",
            font=("Segoe UI", 8, "bold")
        )

    # ============================================================
    # LOGIN BUTTON HOVER
    # ============================================================

    def login_hover_enter(self, event):

        self.login_button.configure(
            bg=self.CYAN,
            fg=self.BG
        )

    def login_hover_leave(self, event):

        self.login_button.configure(
            bg=self.BLUE,
            fg=self.WHITE
        )

    # ============================================================
    # LOGIN FUNCTION
    # ============================================================

    def login(self):

        username = self.username.get().strip()

        password = self.password.get()

        # ========================================================
        # EMPTY FIELDS
        # ========================================================

        if not username or not password:

            messagebox.showwarning(
                "Authentication Required",
                "Please enter your username and password.",
                parent=self
            )

            return

        # ========================================================
        # DATABASE CONNECTION
        # ========================================================

        connection = get_connection()

        if not connection:

            messagebox.showerror(
                "Connection Error",
                "Unable to connect to the Remote Access Management database.",
                parent=self
            )

            return

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            # ====================================================
            # FIND USER
            # ====================================================

            query = """
                SELECT *
                FROM users
                WHERE username = %s
                AND status = 'ACTIVE'
            """

            cursor.execute(
                query,
                (username,)
            )

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            # ====================================================
            # VERIFY PASSWORD
            # ====================================================

            if user:

                password_hash = user.get(
                    "password_hash"
                )

                if password_hash and verify_password(
                    password,
                    password_hash
                ):

                    messagebox.showinfo(
                        "Authentication Successful",
                        f"Welcome {user['username']}!",
                        parent=self
                    )

                    # Close login
                    self.destroy()

                    # Open dashboard
                    import dashboard

                    dashboard.start_dashboard(
                        user
                    )

                    return

            # ====================================================
            # INVALID LOGIN
            # ====================================================

            messagebox.showerror(
                "Authentication Failed",
                "Invalid username or password.",
                parent=self
            )

            self.password.delete(
                0,
                tk.END
            )

            self.password.focus_set()

        except Exception as error:

            try:
                connection.close()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"An error occurred:\n\n{error}",
                parent=self
            )


# ================================================================
# START LOGIN APPLICATION
# ================================================================

def start_login():

    app = Login()

    app.mainloop()


# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

if __name__ == "__main__":

    start_login()