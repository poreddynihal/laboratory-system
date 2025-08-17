import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from tkinter import *
import os
from datetime import datetime
from PIL import Image

# ----------------- DATABASE CONNECTION -------------------
def connect_db():
    return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Nihalreddy@31",
            database="project_698"
    )

class GenerateReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback

        self.logged_in_user = self.controller.username or "Unknown"
        self.login_date = datetime.now().strftime("%m/%d/%Y")

        self.configure(fg_color="#F7F7F7")
        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        # -------- Header --------
        header_frame = ctk.CTkFrame(self, fg_color="#D0D0D0", height=60)
        header_frame.pack(fill="x")

        self.header_username_label = ctk.CTkLabel(header_frame, text=f"Username: {self.logged_in_user}",
                                                  font=("Calibri", 14), text_color="black")
        self.header_username_label.place(x=20, y=10)

        ctk.CTkLabel(header_frame, text=f"Date: {self.login_date}",
                     font=("Calibri", 14), text_color="black").place(x=20, y=35)

        ctk.CTkLabel(header_frame, text="MADHAVI DIAGNOSTIC CENTER",
                     font=("Calibri", 24, "bold"), text_color="black").place(relx=0.5, y=20, anchor="center")

        self.time_label = ctk.CTkLabel(header_frame, text="", font=("Calibri", 14), text_color="black")
        self.time_label.place(relx=0.5, y=50, anchor="center")

        try:
            logout_image = Image.open("logout.png").resize((30, 30))
            logout_icon = ctk.CTkImage(light_image=logout_image, dark_image=logout_image, size=(30, 30))
            logout_button = ctk.CTkButton(header_frame, image=logout_icon, text="",
                                          command=self.controller.logout_user,
                                          width=40, height=40, fg_color="transparent",
                                          hover_color="#CCCCCC")
            logout_button.place(x=1020, y=20)
        except Exception as e:
            print("Logout icon error:", e)

        # -------- Search Frame --------
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(pady=15)

        # Add a label to the left of the search bar
        search_label = ctk.CTkLabel(search_frame, text="Enter Patient ID or Name:", font=("Calibri", 14, "bold"))
        search_label.pack(side="left", padx=10)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search", width=300)
        self.search_entry.pack(side="left", padx=10)

        search_btn = ctk.CTkButton(search_frame, text="Search", width=100, command=self.search_patient, corner_radius=50)
        search_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(search_frame, text="Clear", width=100, command=self.clear_search, corner_radius=50)
        clear_btn.pack(side="left", padx=5)

        # -------- Main Content Area --------
        self.main_frame = ctk.CTkFrame(self, bg_color='white')
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # -------- Back Button --------
        ctk.CTkButton(self, text="Back", width=100, height=35, command=self.back_callback,
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0", corner_radius=50).place(x=100, y=600)

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)



    def search_patient(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a Patient ID or Name.")
            return

        conn = connect_db()
        cursor = conn.cursor()

        if query.isdigit():
            cursor.execute("SELECT patient_id FROM patient_details WHERE patient_id = %s", (query,))
        else:
            cursor.execute("SELECT patient_id FROM patient_details WHERE patient_first_name LIKE %s OR patient_last_name LIKE %s",
                           (f"%{query}%", f"%{query}%"))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            self.show_patient_reports(result[0])
        else:
            messagebox.showerror("Error", "No matching patient found.")

    def clear_search(self):
        self.search_entry.delete(0, "end")
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_patient_reports(self, patient_id):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(self.main_frame, text="Patient Reports", font=("Calibri", 24, "bold"))
        title.pack(pady=10)

        reports = self.fetch_reports(patient_id)
        if not reports:
            ctk.CTkLabel(self.main_frame, text="No reports found for this patient.", font=("Calibri", 14)).pack()
            return

        table = ctk.CTkFrame(self.main_frame)
        table.pack()

        headers = ["Report ID", "Status", "Date", "Print"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(table, text=header, font=("Calibri", 14, "bold"), text_color="white",
                                 fg_color="#007BFF", width=150, height=30)
            label.grid(row=0, column=i, padx=2, pady=2)

        for row, report in enumerate(reports, start=1):
            for col, val in enumerate(report):
                if col == 0:
                    btn = ctk.CTkButton(table, text=str(val), font=("Calibri", 14),
                                        fg_color="transparent", text_color="blue", hover_color="#E0E0E0", width=150,
                                        command=lambda r=report[0]: self.generate_pdf_report(r))
                    btn.grid(row=row, column=col, padx=2, pady=2)
                else:
                    lbl = ctk.CTkLabel(table, text=str(val), font=("Calibri", 14), width=150, height=30)
                    lbl.grid(row=row, column=col, padx=2, pady=2)

            print_btn = ctk.CTkButton(table, text="Print", width=100, command=lambda r=report[0]: self.generate_pdf_report(r))
            print_btn.grid(row=row, column=3, padx=5)

    def fetch_reports(self, patient_id):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT report_id, report_status, report_date 
            FROM patient_reports 
            WHERE report_id IN 
            (SELECT report_id FROM ordered_tests WHERE patient_id = %s)
        """, (patient_id,))
        reports = cursor.fetchall()
        cursor.close()
        conn.close()
        return reports

    def generate_pdf_report(self, report_id):
        details, tests = self.fetch_report_details(report_id)
        if not details:
            return

        pdf_file = f"Patient_Report_{report_id}.pdf"
        c = canvas.Canvas(pdf_file, pagesize=A4)
        w, h = A4

        if os.path.exists("lab_logo.png"):
            c.drawImage(ImageReader("lab_logo.png"), 40, h - 100, width=150, height=60)

        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, h - 50, "MADHAVI DIAGNOSTIC CENTER")
        c.setFont("Helvetica", 12)
        c.drawString(200, h - 70, "Christian Colony, Karimnagar, Telangana, 505001")
        c.drawString(200, h - 85, "Phone: +91 9912268818| Email: madhavilab@gmail.com")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, h - 130, f"PATIENT TEST REPORT - ID: {report_id}")

        c.setFont("Helvetica", 12)
        c.drawString(40, h - 160, f"Name: {details[1]} {details[2]}")
        c.drawString(40, h - 180, f"Gender: {details[3]}")
        c.drawString(40, h - 200, f"Location: {details[4]}, {details[5]}")
        c.drawString(40, h - 220, f"Report Status: {details[7]} | Date: {details[8]}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, h - 260, "Test Name")
        c.drawString(220, h - 260, "Result")
        c.drawString(320, h - 260, "Normal")
        c.drawString(450, h - 260, "Units")
        c.line(40, h - 265, 540, h - 265)

        y = h - 285
        c.setFont("Helvetica", 12)
        for test in tests:
            c.drawString(40, y, str(test[0]))
            c.drawString(220, y, str(test[1]))
            c.drawString(320, y, str(test[2]))
            c.drawString(450, y, str(test[3]))
            y -= 20

        c.save()
        # Save the PDF file path to the database
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patient_reports
                SET file_path = %s
                WHERE report_id = %s
            """, (pdf_file, report_id))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"Report saved: {pdf_file} and file path updated in the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file path to the database: {e}")

        # Open the PDF file
        os.system(f"open {pdf_file}")

    def fetch_report_details(self, report_id):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT p.patient_id, p.patient_first_name, p.patient_last_name, p.gender, p.city, p.state, 
                       r.report_id, r.report_status, r.report_date 
                FROM patient_reports r 
                JOIN ordered_tests o ON r.report_id = o.report_id 
                JOIN patient_details p ON o.patient_id = p.patient_id 
                WHERE r.report_id = %s
                LIMIT 1
            """, (report_id,))
            report_details = cursor.fetchone()

            cursor.execute("""
                SELECT d.test_name, o.result_value, d.normal_values, d.units 
                FROM ordered_tests o 
                JOIN diagnostic_test_info d ON o.test_id = d.test_id 
                WHERE o.report_id = %s
            """, (report_id,))
            test_results = cursor.fetchall()

            cursor.close()
            conn.close()
            return report_details, test_results
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch report: {e}")
            return None, None

    def reset_fields(self):
        """Update the username in the header when page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.header_username_label.configure(text=f"Username: {self.logged_in_user}")
        self.search_entry.delete(0, "end")
        for widget in self.main_frame.winfo_children():
            widget.destroy()
