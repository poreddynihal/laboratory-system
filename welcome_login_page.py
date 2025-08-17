import customtkinter as ctk
from PIL import Image
import mysql.connector
from tkinter import messagebox

class WelcomeLoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#F2F2F2")
        self.build_ui()
        self.welcome_frame.place(x=0, y=0)  # ✅ Show the welcome screen by default



    def connect_db(self):
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Nihalreddy@31",
            database="project_698"
        )

    def build_ui(self):
        # Welcome Page
        self.welcome_frame = ctk.CTkFrame(self, width=1080, height=720, fg_color="#F2F2F2")
        self.welcome_frame.place(x=0, y=0)

        try:
            img = Image.open("background.jpg").resize((540, 720), Image.LANCZOS)
            self.bg_image = ctk.CTkImage(light_image=img, size=(540, 720))
            image_label = ctk.CTkLabel(self.welcome_frame, image=self.bg_image, text="", width=540, height=720)
            image_label.place(x=540, y=0)
        except Exception as e:
            print("Error loading image:", e)

        left_frame = ctk.CTkFrame(self.welcome_frame, width=540, height=720, fg_color="#F2F2F2")
        left_frame.place(x=0, y=0)

        ctk.CTkLabel(left_frame, text="Welcome to Your Trusted\nClinical Laboratory\nSystem",
                     font=("Calibri", 40), text_color="black", justify="left").place(x=50, y=250)

        ctk.CTkButton(left_frame, text="Sign In", font=("Calibri", 20, "bold"),
                      fg_color="#E0E0E0", hover_color="#D9D9D9", text_color="black",
                      width=180, height=50, corner_radius=50, command=self.show_login_page).place(x=160, y=500)

        # Login Page
        self.login_frame = ctk.CTkFrame(self, width=1080, height=720, fg_color="#F2F2F2")

        ctk.CTkLabel(self.login_frame, text="MADHAVI DIAGNOSTIC CENTER",
                     font=("Calibri", 48, "bold"), text_color="black", fg_color="#D0D0D0", width=1080, height=80).place(x=0, y=0)

        center_frame = ctk.CTkFrame(self.login_frame, fg_color="#F2F2F2", width=1000, height=600)
        center_frame.place(relx=0.5, rely=0.52, anchor="center")

        login_fields = ctk.CTkFrame(center_frame, fg_color="#F2F2F2", width=480, height=500)
        login_fields.pack(side="left", padx=30, pady=30)

        ctk.CTkLabel(login_fields, text="Login Details", font=("Calibri", 32, "bold"), text_color="black").pack(pady=20)

        self.username_entry = ctk.CTkEntry(login_fields, placeholder_text="Username", font=("Calibri", 28),
                                           width=420, height=76, corner_radius=50)
        self.username_entry.pack(pady=10)

        self.username_error_label = ctk.CTkLabel(login_fields, text="", font=("Calibri", 14), text_color="red", anchor='w')
        self.username_error_label.pack(pady=(5, 0), padx=(15,0), fill="x")

        # Password Frame — same height as username entry
        password_frame = ctk.CTkFrame(login_fields, width=420, height=76, fg_color="#F2F2F2", corner_radius=50)
        password_frame.pack()

    # Password Entry
        self.password_entry = ctk.CTkEntry(password_frame, placeholder_text="Password", font=("Calibri", 28),
                                   show="*", width=420, height=76, corner_radius=50)
        self.password_entry.pack()

        # Toggle Button — vertically centered and aligned right
        self.toggle_button = ctk.CTkButton(password_frame, text="show", width=40, height=30, fg_color="#F7F7F7",
                                   font=("Calibri", 16), command=self.toggle_password)
        self.toggle_button.place(x=360, y=25)

        # Error Label — under the frame (not inside it)
        self.password_error_label = ctk.CTkLabel(login_fields, text="", font=("Calibri", 14), text_color="red", anchor="w")
        self.password_error_label.pack(pady=(0, 5), padx=(15,0), fill="x")



        ctk.CTkButton(login_fields, text="Login", font=("Calibri", 24, "bold"),
                      fg_color="#E0E0E0", hover_color="#D9D9D9", text_color="black",
                      width=420, height=76, corner_radius=50,
                      command=self.check_login).pack(pady=20)

        try:
            login_img = Image.open("login_art.png").resize((450, 400), Image.LANCZOS)
            self.login_ctk_image = ctk.CTkImage(light_image=login_img, size=(450, 400))
            ctk.CTkLabel(center_frame, image=self.login_ctk_image, text="", fg_color="#F7F7F7").pack(side="right", padx=30)
        except Exception as e:
            print("Error loading login image:", e)

        ctk.CTkButton(self.login_frame, text="Back", font=("Calibri", 14, "bold"),
                      fg_color="#E0E0E0", hover_color="#D9D9D9", text_color="black",
                      width=100, height=40, corner_radius=50,
                      command=self.show_welcome_page).place(x=20, y=670)

    def show_login_page(self):
        self.welcome_frame.place_forget()
        self.login_frame.place(x=0, y=0)

    def show_welcome_page(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.username_error_label.configure(text="")
        self.password_error_label.configure(text="")
        self.login_frame.place_forget()
        self.welcome_frame.place(x=0, y=0)

    def toggle_password(self):
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
            self.toggle_button.configure(text="hide")
        else:
            self.password_entry.configure(show="*")
            self.toggle_button.configure(text="show")

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Reset error messages
        self.username_error_label.configure(text="")
        self.password_error_label.configure(text="")

        # Validation
        if not username:
            self.username_error_label.configure(text="Username required")
            return
        if not password:
            self.password_error_label.configure(text="Password required")
            return

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT password, role FROM staff WHERE staff_username = %s", (username,))
            result = cursor.fetchone()
        except Exception as e:
            print("Database error:", e)
            return

        if result is None:
            self.username_error_label.configure(text="User not found!")
        elif result[0] != password:
            self.password_error_label.configure(text="Wrong password!")
        else:
            role = result[1]
            self.controller.username = username
            self.controller.user_role = role
            self.controller.show_role_based_menu()

        cursor.close()
        conn.close()
