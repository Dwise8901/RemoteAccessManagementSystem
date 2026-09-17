import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class DevicesWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)

        self.window.title("Device Management")

        self.window.geometry("1100x650")

        self.build_interface()

        self.load_devices()

    def build_interface(self):

        tk.Label(
            self.window,
            text="DEVICE MANAGEMENT",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(
            fill="x",
            padx=20
        )

        labels = [
            "Device Name",
            "Hostname",
            "IP Address",
            "Operating System",
            "Location"
        ]

        self.entries = {}

        for index, label in enumerate(labels):

            tk.Label(
                form,
                text=label
            ).grid(
                row=index // 2,
                column=(index % 2) * 2,
                padx=5,
                pady=8,
                sticky="e"
            )

            entry = tk.Entry(
                form,
                width=30
            )

            entry.grid(
                row=index // 2,
                column=(index % 2) * 2 + 1,
                padx=5
            )

            self.entries[label] = entry

        tk.Label(
            form,
            text="Status"
        ).grid(
            row=3,
            column=0
        )

        self.status = ttk.Combobox(
            form,
            values=[
                "ONLINE",
                "OFFLINE",
                "MAINTENANCE"
            ],
            state="readonly"
        )

        self.status.set("OFFLINE")

        self.status.grid(
            row=3,
            column=1
        )

        tk.Button(
            form,
            text="Add Device",
            command=self.add_device
        ).grid(
            row=3,
            column=3,
            pady=15
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
            self.window,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=130
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

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

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

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

            messagebox.showinfo(
                "Success",
                "Device added successfully."
            )

            for entry in self.entries.values():
                entry.delete(0, tk.END)

            self.load_devices()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    def load_devices(self):

        for item in self.table.get_children():

            self.table.delete(item)

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                device_id,
                device_name,
                hostname,
                ip_address,
                operating_system,
                location,
                status
            FROM devices
            ORDER BY device_id DESC
            """
        )

        for row in cursor.fetchall():

            self.table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()
        connection.close()