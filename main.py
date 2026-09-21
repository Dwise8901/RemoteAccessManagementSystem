import tkinter as tk
from tkinter import messagebox

from database import get_connection
from security import verify_password


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "Virtual System Access Control"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Secure Remote System Access Management"


# ============================================================
# APPLICATION COLOURS
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


# ============================================================
# SPLASH SCREEN
# ============================================================

class SplashScreen:

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(APP_NAME)
        self.root.geometry("700x420")
        self.root.resizable(False, False)

        self.root.configure(bg="#0f172a")

        self.center_window()

        self.build_interface()

    # ========================================================
    # CENTER WINDOW
    # ========================================================

    def center_window(self):

        self.root.update_idletasks()

        width = 700
        height = 420

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ========================================================
    # BUILD SPLASH INTERFACE
    # ========================================================

    def build_interface(self):

        # ----------------------------------------------------
        # TOP BAR
        # ----------------------------------------------------

        top_bar = tk.Frame(
            self.root,
            bg="#2563eb",
            height=8
        )

        top_bar.pack(
            fill="x",
            side="top"
        )

        # ----------------------------------------------------
        # MAIN CONTAINER
        # ----------------------------------------------------

        container = tk.Frame(
            self.root,
            bg="#0f172a"
        )

        container.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # LOGO
        # ----------------------------------------------------

        logo_frame = tk.Frame(
            container,
            bg="#1e3a8a",
            width=100,
            height=100
        )

        logo_frame.pack(
            pady=(45, 15)
        )

        logo_frame.pack_propagate(False)

        logo_label = tk.Label(
            logo_frame,
            text="🔐",
            font=("Segoe UI Emoji", 42),
            bg="#1e3a8a",
            fg="white"
        )

        logo_label.pack(
            expand=True
        )

        # ----------------------------------------------------
        # APPLICATION NAME
        # ----------------------------------------------------

        title_label = tk.Label(
            container,
            text=APP_NAME,
            font=("Segoe UI", 25, "bold"),
            bg="#0f172a",
            fg="white"
        )

        title_label.pack()

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description_label = tk.Label(
            container,
            text=APP_DESCRIPTION,
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="#94a3b8"
        )

        description_label.pack(
            pady=(5, 15)
        )

        # ----------------------------------------------------
        # VERSION
        # ----------------------------------------------------

        version_label = tk.Label(
            container,
            text=f"Version {APP_VERSION}",
            font=("Segoe UI", 9),
            bg="#0f172a",
            fg="#64748b"
        )

        version_label.pack()

        # ----------------------------------------------------
        # LOADING TEXT
        # ----------------------------------------------------

        self.loading_label = tk.Label(
            container,
            text="Initializing system...",
            font=("Segoe UI", 10),
            bg="#0f172a",
            fg="#60a5fa"
        )

        self.loading_label.pack(
            pady=(25, 8)
        )

        # ----------------------------------------------------
        # PROGRESS BAR
        # ----------------------------------------------------

        progress_container = tk.Frame(
            container,
            bg="#334155",
            height=6,
            width=350
        )

        progress_container.pack()

        progress_container.pack_propagate(False)

        self.progress_bar = tk.Frame(
            progress_container,
            bg="#2563eb",
            height=6,
            width=0
        )

        self.progress_bar.pack(
            side="left",
            fill="y"
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = tk.Label(
            container,
            text="Secure • Controlled • Auditable",
            font=("Segoe UI", 9),
            bg="#0f172a",
            fg="#475569"
        )

        footer.pack(
            pady=(25, 0)
        )

    # ========================================================
    # START SPLASH
    # ========================================================

    def start(self):

        self.animate_progress(0)

    # ========================================================
    # PROGRESS ANIMATION
    # ========================================================

    def animate_progress(self, value):

        if value <= 100:

            width = int(
                350 * value / 100
            )

            self.progress_bar.config(
                width=width
            )

            if value < 30:

                text = "Initializing system..."

            elif value < 60:

                text = "Loading security modules..."

            elif value < 85:

                text = "Preparing access control..."

            else:

                text = "Starting application..."

            self.loading_label.config(
                text=text
            )

            self.root.after(
                25,
                lambda: self.animate_progress(
                    value + 2
                )
            )

        else:

            self.root.after(
                400,
                self.open_login
            )

    # ========================================================
    # OPEN LOGIN
    # ========================================================

    def open_login(self):

        try:

            self.root.destroy()

            start_login()

        except Exception as error:

            messagebox.showerror(
                "Application Error",
                f"Unable to start the application.\n\n"
                f"Error:\n{error}"
            )


# ============================================================
# LOGIN WINDOW
# ============================================================

class Login(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            APP_NAME
        )

        self.geometry(
            "1050x650"
        )

        self.minsize(
            950,
            600
        )

        self.configure(
            bg=BG
        )

        self.center_window()

        self.build_interface()

        # ENTER KEY = LOGIN
        self.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ========================================================
    # CENTER LOGIN WINDOW
    # ========================================================

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

    # ========================================================
    # BUILD LOGIN INTERFACE
    # ========================================================

    def build_interface(self):

        main = tk.Frame(
            self,
            bg=BG
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

        # ====================================================
        # LEFT GRAPHIC PANEL
        # ====================================================

        graphic_panel = tk.Frame(
            main,
            bg=BG
        )

        graphic_panel.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.create_remote_graphic(
            graphic_panel
        )

        # ====================================================
        # RIGHT LOGIN PANEL
        # ====================================================

        login_panel = tk.Frame(
            main,
            bg=PANEL
        )

        login_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=25,
            pady=25
        )

        # ====================================================
        # SECURITY ICON
        # ====================================================

        icon = tk.Canvas(
            login_panel,
            width=80,
            height=80,
            bg=PANEL,
            highlightthickness=0
        )

        icon.pack(
            pady=(35, 10)
        )

        icon.create_oval(
            8,
            8,
            72,
            72,
            outline=CYAN,
            width=2
        )

        icon.create_oval(
            18,
            18,
            62,
            62,
            fill="#103452",
            outline=BLUE,
            width=1
        )

        icon.create_polygon(
            40,
            24,
            55,
            30,
            52,
            49,
            40,
            59,
            28,
            49,
            25,
            30,
            fill=CYAN,
            outline=""
        )

        icon.create_text(
            40,
            41,
            text="✓",
            fill=BG,
            font=("Segoe UI", 17, "bold")
        )

        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            login_panel,
            text="VIRTUAL SYSTEM ACCESS CONTROL",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 20, "bold")
        ).pack()

        tk.Label(
            login_panel,
            text="MANAGEMENT SYSTEM",
            bg=PANEL,
            fg=CYAN,
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=(0, 5)
        )

        tk.Label(
            login_panel,
            text="Secure administrator authentication",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            pady=(0, 25)
        )

        # ====================================================
        # CONNECTION STATUS
        # ====================================================

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
            fg=GREEN,
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
            fg=GREEN,
            font=("Segoe UI", 8, "bold")
        ).pack(
            side="left",
            pady=8
        )

        # ====================================================
        # USERNAME
        # ====================================================

        tk.Label(
            login_panel,
            text="USERNAME",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=35
        )

        username_frame = tk.Frame(
            login_panel,
            bg=PANEL_LIGHT
        )

        username_frame.pack(
            fill="x",
            padx=35,
            pady=(5, 15)
        )

        tk.Label(
            username_frame,
            text="◉",
            bg=PANEL_LIGHT,
            fg=CYAN,
            font=("Segoe UI", 12)
        ).pack(
            side="left",
            padx=(12, 5)
        )

        self.username = tk.Entry(
            username_frame,
            bg=PANEL_LIGHT,
            fg=WHITE,
            insertbackground=CYAN,
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

        # ====================================================
        # PASSWORD
        # ====================================================

        tk.Label(
            login_panel,
            text="PASSWORD",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=35
        )

        password_frame = tk.Frame(
            login_panel,
            bg=PANEL_LIGHT
        )

        password_frame.pack(
            fill="x",
            padx=35,
            pady=(5, 20)
        )

        tk.Label(
            password_frame,
            text="◆",
            bg=PANEL_LIGHT,
            fg=CYAN,
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            padx=(12, 5)
        )

        self.password = tk.Entry(
            password_frame,
            bg=PANEL_LIGHT,
            fg=WHITE,
            insertbackground=CYAN,
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

        # ====================================================
        # LOGIN BUTTON
        # ====================================================

        self.login_button = tk.Button(
            login_panel,
            text="  CONNECT TO SECURE SYSTEM  ",
            command=self.login,
            bg=BLUE,
            fg=WHITE,
            activebackground=CYAN,
            activeforeground=BG,
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

        self.login_button.bind(
            "<Enter>",
            self.login_hover_enter
        )

        self.login_button.bind(
            "<Leave>",
            self.login_hover_leave
        )

        # ====================================================
        # FOOTER
        # ====================================================

        tk.Label(
            login_panel,
            text="Authorized personnel only",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(
            pady=(20, 3)
        )

        tk.Label(
            login_panel,
            text="Remote Access Security Gateway",
            bg=PANEL,
            fg="#496176",
            font=("Segoe UI", 7)
        ).pack()

        self.username.focus_set()

    # ========================================================
    # REMOTE ACCESS GRAPHIC
    # ========================================================

    def create_remote_graphic(self, parent):

        canvas = tk.Canvas(
            parent,
            bg=BG,
            highlightthickness=0
        )

        canvas.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        # ====================================================
        # HEADER
        # ====================================================

        canvas.create_text(
            45,
            45,
            text="REMOTE ACCESS",
            anchor="w",
            fill=WHITE,
            font=("Segoe UI", 25, "bold")
        )

        canvas.create_text(
            45,
            80,
            text="SECURITY GATEWAY",
            anchor="w",
            fill=CYAN,
            font=("Segoe UI", 12, "bold")
        )

        canvas.create_text(
            45,
            110,
            text="Securely manage authorized remote connections",
            anchor="w",
            fill=MUTED,
            font=("Segoe UI", 9)
        )

        # ====================================================
        # CENTRAL SERVER
        # ====================================================

        server_x = 245
        server_y = 290

        canvas.create_oval(
            server_x - 60,
            server_y - 60,
            server_x + 60,
            server_y + 60,
            fill="#0D2942",
            outline=CYAN,
            width=2
        )

        canvas.create_oval(
            server_x - 43,
            server_y - 43,
            server_x + 43,
            server_y + 43,
            fill="#123A5A",
            outline=BLUE,
            width=1
        )

        canvas.create_text(
            server_x,
            server_y - 8,
            text="VSAC",
            fill=WHITE,
            font=("Segoe UI", 18, "bold")
        )

        canvas.create_text(
            server_x,
            server_y + 17,
            text="SERVER",
            fill=CYAN,
            font=("Segoe UI", 8, "bold")
        )

        # ====================================================
        # CLIENT MACHINES
        # ====================================================

        clients = [
            (80, 200, "ADMIN"),
            (80, 380, "TECHNICIAN"),
            (330, 200, "DEVICE"),
            (330, 380, "USER")
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

            # Device node
            canvas.create_rectangle(
                x,
                y,
                x + 90,
                y + 50,
                fill="#0D2034",
                outline=BLUE,
                width=2
            )

            canvas.create_text(
                x + 45,
                y + 25,
                text=name,
                fill=WHITE,
                font=("Segoe UI", 8, "bold")
            )

        # ====================================================
        # CONNECTION STATUS DOTS
        # ====================================================

        dots = [
            (160, 245),
            (160, 360),
            (350, 245),
            (350, 360)
        ]

        for x, y in dots:

            canvas.create_oval(
                x - 4,
                y - 4,
                x + 4,
                y + 4,
                fill=GREEN,
                outline=""
            )

        # ====================================================
        # SECURITY MESSAGE
        # ====================================================

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
            fill=GREEN,
            font=("Segoe UI", 11, "bold")
        )

        canvas.create_text(
            115,
            492,
            text="SECURE REMOTE ACCESS ENABLED",
            anchor="w",
            fill=GREEN,
            font=("Segoe UI", 8, "bold")
        )

        canvas.create_text(
            115,
            513,
            text="Authentication required before connection",
            anchor="w",
            fill=MUTED,
            font=("Segoe UI", 8)
        )

        # ====================================================
        # FOOTER
        # ====================================================

        canvas.create_text(
            45,
            570,
            text="VIRTUAL SYSTEM ACCESS CONTROL",
            anchor="w",
            fill="#496176",
            font=("Segoe UI", 8, "bold")
        )

    # ========================================================
    # LOGIN BUTTON HOVER
    # ========================================================

    def login_hover_enter(self, event):

        self.login_button.configure(
            bg=CYAN,
            fg=BG
        )

    def login_hover_leave(self, event):

        self.login_button.configure(
            bg=BLUE,
            fg=WHITE
        )

    # ========================================================
    # LOGIN FUNCTION
    # ========================================================

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        # ====================================================
        # EMPTY FIELDS
        # ====================================================

        if not username or not password:

            messagebox.showwarning(
                "Authentication Required",
                "Please enter your username and password.",
                parent=self
            )

            return

        # ====================================================
        # DATABASE CONNECTION
        # ====================================================

        connection = get_connection()

        if not connection:

            messagebox.showerror(
                "Connection Error",
                "Unable to connect to the Virtual System Access Control database.",
                parent=self
            )

            return

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            # =================================================
            # FIND ACTIVE USER
            # =================================================

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

            # =================================================
            # VERIFY PASSWORD
            # =================================================

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

                    # -----------------------------------------
                    # CLOSE LOGIN
                    # -----------------------------------------

                    self.destroy()

                    # -----------------------------------------
                    # OPEN DASHBOARD
                    # -----------------------------------------

                    import dashboard

                    dashboard.start_dashboard(
                        user
                    )

                    return

            # =================================================
            # INVALID LOGIN
            # =================================================

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


# ============================================================
# START LOGIN
# ============================================================

def start_login():

    app = Login()

    app.mainloop()


# ============================================================
# APPLICATION START
# ============================================================

def main():

    try:

        # ----------------------------------------------------
        # Start splash screen
        # ----------------------------------------------------

        splash = SplashScreen()

        splash.start()

        splash.root.mainloop()

    except Exception as error:

        messagebox.showerror(
            "Startup Error",
            f"{APP_NAME} could not start.\n\n"
            f"Error:\n{error}"
        )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()