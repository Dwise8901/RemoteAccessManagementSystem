import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress

from database import get_connection


class DevicesWindow:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)

        self.window.title("Device Management")

        self.window.geometry("1250x750")

        self.window.minsize(1050, 650)

        self.window.configure(
            bg="#eef3f8"
        )

        self.setup_styles()

        self.build_interface()

        self.load_devices()

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
            text="DEVICE MANAGEMENT",
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
            text="Remote Computers • Network Devices • System Status",
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
            "TOTAL DEVICES",
            "#2563eb"
        )

        self.online_label = self.create_card(
            summary,
            "ONLINE",
            "#16a34a"
        )

        self.offline_label = self.create_card(
            summary,
            "OFFLINE",
            "#64748b"
        )

        self.maintenance_label = self.create_card(
            summary,
            "MAINTENANCE",
            "#d97706"
        )

        # -----------------------------------------------------
        # DEVICE FORM
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
            text="  ADD / REGISTER DEVICE",
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
            pady=12
        )

        self.entries = {}

        fields = [
            ("Device Name", 0, 0),
            ("Hostname", 0, 2),
            ("IP Address", 1, 0),
            ("Operating System", 1, 2),
            ("Location", 2, 0)
        ]

        for label, row, column in fields:

            tk.Label(
                form,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg="white",
                fg="#334155"
            ).grid(
                row=row,
                column=column,
                padx=5,
                pady=6,
                sticky="w"
            )

            entry = tk.Entry(
                form,
                width=28,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )

            entry.grid(
                row=row,
                column=column + 1,
                padx=5,
                pady=6
            )

            self.entries[label] = entry

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        tk.Label(
            form,
            text="Status",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=2,
            column=2,
            padx=5,
            pady=6,
            sticky="w"
        )

        self.status = ttk.Combobox(
            form,
            values=[
                "ONLINE",
                "OFFLINE",
                "MAINTENANCE"
            ],
            state="readonly",
            width=25
        )

        self.status.set("OFFLINE")

        self.status.grid(
            row=2,
            column=3,
            padx=5,
            pady=6
        )

        # -----------------------------------------------------
        # ADD BUTTON
        # -----------------------------------------------------

        tk.Button(
            form,
            text="＋ Add Device",
            command=self.add_device,
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
            column=4,
            padx=15
        )

        # -----------------------------------------------------
        # CLEAR BUTTON
        # -----------------------------------------------------

        tk.Button(
            form,
            text="Clear",
            command=self.clear_form,
            bg="#e2e8f0",
            fg="#334155",
            activebackground="#cbd5e1",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7
        ).grid(
            row=2,
            column=5,
            padx=5
        )

        # -----------------------------------------------------
        # SEARCH AND FILTER
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
            width=35,
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
            lambda event: self.load_devices()
        )

        tk.Label(
            filter_frame,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            bg="#eef3f8",
            fg="#334155"
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.status_filter = ttk.Combobox(
            filter_frame,
            values=[
                "ALL",
                "ONLINE",
                "OFFLINE",
                "MAINTENANCE"
            ],
            state="readonly",
            width=16
        )

        self.status_filter.set("ALL")

        self.status_filter.pack(
            side="left"
        )

        self.status_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_devices()
        )

        tk.Button(
            filter_frame,
            text="↻ Refresh",
            command=self.load_devices,
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
        # DEVICE TABLE
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
            "Name",
            "Hostname",
            "IP",
            "OS",
            "Location",
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
            "Name": 180,
            "Hostname": 170,
            "IP": 140,
            "OS": 180,
            "Location": 150,
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
        # STATUS COLOURS
        # -----------------------------------------------------

        self.table.tag_configure(
            "ONLINE",
            background="#f0fdf4",
            foreground="#166534"
        )

        self.table.tag_configure(
            "OFFLINE",
            background="#f8fafc",
            foreground="#475569"
        )

        self.table.tag_configure(
            "MAINTENANCE",
            background="#fff7ed",
            foreground="#9a3412"
        )

        # -----------------------------------------------------
        # DOUBLE CLICK
        # -----------------------------------------------------

        self.table.bind(
            "<Double-1>",
            lambda event: self.view_device()
        )

        # -----------------------------------------------------
        # BOTTOM CONTROLS
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
            command=self.view_device,
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
            text="Edit Device",
            command=self.edit_device,
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
            text="Set Online",
            command=lambda: self.change_status("ONLINE"),
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
            text="Set Offline",
            command=lambda: self.change_status("OFFLINE"),
            bg="#64748b",
            fg="white",
            activebackground="#475569",
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
            text="Maintenance",
            command=lambda: self.change_status("MAINTENANCE"),
            bg="#d97706",
            fg="white",
            activebackground="#b45309",
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
            command=self.delete_device,
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
            text="Close",
            command=self.window.destroy,
            bg="#172554",
            fg="white",
            activebackground="#1e3a8a",
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
    # ADD DEVICE
    # =========================================================

    def add_device(self):

        device_name = self.entries[
            "Device Name"
        ].get().strip()

        hostname = self.entries[
            "Hostname"
        ].get().strip()

        ip_address = self.entries[
            "IP Address"
        ].get().strip()

        operating_system = self.entries[
            "Operating System"
        ].get().strip()

        location = self.entries[
            "Location"
        ].get().strip()

        status = self.status.get()

        if not device_name:

            messagebox.showwarning(
                "Required",
                "Device name is required."
            )

            return

        # -----------------------------------------------------
        # IP VALIDATION
        # -----------------------------------------------------

        if ip_address:

            try:
                ipaddress.ip_address(
                    ip_address
                )

            except ValueError:

                messagebox.showwarning(
                    "Invalid IP Address",
                    "Please enter a valid IPv4 or IPv6 address."
                )

                return

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            # -------------------------------------------------
            # DUPLICATE CHECK
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT device_id
                FROM devices
                WHERE device_name=%s
                """,
                (device_name,)
            )

            if cursor.fetchone():

                messagebox.showwarning(
                    "Duplicate Device",
                    f"A device named '{device_name}' already exists."
                )

                return

            # -------------------------------------------------
            # INSERT
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO devices
                (
                    device_name,
                    hostname,
                    ip_address,
                    operating_system,
                    location,
                    status
                )
                VALUES (%s,%s,%s,%s,%s,%s)
                """,
                (
                    device_name,
                    hostname,
                    ip_address,
                    operating_system,
                    location,
                    status
                )
            )

            connection.commit()

            device_id = cursor.lastrowid

            messagebox.showinfo(
                "Device Added",
                f"Device registered successfully.\n\n"
                f"Device ID: {device_id}\n"
                f"Device: {device_name}\n"
                f"Status: {status}"
            )

            self.clear_form()

            self.load_devices()

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
    # LOAD DEVICES
    # =========================================================

    def load_devices(self):

        for item in self.table.get_children():
            self.table.delete(item)

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        search = self.search_entry.get().strip()

        status_filter = self.status_filter.get()

        try:

            query = """
                SELECT
                    device_id,
                    device_name,
                    hostname,
                    ip_address,
                    operating_system,
                    location,
                    status
                FROM devices
                WHERE 1=1
            """

            parameters = []

            if search:

                query += """
                    AND (
                        CAST(device_id AS CHAR) LIKE %s
                        OR device_name LIKE %s
                        OR hostname LIKE %s
                        OR ip_address LIKE %s
                        OR operating_system LIKE %s
                        OR location LIKE %s
                    )
                """

                search_value = f"%{search}%"

                parameters.extend([
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value,
                    search_value
                ])

            if status_filter != "ALL":

                query += """
                    AND status=%s
                """

                parameters.append(
                    status_filter
                )

            query += """
                ORDER BY device_id DESC
            """

            cursor.execute(
                query,
                parameters
            )

            rows = cursor.fetchall()

            for row in rows:

                device_status = str(
                    row[6]
                ).upper()

                self.table.insert(
                    "",
                    tk.END,
                    values=row,
                    tags=(device_status,)
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
    # UPDATE SUMMARY
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
                    SUM(status='ONLINE'),
                    SUM(status='OFFLINE'),
                    SUM(status='MAINTENANCE')
                FROM devices
                """
            )

            row = cursor.fetchone()

            total = row[0] or 0
            online = row[1] or 0
            offline = row[2] or 0
            maintenance = row[3] or 0

            self.total_label.config(
                text=str(total)
            )

            self.online_label.config(
                text=str(online)
            )

            self.offline_label.config(
                text=str(offline)
            )

            self.maintenance_label.config(
                text=str(maintenance)
            )

        except Exception as error:

            print(
                "Device summary error:",
                error
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # GET SELECTED DEVICE
    # =========================================================

    def get_selected_device(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Device",
                "Please select a device."
            )

            return None

        return self.table.item(
            selected[0]
        )["values"]

    # =========================================================
    # VIEW DEVICE
    # =========================================================

    def view_device(self):

        device = self.get_selected_device()

        if not device:
            return

        details = tk.Toplevel(
            self.window
        )

        details.title(
            f"Device Details - {device[1]}"
        )

        details.geometry(
            "520x480"
        )

        details.configure(
            bg="#f8fafc"
        )

        tk.Label(
            details,
            text="DEVICE DETAILS",
            font=("Segoe UI", 16, "bold"),
            bg="#172554",
            fg="white",
            pady=15
        ).pack(
            fill="x"
        )

        information = [
            ("Device ID", device[0]),
            ("Device Name", device[1]),
            ("Hostname", device[2] or "Not provided"),
            ("IP Address", device[3] or "Not provided"),
            ("Operating System", device[4] or "Not provided"),
            ("Location", device[5] or "Not provided"),
            ("Status", device[6])
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
    # EDIT DEVICE
    # =========================================================

    def edit_device(self):

        device = self.get_selected_device()

        if not device:
            return

        if self.current_user["role"] not in (
            "ADMIN",
            "MANAGER"
        ):

            messagebox.showerror(
                "Permission Denied",
                "Only administrators or managers can edit devices."
            )

            return

        device_id = device[0]

        edit = tk.Toplevel(
            self.window
        )

        edit.title(
            f"Edit Device - {device[1]}"
        )

        edit.geometry(
            "500x500"
        )

        edit.configure(
            bg="#f8fafc"
        )

        tk.Label(
            edit,
            text="EDIT DEVICE",
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
            pady=20
        )

        edit_entries = {}

        fields = [
            ("Device Name", device[1]),
            ("Hostname", device[2] or ""),
            ("IP Address", device[3] or ""),
            ("Operating System", device[4] or ""),
            ("Location", device[5] or "")
        ]

        for index, (label, value) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg="#f8fafc",
                fg="#334155"
            ).grid(
                row=index,
                column=0,
                sticky="w",
                pady=8
            )

            entry = tk.Entry(
                form,
                width=30,
                font=("Segoe UI", 10)
            )

            entry.insert(
                0,
                value
            )

            entry.grid(
                row=index,
                column=1,
                padx=15
            )

            edit_entries[label] = entry

        # Status

        tk.Label(
            form,
            text="Status",
            font=("Segoe UI", 10, "bold"),
            bg="#f8fafc",
            fg="#334155"
        ).grid(
            row=5,
            column=0,
            sticky="w",
            pady=8
        )

        status_combo = ttk.Combobox(
            form,
            values=[
                "ONLINE",
                "OFFLINE",
                "MAINTENANCE"
            ],
            state="readonly",
            width=28
        )

        status_combo.set(
            device[6]
        )

        status_combo.grid(
            row=5,
            column=1,
            padx=15
        )

        # -----------------------------------------------------
        # SAVE
        # -----------------------------------------------------

        def save_changes():

            device_name = edit_entries[
                "Device Name"
            ].get().strip()

            hostname = edit_entries[
                "Hostname"
            ].get().strip()

            ip_address = edit_entries[
                "IP Address"
            ].get().strip()

            operating_system = edit_entries[
                "Operating System"
            ].get().strip()

            location = edit_entries[
                "Location"
            ].get().strip()

            new_status = status_combo.get()

            if not device_name:

                messagebox.showwarning(
                    "Required",
                    "Device name is required."
                )

                return

            if ip_address:

                try:

                    ipaddress.ip_address(
                        ip_address
                    )

                except ValueError:

                    messagebox.showwarning(
                        "Invalid IP",
                        "Please enter a valid IP address."
                    )

                    return

            connection = get_connection()

            if not connection:
                return

            cursor = connection.cursor()

            try:

                cursor.execute(
                    """
                    UPDATE devices
                    SET
                        device_name=%s,
                        hostname=%s,
                        ip_address=%s,
                        operating_system=%s,
                        location=%s,
                        status=%s
                    WHERE device_id=%s
                    """,
                    (
                        device_name,
                        hostname,
                        ip_address,
                        operating_system,
                        location,
                        new_status,
                        device_id
                    )
                )

                connection.commit()

                messagebox.showinfo(
                    "Updated",
                    "Device updated successfully."
                )

                edit.destroy()

                self.load_devices()

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
            activebackground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=25,
            pady=8
        ).pack(
            pady=10
        )

    # =========================================================
    # CHANGE DEVICE STATUS
    # =========================================================

    def change_status(self, new_status):

        device = self.get_selected_device()

        if not device:
            return

        if self.current_user["role"] not in (
            "ADMIN",
            "MANAGER"
        ):

            messagebox.showerror(
                "Permission Denied",
                "Only administrators or managers can change device status."
            )

            return

        if str(device[6]).upper() == new_status:

            messagebox.showinfo(
                "No Change",
                f"This device is already {new_status}."
            )

            return

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE devices
                SET status=%s
                WHERE device_id=%s
                """,
                (
                    new_status,
                    device[0]
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Status Updated",
                f"{device[1]} is now {new_status}."
            )

            self.load_devices()

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
    # DELETE DEVICE
    # =========================================================

    def delete_device(self):

        device = self.get_selected_device()

        if not device:
            return

        if self.current_user["role"] != "ADMIN":

            messagebox.showerror(
                "Permission Denied",
                "Only administrators can delete devices."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Device",
            f"Are you sure you want to delete\n"
            f"'{device[1]}'?"
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
                DELETE FROM devices
                WHERE device_id=%s
                """,
                (device[0],)
            )

            connection.commit()

            messagebox.showinfo(
                "Device Deleted",
                f"Device '{device[1]}' has been deleted."
            )

            self.load_devices()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Delete Error",
                "Unable to delete this device.\n\n"
                f"{error}"
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        for entry in self.entries.values():

            entry.delete(
                0,
                tk.END
            )

        self.status.set(
            "OFFLINE"
        )

        self.entries[
            "Device Name"
        ].focus()