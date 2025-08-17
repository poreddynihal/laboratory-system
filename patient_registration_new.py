import customtkinter as ctk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector
from PIL import Image
from enter_results_new import EnterTestResultsPage

# ------------------ DATABASE CONNECTION FUNCTIONS ------------------

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Nihalreddy@31",
        database="project_698"
    )

# ------------------ PATIENT REGISTRATION PAGE CLASS ------------------

class PatientRegistrationPage(ctk.CTkFrame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback
        self.selected_tests = []
        self.returning_selected_tests = []

        self.logged_in_user = self.controller.username or "Unknown"
        self.login_date = datetime.now().strftime("%m/%d/%Y")

        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        # Header
        self.header = ctk.CTkFrame(self, fg_color="#D0D0D0", height=60)
        self.header.pack(fill="x")



        # Username Label
        self.header_username_label = ctk.CTkLabel(self.header, text=f"Username: {self.logged_in_user}", font=("Calibri", 14), text_color="black")
        self.header_username_label.place(x=20, y=10)

    # Date Label
        ctk.CTkLabel(self.header, text=f"Date: {self.login_date}", font=("Calibri", 14), text_color="black").place(x=20, y=35)

    # Title Label
        ctk.CTkLabel(self.header, text="MADHAVI DIAGNOSTIC CENTER", font=("Calibri", 24, "bold"), text_color="black").place(relx=0.5, y=20, anchor="center")
        self.time_label = ctk.CTkLabel(self.header, text="", font=("Calibri", 14), text_color="black")
        self.time_label.place(relx=0.5, y=50, anchor='center')

        try:
            logout_image = Image.open("Logout.png").resize((30, 30))
            logout_icon = ctk.CTkImage(light_image=logout_image, dark_image=logout_image, size=(30, 30))
            ctk.CTkButton(self.header, image=logout_icon, text="", command=self.logout, width=40, height=40, fg_color="transparent", hover_color="#E0E0E0").place(x=1020, y=20)
        except:
            pass

        # Tab View
        self.tabview = ctk.CTkTabview(self, width=1060, height=630)
        self.tabview.pack(pady=5, padx=10)

        self.new_patient_tab = self.tabview.add("New Patient")
        self.returning_patient_tab = self.tabview.add("Returning Patient")

        self.create_new_patient_tab_widgets()
        self.create_returning_patient_tab_widgets()

    def reset_fields(self):
        """Update the username in the header when the page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.header_username_label.configure(text=f"Username: {self.logged_in_user}")

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)

    def logout(self):
        self.controller.logout_user()


    def get_new_patient_id(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(patient_id) FROM patient_details")
        last_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return last_id + 1 if last_id else 1

    def populate_registered_by_dropdown(self):
        """Fetch staff usernames from the database and populate the dropdown."""
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT staff_username FROM staff")  # Replace with your actual table and column names
            staff_usernames = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()

            # Update the dropdown values
            self.registered_by_dropdown.configure(values=staff_usernames)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching staff usernames: {err}")

    def create_new_patient_tab_widgets(self):
        # Create Scrollable Canvas
        canvas = Canvas(self.new_patient_tab, bg="#F7F7F7", highlightthickness=0)
        scrollbar = Scrollbar(self.new_patient_tab, orient=VERTICAL, command=canvas.yview)
        self.new_patient_frame = Frame(canvas, bg="#F2F2F2")

        self.new_patient_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.new_patient_frame, anchor="nw", width=1040, height=1300)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Patient Info Form Title
        ctk.CTkLabel(self.new_patient_frame, text="PATIENT DETAILS", font=("Calibri", 18, "bold")).place(x=470, y=40)

        #Patient ID
        ctk.CTkLabel(self.new_patient_frame, text="Patient ID:", font=("Calibri", 16)).place(x=70, y=100)
        self.patient_id_label = ctk.CTkLabel(self.new_patient_frame, text=str(self.get_new_patient_id()), font=("Calibri", 16), text_color="blue")
        self.patient_id_label.place(x=150, y=100)


        # Registered by
        ctk.CTkLabel(self.new_patient_frame, text="Registered by:", font=("Calibri", 16)).place(x=200, y=100)
        self.registered_by_dropdown = ctk.CTkComboBox(self.new_patient_frame, values=[], width=150, state="readonly")
        self.registered_by_dropdown.place(x=310, y=100)
        self.registered_by_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.registered_by_error.place(x=330, y=130)
        self.registered_by_dropdown.bind("<<ComboboxSelected>>", lambda e: self.clear_error(self.registered_by_error))

        # Populate the "Registered by" dropdown
        self.populate_registered_by_dropdown()

        # First Name
        ctk.CTkLabel(self.new_patient_frame, text="First Name:", font=("Calibri", 16)).place(x=70, y=160)
        self.first_name_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.first_name_entry.place(x=160, y=160)
        self.first_name_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.first_name_error.place(x=190, y=190)
        self.first_name_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.first_name_error))

        # Last Name
        ctk.CTkLabel(self.new_patient_frame, text="Last Name:", font=("Calibri", 16)).place(x=420, y=160)
        self.last_name_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.last_name_entry.place(x=530, y=160)
        self.last_name_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.last_name_error.place(x=560, y=190)
        self.last_name_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.last_name_error))

        # DOB
        ctk.CTkLabel(self.new_patient_frame, text="DOB:", font=("Calibri", 16)).place(x=70, y=220)
        self.dob_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.dob_entry.place(x=160, y=220)
        self.dob_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.dob_error.place(x=190, y=250)
        self.dob_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.dob_error))

        #Gender
        ctk.CTkLabel(self.new_patient_frame, text="Gender:", font=("Calibri", 16)).place(x=450, y=220)
        self.gender_dropdown = ctk.CTkComboBox(self.new_patient_frame, values=["Male", "Female", "Other"], width=150, state="readonly")
        self.gender_dropdown.place(x=550, y=220)

        # Phone
        ctk.CTkLabel(self.new_patient_frame, text="Phone:", font=("Calibri", 16)).place(x=70, y=280)
        self.phone_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.phone_entry.place(x=160, y=280)
        self.phone_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.phone_error.place(x=230, y=310)
        self.phone_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.phone_error))

        # Email
        ctk.CTkLabel(self.new_patient_frame, text="Email:", font=("Calibri", 16)).place(x=450, y=280)
        self.email_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.email_entry.place(x=530, y=280)
        self.email_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.email_error.place(x=560, y=310)
        self.email_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.email_error))

        # Street Address
        ctk.CTkLabel(self.new_patient_frame, text="Street Address:", font=("Calibri", 16)).place(x=70, y=340)
        self.street_entry = ctk.CTkEntry(self.new_patient_frame, width=300)
        self.street_entry.place(x=230, y=340)


        # City
        ctk.CTkLabel(self.new_patient_frame, text="City:", font=("Calibri", 16)).place(x=670, y=340)
        self.city_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.city_entry.place(x=750, y=340)
        self.city_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.city_error.place(x=770, y=370)
        self.city_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.city_error))

        # State
        ctk.CTkLabel(self.new_patient_frame, text="State:", font=("Calibri", 16)).place(x=70, y=400)
        self.state_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.state_entry.place(x=160, y=400)
        self.state_error = ctk.CTkLabel(self.new_patient_frame, text="", font=("Calibri", 10), text_color="red")
        self.state_error.place(x=230, y=430)
        self.state_entry.bind("<KeyRelease>", lambda e: self.clear_error(self.state_error))

        # Zipcode
        ctk.CTkLabel(self.new_patient_frame, text="Zipcode:", font=("Calibri", 16)).place(x=450, y=400)
        self.zipcode_entry = ctk.CTkEntry(self.new_patient_frame, width=200)
        self.zipcode_entry.place(x=530, y=400)

        # ------------------ FOOTER BUTTONS ------------------
        ctk.CTkButton(self.new_patient_frame, text="Register", width=100, height=35, corner_radius=50,
        fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
        command=self.new_patient_register_tests).place(x=450, y=1100)

        ctk.CTkButton(self.new_patient_frame, text="Add Results", width=120, height=35, corner_radius=50,
        fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0", command= lambda:self.controller.show_frame(EnterTestResultsPage)).place(x=600, y=1100)

        ctk.CTkButton(self.new_patient_frame, text="Back", width=100, height=35, corner_radius=50,
        fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",command=self.back_callback).place(x=100, y=1100)

        ctk.CTkButton(self.new_patient_frame, text="Clear", width=80, height=30, corner_radius=50,
        fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
        command=self.clear_all_fields).place(x=620, y=100)


            # ------------------ TEST SELECTION ------------------
        ctk.CTkLabel(self.new_patient_frame, text="TEST SELECTION", font=("Calibri", 18, "bold")).place(x=470, y=500)
        ctk.CTkLabel(self.new_patient_frame, text="Total Tests :", font=("Calibri", 16)).place(x=850, y=700)
        self.test_count_label = ctk.CTkLabel(self.new_patient_frame, text="0", font=("Calibri", 16), text_color="blue")
        self.test_count_label.place(x=950, y=700)

        ctk.CTkLabel(self.new_patient_frame, text="Selection Type", font=("Calibri", 16)).place(x=70, y=600)
        self.selection_type_dropdown = ctk.CTkComboBox(self.new_patient_frame, values=["test_id", "test_name"], width=120, state="readonly")
        self.selection_type_dropdown.place(x=200, y=600)
        self.selection_type_dropdown.set("test_name")

        self.search_entry = ctk.CTkEntry(self.new_patient_frame, placeholder_text="Search test...", width=300)
        self.search_entry.place(x=360, y=600)

        ctk.CTkButton(self.new_patient_frame, text="Clear", width=80, height=30, corner_radius=50,
            fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
            command=self.clear_search).place(x=680, y=600)

        self.selected_tests = []

        ctk.CTkLabel(self.new_patient_frame, text="* Double-Click to select a test", font=("Calibri", 16), text_color="blue").place(x=360, y=630)

        # Suggestion Treeview
        suggestion_tree_frame = Frame(self.new_patient_frame, bg="#F7F7F7")
        suggestion_tree_frame.place(x=220, y=720, width=600, height=150)
        suggestion_scrollbar = Scrollbar(suggestion_tree_frame)
        suggestion_scrollbar.pack(side=RIGHT, fill=Y)

        self.suggestion_tree = ttk.Treeview(suggestion_tree_frame, columns=("ID", "Code", "Name"), show="headings", height=4, yscrollcommand=suggestion_scrollbar.set)
        for col in ("ID", "Code", "Name"):
            self.suggestion_tree.heading(col, text=col)
            self.suggestion_tree.column(col, width=100 if col == "ID" else 160)
        self.suggestion_tree.pack(fill=BOTH, expand=True)
        suggestion_scrollbar.config(command=self.suggestion_tree.yview)

        self.search_entry.bind("<KeyRelease>", self.update_suggestions)
        self.suggestion_tree.bind("<Double-1>", self.select_test_from_tree)

        # Selected Test Treeview with remove
        selected_table_frame = Frame(self.new_patient_frame, bg="#F7F7F7")
        selected_table_frame.place(x=100, y=900, width=880, height=180)
        scrollbar = Scrollbar(selected_table_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.selected_table = ttk.Treeview(selected_table_frame, columns=("ID", "Code", "Name", "Normal", "Units", "Remove"),
                                           show="headings", yscrollcommand=scrollbar.set)
        for col, width in zip(("ID", "Code", "Name", "Normal", "Units", "Remove"), [60, 100, 160, 140, 100, 60]):
            self.selected_table.heading(col, text=col)
            self.selected_table.column(col, width=width, anchor="center")
        self.selected_table.pack(fill=BOTH, expand=True)
        scrollbar.config(command=self.selected_table.yview)

        self.selected_table.bind("<Button-1>", self.handle_remove_click)

    def create_returning_patient_tab_widgets(self):
    # Scrollable Canvas
        self.returning_canvas = Canvas(self.returning_patient_tab, bg="#F7F7F7", highlightthickness=0)
        self.returning_scrollbar = Scrollbar(self.returning_patient_tab, orient=VERTICAL, command=self.returning_canvas.yview)
        self.returning_frame = Frame(self.returning_canvas, bg="#F2F2F2")

        self.returning_frame.bind(
        "<Configure>",
            lambda e: self.returning_canvas.configure(
                scrollregion=self.returning_canvas.bbox("all")
            )   
        )

        self.returning_canvas.create_window((0, 0), window=self.returning_frame, anchor="nw", width=1040, height=1300)
        self.returning_canvas.configure(yscrollcommand=self.returning_scrollbar.set)
        self.returning_canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.returning_scrollbar.pack(side=RIGHT, fill=Y)

    # Enable mouse wheel scrolling
        self.returning_canvas.bind_all("<MouseWheel>", self._on_mousewheel_returning)




        # ---- RETURNING PATIENTS TAB - Search Section ----

    # Search Label
        ctk.CTkLabel(self.returning_frame, text="Search Patient:", font=("Calibri", 16)).place(x=70, y=40)

    # Search Entry
        self.returning_search_entry = ctk.CTkEntry(self.returning_frame, placeholder_text="Enter part of name...", width=300)
        self.returning_search_entry.place(x=220, y=40)
        
        self.returning_search_entry.bind("<KeyRelease>", self.update_patient_dropdown)

        # Patient Dropdown
        self.returning_patient_dropdown = ctk.CTkComboBox(self.returning_frame, values=[], width=300, state="readonly")
        self.returning_patient_dropdown.place(x=550, y=40)

        # Load Patient Button
        ctk.CTkButton(self.returning_frame, text="Load Patient", width=120, height=30, corner_radius=50,
                command=self.load_patient_details).place(x=880, y=40)
        


        
        # ---- Patient Details (Readonly Fields) ----

        # Patient ID
        ctk.CTkLabel(self.returning_frame, text="Patient ID:", font=("Calibri", 16)).place(x=70, y=100)
        self.returning_patient_id_label = ctk.CTkLabel(self.returning_frame, text="", font=("Calibri", 16), text_color="blue")
        self.returning_patient_id_label.place(x=160, y=100)

        # Registered By
        ctk.CTkLabel(self.returning_frame, text="Registered by:", font=("Calibri", 16)).place(x=300, y=100)
        self.returning_registered_by_dropdown = ctk.CTkComboBox(self.returning_frame, values=[], width=150, state="readonly")
        self.returning_registered_by_dropdown.place(x=430, y=100)

        # First Name
        ctk.CTkLabel(self.returning_frame, text="First Name:", font=("Calibri", 16)).place(x=70, y=160)
        self.returning_first_name_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_first_name_entry.place(x=160, y=160)

        # Last Name
        ctk.CTkLabel(self.returning_frame, text="Last Name:", font=("Calibri", 16)).place(x=420, y=160)
        self.returning_last_name_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_last_name_entry.place(x=530, y=160)

        # DOB
        ctk.CTkLabel(self.returning_frame, text="DOB:", font=("Calibri", 16)).place(x=70, y=220)
        self.returning_dob_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_dob_entry.place(x=160, y=220)

        # Gender
        ctk.CTkLabel(self.returning_frame, text="Gender:", font=("Calibri", 16)).place(x=450, y=220)
        self.returning_gender_dropdown = ctk.CTkComboBox(self.returning_frame, values=["Male", "Female", "Other"], width=150, state="readonly")
        self.returning_gender_dropdown.place(x=550, y=220)

        # Phone
        ctk.CTkLabel(self.returning_frame, text="Phone:", font=("Calibri", 16)).place(x=70, y=280)
        self.returning_phone_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_phone_entry.place(x=160, y=280)

        # Email
        ctk.CTkLabel(self.returning_frame, text="Email:", font=("Calibri", 16)).place(x=450, y=280)
        self.returning_email_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_email_entry.place(x=530, y=280)

        # Street Address
        ctk.CTkLabel(self.returning_frame, text="Street Address:", font=("Calibri", 16)).place(x=70, y=340)
        self.returning_street_entry = ctk.CTkEntry(self.returning_frame, width=400, state="readonly")
        self.returning_street_entry.place(x=230, y=340)

        # City
        ctk.CTkLabel(self.returning_frame, text="City:", font=("Calibri", 16)).place(x=670, y=340)
        self.returning_city_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_city_entry.place(x=750, y=340)

        # State
        ctk.CTkLabel(self.returning_frame, text="State:", font=("Calibri", 16)).place(x=70, y=400)
        self.returning_state_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_state_entry.place(x=160, y=400)

        # Zipcode
        ctk.CTkLabel(self.returning_frame, text="Zipcode:", font=("Calibri", 16)).place(x=450, y=400)
        self.returning_zipcode_entry = ctk.CTkEntry(self.returning_frame, width=200, state="readonly")
        self.returning_zipcode_entry.place(x=530, y=400)

    

 # ------------------ RETURNING PATIENT - TEST SELECTION ------------------

        ctk.CTkLabel(self.returning_frame, text="TEST SELECTION", font=("Calibri", 18, "bold")).place(x=470, y=480)

        ctk.CTkLabel(self.returning_frame, text="Selection Type:", font=("Calibri", 16)).place(x=70, y=550)
        self.returning_selection_type_dropdown = ctk.CTkComboBox(self.returning_frame, values=["test_id", "test_name"], width=120, state="readonly")
        self.returning_selection_type_dropdown.place(x=200, y=550)
        self.returning_selection_type_dropdown.set("test_name")

        self.returning_search_test_entry = ctk.CTkEntry(self.returning_frame, placeholder_text="Search test...", width=300)
        self.returning_search_test_entry.place(x=360, y=550)

        ctk.CTkButton(self.returning_frame, text="Clear", width=80, height=30, corner_radius=50,
        fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
        command=self.returning_clear_search).place(x=680, y=550)

        self.returning_selected_tests = []  # Initialize list to store selected tests

        ctk.CTkLabel(self.returning_frame, text="* Double-Click to select a test", font=("Calibri", 14), text_color="blue").place(x=360, y=590)

        # --- Suggestion Treeview ---
        suggestion_tree_frame = Frame(self.returning_frame, bg="#F7F7F7")
        suggestion_tree_frame.place(x=220, y=630, width=600, height=150)
        suggestion_scrollbar = Scrollbar(suggestion_tree_frame)
        suggestion_scrollbar.pack(side=RIGHT, fill=Y)

        self.returning_suggestion_tree = ttk.Treeview(suggestion_tree_frame, columns=("ID", "Code", "Name"), show="headings", height=4, yscrollcommand=suggestion_scrollbar.set)
        for col in ("ID", "Code", "Name"):
            self.returning_suggestion_tree.heading(col, text=col)
            self.returning_suggestion_tree.column(col, width=100 if col == "ID" else 160)
        self.returning_suggestion_tree.pack(fill=BOTH, expand=True)
        suggestion_scrollbar.config(command=self.returning_suggestion_tree.yview)

        # Bind search
        self.returning_search_test_entry.bind("<KeyRelease>", self.returning_update_suggestions)
        self.returning_suggestion_tree.bind("<Double-1>", self.returning_select_test_from_tree)

        # --- Selected Tests Treeview ---
        selected_tests_frame = Frame(self.returning_frame, bg="#F7F7F7")
        selected_tests_frame.place(x=100, y=900, width=880, height=180)
        scrollbar2 = Scrollbar(selected_tests_frame)
        scrollbar2.pack(side=RIGHT, fill=Y)

        self.returning_selected_table = ttk.Treeview(selected_tests_frame, columns=("ID", "Code", "Name", "Normal", "Units", "Remove"),
                                        show="headings", yscrollcommand=scrollbar2.set)
        for col, width in zip(("ID", "Code", "Name", "Normal", "Units", "Remove"), [60, 100, 160, 140, 100, 60]):
            self.returning_selected_table.heading(col, text=col)
            self.returning_selected_table.column(col, width=width, anchor="center")
        self.returning_selected_table.pack(fill=BOTH, expand=True)
        scrollbar2.config(command=self.returning_selected_table.yview)

        self.returning_selected_table.bind("<Button-1>", self.returning_handle_remove_click)

        # Total Test Count
        ctk.CTkLabel(self.returning_frame, text="Total Tests:", font=("Calibri", 16)).place(x=850, y=700)
        self.returning_test_count_label = ctk.CTkLabel(self.returning_frame, text="0", font=("Calibri", 16), text_color="blue")
        self.returning_test_count_label.place(x=950, y=700)


        # ---- RETURNING PATIENTS TAB - Buttons ----

    # Back Button
        ctk.CTkButton(self.returning_frame, text="Back", width=100, height=35, corner_radius=50,
        fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
        command=self.back_callback).place(x=100, y=1100)

    # Add Results Button
        ctk.CTkButton(self.returning_frame, text="Add Results", width=120, height=35, corner_radius=50,
                  fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
                  command=lambda: self.controller.show_frame(EnterTestResultsPage)).place(x=600, y=1100)

    # Register Button
        ctk.CTkButton(self.returning_frame, text="Register", width=100, height=35, corner_radius=50,
                  fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
                  command=self.returning_register_tests).place(x=450, y=1100)
    
    def _on_mousewheel_returning(self, event):
        self.returning_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def returning_clear_search(self):
        self.returning_search_test_entry.delete(0, 'end')

    def returning_update_suggestions(self, event=None):
        keyword = self.returning_search_test_entry.get().strip()
        for i in self.returning_suggestion_tree.get_children():
            self.returning_suggestion_tree.delete(i)
        if keyword:
            conn = connect_db()
            cursor = conn.cursor()
            if self.returning_selection_type_dropdown.get() == "test_id":
                cursor.execute("SELECT test_id, test_code, test_name, normal_values, units FROM diagnostic_test_info WHERE test_id LIKE %s", (f"%{keyword}%",))
            else:
                cursor.execute("SELECT test_id, test_code, test_name, normal_values, units FROM diagnostic_test_info WHERE test_name LIKE %s", (f"%{keyword}%",))
            results = cursor.fetchall()
            for test in results:
                if test not in self.returning_selected_tests:
                    self.returning_suggestion_tree.insert("", END, values=test)
            cursor.close()
            conn.close()

    def returning_select_test_from_tree(self, event=None):
        selected = self.returning_suggestion_tree.focus()
        values = self.returning_suggestion_tree.item(selected)['values']
        if values and values not in self.returning_selected_tests:
            self.returning_selected_tests.append(values)
            self.returning_selected_table.insert("", END, values=(*values, "❌"))
            self.returning_test_count_label.configure(text=str(len(self.returning_selected_tests)))

    def returning_handle_remove_click(self, event):
        region = self.returning_selected_table.identify("region", event.x, event.y)
        if region == "cell":
            col = self.returning_selected_table.identify_column(event.x)
            row_id = self.returning_selected_table.identify_row(event.y)
            if col == "#6":
                values = self.returning_selected_table.item(row_id)['values']
                if values[:-1] in self.returning_selected_tests:
                    self.returning_selected_tests.remove(values[:-1])
                    self.returning_selected_table.delete(row_id)
                    self.returning_test_count_label.configure(text=str(len(self.returning_selected_tests)))

    def returning_register_tests(self):
        if not self.returning_selected_tests:
            messagebox.showwarning("No Tests Selected", "Please select tests to register!")
            return

        selected_value = self.returning_patient_dropdown.get()
        if not selected_value:
            messagebox.showwarning("No Patient Selected", "Please select a patient!")
            return

        try:
            patient_id = selected_value.split(' - ')[0]
        except IndexError:
            messagebox.showerror("Format Error", "Selected value is not properly formatted.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

        # Step 1: Create a new report
            cursor.execute("""
                INSERT INTO patient_reports (report_status, file_path)
                VALUES (%s, %s)
            """, ("Pending", ""))
            conn.commit()

            report_id = cursor.lastrowid  # capture the newly created report_id

            # Step 2: Insert each selected test into ordered_tests
            for test in self.returning_selected_tests:
                test_id, test_code, test_name = test[0], test[1], test[2]
                cursor.execute("""
                INSERT INTO ordered_tests (patient_id, test_id, report_id, result_value)
                VALUES (%s, %s, %s, NULL)
            """, (patient_id, test_id, report_id))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"Tests registered successfully!\nReport ID: {report_id}")

        # Clear fields after success
            self.clear_returning_patient_fields()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))


    def update_patient_dropdown(self, event=None):
        keyword = self.returning_search_entry.get().strip()
        if keyword:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT patient_id, patient_first_name, patient_last_name
                FROM patient_details
                WHERE patient_first_name LIKE %s OR patient_last_name LIKE %s
            """, (f"%{keyword}%", f"%{keyword}%"))
            results = [f"{row[0]} - {row[1]} {row[2]}" for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            self.returning_patient_dropdown.configure(values=results)

    def load_patient_details(self):
        selected_value = self.returning_patient_dropdown.get()
        if not selected_value:
            messagebox.showwarning("No Patient Selected", "Please select a patient!")
            return

        try:
            patient_id = selected_value.split(' - ')[0]
        except IndexError:
            messagebox.showerror("Format Error", "Selected value is not properly formatted.")
            return

        conn = connect_db()
        cursor = conn.cursor()

    # Fetch patient details from database
        cursor.execute("""
            SELECT registered_by, patient_first_name, patient_last_name, date_of_birth, Gender, 
               Contact_Phone, patient_email, Street_Address, City, State, Zipcode
            FROM patient_details
            WHERE patient_id = %s
        """, (patient_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if not result:
            messagebox.showerror("Not Found", "Patient not found in the database!")
            return

    # Unpack result and populate fields
        (registered_by, first_name, last_name, dob, gender, phone, email, street, city, state, zipcode) = result

        self.returning_patient_id_label.configure(text=patient_id)
        self.returning_registered_by_dropdown.set(registered_by)
        self.returning_first_name_entry.configure(state="normal")
        self.returning_first_name_entry.delete(0, 'end')
        self.returning_first_name_entry.insert(0, first_name)
        self.returning_first_name_entry.configure(state="readonly")

        self.returning_last_name_entry.configure(state="normal")
        self.returning_last_name_entry.delete(0, 'end')
        self.returning_last_name_entry.insert(0, last_name)
        self.returning_last_name_entry.configure(state="readonly")

        self.returning_dob_entry.configure(state="normal")
        self.returning_dob_entry.delete(0, 'end')
        self.returning_dob_entry.insert(0, dob.strftime("%Y-%m-%d") if isinstance(dob, datetime) else dob)
        self.returning_dob_entry.configure(state="readonly")

        self.returning_gender_dropdown.set(gender)

        self.returning_phone_entry.configure(state="normal")
        self.returning_phone_entry.delete(0, 'end')
        self.returning_phone_entry.insert(0, phone)
        self.returning_phone_entry.configure(state="readonly")

        self.returning_email_entry.configure(state="normal")
        self.returning_email_entry.delete(0, 'end')
        self.returning_email_entry.insert(0, email)
        self.returning_email_entry.configure(state="readonly")

        self.returning_street_entry.configure(state="normal")
        self.returning_street_entry.delete(0, 'end')
        self.returning_street_entry.insert(0, street)
        self.returning_street_entry.configure(state="readonly")

        self.returning_city_entry.configure(state="normal")
        self.returning_city_entry.delete(0, 'end')
        self.returning_city_entry.insert(0, city)
        self.returning_city_entry.configure(state="readonly")

        self.returning_state_entry.configure(state="normal")
        self.returning_state_entry.delete(0, 'end')
        self.returning_state_entry.insert(0, state)
        self.returning_state_entry.configure(state="readonly")

        self.returning_zipcode_entry.configure(state="normal")
        self.returning_zipcode_entry.delete(0, 'end')
        self.returning_zipcode_entry.insert(0, zipcode)
        self.returning_zipcode_entry.configure(state="readonly")



    def clear_search(self):
        self.search_entry.delete(0, 'end')

    def update_suggestions(self, event=None):
        keyword = self.search_entry.get().strip()
        for i in self.suggestion_tree.get_children():
            self.suggestion_tree.delete(i)
        if keyword:
            conn = connect_db()
            cursor = conn.cursor()
            if self.selection_type_dropdown.get() == "test_id":
                cursor.execute("SELECT test_id, test_code, test_name, normal_values, units FROM diagnostic_test_info WHERE test_id LIKE %s", (f"%{keyword}%",))
            else:
                cursor.execute("SELECT test_id, test_code, test_name, normal_values, units FROM diagnostic_test_info WHERE test_name LIKE %s", (f"%{keyword}%",))
            results = cursor.fetchall()
            for test in results:
                if test not in self.selected_tests:
                    self.suggestion_tree.insert("", END, values=test)
            cursor.close()
            conn.close()

    def select_test_from_tree(self, event=None):
        selected = self.suggestion_tree.focus()
        values = self.suggestion_tree.item(selected)['values']
        if values and values not in self.selected_tests:
            self.selected_tests.append(values)
            self.selected_table.insert("", END, values=(*values, "❌"))
            self.test_count_label.configure(text=str(len(self.selected_tests)))

    def handle_remove_click(self, event):
        region = self.selected_table.identify("region", event.x, event.y)
        if region == "cell":
            col = self.selected_table.identify_column(event.x)
            row_id = self.selected_table.identify_row(event.y)
            if col == "#6":
                values = self.selected_table.item(row_id)['values']
                if values[:-1] in self.selected_tests:
                    self.selected_tests.remove(values[:-1])
                    self.selected_table.delete(row_id)
                    self.test_count_label.configure(text=str(len(self.selected_tests)))
          
 
    def clear_all_fields(self):
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.dob_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.street_entry.delete(0, 'end')
        self.city_entry.delete(0, 'end')
        self.state_entry.delete(0, 'end')
        self.zipcode_entry.delete(0, 'end')

        self.registered_by_dropdown.set("")
        self.gender_dropdown.set("")
        self.selection_type_dropdown.set("test_name")
        self.search_entry.delete(0, 'end')

        # Clear selected tests
        for item in self.selected_table.get_children():
            self.selected_table.delete(item)
        self.selected_tests.clear()
        self.test_count_label.configure(text="0")

    def validate_inputs(self):
        is_valid = True

        if not self.first_name_entry.get().strip():
            self.first_name_error.configure(text="First Name Required")
            is_valid = False
        if not self.last_name_entry.get().strip():
            self.last_name_error.configure(text="Last Name Required")
            is_valid = False
        if not self.email_entry.get().strip():
            self.email_error.configure(text="Email Required")
            is_valid = False
        if not self.phone_entry.get().strip():
            self.phone_error.configure(text="Phone Required")
            is_valid = False
        if not self.city_entry.get().strip():
            self.city_error.configure(text="City Required")
            is_valid = False
        if not self.state_entry.get().strip():
            self.state_error.configure(text="State Required")
            is_valid = False
        if not self.registered_by_dropdown.get().strip():
            self.registered_by_error.configure(text="Registered By Required")
            is_valid = False

        return is_valid


    def new_patient_register_tests(self):
        if not self.selected_tests:
            messagebox.showwarning("No Tests Selected", "Please select tests to register!")
            return

    # Validate inputs before proceeding
        if not self.validate_inputs():
            return

    # Collect data from fields
        patient_data = {
        "first_name": self.first_name_entry.get().strip(),
        "last_name": self.last_name_entry.get().strip(),
        "email": self.email_entry.get().strip(),
        "dob": self.dob_entry.get().strip(),
        "gender": self.gender_dropdown.get().strip(),
        "street": self.street_entry.get().strip(),
        "city": self.city_entry.get().strip(),
        "state": self.state_entry.get().strip(),
        "zipcode": self.zipcode_entry.get().strip(),
        "phone": self.phone_entry.get().strip(),
        "registered_by": self.registered_by_dropdown.get().strip(),
        }

        try:
            conn = connect_db()
            cursor = conn.cursor()

    # Step 1: Insert the new patient into the database
            query = """
                INSERT INTO patient_details (
                registered_by, patient_first_name, patient_last_name, patient_email, 
                date_of_birth, Gender, Street_Address, City, State, Zipcode, Contact_Phone
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                patient_data["registered_by"], patient_data["first_name"], patient_data["last_name"],
                patient_data["email"], patient_data["dob"], patient_data["gender"],
                patient_data["street"], patient_data["city"], patient_data["state"],
                patient_data["zipcode"], patient_data["phone"]
            ))
            conn.commit()

            # Get the newly created patient_id
            patient_id = cursor.lastrowid

            # Step 2: Create a new report
            cursor.execute("""
                INSERT INTO patient_reports (report_status, file_path)
                VALUES (%s, %s)
            """, ("Pending", ""))
            conn.commit()

            # Get the newly created report_id
            report_id = cursor.lastrowid

            # Step 3: Insert each selected test into ordered_tests
            for test in self.selected_tests:
                test_id, test_code, test_name = test[0], test[1], test[2]
                cursor.execute("""
                        INSERT INTO ordered_tests (patient_id, test_id, report_id, result_value)
                        VALUES (%s, %s, %s, NULL)
                """, (patient_id, test_id, report_id))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"Patient registered successfully!\nReport ID: {report_id}")

        # Clear all fields in the New Patient tab
            self.clear_all_fields()

        # Update the patient ID label
            self.patient_id_label.configure(text=str(self.get_new_patient_id()))

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))

    def clear_returning_patient_fields(self):
            self.returning_patient_id_label.configure(text="")
            self.returning_registered_by_dropdown.set("")
            self.returning_first_name_entry.configure(state="normal")
            self.returning_last_name_entry.configure(state="normal")
            self.returning_dob_entry.configure(state="normal")
            self.returning_phone_entry.configure(state="normal")
            self.returning_email_entry.configure(state="normal")
            self.returning_street_entry.configure(state="normal")
            self.returning_city_entry.configure(state="normal")
            self.returning_state_entry.configure(state="normal")
            self.returning_zipcode_entry.configure(state="normal")

            self.returning_first_name_entry.delete(0, 'end')
            self.returning_last_name_entry.delete(0, 'end')
            self.returning_dob_entry.delete(0, 'end')
            self.returning_phone_entry.delete(0, 'end')
            self.returning_email_entry.delete(0, 'end')
            self.returning_street_entry.delete(0, 'end')
            self.returning_city_entry.delete(0, 'end')
            self.returning_state_entry.delete(0, 'end')
            self.returning_zipcode_entry.delete(0, 'end')

            self.returning_first_name_entry.configure(state="readonly")
            self.returning_last_name_entry.configure(state="readonly")
            self.returning_dob_entry.configure(state="readonly")
            self.returning_phone_entry.configure(state="readonly")
            self.returning_email_entry.configure(state="readonly")
            self.returning_street_entry.configure(state="readonly")
            self.returning_city_entry.configure(state="readonly")
            self.returning_state_entry.configure(state="readonly")
            self.returning_zipcode_entry.configure(state="readonly")

            self.returning_selected_tests.clear()
            for item in self.returning_selected_table.get_children():
                self.returning_selected_table.delete(item)
            self.returning_test_count_label.configure(text="0")
    
    def clear_error(self, label):
            label.configure(text="")

