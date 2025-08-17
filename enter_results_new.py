from tkinter import *
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime
import mysql.connector
from PIL import Image
from report_generation_new import GenerateReportsPage

# Database connection function (make sure you define this in your project)
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Nihalreddy@31",
        database="project_698"
    )

class EnterTestResultsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback

        self.configure(fg_color="#F7F7F7")

        # Initialize logged-in user and date
        self.logged_in_user = self.controller.username or "Unknown"
        self.login_date = datetime.now().strftime("%m/%d/%Y")

        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        # ---------- Header ----------
        self.header = ctk.CTkFrame(self, fg_color="#D0D0D0", height=60)
        self.header.pack(fill="x")

        self.header_username_label = ctk.CTkLabel(self.header, text=f"Username: {self.logged_in_user}",
                                                  font=("Calibri", 14), text_color="black")
        self.header_username_label.place(x=20, y=10)

        ctk.CTkLabel(self.header, text=f"Date: {self.login_date}", font=("Calibri", 14),
                     text_color="black").place(x=20, y=35)

        ctk.CTkLabel(self.header, text="MADHAVI DIAGNOSTIC CENTER", font=("Calibri", 24, "bold"),
                     text_color="black").place(relx=0.5, y=20, anchor="center")

        self.time_label = ctk.CTkLabel(self.header, text="", font=("Calibri", 14), text_color="black")
        self.time_label.place(relx=0.5, y=50, anchor='center')

        try:
            logout_image = Image.open("Logout.png").resize((30, 30))
            logout_icon = ctk.CTkImage(light_image=logout_image, dark_image=logout_image, size=(30, 30))
            ctk.CTkButton(self.header, image=logout_icon, text="", command=self.logout,
                          width=40, height=40, fg_color="transparent", hover_color="#E0E0E0").place(x=1020, y=20)
        except Exception as e:
            print("Logout image error:", e)

        # ---------- Patient Search ----------
        ctk.CTkLabel(self, text="Search by Patient ID:", font=("Calibri", 16)).place(x=130, y=90)
        self.search_entry = ctk.CTkEntry(self, width=250)
        self.search_entry.place(x=300, y=90)

        # ---------- Clear and Enter Buttons ----------
        ctk.CTkButton(self, text="Clear", command=self.clear_search, width=80, corner_radius=50,
                      fg_color="#D9D9D9", text_color="black", hover_color="#D0D0D0").place(x=660, y=90)

        ctk.CTkButton(self, text="Enter", command=self.fetch_patient_and_tests, width=80, corner_radius=50,
                      fg_color="#4CAF50", text_color="white", hover_color="#45A049").place(x=570, y=90)
            # ---------- Instruction Label ----------
        ctk.CTkLabel(self, text="Click on Enter Results to add test results", font=("Calibri", 14, "bold"),
                    text_color="red").place(x=650, y=160)

        # ---------- Patient Info Labels ----------
        self.patient_id_label = ctk.CTkLabel(self, text="Patient ID :", font=("Calibri", 16))
        self.patient_id_label.place(x=130, y=140)

        self.patient_name_label = ctk.CTkLabel(self, text="Patient Name :", font=("Calibri", 16))
        self.patient_name_label.place(x=300, y=140)

        self.dob_label = ctk.CTkLabel(self, text="DOB :", font=("Calibri", 16))
        self.dob_label.place(x=600, y=140)

        self.gender_label = ctk.CTkLabel(self, text="Gender :", font=("Calibri", 16))
        self.gender_label.place(x=800, y=140)

        # ---------- Treeview for Assigned Tests ----------
        tree_frame = Frame(self, bg="white")
        tree_frame.place(x=130, y=190, width=820, height=350)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.test_table = ttk.Treeview(tree_frame, columns=("Order ID", "Test ID", "Test Code", "Report ID", "Enter"),
                                       show="headings", yscrollcommand=tree_scroll.set)
        for col, width in zip(("Order ID", "Test ID", "Test Code", "Report ID", "Enter"), [100, 100, 150, 120, 150]):
            self.test_table.heading(col, text=col)
            self.test_table.column(col, anchor="center", width=width)
        self.test_table.pack(fill=BOTH, expand=True)
        tree_scroll.config(command=self.test_table.yview)

        # ---------- Back Button ----------
        ctk.CTkButton(self, text="Back", command=self.back_callback, width=100, height=35,
                      corner_radius=50, fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0").place(x=100, y=600)

         # ---------- Get Report Button ----------
        ctk.CTkButton(self, text="Get Report", command=self.navigate_to_generate_reports, width=120, height=35,
              corner_radius=50,  fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0").place(x=500, y=600)
        # ---------- Bindings ----------
        self.search_entry.bind("<Return>", lambda event: self.fetch_patient_and_tests())
        self.test_table.bind("<Button-1>", self.handle_enter_click)

    def reset_fields(self):
        """Update the username in the header when page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.header_username_label.configure(text=f"Username: {self.logged_in_user}")

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)

    def logout(self):
        self.controller.logout_user()

    def clear_search(self):
        self.search_entry.delete(0, END)
        self.patient_id_label.configure(text="Patient ID :")
        self.patient_name_label.configure(text="Patient Name :")
        self.dob_label.configure(text="DOB :")
        self.gender_label.configure(text="Gender :")
        self.test_table.delete(*self.test_table.get_children())

    def fetch_patient_and_tests(self):
        pid = self.search_entry.get().strip()
        if not pid.isdigit():
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT patient_first_name, patient_last_name, date_of_birth, gender FROM patient_details WHERE patient_id = %s", (pid,))
        patient = cursor.fetchone()
        if not patient:
            self.clear_search()
            self.patient_id_label.configure(text="Patient ID : Not Found")
            return

        name = f"{patient[0]} {patient[1]}"
        self.patient_id_label.configure(text=f"Patient ID : {pid}", text_color="blue")
        self.patient_name_label.configure(text=f"Patient Name : {name}", text_color="blue")
        self.dob_label.configure(text=f"DOB : {patient[2]}", text_color="blue")
        self.gender_label.configure(text=f"Gender : {patient[3]}", text_color="blue")

        self.test_table.tag_configure("enter", background="#0000FF", font=("Calibri", 12, "bold"))

        cursor.execute("""
            SELECT o.order_id, o.test_id, d.test_code, o.report_id
            FROM ordered_tests o
            JOIN diagnostic_test_info d ON o.test_id = d.test_id
            WHERE o.patient_id = %s
        """, (pid,))
        self.test_table.delete(*self.test_table.get_children())
        for row in cursor.fetchall():
            self.test_table.insert("", END,values=(*row, "Enter results"), tags=("enter_results",))

        cursor.close()
        conn.close()

    def navigate_to_generate_reports(self):
        """Navigate to the Generate Reports Page."""
        self.controller.show_frame(GenerateReportsPage)

    def handle_enter_click(self, event):
        region = self.test_table.identify("region", event.x, event.y)
        col = self.test_table.identify_column(event.x)
        row_id = self.test_table.identify_row(event.y)
        if region == "cell" and col == "#5":
            values = self.test_table.item(row_id)["values"]
            order_id, test_id, test_code, report_id = values[:4]
            self.open_results_entry_frame(order_id, test_id, test_code, report_id)

    def open_results_entry_frame(self, order_id, test_id, test_code, report_id):
        results_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=10, width=500, height=350)
        results_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(results_frame, text="Enter Test Results", font=("Calibri", 20, "bold")).place(relx=0.5, y=20, anchor="center")
        ctk.CTkLabel(results_frame, text=f"Order ID: {order_id}", font=("Calibri", 14)).place(x=50, y=80)
        ctk.CTkLabel(results_frame, text=f"Test ID: {test_id}", font=("Calibri", 14)).place(x=50, y=110)
        ctk.CTkLabel(results_frame, text=f"Test Code: {test_code}", font=("Calibri", 14)).place(x=50, y=140)
        ctk.CTkLabel(results_frame, text=f"Report ID: {report_id}", font=("Calibri", 14)).place(x=50, y=170)
        ctk.CTkLabel(results_frame, text="Result:", font=("Calibri", 14)).place(x=50, y=210)

        existing_result = ""
        result_is_editable = True
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT result_value FROM ordered_tests WHERE order_id = %s", (order_id,))
            result_row = cursor.fetchone()
            if result_row and result_row[0]:
                existing_result = result_row[0]
                result_is_editable = False
            cursor.close()
            conn.close()
        except Exception as e:
            print("Error fetching result:", e)

        result_entry = ctk.CTkEntry(results_frame, width=250)
        result_entry.place(x=150, y=210)
        result_entry.insert(0, existing_result)
        if not result_is_editable:
            result_entry.configure(state="disabled")

        def save_results():
            if not result_is_editable:
                return
            result = result_entry.get().strip()
            if not result:
                messagebox.showerror("Error", "Please enter the result!")
                return
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE ordered_tests SET result_value = %s, tested_date = NOW() WHERE order_id = %s", (result, order_id))
                cursor.execute("UPDATE patient_reports SET report_status = 'Completed' WHERE report_id = %s", (report_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Test result saved and report marked as Completed.")
                results_frame.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save result: {e}")

        if result_is_editable:
            ctk.CTkButton(results_frame, text="Save", command=save_results, width=100, fg_color="#4CAF50", corner_radius=50,
                          text_color="white").place(x=150, y=270)
        ctk.CTkButton(results_frame, text="Cancel", command=results_frame.destroy, width=100, fg_color="#D9534F", corner_radius=50,
                      text_color="white").place(x=270, y=270)
