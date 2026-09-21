import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

from database import get_connection


class AuditLogsWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Audit Logs - Virtual System Access Control")
        self.window.geometry("1250x720")
        self.window.minsize(1050, 650)
        self.window.configure(bg="#f1f5f9")

        self.build_interface()
        self.load_logs()

    # ==========================================================
    # INTERFACE
    # ==========================================================

    def build_interface(self):

        # ------------------------------------------------------
        # COLORS
        # ------------------------------------------------------

        self.colors = {
            "navy": "#172554",
            "blue": "#2563eb",
            "light_blue": "#dbeafe",
            "cyan": "#0891b2",
            "green": "#16a34a",
            "light_green": "#dcfce7",
            "orange": "#ea580c",
            "light_orange": "#ffedd5",
            "red": "#dc2626",
            "light_red": "#fee2e2",
            "purple": "#7c3aed",
            "light_purple": "#ede9fe",
            "white": "#ffffff",
            "background": "#f1f5f9",
            "text": "#0f172a",
            "muted": "#64748b",
            "border": "#cbd5e1"
        }

        # ------------------------------------------------------
        # STYLE
        # ------------------------------------------------------

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Audit.Treeview",
            background="white",
            foreground="#0f172a",
            rowheight=38,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Audit.Treeview.Heading",
            background="#172554",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Audit.Treeview",
            background=[
                ("selected", "#bfdbfe")
            ],
            foreground=[
                ("selected", "#172554")
            ]
        )

        style.configure(
            "Audit.TCombobox",
            padding=7,
            font=("Segoe UI", 10)
        )

        # ------------------------------------------------------
        # HEADER
        # ------------------------------------------------------

        header = tk.Frame(
            self.window,
            bg=self.colors["navy"],
            height=90
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        icon = tk.Label(
            header,
            text="◉",
            font=("Segoe UI", 28, "bold"),
            fg="#60a5fa",
            bg=self.colors["navy"]
        )

        icon.pack(
            side="left",
            padx=(25, 10)
        )

        title_frame = tk.Frame(
            header,
            bg=self.colors["navy"]
        )

        title_frame.pack(
            side="left",
            pady=15
        )

        tk.Label(
            title_frame,
            text="AUDIT LOGS",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=self.colors["navy"]
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="Monitor and review system operations",
            font=("Segoe UI", 10),
            fg="#bfdbfe",
            bg=self.colors["navy"]
        ).pack(
            anchor="w"
        )

        # ------------------------------------------------------
        # SUMMARY CARDS
        # ------------------------------------------------------

        summary_frame = tk.Frame(
            self.window,
            bg=self.colors["background"]
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        self.total_value = self.create_summary_card(
            summary_frame,
            "TOTAL OPERATIONS",
            "0",
            self.colors["blue"],
            self.colors["light_blue"]
        )

        self.users_value = self.create_summary_card(
            summary_frame,
            "USERS INVOLVED",
            "0",
            self.colors["purple"],
            self.colors["light_purple"]
        )

        self.access_value = self.create_summary_card(
            summary_frame,
            "ACCESS / LOGIN",
            "0",
            self.colors["green"],
            self.colors["light_green"]
        )

        self.other_value = self.create_summary_card(
            summary_frame,
            "OTHER OPERATIONS",
            "0",
            self.colors["orange"],
            self.colors["light_orange"]
        )

        # ------------------------------------------------------
        # SEARCH / FILTER AREA
        # ------------------------------------------------------

        control_card = tk.Frame(
            self.window,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        control_card.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            control_card,
            text="Search:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.colors["text"]
        ).pack(
            side="left",
            padx=(15, 5),
            pady=12
        )

        self.search_entry = tk.Entry(
            control_card,
            font=("Segoe UI", 10),
            bg="#f8fafc",
            fg=self.colors["text"],
            relief="flat",
            width=32
        )

        self.search_entry.pack(
            side="left",
            ipady=7,
            padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        tk.Label(
            control_card,
            text="Operation:",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg=self.colors["text"]
        ).pack(
            side="left",
            padx=(20, 5)
        )

        self.action_filter = ttk.Combobox(
            control_card,
            values=[
                "ALL",
                "LOGIN",
                "LOGOUT",
                "CREATE",
                "UPDATE",
                "DELETE",
                "ACCESS",
                "APPROVE",
                "REJECT",
                "OTHER"
            ],
            state="readonly",
            width=15,
            style="Audit.TCombobox"
        )

        self.action_filter.set("ALL")

        self.action_filter.pack(
            side="left",
            padx=5
        )

        self.action_filter.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        # Refresh button
        tk.Button(
            control_card,
            text="↻ Refresh",
            command=self.load_logs,
            bg=self.colors["blue"],
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=8,
            pady=7
        )

        # Report button
        tk.Button(
            control_card,
            text="▣ Operation Report",
            command=self.show_operation_report,
            bg=self.colors["purple"],
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=5,
            pady=7
        )

        # Export button
        tk.Button(
            control_card,
            text="↓ Export CSV",
            command=self.export_csv,
            bg=self.colors["green"],
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(
            side="right",
            padx=5,
            pady=7
        )

        # ------------------------------------------------------
        # TABLE
        # ------------------------------------------------------

        table_card = tk.Frame(
            self.window,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "User",
            "Action",
            "Description",
            "IP Address",
            "Created"
        )

        table_container = tk.Frame(
            table_card,
            bg="white"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="Audit.Treeview",
            selectmode="browse"
        )

        column_widths = {
            "ID": 70,
            "User": 130,
            "Action": 120,
            "Description": 390,
            "IP Address": 140,
            "Created": 180
        }

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                width=column_widths[column],
                minwidth=70,
                anchor="center"
            )

        # Scrollbars
        vertical_scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.table.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_container,
            orient="horizontal",
            command=self.table.xview
        )

        self.table.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.table.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_container.grid_rowconfigure(
            0,
            weight=1
        )

        table_container.grid_columnconfigure(
            0,
            weight=1
        )

        # ------------------------------------------------------
        # ROW COLORS
        # ------------------------------------------------------

        self.table.tag_configure(
            "login",
            background="#ecfdf5",
            foreground="#166534"
        )

        self.table.tag_configure(
            "logout",
            background="#f1f5f9",
            foreground="#475569"
        )

        self.table.tag_configure(
            "create",
            background="#eff6ff",
            foreground="#1d4ed8"
        )

        self.table.tag_configure(
            "update",
            background="#fff7ed",
            foreground="#c2410c"
        )

        self.table.tag_configure(
            "delete",
            background="#fef2f2",
            foreground="#b91c1c"
        )

        self.table.tag_configure(
            "access",
            background="#f0fdfa",
            foreground="#0f766e"
        )

        self.table.tag_configure(
            "approve",
            background="#f0fdf4",
            foreground="#15803d"
        )

        self.table.tag_configure(
            "reject",
            background="#fff1f2",
            foreground="#be123c"
        )

        self.table.tag_configure(
            "other",
            background="#f8fafc",
            foreground="#334155"
        )

        # Double click for details
        self.table.bind(
            "<Double-1>",
            self.show_selected_operation
        )

        # ------------------------------------------------------
        # FOOTER
        # ------------------------------------------------------

        footer = tk.Frame(
            self.window,
            bg=self.colors["navy"],
            height=35
        )

        footer.pack(
            fill="x"
        )

        footer.pack_propagate(False)

        self.footer_label = tk.Label(
            footer,
            text="Audit monitoring active",
            font=("Segoe UI", 9),
            fg="#bfdbfe",
            bg=self.colors["navy"]
        )

        self.footer_label.pack(
            side="left",
            padx=20
        )

        tk.Button(
            footer,
            text="Close",
            command=self.window.destroy,
            bg="#334155",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15
        ).pack(
            side="right",
            padx=15,
            pady=5
        )

    # ==========================================================
    # SUMMARY CARD
    # ==========================================================

    def create_summary_card(
        self,
        parent,
        title,
        value,
        color,
        light_color
    ):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )

        indicator = tk.Frame(
            card,
            bg=color,
            width=6
        )

        indicator.pack(
            side="left",
            fill="y"
        )

        content = tk.Frame(
            card,
            bg="white"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        tk.Label(
            content,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg=self.colors["muted"],
            bg="white"
        ).pack(
            anchor="w"
        )

        value_label = tk.Label(
            content,
            text=value,
            font=("Segoe UI", 20, "bold"),
            fg=color,
            bg="white"
        )

        value_label.pack(
            anchor="w"
        )

        return value_label

    # ==========================================================
    # LOAD LOGS
    # ==========================================================

    def load_logs(self):

        connection = get_connection()

        if not connection:

            messagebox.showerror(
                "Database Error",
                "Could not connect to the database.",
                parent=self.window
            )

            return

        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                SELECT
                    al.log_id,
                    COALESCE(u.username, ''),
                    al.action,
                    COALESCE(al.description, ''),
                    COALESCE(al.ip_address, ''),
                    al.created_at
                FROM audit_logs al
                LEFT JOIN users u
                    ON al.user_id = u.user_id
                ORDER BY al.log_id DESC
                """
            )

            self.all_rows = cursor.fetchall()

            self.apply_filters()

            self.update_statistics()

            self.footer_label.config(
                text=f"{len(self.all_rows)} audit operation(s) recorded"
            )

        except Exception as error:

            messagebox.showerror(
                "Error Loading Audit Logs",
                str(error),
                parent=self.window
            )

        finally:

            cursor.close()
            connection.close()

    # ==========================================================
    # FILTER
    # ==========================================================

    def apply_filters(self):

        if not hasattr(self, "all_rows"):
            return

        search_text = self.search_entry.get().strip().lower()

        selected_action = self.action_filter.get().upper()

        # Clear table
        for item in self.table.get_children():
            self.table.delete(item)

        displayed_rows = []

        for row in self.all_rows:

            user = str(row[1] or "").lower()
            action = str(row[2] or "").upper()
            description = str(row[3] or "").lower()
            ip_address = str(row[4] or "").lower()

            searchable_text = (
                user
                + " "
                + action
                + " "
                + description
                + " "
                + ip_address
            )

            # Search
            if search_text and search_text not in searchable_text:
                continue

            # Action filter
            if selected_action != "ALL":

                if selected_action == "OTHER":

                    known_actions = [
                        "LOGIN",
                        "LOGOUT",
                        "CREATE",
                        "UPDATE",
                        "DELETE",
                        "ACCESS",
                        "APPROVE",
                        "REJECT"
                    ]

                    if action in known_actions:
                        continue

                elif action != selected_action:
                    continue

            displayed_rows.append(row)

            tag = self.get_action_tag(action)

            self.table.insert(
                "",
                tk.END,
                values=row,
                tags=(tag,)
            )

        self.footer_label.config(
            text=f"Showing {len(displayed_rows)} of {len(self.all_rows)} operation(s)"
        )

    # ==========================================================
    # ACTION COLOR
    # ==========================================================

    def get_action_tag(self, action):

        action = str(action).upper()

        if "LOGIN" in action:
            return "login"

        if "LOGOUT" in action:
            return "logout"

        if "CREATE" in action or "ADD" in action:
            return "create"

        if "UPDATE" in action or "EDIT" in action:
            return "update"

        if "DELETE" in action or "REMOVE" in action:
            return "delete"

        if "ACCESS" in action or "SESSION" in action:
            return "access"

        if "APPROVE" in action:
            return "approve"

        if "REJECT" in action or "DENY" in action:
            return "reject"

        return "other"

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def update_statistics(self):

        total = len(self.all_rows)

        users = set()

        access_count = 0
        other_count = 0

        known_actions = [
            "LOGIN",
            "LOGOUT",
            "ACCESS",
            "SESSION",
            "APPROVE",
            "REJECT"
        ]

        for row in self.all_rows:

            username = str(row[1] or "").strip()

            action = str(row[2] or "").upper()

            if username:
                users.add(username)

            if any(word in action for word in known_actions):
                access_count += 1
            else:
                other_count += 1

        self.total_value.config(
            text=str(total)
        )

        self.users_value.config(
            text=str(len(users))
        )

        self.access_value.config(
            text=str(access_count)
        )

        self.other_value.config(
            text=str(other_count)
        )

    # ==========================================================
    # OPERATION REPORT
    # ==========================================================

    def show_operation_report(self):

        if not hasattr(self, "all_rows") or not self.all_rows:

            messagebox.showinfo(
                "Operation Report",
                "There are currently no audit operations to report.",
                parent=self.window
            )

            return

        report_window = tk.Toplevel(self.window)

        report_window.title(
            "System Operation Report"
        )

        report_window.geometry(
            "750x600"
        )

        report_window.configure(
            bg="#f1f5f9"
        )

        # Header
        header = tk.Frame(
            report_window,
            bg="#172554",
            height=85
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="SYSTEM OPERATION REPORT",
            font=("Segoe UI", 19, "bold"),
            fg="white",
            bg="#172554"
        ).pack(
            pady=(14, 0)
        )

        tk.Label(
            header,
            text="Virtual System Access Control",
            font=("Segoe UI", 10),
            fg="#bfdbfe",
            bg="#172554"
        ).pack()

        # Report body
        body = tk.Frame(
            report_window,
            bg="#f1f5f9"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        # Calculate operation statistics
        action_counts = {}

        users = set()

        for row in self.all_rows:

            action = str(row[2] or "UNKNOWN").upper()

            action_counts[action] = (
                action_counts.get(action, 0) + 1
            )

            username = str(row[1] or "").strip()

            if username:
                users.add(username)

        # Summary
        summary = tk.Frame(
            body,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )

        summary.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            summary,
            text=f"Total Operations: {len(self.all_rows)}",
            font=("Segoe UI", 12, "bold"),
            fg="#2563eb",
            bg="white"
        ).pack(
            side="left",
            padx=20,
            pady=15
        )

        tk.Label(
            summary,
            text=f"Users Involved: {len(users)}",
            font=("Segoe UI", 12, "bold"),
            fg="#7c3aed",
            bg="white"
        ).pack(
            side="left",
            padx=20
        )

        # Operations table
        report_table = ttk.Treeview(
            body,
            columns=("Operation", "Count", "Percentage"),
            show="headings",
            height=12
        )

        report_table.heading(
            "Operation",
            text="Operation"
        )

        report_table.heading(
            "Count",
            text="Number of Operations"
        )

        report_table.heading(
            "Percentage",
            text="Percentage"
        )

        report_table.column(
            "Operation",
            width=250,
            anchor="center"
        )

        report_table.column(
            "Count",
            width=200,
            anchor="center"
        )

        report_table.column(
            "Percentage",
            width=180,
            anchor="center"
        )

        report_table.pack(
            fill="both",
            expand=True
        )

        total = len(self.all_rows)

        for action, count in sorted(
            action_counts.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            percentage = (count / total) * 100

            report_table.insert(
                "",
                tk.END,
                values=(
                    action,
                    count,
                    f"{percentage:.1f}%"
                )
            )

        # Close
        tk.Button(
            report_window,
            text="Close Report",
            command=report_window.destroy,
            bg="#172554",
            fg="white",
            activebackground="#1e3a8a",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(
            pady=(0, 20)
        )

    # ==========================================================
    # SELECTED OPERATION DETAILS
    # ==========================================================

    def show_selected_operation(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        if not values:
            return

        detail_window = tk.Toplevel(
            self.window
        )

        detail_window.title(
            "Operation Details"
        )

        detail_window.geometry(
            "600x430"
        )

        detail_window.configure(
            bg="#f1f5f9"
        )

        # Header
        tk.Label(
            detail_window,
            text="OPERATION DETAILS",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#172554",
            pady=15
        ).pack(
            fill="x"
        )

        details = tk.Frame(
            detail_window,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1
        )

        details.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=25
        )

        labels = [
            ("Log ID", values[0]),
            ("User", values[1]),
            ("Action", values[2]),
            ("Description", values[3]),
            ("IP Address", values[4]),
            ("Created", values[5])
        ]

        for index, (label, value) in enumerate(labels):

            tk.Label(
                details,
                text=label + ":",
                font=("Segoe UI", 10, "bold"),
                fg="#475569",
                bg="white"
            ).grid(
                row=index,
                column=0,
                sticky="nw",
                padx=20,
                pady=10
            )

            tk.Label(
                details,
                text=str(value),
                font=("Segoe UI", 10),
                fg="#0f172a",
                bg="white",
                wraplength=350,
                justify="left"
            ).grid(
                row=index,
                column=1,
                sticky="nw",
                padx=20,
                pady=10
            )

        details.columnconfigure(
            1,
            weight=1
        )

        tk.Button(
            detail_window,
            text="Close",
            command=detail_window.destroy,
            bg="#172554",
            fg="white",
            activebackground="#1e3a8a",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=8
        ).pack(
            pady=(0, 20)
        )

    # ==========================================================
    # EXPORT CSV
    # ==========================================================

    def export_csv(self):

        if not hasattr(self, "all_rows") or not self.all_rows:

            messagebox.showinfo(
                "Export Report",
                "There are no audit records to export.",
                parent=self.window
            )

            return

        file_path = filedialog.asksaveasfilename(
            parent=self.window,
            title="Save Audit Report",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv"),
                ("All Files", "*.*")
            ],
            initialfile="system_operation_report.csv"
        )

        if not file_path:
            return

        try:

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "Log ID",
                    "User",
                    "Action",
                    "Description",
                    "IP Address",
                    "Created"
                ])

                writer.writerows(
                    self.all_rows
                )

            messagebox.showinfo(
                "Export Successful",
                f"Audit report exported successfully.\n\n"
                f"Location:\n{file_path}",
                parent=self.window
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error),
                parent=self.window
            )