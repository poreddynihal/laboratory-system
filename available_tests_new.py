import customtkinter as ctk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from PIL import Image

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Nihalreddy@31",
        database="project_698"
    )

class ViewAvailableTestsPage(ctk.CTkFrame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback

        self.configure(fg_color="#F7F7F7")

        self.logged_in_user = self.controller.username or "Unknown"
        self.login_date = datetime.now().strftime("%m/%d/%Y")

        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        # --------- Header ---------
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
            ctk.CTkButton(header_frame, image=logout_icon, text="", command=self.logout,
                          width=40, height=40, fg_color="transparent", hover_color="#CCCCCC").place(x=1020, y=20)
        except Exception as e:
            print("Logout image error:", e)


        # --------- Heading ---------
        ctk.CTkLabel(self, text="View Available Tests",
                     font=("Calibri", 20, "bold"), text_color="black").place(relx=0.5, y=100, anchor="center")

        # --------- Search Section ---------
        ctk.CTkLabel(self, text="Search").place(x=120, y=140)
        self.search_entry = ctk.CTkEntry(self, width=500, placeholder_text="Search by test name")
        self.search_entry.place(x=120, y=170)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        ctk.CTkLabel(self, text="Total Available Tests:", font=("Calibri", 14)).place(x=700, y=170)
        self.total_tests_label = ctk.CTkLabel(self, text="0", text_color="red")
        self.total_tests_label.place(x=880, y=170)

        # --------- Scrollable Container ---------
        scrollable_container = ctk.CTkFrame(self, fg_color="#F7F7F7", width=800, height=400)
        scrollable_container.place(x=120, y=220)

        self.canvas = ctk.CTkCanvas(scrollable_container, bg="#F7F7F7", highlightthickness=0, width=780, height=400)
        self.scrollable_frame = Frame(self.canvas, bg="#F7F7F7")

        scrollbar = Scrollbar(scrollable_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # --------- Back Button ---------
        ctk.CTkButton(self, text="Back", font=("Calibri", 14, "bold"),
                      width=100, text_color="black", fg_color="#D0D0D0", hover_color="#C0C0C0", corner_radius=50,
                      command=self.back_callback).place(x=100, y=660)

        self.display_checkboxes()

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)

    def logout(self):
        self.controller.logout_user()

    def fetch_tests(self, keyword=""):
        conn = connect_db()
        cursor = conn.cursor()
        if keyword:
            cursor.execute("SELECT test_name FROM diagnostic_test_info WHERE is_available = 1 AND test_name LIKE %s", (f"%{keyword}%",))
        else:
            cursor.execute("SELECT test_name FROM diagnostic_test_info WHERE is_available = 1")
        tests = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return tests

    def display_checkboxes(self, keyword=""):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tests = self.fetch_tests(keyword)
        for idx, name in enumerate(tests):
            col = idx % 2
            row = idx // 2
            chk = ctk.CTkCheckBox(self.scrollable_frame, text=name, state="disabled", variable=ctk.IntVar(value=1))
            chk.grid(row=row, column=col, padx=20, pady=5, sticky="w")

        self.total_tests_label.configure(text=str(len(tests)))

    def on_search(self, event=None):
        keyword = self.search_entry.get().strip()
        self.display_checkboxes(keyword)

    def reset_fields(self):
        """Update the username in the header when page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.header_username_label.configure(text=f"Username: {self.logged_in_user}")
        self.search_entry.delete(0, "end")
        self.display_checkboxes()
