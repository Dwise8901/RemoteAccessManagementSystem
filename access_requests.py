import tkinter as tk
from tkinter import ttk, messagebox

from database import get_connection


class AccessRequestsWindow:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Remote Access Request Management")
        self.window.geometry("1250x750")
        self.window.minsize(1050, 650)
        self.window.configure(bg="#eef3f8")

        self.setup_styles()
        self.build_interface()

        self.load_devices()
        self.load_requests()

    # =========================================================
    # COLOURS / STYLES
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

        title = tk.Label(
            header,
            text="REMOTE ACCESS REQUESTS",
            font=("Segoe UI", 20, "bold"),
            bg="#172554",
            fg="white"
        )

        title.pack(
            side="left",
            padx=25,
            pady=20
        )

        subtitle = tk.Label(
            header,
            text="Access Authorization & Request Management",
            font=("Segoe UI", 10),
            bg="#172554",
            fg="#bfdbfe"
        )

        subtitle.pack(
            side="left",
            pady=22
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
            "TOTAL REQUESTS",
            "#1d4ed8"
        )

        self.pending_label = self.create_card(
            summary,
            "PENDING",
            "#d97706"
        )

        self.approved_label = self.create_card(
            summary,
            "APPROVED",
            "#15803d"
        )

        self.rejected_label = self.create_card(
            summary,
            "REJECTED",
            "#dc2626"
        )

        # -----------------------------------------------------
        # REQUEST FORM
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

        form_title = tk.Label(
            form_container,
            text="  CREATE ACCESS REQUEST",
            font=("Segoe UI", 12, "bold"),
            bg="#2563eb",
            fg="white",
            anchor="w"
        )

        form_title.pack(
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

        # Device

        tk.Label(
            form,
            text="Device",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=0,
            column=0,
            padx=(5, 8),
            pady=5,
            sticky="w"
        )

        self.device = ttk.Combobox(
            form,
            width=35,
            state="readonly"
        )

        self.device.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # Reason

        tk.Label(
            form,
            text="Reason",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#334155"
        ).grid(
            row=0,
            column=2,
            padx=(25, 8),
            pady=5,
            sticky="w"
        )

        self.reason = tk.Entry(
            form,
            width=42,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        self.reason.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # Request button

        tk.Button(
            form,
            text="  REQUEST ACCESS  ",
            command=self.request_access,
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=8
        ).grid(
            row=0,
            column=4,
            padx=15
        )

        # Clear button

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
            pady=8
        ).grid(
            row=0,
            column=5,
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
            text="Search Requests:",
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
            lambda event: self.load_requests()
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
                "PENDING",
                "APPROVED",
                "REJECTED"
            ],
            state="readonly",
            width=15
        )

        self.status_filter.set("ALL")

        self.status_filter.pack(
            side="left"
        )

        self.status_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.load_requests()
        )

        tk.Button(
            filter_frame,
            text="↻ Refresh",
            command=self.load_requests,
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
            "Requester",
            "Device",
            "Reason",
            "Requested",
            "Status",
            "Approved By"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        widths = {
            "ID": 60,
            "Requester": 130,
            "Device": 180,
            "Reason": 250,
            "Requested": 150,
            "Status": 110,
            "Approved By": 130
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

        # Scrollbars

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
            "PENDING",
            background="#fff7ed",
            foreground="#9a3412"
        )

        self.table.tag_configure(
            "APPROVED",
            background="#f0fdf4",
            foreground="#166534"
        )

        self.table.tag_configure(
            "REJECTED",
            background="#fef2f2",
            foreground="#991b1b"
        )

        # Double click

        self.table.bind(
            "<Double-1>",
            lambda event: self.view_request()
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

        # View

        tk.Button(
            controls,
            text="View Details",
            command=self.view_request,
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

        # Approve

        self.approve_button = tk.Button(
            controls,
            text="Approve Selected",
            command=self.approve_request,
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        self.approve_button.pack(
            side="left",
            padx=5
        )

        # Reject

        self.reject_button = tk.Button(
            controls,
            text="Reject Selected",
            command=self.reject_request,
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )

        self.reject_button.pack(
            side="left",
            padx=5
        )

        # Cancel

        tk.Button(
            controls,
            text="Cancel My Request",
            command=self.cancel_request,
            bg="#ea580c",
            fg="white",
            activebackground="#c2410c",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="left",
            padx=5
        )

        # Close

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
    # LOAD DEVICES
    # =========================================================

    def load_devices(self):

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT device_id, device_name
                FROM devices
                ORDER BY device_name
                """
            )

            rows = cursor.fetchall()

            self.device_map = {
                name: device_id
                for device_id, name in rows
            }

            self.device["values"] = list(
                self.device_map.keys()
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # REQUEST ACCESS
    # =========================================================

    def request_access(self):

        selected_device = self.device.get()
        reason = self.reason.get().strip()

        if not selected_device:

            messagebox.showwarning(
                "Device Required",
                "Please select a device."
            )

            return

        if not reason:

            messagebox.showwarning(
                "Reason Required",
                "Please enter a reason for requesting remote access."
            )

            return

        if len(reason) < 5:

            messagebox.showwarning(
                "Invalid Reason",
                "Please provide a more descriptive reason."
            )

            return

        device_id = self.device_map[selected_device]

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        try:

            # Prevent duplicate pending requests

            cursor.execute(
                """
                SELECT request_id
                FROM access_requests
                WHERE requester_id=%s
                AND device_id=%s
                AND status='PENDING'
                """,
                (
                    self.current_user["user_id"],
                    device_id
                )
            )

            existing = cursor.fetchone()

            if existing:

                messagebox.showwarning(
                    "Request Already Exists",
                    f"You already have a pending request for this device.\n\n"
                    f"Request ID: {existing[0]}"
                )

                return

            cursor.execute(
                """
                INSERT INTO access_requests
                (
                    requester_id,
                    device_id,
                    reason,
                    status
                )
                VALUES (%s,%s,%s,'PENDING')
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
                "Request Submitted",
                f"Remote access request submitted successfully.\n\n"
                f"Request ID: {request_id}\n"
                f"Device: {selected_device}\n"
                f"Status: PENDING"
            )

            self.clear_form()
            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Request Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # LOAD REQUESTS
    # =========================================================

    def load_requests(self):

        for item in self.table.get_children():
            self.table.delete(item)

        connection = get_connection()

        if not connection:
            return

        cursor = connection.cursor()

        search = self.search_entry.get().strip()

        status = self.status_filter.get()

        try:

            query = """
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
                WHERE 1=1
            """

            parameters = []

            # Search

            if search:

                query += """
                    AND (
                        CAST(ar.request_id AS CHAR) LIKE %s
                        OR u.username LIKE %s
                        OR d.device_name LIKE %s
                        OR ar.reason LIKE %s
                    )
                """

                search_value = f"%{search}%"

                parameters.extend([
                    search_value,
                    search_value,
                    search_value,
                    search_value
                ])

            # Status filter

            if status != "ALL":

                query += """
                    AND ar.status=%s
                """

                parameters.append(status)

            query += """
                ORDER BY ar.request_id DESC
            """

            cursor.execute(
                query,
                parameters
            )

            rows = cursor.fetchall()

            for row in rows:

                request_status = str(row[5]).upper()

                self.table.insert(
                    "",
                    tk.END,
                    values=row,
                    tags=(request_status,)
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
                    SUM(status='PENDING'),
                    SUM(status='APPROVED'),
                    SUM(status='REJECTED')
                FROM access_requests
                """
            )

            row = cursor.fetchone()

            total = row[0] or 0
            pending = row[1] or 0
            approved = row[2] or 0
            rejected = row[3] or 0

            self.total_label.config(
                text=str(total)
            )

            self.pending_label.config(
                text=str(pending)
            )

            self.approved_label.config(
                text=str(approved)
            )

            self.rejected_label.config(
                text=str(rejected)
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
    # GET SELECTED REQUEST
    # =========================================================

    def get_selected_request(self):

        selected = self.table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Request",
                "Please select an access request."
            )

            return None

        values = self.table.item(
            selected[0]
        )["values"]

        return values

    # =========================================================
    # VIEW REQUEST
    # =========================================================

    def view_request(self):

        request = self.get_selected_request()

        if not request:
            return

        details = tk.Toplevel(
            self.window
        )

        details.title(
            f"Access Request #{request[0]}"
        )

        details.geometry(
            "500x430"
        )

        details.configure(
            bg="#f8fafc"
        )

        tk.Label(
            details,
            text="ACCESS REQUEST DETAILS",
            font=("Segoe UI", 16, "bold"),
            bg="#172554",
            fg="white",
            pady=15
        ).pack(
            fill="x"
        )

        information = [
            ("Request ID", request[0]),
            ("Requester", request[1]),
            ("Device", request[2]),
            ("Reason", request[3]),
            ("Requested At", request[4]),
            ("Status", request[5]),
            ("Approved / Rejected By", request[6] or "Not yet processed")
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
                fg="#334155",
                anchor="w"
            ).grid(
                row=index,
                column=0,
                sticky="w",
                pady=8
            )

            value_label = tk.Label(
                content,
                text=str(value),
                font=("Segoe UI", 10),
                bg="#f8fafc",
                fg="#0f172a",
                anchor="w",
                wraplength=280,
                justify="left"
            )

            value_label.grid(
                row=index,
                column=1,
                sticky="w",
                padx=20,
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
    # APPROVE REQUEST
    # =========================================================

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
        status = str(request[5]).upper()

        if status != "PENDING":

            messagebox.showwarning(
                "Already Processed",
                "Only pending requests can be approved."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Approval",
            f"Approve access request #{request_id}?"
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

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Updated",
                    "The request has already been processed."
                )

            else:

                messagebox.showinfo(
                    "Request Approved",
                    f"Access request #{request_id} has been approved."
                )

            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Approval Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # REJECT REQUEST
    # =========================================================

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
        status = str(request[5]).upper()

        if status != "PENDING":

            messagebox.showwarning(
                "Already Processed",
                "Only pending requests can be rejected."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm Rejection",
            f"Reject access request #{request_id}?"
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

            if cursor.rowcount == 0:

                messagebox.showwarning(
                    "Not Updated",
                    "The request has already been processed."
                )

            else:

                messagebox.showinfo(
                    "Request Rejected",
                    f"Access request #{request_id} has been rejected."
                )

            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Rejection Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # CANCEL REQUEST
    # =========================================================

    def cancel_request(self):

        request = self.get_selected_request()

        if not request:
            return

        request_id = request[0]
        requester = request[1]
        status = str(request[5]).upper()

        if requester != self.current_user["username"]:

            messagebox.showerror(
                "Permission Denied",
                "You can only cancel your own requests."
            )

            return

        if status != "PENDING":

            messagebox.showwarning(
                "Cannot Cancel",
                "Only pending requests can be cancelled."
            )

            return

        confirm = messagebox.askyesno(
            "Cancel Request",
            f"Cancel access request #{request_id}?"
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
                UPDATE access_requests
                SET
                    status='REJECTED'
                WHERE request_id=%s
                AND requester_id=%s
                AND status='PENDING'
                """,
                (
                    request_id,
                    self.current_user["user_id"]
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Request Cancelled",
                f"Access request #{request_id} has been cancelled."
            )

            self.load_requests()

        except Exception as error:

            connection.rollback()

            messagebox.showerror(
                "Cancel Error",
                str(error)
            )

        finally:

            cursor.close()
            connection.close()

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.device.set("")

        self.reason.delete(
            0,
            tk.END
        )

        self.reason.focus()