import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
from PIL import Image

# --------- DATABASE CONNECTION ----------
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Nihalreddy@31",
        database="project_698"
    )

class ManageStaffPage(ctk.CTkFrame):
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
        # -------- HEADER --------
        header_frame = ctk.CTkFrame(self, fg_color="#D0D0D0", height=80)
        header_frame.pack(fill="x")

        self.username_label = ctk.CTkLabel(header_frame, text=f"Username: {self.logged_in_user}",
                                           font=("Calibri", 14), text_color="black")
        self.username_label.place(x=20, y=10)

        ctk.CTkLabel(header_frame, text=f"Date: {self.login_date}", font=("Calibri", 14),
                     text_color="black").place(x=20, y=35)

        ctk.CTkLabel(header_frame, text="MADHAVI DIAGNOSTIC CENTER",
                     font=("Calibri", 24, "bold"), text_color="black").place(relx=0.5, y=20, anchor="center")

        self.time_label = ctk.CTkLabel(header_frame, text="", font=("Calibri", 14), text_color="black")
        self.time_label.place(x=500, y=50)

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

        # -------- TITLE --------
        ctk.CTkLabel(self, text="MANAGE STAFF", font=("Calibri", 20, "bold")).place(relx=0.5, y=120, anchor="center")

        # -------- ADD STAFF --------
        ctk.CTkLabel(self, text="Username:").place(x=300, y=170)
        self.entry_username = ctk.CTkEntry(self, width=180)
        self.entry_username.place(x=380, y=170)

        ctk.CTkLabel(self, text="Role:").place(x=600, y=170)
        self.role_combo = ctk.CTkComboBox(self, values=["Lab Technician", "Lab Assistant"],
                                          width=180, state="readonly")
        self.role_combo.place(x=650, y=170)

        ctk.CTkLabel(self, text="First name:").place(x=300, y=210)
        self.entry_fname = ctk.CTkEntry(self, width=180)
        self.entry_fname.place(x=380, y=210)

        ctk.CTkLabel(self, text="Last name:").place(x=600, y=210)
        self.entry_lname = ctk.CTkEntry(self, width=180)
        self.entry_lname.place(x=680, y=210)

        ctk.CTkLabel(self, text="Password:").place(x=300, y=250)
        self.entry_password = ctk.CTkEntry(self, width=180, show="*")
        self.entry_password.place(x=380, y=250)

        ctk.CTkButton(self, text="Add Staff", width=120, font=("Calibri", 14),
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
                      command=self.add_staff, corner_radius=50).place(x=580, y=250)

        # -------- REMOVE STAFF --------
        ctk.CTkLabel(self, text="REMOVE STAFF", font=("Calibri", 20, "bold")).place(relx=0.5, y=330, anchor="center")

        ctk.CTkLabel(self, text="Username:").place(x=300, y=370)
        self.remove_username = ctk.CTkEntry(self, width=300, placeholder_text="Username to remove")
        self.remove_username.place(x=380, y=370)

        ctk.CTkButton(self, text="Remove Staff", width=140, font=("Calibri", 14),
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
                      command=self.remove_staff, corner_radius=50).place(x=700, y=370)

        # -------- BACK BUTTON --------
        ctk.CTkButton(self, text="Back", width=100,height=35, corner_radius=50,
                      fg_color="#D0D0D0", text_color="black", hover_color="#C0C0C0",
                      command=self.back_callback).place(x=100, y=600)

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)

    def add_staff(self):
        uname = self.entry_username.get()
        passwd = self.entry_password.get()
        fname = self.entry_fname.get()
        lname = self.entry_lname.get()
        role = self.role_combo.get()

        if not (uname and passwd and fname and lname and role):
            messagebox.showerror("Input Error", "All fields are required.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO staff (staff_username, password, role, staff_first_name, staff_last_name)
                VALUES (%s, %s, %s, %s, %s)
            """, (uname, passwd, role, fname, lname))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", f"Staff '{uname}' added successfully.")
            self.clear_add_fields()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def remove_staff(self):
        uname = self.remove_username.get()
        if not uname:
            messagebox.showerror("Input Error", "Please enter a username to remove.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM staff WHERE staff_username = %s", (uname,))
            conn.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Staff '{uname}' removed successfully.")
            else:
                messagebox.showwarning("Not Found", f"No staff found with username '{uname}'.")
            cursor.close()
            conn.close()
            self.remove_username.delete(0, "end")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    def clear_add_fields(self):
        self.entry_username.delete(0, "end")
        self.entry_password.delete(0, "end")
        self.entry_fname.delete(0, "end")
        self.entry_lname.delete(0, "end")
        self.role_combo.set("")

    def reset_fields(self):
        """Update the username in the header when page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.username_label.configure(text=f"Username: {self.logged_in_user}")
        self.clear_add_fields()
        self.remove_username.delete(0, "end")
