import customtkinter as ctk
from PIL import Image
from datetime import datetime
from welcome_login_page import WelcomeLoginPage
from patient_registration_new import PatientRegistrationPage
from enter_results_new import EnterTestResultsPage
from add_select_tests_new import AddSelectTestsPage
from report_generation_new import GenerateReportsPage
from update_delete_details_new import UpdateDeletePatientPage
from add_remove_staff_new import ManageStaffPage



class LabTechMenu(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.main_loaded = False

    def load_ui(self):
        if self.main_loaded:
            return

        self.configure(fg_color="#F7F7F7")

        # Get user info
        username = self.controller.username or "Unknown"
        login_date = datetime.now().strftime("%m/%d/%Y")

        # ---------------- HEADER ----------------
        header_frame = ctk.CTkFrame(self, fg_color="#D0D0D0", width=1080, height=80)
        header_frame.place(x=0, y=0)

        ctk.CTkLabel(header_frame, text=f"Username: {username}", font=("Calibri", 14, "bold"),
                     text_color="black").place(x=20, y=10)
        ctk.CTkLabel(header_frame, text=f"Date: {login_date}", font=("Calibri", 14, "bold"),
                     text_color="black").place(x=20, y=35)

        ctk.CTkLabel(header_frame, text="MADHAVI DIAGNOSTIC CENTER", font=("Calibri", 36, "bold"),
                     text_color="black").place(relx=0.5, y=20, anchor="center")

        self.time_label = ctk.CTkLabel(header_frame, text="", font=("Calibri", 14), text_color="black")
        self.time_label.place(relx=0.5, y=60, anchor="center")
        self.update_time()

        # ---------------- MAIN MENU ----------------
        ctk.CTkLabel(self, text="MAIN MENU", font=("Calibri", 30), text_color="black").place(relx=0.5, y=150, anchor="center")

        # Load Icons
        img_folder = ctk.CTkImage(light_image=Image.open("patient_registration.png"), size=(60, 60))
        img_flask = ctk.CTkImage(light_image=Image.open("enter_results.png"), size=(60, 60))
        img_check = ctk.CTkImage(light_image=Image.open("tests.png"), size=(60, 60))
        img_report = ctk.CTkImage(light_image=Image.open("reports.png"), size=(60, 60))
        img_edit = ctk.CTkImage(light_image=Image.open("update_delete.png"), size=(60, 60))
        img_staff = ctk.CTkImage(light_image=Image.open("delete_staff.png"), size=(60, 60))
        logout_img = ctk.CTkImage(light_image=Image.open("logout.png"), size=(30, 30))

        # Button Data
        buttons_data = [
            ("Patient Registration", img_folder),
            ("Enter Test Results", img_flask),
            ("Add/Select\nAvailable Tests", img_check),
            ("Generate Reports", img_report),
            ("Update/Delete\nPatient Details", img_edit),
            ("Add/Remove\nStaff", img_staff),
        ]

        x_positions = [160, 440, 720]
        y_positions = [250, 440]

        for i, (label, icon) in enumerate(buttons_data):
            x = x_positions[i % 3]
            y = y_positions[i // 3]

            if label == "Patient Registration":
                button_command = lambda: self.controller.show_frame(PatientRegistrationPage)
            elif label == "Enter Test Results":
                button_command = lambda: self.controller.show_frame(EnterTestResultsPage)  # Replace with actual navigation
            elif label == "Add/Select\nAvailable Tests":
                button_command = lambda: self.controller.show_frame(AddSelectTestsPage)
            elif label == "Generate Reports":
                button_command = lambda: self.controller.show_frame(GenerateReportsPage)  # Replace with actual navigation
            elif label == "Update/Delete\nPatient Details":
                button_command = lambda: self.controller.show_frame(UpdateDeletePatientPage)  # Replace with actual navigation
            elif label == "Add/Remove\nStaff":
                button_command = lambda: self.controller.show_frame(ManageStaffPage)  # Replace with actual navigation
            else:
                button_command = None

            ctk.CTkButton(self, text=label, image=icon, compound="top", width=160, height=140, corner_radius=25,
                        font=("Calibri", 14, "bold"), fg_color="#E0E0E0", hover_color="#D0D0D0", text_color="black",
                        command=button_command
                        ).place(x=x, y=y)

        # Logout Button
        ctk.CTkButton(header_frame, text="", image=logout_img, width=40, height=40,
                      fg_color="transparent", hover_color="#CCCCCC",
                      command=self.controller.logout_user
                      ).place(x=1020, y=20)

        self.main_loaded = True

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)
