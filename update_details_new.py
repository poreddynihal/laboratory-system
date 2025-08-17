import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import mysql.connector
from PIL import Image

# ---------------- DATABASE CONNECTION ------------------
def connect_db():
    return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Nihalreddy@31",
            database="project_698"
    )

class UpdatePatientPage(ctk.CTkFrame):
    def __init__(self, parent, controller, back_callback=None):
        super().__init__(parent)
        self.controller = controller
        self.back_callback = back_callback

        self.selected_patient_id = None
        self.configure(fg_color="#F7F7F7")

        self.logged_in_user = self.controller.username or "Unknown"
        self.login_date = datetime.now().strftime("%m/%d/%Y")

        self.create_widgets()
        self.update_time()

    def create_widgets(self):
        # ---------- Header ----------
        self.header = ctk.CTkFrame(self, fg_color="#D0D0D0", height=60)
        self.header.pack(fill="x")

        self.username_label = ctk.CTkLabel(self.header, text=f"Username: {self.logged_in_user}",
                                           font=("Calibri", 14), text_color="black")
        self.username_label.place(x=20, y=10)

        ctk.CTkLabel(self.header, text=f"Date: {self.login_date}", font=("Calibri", 14),
                     text_color="black").place(x=20, y=35)

        ctk.CTkLabel(self.header, text="MADHAVI DIAGNOSTIC CENTER",
                     font=("Calibri", 24, "bold"), text_color="black").place(relx=0.5, y=20, anchor="center")

        self.time_label = ctk.CTkLabel(self.header, text="", font=("Calibri", 14), text_color="black")
        self.time_label.place(relx=0.5, y=50, anchor='center')

        try:
            logout_image = Image.open("logout.png").resize((30, 30))
            logout_icon = ctk.CTkImage(light_image=logout_image, dark_image=logout_image, size=(30, 30))
            logout_button = ctk.CTkButton(self.header, image=logout_icon, text="",
                                          command=self.controller.logout_user,
                                          width=40, height=40, fg_color="transparent",
                                          hover_color="#CCCCCC")
            logout_button.place(x=1020, y=20)
        except Exception as e:
            print("Logout icon error:", e)
        # -------- SEARCH BAR --------
        ctk.CTkLabel(self, text="Search Patient:", font=("Calibri", 14)).place(x=250, y=100)
        self.search_entry = ctk.CTkEntry(self, width=400, placeholder_text="Enter first or last name")
        self.search_entry.place(x=380, y=100)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        ctk.CTkButton(self, text="Clear", command=self.clear_fields, width=80,
                      fg_color="#D9D9D9", text_color="black", corner_radius=50).place(x=800, y=100)

        # Suggestion Frame
        self.suggestion_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", width=400, height=80)
        self.suggestion_canvas = ctk.CTkCanvas(self.suggestion_frame, bg="#FFFFFF", highlightthickness=0, width=400, height=80)
        self.scrollbar = ctk.CTkScrollbar(self.suggestion_frame, command=self.suggestion_canvas.yview)
        self.scrollable_inner = ctk.CTkFrame(self.suggestion_canvas, fg_color="#FFFFFF")

        self.suggestion_canvas.create_window((0, 0), window=self.scrollable_inner, anchor="nw")
        self.suggestion_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.suggestion_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.suggestion_frame.place_forget()

        # -------- FORM FIELDS --------
        self.fname_entry = ctk.CTkEntry(self, width=200)
        self.lname_entry = ctk.CTkEntry(self, width=200)
        self.dob_entry = ctk.CTkEntry(self, width=100)
        self.gender_combobox = ctk.CTkComboBox(self, values=["Male", "Female", "Other"], state="readonly", width=100)
        self.phone_entry = ctk.CTkEntry(self, width=200)
        self.email_entry = ctk.CTkEntry(self, width=200)
        self.address_entry = ctk.CTkEntry(self, width=200)
        self.city_entry = ctk.CTkEntry(self, width=150)
        self.state_entry = ctk.CTkEntry(self, width=120)
        self.zipcode_entry = ctk.CTkEntry(self, width=100)

        self.entries = [self.fname_entry, self.lname_entry, self.dob_entry, self.gender_combobox,
                        self.phone_entry, self.email_entry, self.address_entry, self.city_entry,
                        self.state_entry, self.zipcode_entry]

        labels = ["First name:", "Last name:", "DOB:", "Gender:", "Phone:", "Email:",
                  "Street Address:", "City:", "State:", "Zipcode:"]
        positions = [(120, 320), (440, 320), (120, 370), (440, 370),
                     (120, 420), (440, 420), (120, 470), (440, 470), (720, 470), (120, 520)]

        for label, entry, (x, y) in zip(labels, self.entries, positions):
            ctk.CTkLabel(self, text=label, font=("Calibri", 14)).place(x=x+5, y=y)
            entry.place(x=x+120, y=y)

        # -------- BUTTONS --------
        ctk.CTkButton(self, text="Update", command=self.update_patient,
                      width=100, fg_color="#D9D9D9", text_color="black", corner_radius=50).place(x=500, y=580)

        ctk.CTkButton(self, text="Back", command=self.back_callback,
                      width=100, fg_color="#D0D0D0", text_color="black", corner_radius=50).place(x=100, y=660)

    def update_time(self):
        self.time_label.configure(text=f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.after(1000, self.update_time)


    def clear_fields(self):
        self.search_entry.delete(0, "end")
        self.suggestion_frame.place_forget()
        for field in self.entries:
            if isinstance(field, ctk.CTkEntry):
                field.delete(0, "end")
            elif isinstance(field, ctk.CTkComboBox):
                field.set("")
        self.selected_patient_id = None

    def on_search(self, event=None):
        keyword = self.search_entry.get().strip()
        for widget in self.scrollable_inner.winfo_children():
            widget.destroy()

        if keyword:
            results = self.fetch_matching_patients(keyword)
            if results:
                for pid, fname, lname in results:
                    btn = ctk.CTkButton(self.scrollable_inner, text=f"{fname} {lname}",
                                        text_color="black", fg_color="#E0F7FA", hover_color="#B2EBF2",
                                        width=380, anchor="w",
                                        command=lambda p=pid: self.load_patient_details(p))
                    btn.pack(fill="x", padx=5, pady=2)
                self.suggestion_frame.place(x=230, y=130)
                self.scrollable_inner.update_idletasks()
                self.suggestion_canvas.configure(scrollregion=self.suggestion_canvas.bbox("all"))
            else:
                self.suggestion_frame.place_forget()
        else:
            self.suggestion_frame.place_forget()

    def fetch_matching_patients(self, keyword):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT patient_id, patient_first_name, patient_last_name 
            FROM patient_details
            WHERE patient_first_name LIKE %s OR patient_last_name LIKE %s
        """, (f"{keyword}%", f"{keyword}%"))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def load_patient_details(self, pid):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient_details WHERE patient_id = %s", (pid,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if data:
            self.fname_entry.delete(0, 'end')
            self.lname_entry.delete(0, 'end')
            self.dob_entry.delete(0, 'end')
            self.gender_combobox.set(data[7])
            self.phone_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.address_entry.delete(0, 'end')
            self.city_entry.delete(0, 'end')
            self.state_entry.delete(0, 'end')
            self.zipcode_entry.delete(0, 'end')

            self.fname_entry.insert(0, data[3])
            self.lname_entry.insert(0, data[4])
            self.dob_entry.insert(0, str(data[6]))
            self.phone_entry.insert(0, data[12])
            self.email_entry.insert(0, data[5])
            self.address_entry.insert(0, data[8])
            self.city_entry.insert(0, data[9])
            self.state_entry.insert(0, data[10])
            self.zipcode_entry.insert(0, data[11])

            self.search_entry.delete(0, 'end')
            self.suggestion_frame.place_forget()
            self.selected_patient_id = pid

    def update_patient(self):
        if not self.selected_patient_id:
            messagebox.showwarning("No patient", "Please select a patient to update.")
            return
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patient_details
                SET patient_first_name=%s, patient_last_name=%s, date_of_birth=%s, Gender=%s,
                    Contact_Phone=%s, patient_email=%s, Street_Address=%s, City=%s, State=%s, Zipcode=%s
                WHERE patient_id=%s
            """, (
                self.fname_entry.get(), self.lname_entry.get(), self.dob_entry.get(), self.gender_combobox.get(),
                self.phone_entry.get(), self.email_entry.get(), self.address_entry.get(), self.city_entry.get(),
                self.state_entry.get(), self.zipcode_entry.get(), self.selected_patient_id
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Patient record updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_fields(self):
        """Update the username in the header when page is shown."""
        self.logged_in_user = self.controller.username or "Unknown"
        self.username_label.configure(text=f"Username: {self.logged_in_user}")
        self.clear_fields()

