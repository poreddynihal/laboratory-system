import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from PIL import Image
from datetime import datetime
import mysql.connector

# ------------- DATABASE CONNECTION -------------
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Nihalreddy@31",
        database="project_698"
    )

# ------------- CLASS ----------------
class AddSelectTestsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback

        self.configure(fg_color="#F7F7F7")

        self.logged_in_user = self.controller.username or "Unknown"
        self.login_date = datetime.now().strftime("%m/%d/%Y")

        self.test_data = []  # Store (test_name, is_available) for saving
        self.checkbox_widgets = []
        self.selected_vars = []
        
        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        
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

        # ---------------- ADD NEW TESTS SECTION ----------------
        ctk.CTkLabel(self, text="Add New Test", font=("Calibri", 20, "bold"), text_color="black").place(relx=0.5, y=100, anchor="center")

        ctk.CTkLabel(self, text="Test Code:").place(x=50, y=140)
        self.test_code_entry = ctk.CTkEntry(self, width=120)
        self.test_code_entry.place(x=50, y=165)

        ctk.CTkLabel(self, text="Test Name:").place(x=200, y=140)
        self.test_name_entry = ctk.CTkEntry(self, width=200)
        self.test_name_entry.place(x=200, y=165)

        ctk.CTkLabel(self, text="Normal Values:").place(x=450, y=140)
        self.normal_values_entry = ctk.CTkEntry(self, width=180)
        self.normal_values_entry.place(x=450, y=165)

        ctk.CTkLabel(self, text="Units:").place(x=700, y=140)
        self.units_entry = ctk.CTkEntry(self, width=120)
        self.units_entry.place(x=700, y=165)

        self.availability_chk = ctk.CTkCheckBox(self, text="Available")
        self.availability_chk.place(x=850, y=160)

        ctk.CTkButton(self, text="Add Test", width=100, height =35, command=self.add_test, corner_radius=50,
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0").place(x=950, y=160)

        # ---------------- SELECT AVAILABLE TESTS SECTION ----------------
        ctk.CTkLabel(self, text="Select Available Tests", font=("Calibri", 20, "bold"), text_color="black").place(relx=0.5, y=220, anchor="center")

        ctk.CTkLabel(self, text="Search:").place(x=120, y=260)
        self.search_entry = ctk.CTkEntry(self, width=400, placeholder_text="Search by test name")
        self.search_entry.place(x=200, y=260)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        ctk.CTkLabel(self, text="Total Available Tests:", font=("Calibri", 14)).place(x=650, y=260)
        self.total_tests_label = ctk.CTkLabel(self, text="0", text_color="blue")
        self.total_tests_label.place(x=820, y=260)

        # Scrollable container
        scrollable_container = ctk.CTkFrame(self, fg_color="#F7F7F7", width=800, height=200)
        scrollable_container.place(x=120, y=300)

        self.canvas = Canvas(scrollable_container, bg="#F7F7F7", highlightthickness=0, width=780, height=200)
        self.scrollable_frame = Frame(self.canvas, bg="#F7F7F7")

        scrollbar = Scrollbar(scrollable_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # ---------------- BUTTONS BOTTOM ----------------
        ctk.CTkButton(self, text="Back", width=100, command=self.back_callback, corner_radius=50,
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0").place(x=100, y=600)

        ctk.CTkButton(self, text="Save Changes", width=100,height=35, command=self.save_changes, corner_radius=50,
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0").place(x=400, y=580)

        self.display_checkboxes()

    # ---------------- BUTTON FUNCTIONS ----------------


    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)

    def logout(self):
        self.controller.logout_user()

    def fetch_tests(self, keyword=""):
        conn = connect_db()
        cursor = conn.cursor()
        if keyword:
            cursor.execute("SELECT test_name, is_available FROM diagnostic_test_info WHERE test_name LIKE %s", (f"%{keyword}%",))
        else:
            cursor.execute("SELECT test_name, is_available FROM diagnostic_test_info")
        self.test_data = cursor.fetchall()
        cursor.close()
        conn.close()

    def display_checkboxes(self, keyword=""):
        for widget in self.checkbox_widgets:
            widget.destroy()
        self.checkbox_widgets.clear()
        self.selected_vars.clear()

        self.fetch_tests(keyword)

        for idx, (test_name, is_available) in enumerate(self.test_data):
            col = idx % 2
            row = idx // 2
            var = IntVar(value=is_available)
            chk = Checkbutton(self.scrollable_frame, text=test_name, variable=var, bg="#F7F7F7")
            chk.grid(row=row, column=col, padx=20, pady=5, sticky="w")
            self.selected_vars.append((test_name, var))
            self.checkbox_widgets.append(chk)

        self.total_tests_label.configure(text=str(len(self.test_data)))

    def on_search(self, event=None):
        keyword = self.search_entry.get().strip()
        self.display_checkboxes(keyword)

    def add_test(self):
        test_code = self.test_code_entry.get().strip()
        test_name = self.test_name_entry.get().strip()
        normal_values = self.normal_values_entry.get().strip()
        units = self.units_entry.get().strip()
        is_available = 1 if self.availability_chk.get() == 1 else 0

        if not test_code or not test_name:
            messagebox.showerror("Input Error", "Test Code and Test Name are required!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO diagnostic_test_info (test_code, test_name, normal_values, units, is_available)
                VALUES (%s, %s, %s, %s, %s)
            """, (test_code, test_name, normal_values, units, is_available))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "New test added successfully!")

            self.test_code_entry.delete(0, 'end')
            self.test_name_entry.delete(0, 'end')
            self.normal_values_entry.delete(0, 'end')
            self.units_entry.delete(0, 'end')
            self.availability_chk.deselect()

            self.display_checkboxes()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def save_changes(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()

            for test_name, var in self.selected_vars:
                is_available = var.get()
                cursor.execute("UPDATE diagnostic_test_info SET is_available = %s WHERE test_name = %s", (is_available, test_name))

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Availability status updated successfully!")
            self.display_checkboxes()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def reset_fields(self):
        """Update the username in the header when page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.header_username_label.configure(text=f"Username: {self.logged_in_user}")
        self.search_entry.delete(0, "end")
        self.display_checkboxes()
