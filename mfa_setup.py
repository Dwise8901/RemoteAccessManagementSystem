import tkinter as tk
from tkinter import messagebox
import pyotp
import qrcode
from PIL import Image, ImageTk

from database import get_connection
from security import generate_mfa_secret, verify_mfa_code


class MFASetupWindow:

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
    # INITIALIZE
    # ============================================================

    def __init__(self, parent, current_user):

        self.parent = parent
        self.current_user = current_user

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Multi-Factor Authentication Setup"
        )

        self.window.geometry(
            "850x700"
        )

        self.window.minsize(
            800,
            650
        )

        self.window.configure(
            bg=self.BG
        )

        self.window.transient(parent)

        self.window.grab_set()

        self.center_window()

        # QR image reference
        self.qr_photo = None

        # MFA secret
        self.mfa_secret = None

        # Build interface
        self.build_interface()

        # Load current MFA status
        self.load_mfa_status()

    # ============================================================
    # CENTER WINDOW
    # ============================================================

    def center_window(self):

        self.window.update_idletasks()

        width = 850
        height = 700

        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (
            screen_width - width
        ) // 2

        y = (
            screen_height - height
        ) // 2

        self.window.geometry(
            f"{width}x{height}+{x}+{y}"
        )

    # ============================================================
    # BUILD INTERFACE
    # ============================================================

    def build_interface(self):

        # ========================================================
        # MAIN CONTAINER
        # ========================================================

        main = tk.Frame(
            self.window,
            bg=self.BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        # ========================================================
        # HEADER
        # ========================================================

        header = tk.Frame(
            main,
            bg=self.PANEL
        )

        header.pack(
            fill="x"
        )

        # Security icon
        icon = tk.Canvas(
            header,
            width=70,
            height=70,
            bg=self.PANEL,
            highlightthickness=0
        )

        icon.pack(
            side="left",
            padx=20,
            pady=15
        )

        icon.create_oval(
            8,
            8,
            62,
            62,
            outline=self.CYAN,
            width=2
        )

        icon.create_oval(
            18,
            18,
            52,
            52,
            fill="#103452",
            outline=self.BLUE
        )

        icon.create_text(
            35,
            35,
            text="2FA",
            fill=self.CYAN,
            font=("Segoe UI", 10, "bold")
        )

        # Header text
        header_text = tk.Frame(
            header,
            bg=self.PANEL
        )

        header_text.pack(
            side="left",
            pady=15
        )

        tk.Label(
            header_text,
            text="MULTI-FACTOR AUTHENTICATION",
            bg=self.PANEL,
            fg=self.WHITE,
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            header_text,
            text="Protect your Virtual System Access Control account",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )

        # ========================================================
        # USER INFORMATION
        # ========================================================

        user_frame = tk.Frame(
            main,
            bg="#09291F"
        )

        user_frame.pack(
            fill="x",
            pady=(15, 15)
        )

        username = self.current_user.get(
            "username",
            "Unknown"
        )

        full_name = self.current_user.get(
            "full_name",
            ""
        )

        role = self.current_user.get(
            "role",
            "USER"
        )

        tk.Label(
            user_frame,
            text="●",
            bg="#09291F",
            fg=self.GREEN,
            font=("Segoe UI", 12)
        ).pack(
            side="left",
            padx=(15, 7),
            pady=10
        )

        tk.Label(
            user_frame,
            text=f"Account: {username}",
            bg="#09291F",
            fg=self.WHITE,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            user_frame,
            text=f"   {full_name}   |   {role}",
            bg="#09291F",
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(
            side="left"
        )

        # ========================================================
        # CONTENT
        # ========================================================

        content = tk.Frame(
            main,
            bg=self.BG
        )

        content.pack(
            fill="both",
            expand=True
        )

        content.grid_columnconfigure(
            0,
            weight=1
        )

        content.grid_columnconfigure(
            1,
            weight=1
        )

        content.grid_rowconfigure(
            0,
            weight=1
        )

        # ========================================================
        # LEFT INSTRUCTIONS PANEL
        # ========================================================

        instructions = tk.Frame(
            content,
            bg=self.PANEL
        )

        instructions.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        tk.Label(
            instructions,
            text="SETUP INSTRUCTIONS",
            bg=self.PANEL,
            fg=self.CYAN,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        steps = [
            (
                "1",
                "Install an authenticator app",
                "Use Google Authenticator, Microsoft Authenticator, "
                "Authy, or another TOTP-compatible application."
            ),
            (
                "2",
                "Scan the QR code",
                "Open your authenticator app and scan the QR code "
                "shown on this screen."
            ),
            (
                "3",
                "Enter the security code",
                "Your authenticator will generate a 6-digit code. "
                "Enter the current code below."
            ),
            (
                "4",
                "Verify and enable MFA",
                "The system will verify your code before enabling "
                "multi-factor authentication."
            )
        ]

        for number, title, description in steps:

            step_frame = tk.Frame(
                instructions,
                bg=self.PANEL
            )

            step_frame.pack(
                fill="x",
                padx=20,
                pady=8
            )

            # Number circle
            number_canvas = tk.Canvas(
                step_frame,
                width=35,
                height=35,
                bg=self.PANEL,
                highlightthickness=0
            )

            number_canvas.pack(
                side="left",
                anchor="n"
            )

            number_canvas.create_oval(
                3,
                3,
                32,
                32,
                fill=self.BLUE,
                outline=self.CYAN
            )

            number_canvas.create_text(
                17,
                17,
                text=number,
                fill=self.WHITE,
                font=("Segoe UI", 9, "bold")
            )

            # Text
            text_frame = tk.Frame(
                step_frame,
                bg=self.PANEL
            )

            text_frame.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(10, 0)
            )

            tk.Label(
                text_frame,
                text=title,
                bg=self.PANEL,
                fg=self.WHITE,
                font=("Segoe UI", 9, "bold"),
                anchor="w"
            ).pack(
                fill="x"
            )

            tk.Label(
                text_frame,
                text=description,
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 8),
                justify="left",
                wraplength=300,
                anchor="w"
            ).pack(
                fill="x",
                pady=(3, 0)
            )

        # ========================================================
        # RIGHT QR PANEL
        # ========================================================

        qr_panel = tk.Frame(
            content,
            bg=self.PANEL
        )

        qr_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )

        tk.Label(
            qr_panel,
            text="AUTHENTICATOR QR CODE",
            bg=self.PANEL,
            fg=self.WHITE,
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=(20, 5)
        )

        tk.Label(
            qr_panel,
            text="Scan this code with your authenticator app",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(
            pady=(0, 15)
        )

        # QR display
        self.qr_frame = tk.Frame(
            qr_panel,
            bg="#FFFFFF",
            width=260,
            height=260
        )

        self.qr_frame.pack(
            pady=5
        )

        self.qr_frame.pack_propagate(
            False
        )

        self.qr_label = tk.Label(
            self.qr_frame,
            bg="#FFFFFF"
        )

        self.qr_label.pack(
            fill="both",
            expand=True
        )

        # QR status
        self.qr_status = tk.Label(
            qr_panel,
            text="Preparing secure QR code...",
            bg=self.PANEL,
            fg=self.ORANGE,
            font=("Segoe UI", 8)
        )

        self.qr_status.pack(
            pady=10
        )

        # ========================================================
        # OTP SECTION
        # ========================================================

        otp_label = tk.Label(
            qr_panel,
            text="ENTER 6-DIGIT AUTHENTICATOR CODE",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        )

        otp_label.pack(
            pady=(5, 5)
        )

        self.otp_entry = tk.Entry(
            qr_panel,
            bg=self.PANEL_LIGHT,
            fg=self.WHITE,
            insertbackground=self.CYAN,
            justify="center",
            relief="flat",
            bd=0,
            font=("Segoe UI", 20, "bold"),
            width=8
        )

        self.otp_entry.pack(
            ipady=7
        )

        self.otp_entry.bind(
            "<KeyRelease>",
            self.limit_otp
        )

        self.otp_entry.bind(
            "<Return>",
            lambda event: self.verify_and_enable()
        )

        # ========================================================
        # BUTTONS
        # ========================================================

        button_frame = tk.Frame(
            main,
            bg=self.BG
        )

        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        self.enable_button = tk.Button(
            button_frame,
            text="  VERIFY & ENABLE MFA  ",
            command=self.verify_and_enable,
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

        self.enable_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        self.disable_button = tk.Button(
            button_frame,
            text="DISABLE MFA",
            command=self.disable_mfa,
            bg="#47202A",
            fg=self.RED,
            activebackground=self.RED,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            pady=11
        )

        self.disable_button.pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="CLOSE",
            command=self.close_window,
            bg=self.PANEL,
            fg=self.MUTED,
            activebackground=self.PANEL_LIGHT,
            activeforeground=self.WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            pady=11
        ).pack(
            side="left",
            padx=(5, 0)
        )

    # ============================================================
    # LOAD MFA STATUS
    # ============================================================

    def load_mfa_status(self):

        username = self.current_user.get(
            "username"
        )

        if not username:

            self.qr_status.configure(
                text="Unable to identify user.",
                fg=self.RED
            )

            return

        connection = get_connection()

        if not connection:

            self.qr_status.configure(
                text="Database connection failed.",
                fg=self.RED
            )

            messagebox.showerror(
                "Database Error",
                "Unable to connect to the database.",
                parent=self.window
            )

            return

        try:

            cursor = connection.cursor(
                dictionary=True
            )

            query = """
                SELECT user_id,
                       username,
                       mfa_enabled,
                       mfa_secret
                FROM users
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (
                    self.current_user.get(
                        "user_id"
                    ),
                )
            )

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if not user:

                self.qr_status.configure(
                    text="User account was not found.",
                    fg=self.RED
                )

                return

            # ====================================================
            # MFA ALREADY ENABLED
            # ====================================================

            if user.get("mfa_enabled"):

                self.qr_status.configure(
                    text="● MFA is currently ENABLED",
                    fg=self.GREEN
                )

                self.enable_button.configure(
                    text="  MFA ALREADY ENABLED  ",
                    state="disabled"
                )

                self.disable_button.configure(
                    state="normal"
                )

                # Don't generate a new secret automatically
                if user.get("mfa_secret"):

                    self.mfa_secret = user.get(
                        "mfa_secret"
                    )

                return

            # ====================================================
            # MFA NOT ENABLED
            # ====================================================

            self.disable_button.configure(
                state="disabled"
            )

            self.generate_qr_code()

        except Exception as error:

            try:
                connection.close()
            except Exception:
                pass

            self.qr_status.configure(
                text="Unable to load MFA status.",
                fg=self.RED
            )

            messagebox.showerror(
                "MFA Error",
                f"An error occurred:\n\n{error}",
                parent=self.window
            )

    # ============================================================
    # GENERATE QR CODE
    # ============================================================

    def generate_qr_code(self):

        try:

            # Generate secret
            self.mfa_secret = generate_mfa_secret()

            username = self.current_user.get(
                "username",
                "user"
            )

            # Application name shown inside authenticator
            issuer = "Virtual System Access Control"

            # Build TOTP URI
            totp = pyotp.TOTP(
                self.mfa_secret
            )

            provisioning_uri = totp.provisioning_uri(
                name=username,
                issuer_name=issuer
            )

            # Generate QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4
            )

            qr.add_data(
                provisioning_uri
            )

            qr.make(
                fit=True
            )

            qr_image = qr.make_image(
                fill_color="black",
                back_color="white"
            )

            # Convert to PIL image
            qr_image = qr_image.convert(
                "RGB"
            )

            # Resize for display
            qr_image = qr_image.resize(
                (240, 240)
            )

            # Convert to Tkinter image
            self.qr_photo = ImageTk.PhotoImage(
                qr_image
            )

            self.qr_label.configure(
                image=self.qr_photo
            )

            self.qr_status.configure(
                text="● QR code generated — scan to continue",
                fg=self.GREEN
            )

            # Focus OTP
            self.otp_entry.focus_set()

        except Exception as error:

            self.qr_status.configure(
                text="Failed to generate QR code.",
                fg=self.RED
            )

            messagebox.showerror(
                "QR Code Error",
                f"Unable to generate the MFA QR code:\n\n{error}",
                parent=self.window
            )

    # ============================================================
    # LIMIT OTP
    # ============================================================

    def limit_otp(self, event=None):

        value = self.otp_entry.get()

        # Digits only
        value = "".join(
            character
            for character in value
            if character.isdigit()
        )

        # Maximum six digits
        value = value[:6]

        self.otp_entry.delete(
            0,
            tk.END
        )

        self.otp_entry.insert(
            0,
            value
        )

    # ============================================================
    # VERIFY AND ENABLE MFA
    # ============================================================

    def verify_and_enable(self):

        if not self.mfa_secret:

            messagebox.showerror(
                "MFA Setup Error",
                "No MFA secret is available.\n\n"
                "Please close and reopen the MFA setup window.",
                parent=self.window
            )

            return

        code = self.otp_entry.get().strip()

        # ========================================================
        # CHECK CODE
        # ========================================================

        if len(code) != 6 or not code.isdigit():

            messagebox.showwarning(
                "Invalid Code",
                "Please enter the 6-digit code shown in "
                "your authenticator application.",
                parent=self.window
            )

            self.otp_entry.focus_set()

            return

        # ========================================================
        # VERIFY CODE
        # ========================================================

        try:

            valid = verify_mfa_code(
                self.mfa_secret,
                code
            )

        except Exception:

            valid = False

        if not valid:

            messagebox.showerror(
                "Verification Failed",
                "The authenticator code is incorrect or expired.\n\n"
                "Please enter the current 6-digit code.",
                parent=self.window
            )

            self.otp_entry.delete(
                0,
                tk.END
            )

            self.otp_entry.focus_set()

            return

        # ========================================================
        # SAVE MFA
        # ========================================================

        connection = get_connection()

        if not connection:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to the database.",
                parent=self.window
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE users
                SET mfa_enabled = 1,
                    mfa_secret = %s
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (
                    self.mfa_secret,
                    self.current_user.get(
                        "user_id"
                    )
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            # Update current user object
            self.current_user[
                "mfa_enabled"
            ] = 1

            self.current_user[
                "mfa_secret"
            ] = self.mfa_secret

            # ====================================================
            # SUCCESS
            # ====================================================

            self.qr_status.configure(
                text="● MFA ENABLED SUCCESSFULLY",
                fg=self.GREEN
            )

            self.enable_button.configure(
                text="  MFA ENABLED  ",
                state="disabled"
            )

            self.disable_button.configure(
                state="normal"
            )

            messagebox.showinfo(
                "MFA Enabled",
                "Multi-factor authentication has been enabled "
                "successfully for your account.\n\n"
                "The next time you log in, you will need your "
                "password and the 6-digit authenticator code.",
                parent=self.window
            )

        except Exception as error:

            try:
                connection.rollback()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Unable to save MFA settings:\n\n{error}",
                parent=self.window
            )

    # ============================================================
    # DISABLE MFA
    # ============================================================

    def disable_mfa(self):

        username = self.current_user.get(
            "username",
            "this account"
        )

        confirm = messagebox.askyesno(
            "Disable MFA",
            f"Are you sure you want to disable MFA for "
            f"{username}?\n\n"
            "This will remove the authenticator requirement "
            "from the account.",
            parent=self.window
        )

        if not confirm:

            return

        connection = get_connection()

        if not connection:

            messagebox.showerror(
                "Database Error",
                "Unable to connect to the database.",
                parent=self.window
            )

            return

        try:

            cursor = connection.cursor()

            query = """
                UPDATE users
                SET mfa_enabled = 0,
                    mfa_secret = NULL
                WHERE user_id = %s
            """

            cursor.execute(
                query,
                (
                    self.current_user.get(
                        "user_id"
                    ),
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            # Update user object
            self.current_user[
                "mfa_enabled"
            ] = 0

            self.current_user[
                "mfa_secret"
            ] = None

            messagebox.showinfo(
                "MFA Disabled",
                "Multi-factor authentication has been disabled "
                "for this account.",
                parent=self.window
            )

            self.window.destroy()

        except Exception as error:

            try:
                connection.rollback()
            except Exception:
                pass

            try:
                connection.close()
            except Exception:
                pass

            messagebox.showerror(
                "Database Error",
                f"Unable to disable MFA:\n\n{error}",
                parent=self.window
            )

    # ============================================================
    # CLOSE WINDOW
    # ============================================================

    def close_window(self):

        try:

            self.window.grab_release()

        except Exception:
            pass

        self.window.destroy()


# ================================================================
# FUNCTION FOR OPENING MFA SETUP
# ================================================================

def open_mfa_setup(parent, current_user):

    MFASetupWindow(
        parent,
        current_user
    )