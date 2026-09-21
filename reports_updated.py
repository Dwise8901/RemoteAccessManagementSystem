import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from database import get_connection
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


class ReportsWindow:

    def __init__(self, parent, current_user):

        self.current_user = current_user

        self.window = tk.Toplevel(parent)
        self.window.title("Reports")
        self.window.geometry("900x550")
        self.window.resizable(True, True)

        self.build_interface()
        self.load_report()

    def build_interface(self):

        # ==========================================================
        # WINDOW STYLE
        # ==========================================================
        self.window.configure(bg="#eef2f7")

        style = ttk.Style(self.window)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Report.Treeview",
            background="#ffffff",
            foreground="#1f2937",
            rowheight=38,
            fieldbackground="#ffffff",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Report.Treeview.Heading",
            background="#1f4e78",
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=(10, 10)
        )

        style.map(
            "Report.Treeview.Heading",
            background=[("active", "#173b5c")]
        )

        style.configure(
            "Report.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 8)
        )

        # ==========================================================
        # HEADER
        # ==========================================================
        header = tk.Frame(
            self.window,
            bg="#173b5c",
            height=105
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="VIRTUAL SYSTEM ACCESS CONTROL",
            bg="#173b5c",
            fg="white",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(16, 2))

        tk.Label(
            header,
            text="SYSTEM REPORT & ACTIVITY SUMMARY",
            bg="#173b5c",
            fg="#dbeafe",
            font=("Segoe UI", 10)
        ).pack()

        # ==========================================================
        # SUMMARY CARDS
        # ==========================================================
        self.summary_frame = tk.Frame(
            self.window,
            bg="#eef2f7"
        )
        self.summary_frame.pack(
            fill="x",
            padx=25,
            pady=(20, 5)
        )

        self.summary_cards = {}

        card_definitions = [
            ("users", "TOTAL USERS", "👥", "#2563eb"),
            ("devices", "TOTAL DEVICES", "🖥", "#0891b2"),
            ("pending", "PENDING REQUESTS", "⏳", "#d97706"),
            ("approved", "APPROVED REQUESTS", "✓", "#16a34a"),
            ("rejected", "REJECTED REQUESTS", "✕", "#dc2626"),
            ("sessions", "REMOTE SESSIONS", "↔", "#7c3aed"),
        ]

        for index, (key, title, icon, accent) in enumerate(card_definitions):
            card = tk.Frame(
                self.summary_frame,
                bg="white",
                bd=1,
                relief="solid"
            )
            card.grid(
                row=0,
                column=index,
                padx=5,
                sticky="nsew"
            )

            self.summary_frame.columnconfigure(index, weight=1)

            tk.Frame(
                card,
                bg=accent,
                width=5
            ).pack(side="left", fill="y")

            inside = tk.Frame(card, bg="white")
            inside.pack(
                side="left",
                fill="both",
                expand=True,
                padx=10,
                pady=9
            )

            tk.Label(
                inside,
                text=icon,
                bg="white",
                fg=accent,
                font=("Segoe UI Symbol", 15, "bold")
            ).pack(side="left", padx=(0, 8))

            text_area = tk.Frame(inside, bg="white")
            text_area.pack(side="left", fill="both", expand=True)

            tk.Label(
                text_area,
                text=title,
                bg="white",
                fg="#6b7280",
                font=("Segoe UI", 8, "bold")
            ).pack(anchor="w")

            value_label = tk.Label(
                text_area,
                text="0",
                bg="white",
                fg="#111827",
                font=("Segoe UI", 17, "bold")
            )
            value_label.pack(anchor="w")

            self.summary_cards[key] = value_label

        # ==========================================================
        # REPORT INFORMATION BAR
        # ==========================================================
        info_bar = tk.Frame(
            self.window,
            bg="white",
            bd=1,
            relief="solid"
        )
        info_bar.pack(
            fill="x",
            padx=25,
            pady=(15, 8)
        )

        tk.Label(
            info_bar,
            text="SYSTEM REPORT",
            bg="white",
            fg="#173b5c",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=15, pady=10)

        self.generated_label = tk.Label(
            info_bar,
            text="Generated: --",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 9)
        )
        self.generated_label.pack(side="right", padx=15)

        # ==========================================================
        # TABLE
        # ==========================================================
        table_frame = tk.Frame(
            self.window,
            bg="white",
            bd=1,
            relief="solid"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 12)
        )

        columns = ("Item", "Count", "Status")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Report.Treeview",
            selectmode="browse"
        )

        self.table.heading(
            "Item",
            text="REPORT ITEM"
        )
        self.table.heading(
            "Count",
            text="COUNT"
        )
        self.table.heading(
            "Status",
            text="STATUS"
        )

        self.table.column(
            "Item",
            width=390,
            minwidth=260,
            anchor="w"
        )
        self.table.column(
            "Count",
            width=150,
            minwidth=100,
            anchor="center"
        )
        self.table.column(
            "Status",
            width=190,
            minwidth=130,
            anchor="center"
        )

        # Alternating row colours.
        self.table.tag_configure(
            "even",
            background="#f8fafc",
            foreground="#1f2937"
        )
        self.table.tag_configure(
            "odd",
            background="#e8f1fb",
            foreground="#1f2937"
        )

        # Status-specific colours.
        self.table.tag_configure(
            "positive",
            foreground="#15803d",
            font=("Segoe UI", 10, "bold")
        )
        self.table.tag_configure(
            "warning",
            foreground="#b45309",
            font=("Segoe UI", 10, "bold")
        )
        self.table.tag_configure(
            "negative",
            foreground="#b91c1c",
            font=("Segoe UI", 10, "bold")
        )
        self.table.tag_configure(
            "neutral",
            foreground="#374151",
            font=("Segoe UI", 10, "bold")
        )

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

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # ==========================================================
        # BUTTON BAR
        # ==========================================================
        button_frame = tk.Frame(
            self.window,
            bg="#eef2f7"
        )
        button_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 18)
        )

        ttk.Button(
            button_frame,
            text="⟳  Refresh Report",
            command=self.load_report,
            style="Report.TButton"
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ttk.Button(
            button_frame,
            text="▣  Export to Excel",
            command=self.export_to_excel,
            style="Report.TButton"
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            button_frame,
            text="Close",
            command=self.window.destroy,
            style="Report.TButton"
        ).pack(
            side="right"
        )

    def get_report_data(self):

        connection = get_connection()

        if not connection:
            raise Exception(
                "Could not connect to the database."
            )

        cursor = connection.cursor()

        queries = [
            (
                "Total Users",
                "SELECT COUNT(*) FROM users"
            ),
            (
                "Total Devices",
                "SELECT COUNT(*) FROM devices"
            ),
            (
                "Pending Requests",
                """
                SELECT COUNT(*)
                FROM access_requests
                WHERE status = 'PENDING'
                """
            ),
            (
                "Approved Requests",
                """
                SELECT COUNT(*)
                FROM access_requests
                WHERE status = 'APPROVED'
                """
            ),
            (
                "Rejected Requests",
                """
                SELECT COUNT(*)
                FROM access_requests
                WHERE status = 'REJECTED'
                """
            ),
            (
                "Remote Sessions",
                """
                SELECT COUNT(*)
                FROM remote_sessions
                """
            )
        ]

        report_data = []

        try:

            for name, query in queries:

                cursor.execute(query)

                result = cursor.fetchone()

                count = result[0] if result else 0

                report_data.append(
                    (name, count)
                )

            return report_data

        finally:

            cursor.close()
            connection.close()

    def get_status_for_item(self, name, count):
        """Return a readable status and a status colour category."""

        if name == "Pending Requests":
            return (
                "ACTION REQUIRED" if count > 0 else "CLEAR",
                "warning" if count > 0 else "positive"
            )

        if name == "Approved Requests":
            return (
                "APPROVED",
                "positive"
            )

        if name == "Rejected Requests":
            return (
                "REVIEW",
                "negative" if count > 0 else "neutral"
            )

        if name == "Remote Sessions":
            return (
                "RECORDED",
                "positive" if count > 0 else "neutral"
            )

        if name in ("Total Users", "Total Devices"):
            return (
                "AVAILABLE",
                "positive" if count > 0 else "warning"
            )

        return ("INFO", "neutral")

    def update_summary_cards(self, report_data):

        mapping = {
            "Total Users": "users",
            "Total Devices": "devices",
            "Pending Requests": "pending",
            "Approved Requests": "approved",
            "Rejected Requests": "rejected",
            "Remote Sessions": "sessions"
        }

        for name, count in report_data:
            key = mapping.get(name)

            if key and key in self.summary_cards:
                self.summary_cards[key].config(
                    text=f"{count:,}"
                )

    def load_report(self):

        # Clear old report.
        for item in self.table.get_children():
            self.table.delete(item)

        try:

            report_data = self.get_report_data()

            self.update_summary_cards(report_data)

            self.generated_label.config(
                text=(
                    "Generated: "
                    + datetime.now().strftime("%d %b %Y  |  %I:%M:%S %p")
                )
            )

            for index, (name, count) in enumerate(report_data):

                status, status_tag = self.get_status_for_item(
                    name,
                    count
                )

                # Alternate the background colour by row while also
                # retaining the status colour through the Status column.
                row_tag = "even" if index % 2 == 0 else "odd"

                item_id = self.table.insert(
                    "",
                    tk.END,
                    values=(
                        name,
                        f"{count:,}",
                        status
                    ),
                    tags=(row_tag,)
                )

                # Apply status styling to the status cell itself.
                # Tkinter Treeview does not support per-cell colours,
                # so the status is highlighted using a small prefix.
                self.table.set(
                    item_id,
                    "Status",
                    status
                )

        except Exception as error:

            messagebox.showerror(
                "Report Error",
                str(error),
                parent=self.window
            )

    def export_to_excel(self):

        try:

            # Get current data from MySQL.
            report_data = self.get_report_data()

            # Ask user where to save the Excel file.
            file_path = filedialog.asksaveasfilename(
                parent=self.window,
                title="Save Excel Report",
                defaultextension=".xlsx",
                filetypes=[
                    (
                        "Excel Workbook",
                        "*.xlsx"
                    )
                ],
                initialfile=(
                    "Remote_Access_System_Report_"
                    + datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )
                    + ".xlsx"
                )
            )

            if not file_path:
                return

            # ======================================================
            # CREATE WORKBOOK
            # ======================================================
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = "System Report"

            from openpyxl.styles import (
                Font,
                Alignment,
                PatternFill,
                Border,
                Side
            )

            # Colours.
            navy = "173B5C"
            blue = "1F4E78"
            light_blue = "E8F1FB"
            light_gray = "F8FAFC"
            white = "FFFFFF"
            green = "15803D"
            light_green = "DCFCE7"
            orange = "B45309"
            light_orange = "FEF3C7"
            red = "B91C1C"
            light_red = "FEE2E2"
            border_color = "D1D5DB"

            thin_border = Border(
                left=Side(style="thin", color=border_color),
                right=Side(style="thin", color=border_color),
                top=Side(style="thin", color=border_color),
                bottom=Side(style="thin", color=border_color)
            )

            # ======================================================
            # EXCEL HEADER
            # ======================================================
            worksheet.merge_cells("A1:C1")
            worksheet["A1"] = (
                "VIRTUAL SYSTEM ACCESS CONTROL"
            )
            worksheet["A1"].font = Font(
                bold=True,
                size=18,
                color=white
            )
            worksheet["A1"].fill = PatternFill(
                "solid",
                fgColor=navy
            )
            worksheet["A1"].alignment = Alignment(
                horizontal="center",
                vertical="center"
            )
            worksheet.row_dimensions[1].height = 32

            worksheet.merge_cells("A2:C2")
            worksheet["A2"] = "SYSTEM REPORT & ACTIVITY SUMMARY"
            worksheet["A2"].font = Font(
                bold=True,
                size=13,
                color="DDEBFA"
            )
            worksheet["A2"].fill = PatternFill(
                "solid",
                fgColor=blue
            )
            worksheet["A2"].alignment = Alignment(
                horizontal="center"
            )

            worksheet["A3"] = "Generated"
            worksheet["B3"] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            worksheet.merge_cells("B3:C3")

            worksheet["A3"].font = Font(
                bold=True,
                color=navy
            )

            for cell in worksheet[3]:
                cell.fill = PatternFill(
                    "solid",
                    fgColor="EEF2F7"
                )

            # ======================================================
            # EXCEL TABLE HEADINGS
            # ======================================================
            headings = ["Report Item", "Count", "Status"]

            for column, heading in enumerate(headings, start=1):
                cell = worksheet.cell(
                    row=5,
                    column=column,
                    value=heading
                )
                cell.font = Font(
                    bold=True,
                    color=white
                )
                cell.fill = PatternFill(
                    "solid",
                    fgColor=blue
                )
                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )
                cell.border = thin_border

            worksheet.row_dimensions[5].height = 25

            # ======================================================
            # EXCEL DATA
            # ======================================================
            row_number = 6

            for index, (name, count) in enumerate(report_data):

                status, status_tag = self.get_status_for_item(
                    name,
                    count
                )

                values = [
                    name,
                    count,
                    status
                ]

                for column, value in enumerate(values, start=1):

                    cell = worksheet.cell(
                        row=row_number,
                        column=column,
                        value=value
                    )

                    cell.border = thin_border
                    cell.alignment = Alignment(
                        horizontal=(
                            "left" if column == 1 else "center"
                        ),
                        vertical="center"
                    )

                    # Alternating rows.
                    cell.fill = PatternFill(
                        "solid",
                        fgColor=(
                            light_gray
                            if index % 2 == 0
                            else light_blue
                        )
                    )

                # Colour the status cell.
                status_cell = worksheet.cell(
                    row=row_number,
                    column=3
                )

                if status_tag == "positive":
                    status_cell.font = Font(
                        bold=True,
                        color=green
                    )
                    status_cell.fill = PatternFill(
                        "solid",
                        fgColor=light_green
                    )

                elif status_tag == "warning":
                    status_cell.font = Font(
                        bold=True,
                        color=orange
                    )
                    status_cell.fill = PatternFill(
                        "solid",
                        fgColor=light_orange
                    )

                elif status_tag == "negative":
                    status_cell.font = Font(
                        bold=True,
                        color=red
                    )
                    status_cell.fill = PatternFill(
                        "solid",
                        fgColor=light_red
                    )

                else:
                    status_cell.font = Font(
                        bold=True,
                        color="374151"
                    )

                row_number += 1

            # ======================================================
            # EXCEL SUMMARY
            # ======================================================
            summary_row = row_number + 2

            worksheet.merge_cells(
                start_row=summary_row,
                start_column=1,
                end_row=summary_row,
                end_column=3
            )

            worksheet.cell(
                row=summary_row,
                column=1,
                value=(
                    "Report generated by the Remote Access "
                    "Management System"
                )
            )

            worksheet.cell(
                row=summary_row,
                column=1
            ).font = Font(
                italic=True,
                color="6B7280"
            )

            worksheet.cell(
                row=summary_row,
                column=1
            ).alignment = Alignment(
                horizontal="center"
            )

            # ======================================================
            # EXCEL DIMENSIONS / FREEZE / FILTER
            # ======================================================
            worksheet.column_dimensions["A"].width = 36
            worksheet.column_dimensions["B"].width = 18
            worksheet.column_dimensions["C"].width = 24

            worksheet.freeze_panes = "A6"
            worksheet.auto_filter.ref = (
                f"A5:C{row_number - 1}"
            )

            # Print-friendly settings.
            worksheet.print_title_rows = "1:5"
            worksheet.sheet_view.showGridLines = False

            workbook.save(file_path)

            messagebox.showinfo(
                "Export Successful",
                "Professional Excel report generated successfully.\n\n"
                f"Saved to:\n{file_path}",
                parent=self.window
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error),
                parent=self.window
            )
