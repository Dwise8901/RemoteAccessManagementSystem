import tkinter as tk
from tkinter import messagebox

from database import get_connection
from security import verify_password, verify_mfa_code


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
    ORANGE = "#FFB020"

    # ============================================================
    # WINDOW
    # ============================================================

    def __init__(self):

        super().__init__()

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

        self.center_window()

        self.build_interface()

        # ENTER = LOGIN
        self.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ============================================================
    # CENTER LOGIN WINDOW
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
        # LEFT GRAPHIC
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

        icon.create_oval(
            8,
            8,
            72,
            72,
            outline=self.CYAN,
            width=2
        )

        icon.create_oval(
            18,
            18,
            62,
            62,
            fill="#103452",
            outline=self.BLUE,
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
            text="Secure multi-factor authentication",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            pady=(0, 25)
        )

        # ========================================================
        # SECURITY STATUS
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
            text="MFA PROTECTED CONNECTION",
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
            text="Password + Authenticator Code Required",
            bg=self.PANEL,
            fg="#496176",
            font=("Segoe UI", 7)
        ).pack()

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
            text="VIRTUAL ACCESS",
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
            text="Securely manage authorized system access",
            anchor="w",
            fill=self.MUTED,
            font=("Segoe UI", 9)
        )

        # ========================================================
        # NETWORK
        # ========================================================

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
            text="VSAC",
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

        clients = [
            (80, 200, "ADMIN"),
            (80, 380, "TECHNICIAN"),
            (330, 200, "DEVICE"),
            (330, 380, "USER"),
        ]

        for x, y, name in clients:

            canvas.create_line(
                x + 45,
                y + 25,
                server_x,
                server_y,
                fill="#245A7E",
                width=2
            )

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
            text="MULTI-FACTOR AUTHENTICATION",
            anchor="w",
            fill=self.GREEN,
            font=("Segoe UI", 8, "bold")
        )

        canvas.create_text(
            115,
            513,
            text="Password + authenticator verification required",
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
    # LOGIN
    # ============================================================

    def login(self):

        username = self.username.get().strip()
        password = self.password.get()

        # ========================================================
        # CHECK EMPTY FIELDS
        # ========================================================

        if not username or not password:

            messagebox.showwarning(
                "Authentication Required",
                "Please enter your username and password.",
                parent=self
            )

            return

        # ========================================================
        # DISABLE LOGIN BUTTON
        # ========================================================

        self.login_button.configure(
            state="disabled",
            text="  AUTHENTICATING...  "
        )

        self.update_idletasks()

        # ========================================================
        # DATABASE CONNECTION
        # ========================================================

        connection = get_connection()

        if not connection:

            self.reset_login_button()

            messagebox.showerror(
                "Connection Error",
                "Unable to connect to the Virtual System Access Control database.",
                parent=self
            )

            return

        cursor = None

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            # ====================================================
            # FIND USER
            # ====================================================

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            user = cursor.fetchone()

            # ====================================================
            # USER NOT FOUND
            # ====================================================

            if not user:

                self.authentication_failed(
                    "Invalid username or password."
                )

                return

            # ====================================================
            # ACCOUNT STATUS
            # ====================================================

            account_status = str(
                user.get(
                    "status",
                    ""
                )
            ).strip().upper()

            if account_status != "ACTIVE":

                self.reset_login_button()

                messagebox.showerror(
                    "Account Unavailable",
                    f"Your account is currently {account_status}.\n\n"
                    "Please contact the system administrator.",
                    parent=self
                )

                self.password.delete(
                    0,
                    tk.END
                )

                self.password.focus_set()

                return

            # ====================================================
            # VERIFY PASSWORD
            # ====================================================

            password_hash = user.get(
                "password_hash"
            )

            if not password_hash:

                self.authentication_failed(
                    "Invalid username or password."
                )

                return

            try:

                password_valid = verify_password(
                    password,
                    password_hash
                )

            except Exception as error:

                print(
                    "Password verification error:",
                    error
                )

                password_valid = False

            if not password_valid:

                self.authentication_failed(
                    "Invalid username or password."
                )

                return

            # ====================================================
            # CHECK MFA STATUS
            # ====================================================

            raw_mfa_enabled = user.get(
                "mfa_enabled",
                0
            )

            mfa_enabled = str(
                raw_mfa_enabled
            ).strip().lower() in (
                "1",
                "true",
                "yes",
                "on"
            )

            mfa_secret = user.get(
                "mfa_secret"
            )

            # ====================================================
            # CLOSE DATABASE CONNECTION
            # ====================================================

            cursor.close()
            cursor = None

            connection.close()
            connection = None

            # ====================================================
            # MFA ENABLED
            # ====================================================

            if mfa_enabled:

                # MFA is enabled but secret is missing
                if not mfa_secret:

                    self.reset_login_button()

                    messagebox.showerror(
                        "MFA Configuration Error",
                        "MFA is enabled for this account, "
                        "but no MFA secret is stored.\n\n"
                        "Please contact the system administrator.",
                        parent=self
                    )

                    return

                # ------------------------------------------------
                # PASSWORD VERIFIED
                # NOW REQUIRE MFA
                # ------------------------------------------------

                self.reset_login_button()

                self.show_mfa_window(
                    user,
                    mfa_secret
                )

                return

            # ====================================================
            # MFA NOT ENABLED
            # ====================================================

            self.reset_login_button()

            messagebox.showwarning(
                "MFA Setup Required",
                "Your password is correct, but MFA has not "
                "been configured for this account.\n\n"
                "You must complete MFA setup before accessing "
                "the Virtual System Access Control dashboard.",
                parent=self
            )

            self.open_mfa_setup(
                user
            )

        except Exception as error:

            print(
                "Login error:",
                error
            )

            self.reset_login_button()

            messagebox.showerror(
                "Authentication Error",
                f"An error occurred during authentication:\n\n"
                f"{error}",
                parent=self
            )

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if connection:

                try:
                    connection.close()
                except Exception:
                    pass

    # ============================================================
    # RESET LOGIN BUTTON
    # ============================================================

    def reset_login_button(self):

        self.login_button.configure(
            state="normal",
            text="  CONNECT TO SECURE SYSTEM  "
        )

    # ============================================================
    # AUTHENTICATION FAILED
    # ============================================================

    def authentication_failed(
        self,
        message
    ):

        self.reset_login_button()

        messagebox.showerror(
            "Authentication Failed",
            message,
            parent=self
        )

        self.password.delete(
            0,
            tk.END
        )

        self.password.focus_set()

    # ============================================================
    # OPEN MFA SETUP
    # ============================================================

    def open_mfa_setup(
        self,
        user
    ):

        try:

            from mfa_setup import MFASetupWindow

            MFASetupWindow(
                self,
                user,
                on_success=lambda:
                self.mfa_setup_success(user)
            )

        except Exception as error:

            messagebox.showerror(
                "MFA Setup Error",
                f"Unable to open MFA setup:\n\n{error}",
                parent=self
            )

    # ============================================================
    # MFA SETUP SUCCESS
    # ============================================================

    def mfa_setup_success(
        self,
        user
    ):

        messagebox.showinfo(
            "MFA Enabled",
            "Multi-Factor Authentication has been "
            "successfully enabled.\n\n"
            "Your account is now protected by password "
            "and authenticator verification.",
            parent=self
        )

        # --------------------------------------------------------
        # MFA SETUP WAS VERIFIED
        # --------------------------------------------------------
        # The user can now enter the dashboard.

        self.login_success(
            user,
            mfa_required=True
        )

    # ============================================================
    # MFA VERIFICATION WINDOW
    # ============================================================

    def show_mfa_window(
        self,
        user,
        mfa_secret
    ):

        # Prevent duplicate MFA windows
        if hasattr(
            self,
            "mfa_window"
        ):

            try:

                if self.mfa_window.winfo_exists():

                    self.mfa_window.lift()
                    self.mfa_window.focus_force()

                    return

            except Exception:
                pass

        self.mfa_window = tk.Toplevel(
            self
        )

        self.mfa_window.title(
            "MFA Verification"
        )

        self.mfa_window.geometry(
            "500x470"
        )

        self.mfa_window.resizable(
            False,
            False
        )

        self.mfa_window.configure(
            bg=self.BG
        )

        self.mfa_window.transient(
            self
        )

        self.mfa_window.grab_set()

        self.center_mfa_window()

        # ========================================================
        # SECURITY ICON
        # ========================================================

        icon = tk.Canvas(
            self.mfa_window,
            width=75,
            height=75,
            bg=self.BG,
            highlightthickness=0
        )

        icon.pack(
            pady=(25, 5)
        )

        icon.create_oval(
            8,
            8,
            67,
            67,
            outline=self.CYAN,
            width=2
        )

        icon.create_oval(
            18,
            18,
            57,
            57,
            fill="#103452",
            outline=self.BLUE,
            width=1
        )

        icon.create_text(
            37,
            38,
            text="2FA",
            fill=self.CYAN,
            font=("Segoe UI", 11, "bold")
        )

        # ========================================================
        # TITLE
        # ========================================================

        tk.Label(
            self.mfa_window,
            text="MULTI-FACTOR AUTHENTICATION",
            bg=self.BG,
            fg=self.WHITE,
            font=("Segoe UI", 17, "bold")
        ).pack()

        tk.Label(
            self.mfa_window,
            text="Authenticator Verification",
            bg=self.BG,
            fg=self.CYAN,
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=(2, 8)
        )

        tk.Label(
            self.mfa_window,
            text=f"Welcome, {user.get('username', '')}",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack()

        # ========================================================
        # INFORMATION PANEL
        # ========================================================

        info = tk.Frame(
            self.mfa_window,
            bg=self.PANEL
        )

        info.pack(
            fill="x",
            padx=45,
            pady=20
        )

        tk.Label(
            info,
            text="Enter the 6-digit code from your",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9)
        ).pack(
            pady=(15, 2)
        )

        tk.Label(
            info,
            text="Authenticator application",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=(0, 15)
        )

        # ========================================================
        # MFA CODE
        # ========================================================

        self.mfa_code = tk.Entry(
            self.mfa_window,
            bg=self.PANEL_LIGHT,
            fg=self.WHITE,
            insertbackground=self.CYAN,
            justify="center",
            relief="flat",
            bd=0,
            font=("Segoe UI", 24, "bold"),
            width=8
        )

        self.mfa_code.pack(
            pady=(0, 15),
            ipady=8
        )

        self.mfa_code.focus_set()

        self.mfa_code.bind(
            "<KeyRelease>",
            self.limit_mfa_code
        )

        self.mfa_code.bind(
            "<Return>",
            lambda event:
            self.verify_mfa(
                user,
                mfa_secret
            )
        )

        # ========================================================
        # VERIFY BUTTON
        # ========================================================

        verify_button = tk.Button(
            self.mfa_window,
            text="  VERIFY AUTHENTICATOR CODE  ",
            command=lambda:
            self.verify_mfa(
                user,
                mfa_secret
            ),
            bg=self.BLUE,
            fg=self.WHITE,
            activebackground=self.CYAN,
            activeforeground=self.BG,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            pady=11
        )

        verify_button.pack(
            fill="x",
            padx=80
        )

        # ========================================================
        # CANCEL
        # ========================================================

        tk.Button(
            self.mfa_window,
            text="Cancel",
            command=self.cancel_mfa,
            bg=self.PANEL,
            fg=self.MUTED,
            activebackground=self.PANEL_LIGHT,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9)
        ).pack(
            pady=(12, 5)
        )

        # ========================================================
        # SECURITY MESSAGE
        # ========================================================

        tk.Label(
            self.mfa_window,
            text="●  MFA verification protects your system access",
            bg=self.BG,
            fg=self.GREEN,
            font=("Segoe UI", 8)
        ).pack(
            pady=(5, 15)
        )

        self.current_mfa_user = user
        self.current_mfa_secret = mfa_secret

    # ============================================================
    # CENTER MFA WINDOW
    # ============================================================

    def center_mfa_window(self):

        self.mfa_window.update_idletasks()

        width = 500
        height = 470

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (
            screen_width - width
        ) // 2

        y = (
            screen_height - height
        ) // 2

        self.mfa_window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ============================================================
    # LIMIT MFA CODE
    # ============================================================

    def limit_mfa_code(
        self,
        event=None
    ):

        value = self.mfa_code.get()

        value = "".join(
            character
            for character in value
            if character.isdigit()
        )

        value = value[:6]

        self.mfa_code.delete(
            0,
            tk.END
        )

        self.mfa_code.insert(
            0,
            value
        )

    # ============================================================
    # VERIFY MFA
    # ============================================================

    def verify_mfa(
        self,
        user,
        mfa_secret
    ):

        code = self.mfa_code.get().strip()

        # ========================================================
        # VALIDATE CODE
        # ========================================================

        if (
            len(code) != 6
            or not code.isdigit()
        ):

            messagebox.showwarning(
                "Invalid MFA Code",
                "Please enter the 6-digit code from "
                "your authenticator application.",
                parent=self.mfa_window
            )

            self.mfa_code.focus_set()

            return

        # ========================================================
        # VERIFY TOTP
        # ========================================================

        try:

            valid = verify_mfa_code(
                mfa_secret,
                code
            )

        except Exception as error:

            print(
                "MFA verification error:",
                error
            )

            valid = False

        # ========================================================
        # INVALID CODE
        # ========================================================

        if not valid:

            messagebox.showerror(
                "MFA Verification Failed",
                "The authenticator code is incorrect "
                "or has expired.\n\n"
                "Please enter the current 6-digit code.",
                parent=self.mfa_window
            )

            self.mfa_code.delete(
                0,
                tk.END
            )

            self.mfa_code.focus_set()

            return

        # ========================================================
        # MFA SUCCESS
        # ========================================================

        try:

            self.mfa_window.grab_release()

        except Exception:
            pass

        self.mfa_window.destroy()

        self.login_success(
            user,
            mfa_required=True
        )

    # ============================================================
    # CANCEL MFA
    # ============================================================

    def cancel_mfa(self):

        try:

            self.mfa_window.grab_release()

        except Exception:
            pass

        self.mfa_window.destroy()

        self.reset_login_button()

        self.password.delete(
            0,
            tk.END
        )

        self.password.focus_set()

    # ============================================================
    # LOGIN SUCCESS
    # ============================================================

    def login_success(
        self,
        user,
        mfa_required=False
    ):

        # ========================================================
        # SECURITY CHECK
        # ========================================================

        if not mfa_required:

            messagebox.showerror(
                "Access Denied",
                "MFA verification is required before "
                "accessing the dashboard.",
                parent=self
            )

            return

        # ========================================================
        # SUCCESS MESSAGE
        # ========================================================

        messagebox.showinfo(
            "Authentication Successful",
            f"Welcome {user.get('username', '')}!\n\n"
            "Password authentication and MFA verification "
            "were successful.",
            parent=self
        )

        # ========================================================
        # CLOSE LOGIN
        # ========================================================

        self.destroy()

        # ========================================================
        # OPEN DASHBOARD
        # ========================================================

        try:

            import dashboard

            dashboard.start_dashboard(
                user
            )

        except Exception as error:

            messagebox.showerror(
                "Dashboard Error",
                f"Unable to open the dashboard:\n\n{error}"
            )


# =================================================================
# START LOGIN APPLICATION
# =================================================================

def start_login():

    app = Login()

    app.mainloop()


# =================================================================
# PROGRAM ENTRY POINT
# =================================================================

if __name__ == "__main__":

    start_login()