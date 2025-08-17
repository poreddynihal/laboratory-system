import customtkinter as ctk
from tkinter import messagebox  # for confirmation popup
from welcome_login_page import WelcomeLoginPage
from mainmenu_labtech import LabTechMenu
from mainmenu_labassist import LabAssistantMenu

# Importing other pages
from patient_registration_new import PatientRegistrationPage
from enter_results_new import EnterTestResultsPage
from add_select_tests_new import AddSelectTestsPage
from available_tests_new import ViewAvailableTestsPage
from report_generation_new import GenerateReportsPage
from update_delete_details_new import UpdateDeletePatientPage
from update_details_new import UpdatePatientPage
from add_remove_staff_new import ManageStaffPage



class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Madhavi Diagnostic Center")
        self.geometry("1080x720")
        self.resizable(False, False)

        # Store global user data
        self.username = None
        self.user_role = None

        # Page container
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Register and preload pages
        self.frames = {}
        for Page in (
            WelcomeLoginPage,
            LabTechMenu,
            LabAssistantMenu,
            PatientRegistrationPage,
            EnterTestResultsPage,
            AddSelectTestsPage,
            ViewAvailableTestsPage,
            GenerateReportsPage,
            UpdateDeletePatientPage,
            UpdatePatientPage,
            ManageStaffPage,
        ):
            if Page == PatientRegistrationPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == EnterTestResultsPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == AddSelectTestsPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == ViewAvailableTestsPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == GenerateReportsPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == UpdateDeletePatientPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == UpdatePatientPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            elif Page == ManageStaffPage:
                frame = Page(self.container, self, back_callback=self.show_role_based_menu)
            else:
                frame = Page(self.container, self)
            self.frames[Page] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeLoginPage)

    def show_frame(self, page_class):
        """Raise the specified frame to the front."""
        frame = self.frames[page_class]
        if hasattr(frame, "reset_fields"):
            frame.reset_fields()  # Call reset_fields if the page has it
        frame.tkraise()

    def login_user(self, username, role):
        """Handle user login and navigate to the appropriate menu."""
        self.username = username  # Set the logged-in username
        self.user_role = role  # Set the user role
        if role == "Lab Technician":
            self.show_frame(LabTechMenu)
        elif role == "Lab Assistant":
            self.show_frame(LabAssistantMenu)

    def show_role_based_menu(self):
        """Navigate to the role-specific main menu after login."""
        if self.user_role == "Lab Technician":
            self.frames[LabTechMenu].load_ui()
            self.show_frame(LabTechMenu)
        elif self.user_role == "Lab Assistant":
            self.frames[LabAssistantMenu].load_ui()
            self.show_frame(LabAssistantMenu)

    def logout_user(self):
        """Handles logout: confirmation, cleanup, and return to welcome."""
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if not answer:
            return

        # Clear login data
        welcome_page = self.frames[WelcomeLoginPage]
        welcome_page.username_entry.delete(0, "end")
        welcome_page.password_entry.delete(0, "end")
        welcome_page.username_error_label.configure(text="")
        welcome_page.password_error_label.configure(text="")
        welcome_page.show_welcome_page()

        # Clear session state
        self.username = None
        self.user_role = None

        # Smooth return to welcome screen
        self.show_frame(WelcomeLoginPage)

    
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = App()
    app.mainloop()