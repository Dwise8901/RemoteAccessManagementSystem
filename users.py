import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection
from security import hash_password


class UsersWindow:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)

        self.window.title("User Management")

        self.window.geometry("1250x750")

        self.window.minsize(1050, 650)

        self.window.configure(
            bg="#eef3f8"
        )

        self.setup_styles()

        self.build_interface()

        self.load_users()

    # =========================================================
    # STYLES
    # =========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#1e293b",
            rowheight=38,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#172554",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#bfdbfe")
            ],
            foreground=[
                ("selected", "#172554")
            ]
        )

        style.configure(
            "TCombobox",
            padding=7,
            font=("Segoe UI", 10)
        )

    # =========================================================
    # MAIN INTERFACE
    # =========================================================

    def build_interface(self):

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            self.window,
            bg="#172554",
            height=85
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="USER MANAGEMENT",
            font=("Segoe UI", 20, "bold"),
            bg="#172554",
            fg="white"
        ).pack(
            side="left",
            padx=25,
            pady=20
        )

        tk.Label(
            header,
            text="User Accounts • Roles • Security • Access Control",
            font=("Segoe UI", 10),
            bg="#172554",
            fg="#bfdbfe"
        ).pack(
            side="left"
        )

        # -----------------------------------------------------
        # SUMMARY CARDS
        # -----------------------------------------------------

        summary = tk.Frame(
            self.window,
            bg="#eef3f8"
        )

        summary.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.total_label = self.create_card(
            summary,
            "TOTAL USERS",
            "#2563eb"
        )

        self.active_label = self.create_card(
            summary,
            "ACTIVE",
            "#16a34a"
        )

        self.inactive_label = self.create_card(
            summary,
            "INACTIVE",
            "#dc2626"
        )

        self.admin_label = self.create_card(
            summary,
            "ADMINISTRATORS",
            "#7c3aed"
        )

        # -----------------------------------------------------
        # USER FORM
        # -----------------------------------------------------

        form_container = tk.Frame(
            self.window,
            bg="white",
            highlightbackground="#dbe3ec",
            highlightthickness=1
        )

        form_container.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            form_container,
            text="  CREATE / EDIT USER ACCOUNT",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            anchor="w"
        ).pack(
            fill="x"
        )

        form = tk.Frame(
            form_container,
            bg="white"
        )

        form.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # -----------------------------------------------------
        # USERNAME
        # -----------------------------------------------------

        tk.Label(
            form,
            text="Username",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=6,
            sticky="w"
        )

        self.username = tk.Entry(
            form,
            width=25,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.username.grid(
            row=0,
            column=1,
            padx=5
        )

        # -----------------------------------------------------
        # PASSWORD
        # -----------------------------------------------------

        tk.Label(
            form,
            text="Password",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=0,
            column=2,
            padx=(25, 5),
            pady=6,
            sticky="w"
        )

        self.password = tk.Entry(
            form,
            width=25,
            show="*",
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.password.grid(
            row=0,
            column=3,
            padx=5
        )

        # -----------------------------------------------------
        # FULL NAME
        # -----------------------------------------------------

        tk.Label(
            form,
            text="Full Name",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=6,
            sticky="w"
        )

        self.full_name = tk.Entry(
            form,
            width=25,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.full_name.grid(
            row=1,
            column=1,
            padx=5
        )

        # -----------------------------------------------------
        # EMAIL
        # -----------------------------------------------------

        tk.Label(
            form,
            text="Email",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=1,
            column=2,
            padx=(25, 5),
            pady=6,
            sticky="w"
        )

        self.email = tk.Entry(
            form,
            width=25,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.email.grid(
            row=1,
            column=3,
            padx=5
        )

        # -----------------------------------------------------
        # ROLE
        # -----------------------------------------------------

        tk.Label(
            form,
            text="Role",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=2,
            column=0,
            padx=5,
            pady=6,
            sticky="w"
        )

        self.role = ttk.Combobox(
            form,
            values=[
                "ADMIN",
                "MANAGER",
                "TECHNICIAN",
                "USER"
            ],
            state="readonly",
            width=23
        )

        self.role.set("USER")

        self.role.grid(
            row=2,
            column=1,
            padx=5
        )

        # -----------------------------------------------------
        # ADD USER
        # -----------------------------------------------------

        tk.Button(
            form,
            text="＋ Add User",
            command=self.add_user,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).grid(
            row=2,
            column=3,
            sticky="e",
            padx=5
        )

        # -----------------------------------------------------
        # SEARCH / FILTER
        # -----------------------------------------------------

        filter_frame = tk.Frame(
            self.window,
            bg="#eef3f8"
        )

        filter_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        tk.Label(
            filter_frame,
            text="Search:",
            font=("Segoe UI", 10, "bold"),
            bg="#eef3f8",
            fg="#334155"
        ).pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            filter_frame,
            width=30,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.load_users()
        )

        tk.Label(
            filter_frame,
            text="Role:",
            font=("Segoe UI", 10, "bold"),
            bg="#eef3f8",
            fg="#334155"
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.role_filter = ttk.Combobox(
            filter_frame,
            values=[
                "ALL",
                "ADMIN",
                "MANAGER",
                "TECHNICIAN",
                "USER"
            ],
            state="readonly",
            width=15
        )

        self.role_filter.set("ALL")

        self.role_filter.pack(
            side="left"
        )

        self.role_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_users()
        )

        tk.Button(
            filter_frame,
            text="↻ Refresh",
            command=self.load_users,
            bg="#0f766e",
            fg="white",
            activebackground="#115e59",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=5
        ).pack(
            side="right"
        )

        # -----------------------------------------------------
        # TABLE
        # -----------------------------------------------------

        table_frame = tk.Frame(
            self.window,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Username",
            "Full Name",
            "Email",
            "Role",
            "Status"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        widths = {
            "ID": 60,
            "Username": 150,
            "Full Name": 190,
            "Email": 240,
            "Role": 130,
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
                anchor="center"
            )

        # -----------------------------------------------------
        # SCROLLBARS
        # -----------------------------------------------------

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        self.table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.grid_rowconfigure(
            0,
            weight=1
        )

        table_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # -----------------------------------------------------
        # ROW COLOURS
        # -----------------------------------------------------

        self.table.tag_configure(
            "ADMIN",
            background="#f3e8ff",
            foreground="#6b21a8"
        )

        self.table.tag_configure(
            "MANAGER",
            background="#dbeafe",
            foreground="#1e40af"
        )

        self.table.tag_configure(
            "TECHNICIAN",
            background="#ecfeff",
            foreground="#155e75"
        )

        self.table.tag_configure(
            "USER",
            background="#f8fafc",
            foreground="#334155"
        )

        # -----------------------------------------------------
        # DOUBLE CLICK
        # -----------------------------------------------------

        self.table.bind(
            "<Double-1>",
            lambda event: self.view_user()
        )

        # -----------------------------------------------------
        # BOTTOM BUTTONS
        # -----------------------------------------------------

        controls = tk.Frame(
            self.window,
            bg="#eef3f8"
        )

        controls.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        tk.Button(
            controls,
            text="View Details",
            command=self.view_user,
            bg="#475569",
            fg="white",
            activebackground="#334155",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="Edit User",
            command=self.edit_user,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="Reset Password",
            command=self.reset_password,
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="Activate",
            command=self.activate_user,
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="Deactivate",
            command=self.deactivate_user,
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="Delete",
            command=self.delete_user,
            bg="#991b1b",
            fg="white",
            activebackground="#7f1d1d",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            controls,
            text="Close",
            command=self.window.destroy,
            bg="#64748b",
            fg="white",
            activebackground="#475569",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8
        ).pack(
            side="right"
        )

    # =========================================================
    # SUMMARY CARD
    # =========================================================

    def create_card(self, parent, title, colour):

        card = tk.Frame(
            parent,
            bg=colour,
            height=75
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            bg=colour,
            fg="white"
        ).pack(
            pady=(10, 0)
        )

        value = tk.Label(
            card,
            text="0",
            font=("Segoe UI", 20, "bold"),
            bg=colour,
            fg="white"
        )

        value.pack()

        return value

    # =========================================================
    # ADD USER
    # =========================================================

    def add_user(self):

        username = self.username.get().strip()
        password = self.password.get()
        full_name = self.full_name.get().strip()
        email = self.email.get().strip()
        role = self.role.get()

        if not username or not password or not full_name:

            messagebox.showwarning(
                "Missing Information",
                "Username, password and full name are required."
            )

            return

        if len(password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )

            return

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            # Check duplicate username

            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE username=%s
                """,
                (username,)
            )

            if cursor.fetchone():

                messagebox.showwarning(
                    "Username Exists",
                    f"The username '{username}' already exists."
                )

                return

            password_hash = hash_password(
                password
            )

            cursor.execute(
                """
                INSERT INTO users
                (
                    username,
                    password_hash,
                    full_name,
                    email,
                    role,
                    status
                )
                VALUES (%s,%s,%s,%s,%s,'ACTIVE')
                """,
                (
                    username,
                    password_hash,
                    full_name,
                    email,
                    role
                )
            )

            connection.commit()

            messagebox.showinfo(
                "User Created",
                f"User '{username}' was created successfully."
            )

            self.clear_form()

            self.load_users()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # LOAD USERS
    # =========================================================

    def load_users(self):

        for item in self.table.get_children():
            self.table.delete(item)

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        search = self.search_entry.get().strip()

        selected_role = self.role_filter.get()

        try:

            query = """
                SELECT
                    user_id,
                    username,
                    full_name,
                    email,
                    role,
                    status
                FROM users
                WHERE 1=1
            """

            parameters = []

            if search:

                query += """
                    AND (
                        CAST(user_id AS CHAR) LIKE %s
                        OR username LIKE %s
                        OR full_name LIKE %s
                        OR email LIKE %s
                    )
                """

                search_value = f"%{search}%"

                parameters.extend([
                    search_value,
                    search_value,
                    search_value,
                    search_value
                ])

            if selected_role != "ALL":

                query += """
                    AND role=%s
                """

                parameters.append(
                    selected_role
                )

            query += """
                ORDER BY user_id DESC
            """

            cursor.execute(
                query,
                parameters
            )

            rows = cursor.fetchall()

            for row in rows:

                role = str(row[4]).upper()

                self.table.insert(
                    "",
                    tk.END,
                    values=row,
                    tags=(role,)
                )

            self.update_summary()

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # SUMMARY
    # =========================================================

    def update_summary(self):

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    COUNT(*),
                    SUM(status='ACTIVE'),
                    SUM(status='INACTIVE'),
                    SUM(role='ADMIN')
                FROM users
                """
            )

            row = cursor.fetchone()

            total = row[0] or 0
            active = row[1] or 0
            inactive = row[2] or 0
            admins = row[3] or 0

            self.total_label.config(
                text=str(total)
            )

            self.active_label.config(
                text=str(active)
            )

            self.inactive_label.config(
                text=str(inactive)
            )

            self.admin_label.config(
                text=str(admins)
            )

        except Exception as error:

            print(
                "Summary error:",
                error
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # GET SELECTED USER
    # =========================================================

    def get_selected_user(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select User",
                "Please select a user."
            )

            return None

        return self.table.item(
            selected[0]
        )["values"]

    # =========================================================
    # VIEW USER
    # =========================================================

    def view_user(self):

        user = self.get_selected_user()

        if not user:
            return

        details = tk.Toplevel(
            self.window
        )

        details.title(
            f"User Details - {user[1]}"
        )

        details.geometry(
            "500x430"
        )

        details.configure(
            bg="#f8fafc"
        )

        tk.Label(
            details,
            text="USER ACCOUNT DETAILS",
            font=("Segoe UI", 16, "bold"),
            bg="#172554",
            fg="white",
            pady=15
        ).pack(
            fill="x"
        )

        information = [
            ("User ID", user[0]),
            ("Username", user[1]),
            ("Full Name", user[2]),
            ("Email", user[3] or "Not provided"),
            ("Role", user[4]),
            ("Status", user[5])
        ]

        content = tk.Frame(
            details,
            bg="#f8fafc"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        for index, (label, value) in enumerate(information):

            tk.Label(
                content,
                text=f"{label}:",
                font=("Segoe UI", 10, "bold"),
                bg="#f8fafc",
                fg="#334155"
            ).grid(
                row=index,
                column=0,
                sticky="w",
                pady=8
            )

            tk.Label(
                content,
                text=str(value),
                font=("Segoe UI", 10),
                bg="#f8fafc",
                fg="#0f172a"
            ).grid(
                row=index,
                column=1,
                sticky="w",
                padx=25,
                pady=8
            )

        tk.Button(
            details,
            text="Close",
            command=details.destroy,
            bg="#172554",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=25,
            pady=8
        ).pack(
            pady=(0, 20)
        )

    # =========================================================
    # EDIT USER
    # =========================================================

    def edit_user(self):

        user = self.get_selected_user()

        if not user:
            return

        if self.current_user["role"] != "ADMIN":

            messagebox.showerror(
                "Permission Denied",
                "Only administrators can edit user accounts."
            )

            return

        user_id = user[0]

        edit = tk.Toplevel(
            self.window
        )

        edit.title(
            f"Edit User - {user[1]}"
        )

        edit.geometry(
            "480x400"
        )

        edit.configure(
            bg="#f8fafc"
        )

        tk.Label(
            edit,
            text="EDIT USER ACCOUNT",
            font=("Segoe UI", 16, "bold"),
            bg="#172554",
            fg="white",
            pady=15
        ).pack(
            fill="x"
        )

        form = tk.Frame(
            edit,
            bg="#f8fafc"
        )

        form.pack(
            padx=30,
            pady=25
        )

        tk.Label(
            form,
            text="Username",
            bg="#f8fafc",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=8
        )

        username_entry = tk.Entry(
            form,
            width=30,
            font=("Segoe UI", 10)
        )

        username_entry.insert(
            0,
            user[1]
        )

        username_entry.grid(
            row=0,
            column=1,
            padx=15
        )

        tk.Label(
            form,
            text="Full Name",
            bg="#f8fafc",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=8
        )

        full_name_entry = tk.Entry(
            form,
            width=30,
            font=("Segoe UI", 10)
        )

        full_name_entry.insert(
            0,
            user[2]
        )

        full_name_entry.grid(
            row=1,
            column=1,
            padx=15
        )

        tk.Label(
            form,
            text="Email",
            bg="#f8fafc",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=8
        )

        email_entry = tk.Entry(
            form,
            width=30,
            font=("Segoe UI", 10)
        )

        email_entry.insert(
            0,
            user[3] or ""
        )

        email_entry.grid(
            row=2,
            column=1,
            padx=15
        )

        tk.Label(
            form,
            text="Role",
            bg="#f8fafc",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=8
        )

        role_combo = ttk.Combobox(
            form,
            values=[
                "ADMIN",
                "MANAGER",
                "TECHNICIAN",
                "USER"
            ],
            state="readonly",
            width=28
        )

        role_combo.set(
            user[4]
        )

        role_combo.grid(
            row=3,
            column=1,
            padx=15
        )

        def save_changes():

            new_username = username_entry.get().strip()
            new_full_name = full_name_entry.get().strip()
            new_email = email_entry.get().strip()
            new_role = role_combo.get()

            if not new_username or not new_full_name:

                messagebox.showwarning(
                    "Missing Information",
                    "Username and full name are required."
                )

                return

            connection = get_connection()

            if not connection:
                return

            cursor = connection.cursor()

            try:

                cursor.execute(
                    """
                    UPDATE users
                    SET
                        username=%s,
                        full_name=%s,
                        email=%s,
                        role=%s
                    WHERE user_id=%s
                    """,
                    (
                        new_username,
                        new_full_name,
                        new_email,
                        new_role,
                        user_id
                    )
                )

                connection.commit()

                messagebox.showinfo(
                    "Updated",
                    "User account updated successfully."
                )

                edit.destroy()

                self.load_users()

            except Exception as error:

                connection.rollback()

                messagebox.showerror(
                    "Update Error",
                    str(error)
                )

            finally:

                cursor.close()
                connection.close()

        tk.Button(
            edit,
            text="Save Changes",
            command=save_changes,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=25,
            pady=8
        ).pack(
            pady=10
        )

    # =========================================================
    # RESET PASSWORD
    # =========================================================

    def reset_password(self):

        user = self.get_selected_user()

        if not user:
            return

        if self.current_user["role"] != "ADMIN":

            messagebox.showerror(
                "Permission Denied",
                "Only administrators can reset passwords."
            )

            return

        new_password = tk.simpledialog.askstring(
            "Reset Password",
            f"Enter new password for {user[1]}:",
            show="*"
        )

        if not new_password:
            return

        if len(new_password) < 6:

            messagebox.showwarning(
                "Weak Password",
                "Password must contain at least 6 characters."
            )

            return

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            password_hash = hash_password(
                new_password
            )

            cursor.execute(
                """
                UPDATE users
                SET password_hash=%s
                WHERE user_id=%s
                """,
                (
                    password_hash,
                    user[0]
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Password Reset",
                f"Password for '{user[1]}' has been reset."
            )

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Password Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # ACTIVATE USER
    # =========================================================

    def activate_user(self):

        user = self.get_selected_user()

        if not user:
            return

        if self.current_user["role"] != "ADMIN":

            messagebox.showerror(
                "Permission Denied",
                "Only administrators can activate users."
            )

            return

        self.change_status(
            user[0],
            "ACTIVE"
        )

    # =========================================================
    # DEACTIVATE USER
    # =========================================================

    def deactivate_user(self):

        user = self.get_selected_user()

        if not user:
            return

        if self.current_user["role"] != "ADMIN":

            messagebox.showerror(
                "Permission Denied",
                "Only administrators can deactivate users."
            )

            return

        # Prevent admin from accidentally disabling themselves

        if user[0] == self.current_user["user_id"]:

            messagebox.showwarning(
                "Action Not Allowed",
                "You cannot deactivate your own account."
            )

            return

        confirm = messagebox.askyesno(
            "Deactivate User",
            f"Deactivate user '{user[1]}'?"
        )

        if not confirm:
            return

        self.change_status(
            user[0],
            "INACTIVE"
        )

    # =========================================================
    # CHANGE STATUS
    # =========================================================

    def change_status(self, user_id, status):

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE users
                SET status=%s
                WHERE user_id=%s
                """,
                (
                    status,
                    user_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Account Updated",
                f"User status changed to {status}."
            )

            self.load_users()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Status Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # DELETE USER
    # =========================================================

    def delete_user(self):

        user = self.get_selected_user()

        if not user:
            return

        if self.current_user["role"] != "ADMIN":

            messagebox.showerror(
                "Permission Denied",
                "Only administrators can delete users."
            )

            return

        if user[0] == self.current_user["user_id"]:

            messagebox.showwarning(
                "Action Not Allowed",
                "You cannot delete your own account."
            )

            return

        confirm = messagebox.askyesno(
            "Delete User",
            f"Are you sure you want to permanently delete\n"
            f"user '{user[1]}'?"
        )

        if not confirm:
            return

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                DELETE FROM users
                WHERE user_id=%s
                """,
                (user[0],)
            )

            connection.commit()

            messagebox.showinfo(
                "User Deleted",
                f"User '{user[1]}' has been deleted."
            )

            self.load_users()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Delete Error",
                "Unable to delete this user.\n\n"
                f"{error}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.username.delete(
            0,
            tk.END
        )

        self.password.delete(
            0,
            tk.END
        )

        self.full_name.delete(
            0,
            tk.END
        )

        self.email.delete(
            0,
            tk.END
        )

        self.role.set(
            "USER"
        )

        self.username.focus()