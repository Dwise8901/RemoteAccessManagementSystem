import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class AccessRequestsWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)

        self.window.title("Access Requests")

        self.window.geometry("1150x650")

        self.build_interface()

        self.load_devices()

        self.load_requests()

    def build_interface(self):

        tk.Label(
            self.window,
            text="REMOTE ACCESS REQUESTS",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15)

        form = tk.Frame(self.window)

        form.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            form,
            text="Device"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.device = ttk.Combobox(
            form,
            width=40,
            state="readonly"
        )

        self.device.grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Label(
            form,
            text="Reason"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=10
        )

        self.reason = tk.Entry(
            form,
            width=50
        )

        self.reason.grid(
            row=1,
            column=1
        )

        tk.Button(
            form,
            text="Request Access",
            command=self.request_access
        ).grid(
            row=1,
            column=2,
            padx=10
        )

        columns = (
            "ID",
            "Requester",
            "Device",
            "Reason",
            "Requested",
            "Status",
            "Approved By"
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
                width=140
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        controls = tk.Frame(
            self.window
        )

        controls.pack(
            pady=10
        )

        tk.Button(
            controls,
            text="Approve Selected",
            command=self.approve_request
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            controls,
            text="Reject Selected",
            command=self.reject_request
        ).pack(
            side="left",
            padx=10
        )

    def load_devices(self):

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT device_id, device_name
            FROM devices
            ORDER BY device_name
            """
        )

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        self.device_map = {
            name: device_id
            for device_id, name in rows
        }

        self.device["values"] = list(
            self.device_map.keys()
        )

    def request_access(self):

        selected_device = self.device.get()

        reason = self.reason.get().strip()

        if not selected_device or not reason:

            messagebox.showwarning(
                "Required",
                "Select a device and enter a reason."
            )

            return

        device_id = self.device_map[
            selected_device
        ]

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO access_requests
                (
                    requester_id,
                    device_id,
                    reason
                )
                VALUES (%s,%s,%s)
                """,
                (
                    self.current_user["user_id"],
                    device_id,
                    reason
                )
            )

            connection.commit()

            request_id = cursor.lastrowid

            messagebox.showinfo(
                "Success",
                f"Access request submitted successfully.\n\n"
                f"Request ID: {request_id}"
            )

            self.reason.delete(
                0,
                tk.END
            )

            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()


    def load_requests(self):

        for item in self.table.get_children():

            self.table.delete(item)

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                ar.request_id,
                u.username,
                d.device_name,
                ar.reason,
                ar.requested_at,
                ar.status,
                COALESCE(a.username, '')
            FROM access_requests ar
            JOIN users u
                ON ar.requester_id = u.user_id
            JOIN devices d
                ON ar.device_id = d.device_id
            LEFT JOIN users a
                ON ar.approved_by = a.user_id
            ORDER BY ar.request_id DESC
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

    def get_selected_request(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Request",
                "Select an access request."
            )

            return None

        values = self.table.item(
            selected[0]
        )["values"]

        return values

    def approve_request(self):

        if self.current_user["role"] not in (
            "ADMIN",
            "MANAGER"
        ):

            messagebox.showerror(
                "Permission Denied",
                "Only administrators or managers can approve requests."
            )

            return

        request = self.get_selected_request()

        if not request:
            return

        request_id = request[0]

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE access_requests
                SET
                    status='APPROVED',
                    approved_by=%s,
                    approved_at=NOW()
                WHERE request_id=%s
                AND status='PENDING'
                """,
                (
                    self.current_user["user_id"],
                    request_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Approved",
                "Access request approved."
            )

            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    def reject_request(self):

        if self.current_user["role"] not in (
            "ADMIN",
            "MANAGER"
        ):

            messagebox.showerror(
                "Permission Denied",
                "Only administrators or managers can reject requests."
            )

            return

        request = self.get_selected_request()

        if not request:
            return

        request_id = request[0]

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                UPDATE access_requests
                SET
                    status='REJECTED',
                    approved_by=%s,
                    approved_at=NOW()
                WHERE request_id=%s
                AND status='PENDING'
                """,
                (
                    self.current_user["user_id"],
                    request_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Rejected",
                "Access request rejected."
            )

            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()