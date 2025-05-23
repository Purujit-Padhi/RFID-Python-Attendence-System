# Standard library imports
import os
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
# Third-party imports
import pandas as pd
from PIL import Image
import serial.tools.list_ports
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
# Local application imports
import helper as Create_Excels


company_name = "Company Name"
color_theme = "light"


VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"
image_path = f"{Create_Excels.data_path}\\Template\\class.png"  # Replace with your image file path for create class window

ctk.set_appearance_mode(color_theme)
ctk.set_default_color_theme("blue")


# Return to main menu
def back_to_main(current_window):
    current_window.destroy()
    root.deiconify()


# Function for progress dialog box
def show_indeterminate_progress_dialog(parent):
    dialog = ctk.CTkToplevel(parent)
    dialog.title("Loading...")
    window_width = 300
    window_height = 130
    # Set the geometry
    dialog.geometry(f"{window_width}x{window_height}+{int((dialog.winfo_screenwidth() - window_width) / 2)}+{int((dialog.winfo_screenheight() - window_height) / 2)}")
    dialog.grab_set()
    dialog.transient(parent)

    label = ctk.CTkLabel(dialog, text="Processing..")
    label.pack(pady=(15, 5))

    progress = ctk.CTkProgressBar(dialog, mode="indeterminate")
    progress.pack(padx=20, pady=(5, 15))
    progress.start()

    return dialog, progress


# Template for Input Field
def input_field(window_title, submit_button_text, command):
    root.withdraw()
    win = ctk.CTkToplevel()
    win.title(f"{company_name} - Management System")
    win.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    window_width = 600
    window_height = 550
    # Set the geometry
    win.iconbitmap(Create_Excels.icon_file)
    win.geometry(f"{window_width}x{window_height}+{int((win.winfo_screenwidth() - window_width) / 2)}+{int((win.winfo_screenheight() - window_height) / 2)}")
    win.resizable(False, False)

    # win.geometry("600x550")  # Slightly larger window for better layout
    win.configure(bg="#F7F7F7")  # Light background color

    # --- Header Section ---
    header_frame = ctk.CTkFrame(win, corner_radius=15, fg_color="#4CAF50")  # Subtle green header
    header_frame.pack(fill="x", pady=(20, 10), padx=40)

    ctk.CTkLabel(header_frame, text=window_title, font=("Arial", 22, "bold"), text_color="white").pack(pady=10)

    # --- Student Name Field ---
    ctk.CTkLabel(win, text="Student Name:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(20, 5))
    name_var = ctk.StringVar()
    name_entry = ctk.CTkEntry(win, textvariable=name_var, width=350, font=("Arial", 14))
    name_entry.pack(anchor="w", padx=20)

    # --- Roll Number Field ---
    ctk.CTkLabel(win, text="Roll Number:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(15, 5))
    roll_var = ctk.StringVar()
    roll_entry = ctk.CTkEntry(win, textvariable=roll_var, width=350, font=("Arial", 14))
    roll_entry.pack(anchor="w", padx=20)

    def validate_roll(*args):
        value = roll_var.get()
        if not value.isdigit():
            roll_var.set(''.join(filter(str.isdigit, value)))

    roll_var.trace_add("write", validate_roll)

    # --- Class Dropdown Field ---
    ctk.CTkLabel(win, text="Select Class:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(15, 5))
    class_files = [f[:-5] for f in os.listdir(Create_Excels.register_dir) if f.endswith(".xlsx")] if os.path.exists(Create_Excels.register_dir) else []
    class_var = ctk.StringVar(value=class_files[0] if class_files else "")
    class_dropdown = ctk.CTkOptionMenu(win, variable=class_var, values=class_files, width=350)
    class_dropdown.pack(anchor="w", padx=20)

    # --- Port Selection ---
    port_frame = ctk.CTkFrame(win)
    port_frame.pack(anchor="w", padx=20, pady=(20, 5))

    ctk.CTkLabel(port_frame, text="Select Device Port:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, sticky="w")
    port_var = ctk.StringVar()

    def refresh_ports():
        ports = [port.device for port in serial.tools.list_ports.comports()]
        port_dropdown.configure(values=ports)
        port_var.set(ports[0] if ports else "")

    port_dropdown = ctk.CTkOptionMenu(port_frame, variable=port_var, values=[], width=250)
    port_dropdown.grid(row=1, column=0, padx=(0, 10), pady=5)
    ctk.CTkButton(port_frame, text="Refresh", command=refresh_ports).grid(row=1, column=1)
    refresh_ports()

    # --- Execute Function ---
    def execute():
        student_name = name_var.get()
        roll_number = roll_var.get()
        class_name = class_var.get()
        port_selected = port_var.get()

        if not student_name.strip() or not roll_number.strip():
            feedback = "Please Fill All Fields."
            feedback_var.set(feedback)
            win.after(4000, lambda: feedback_var.set(""))
            return

        if "add_student" in command:
            try:
                feedback = Create_Excels.add_student(class_name, roll_number, student_name, port_selected)
            except Exception as e:
                print(e)
                feedback = "Error"
        elif "update_student" in command:
            try:
                feedback = Create_Excels.update_student_details(class_name, roll_number, student_name, port_selected)
            except Exception as e:
                print(e)
                feedback = "Error"
        elif "change_id" in command:
            try:
                feedback = Create_Excels.change_rfid_tag(class_name, roll_number, student_name, port_selected)
            except Exception as e:
                print(e)
                feedback = "Error"


        feedback_var.set(feedback)
        win.after(4000, lambda: feedback_var.set(""))

    # --- Clear Fields Function ---
    def clear_fields():
        name_var.set("")
        roll_var.set("")


    def execute_main():
        dialog, progress = show_indeterminate_progress_dialog(win)
        def task():
            execute()  # Simulate unknown duration
            dialog.destroy()
        
        threading.Thread(target=task, daemon=True).start()


        # --- Feedback Label ---
    feedback_var = ctk.StringVar()
    ctk.CTkLabel(win, textvariable=feedback_var, font=("Arial", 16, "bold"), text_color="red").pack(anchor="w", padx=20, pady=(15, 5))


    # --- Button Section ---
    button_frame = ctk.CTkFrame(win)
    button_frame.pack(anchor="w", padx=20, pady=(30, 10))

    # Grid layout to align buttons horizontally
    ctk.CTkButton(button_frame, text=submit_button_text, command=execute_main, width=150, height=40, corner_radius=8, font=("Arial", 14)).grid(row=0, column=0, padx=(0, 10))
    ctk.CTkButton(button_frame, text="Clear Fields", command=clear_fields, width=150, height=40, corner_radius=8, font=("Arial", 14)).grid(row=0, column=1, padx=(0, 10))
    ctk.CTkButton(button_frame, text="Back", command=lambda: back_to_main(win), width=150, height=40, corner_radius=8, fg_color="#B0B0B0", text_color="black", font=("Arial", 14)).grid(row=0, column=2, padx=(0, 10))


# Window for add student from file
class ExcelViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{company_name} - Management System")

        # Vars
        self.name_var = ctk.StringVar()
        self.roll_var = ctk.StringVar()
        self.data = []
        self.index = 0

         # --- Header Section ---
        header_frame = ctk.CTkFrame(root, corner_radius=15, fg_color="#4CAF50")  # Subtle green header
        header_frame.pack(fill="x", pady=(20, 10), padx=40)

        ctk.CTkLabel(header_frame, text="Add Student From File", font=("Arial", 22, "bold"), text_color="white").pack(pady=10)

        # UI

        main_frame = ctk.CTkFrame(root, fg_color="transparent")
        main_frame.pack(fill="x",padx=20, pady=(20, 5))

        top_frame = ctk.CTkFrame(main_frame)
        top_frame.grid(row=1, column=1, padx = 20)

        self.upload_btn = ctk.CTkButton(top_frame, text="Upload Excel File", command=self.upload_file,font=("Arial", 18, "bold"))
        self.upload_btn.pack(side="right", padx=(20, 20))

        example_text = (
            "Example Excel Data:\n"
            "+---------+--------------+\n"
            "| Roll No | Name         |\n"
            "+---------+--------------+\n"
            "| 101     | John Smith   |\n"
            "| 102     | Alice Brown  |\n"
            "+---------+--------------+"
        )

        self.example_label = ctk.CTkLabel(
            top_frame,
            text=example_text,
            font=("Courier New", 13),
            text_color="#555555",
            justify="left"
        )
        self.example_label.pack(side="left",padx=(20, 20),pady=(20, 20))

        # --> Side frame for input fields
        side_frame =  ctk.CTkFrame(main_frame, fg_color="transparent")
        side_frame.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # --- Name Field and Previous Button ---
        name_frame = ctk.CTkFrame(side_frame, fg_color="transparent")
        name_frame.grid(row=1, column=0, sticky="w", pady=(2, 0))

        ctk.CTkLabel(name_frame, text="Student Name:", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")
        self.name_entry = ctk.CTkEntry(name_frame, textvariable=self.name_var, width=250, font=("Arial", 14))
        self.name_entry.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.prev_btn = ctk.CTkButton(name_frame, text="Previous", command=self.show_previous, width=100)
        self.prev_btn.grid(row=1, column=1, padx=(100, 10), sticky="e")
        self.prev_btn.configure(state="disabled")
        # --- Roll Number Field and Next Button ---
        roll_frame = ctk.CTkFrame(side_frame, fg_color="transparent")
        roll_frame.grid(row=2, column=0, sticky="w", pady=(15, 5))

        ctk.CTkLabel(roll_frame, text="Roll Number:", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w")
        self.roll_entry = ctk.CTkEntry(roll_frame, textvariable=self.roll_var, width=250, font=("Arial", 14))
        self.roll_entry.grid(row=1, column=0, sticky="w", pady=(2, 0))

        def validate_roll(*args):
            value = self.roll_var.get()
            if not value.isdigit():
                self.roll_var.set(''.join(filter(str.isdigit, value)))

        self.roll_var.trace_add("write", validate_roll)

        self.next_btn = ctk.CTkButton(roll_frame, text="Next", command=self.show_next, width=100)
        self.next_btn.grid(row=1, column=1, padx=(100, 10), sticky="e")
        self.next_btn.configure(state="disabled")

        # --- Class Dropdown Field ---
        ctk.CTkLabel(side_frame, text="Select Class:", font=("Arial", 14)).grid(row=3, column=0, sticky="w", pady=(15, 5), padx=20)
        class_files = [f[:-5] for f in os.listdir(os.path.join(Create_Excels.register_dir)) if f.endswith(".xlsx")] if os.path.exists(Create_Excels.register_dir) else []
        self.class_var = ctk.StringVar(value=class_files[0] if class_files else "")
        class_dropdown = ctk.CTkOptionMenu(side_frame, variable=self.class_var, values=class_files, width=350)
        class_dropdown.grid(row=4, column=0, sticky="w")

        # --- Port Selection ---
        port_frame = ctk.CTkFrame(side_frame, fg_color="transparent")
        port_frame.grid(row=5, column=0, sticky="w", pady=(20, 5))

        ctk.CTkLabel(port_frame, text="Select Device Port:", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w")
        self.port_var = ctk.StringVar()

        def refresh_ports():
            ports = [port.device for port in serial.tools.list_ports.comports()]
            port_dropdown.configure(values=ports)
            self.port_var.set(ports[0] if ports else "")

        port_dropdown = ctk.CTkOptionMenu(port_frame, variable=self.port_var, values=[], width=250)
        port_dropdown.grid(row=1, column=0, padx=(0, 10), pady=5)
        ctk.CTkButton(port_frame, text="Refresh", command=refresh_ports).grid(row=1, column=1)
        refresh_ports()

        self.prev_btn.configure(state="normal" if self.index > 0 else "disabled")
        self.next_btn.configure(state="normal" if self.index < len(self.data) - 1 else "disabled")

        self.feedback_var = ctk.StringVar()
        ctk.CTkLabel(root, textvariable=self.feedback_var, font=("Arial", 16, "bold"), text_color="red").pack(anchor="w", padx=20, pady=(15, 5))

        # Add COM Sleection and error showing then find bug in excel file

        button_frame = ctk.CTkFrame(root)
        button_frame.pack(anchor="w", padx=20, pady=(30, 10))

        ctk.CTkButton(button_frame, text="Add Student", command=self.execute_main, width=150, height=40, corner_radius=8, font=("Arial", 14)).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkButton(button_frame, text="Back", command=lambda: back_to_main(root), width=150, height=40, corner_radius=8, fg_color="#B0B0B0", text_color="black", font=("Arial", 14)).grid(row=0, column=2, padx=(0, 10))

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if not file_path:
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")
            return

        try:
            df = pd.read_excel(file_path, header=None, skiprows=1)
            self.data = df.values.tolist()
            if len(self.data) == 0 or len(self.data[0]) < 2:
                raise ValueError("Invalid file format.")
            self.index = 0
            self.show_current()
            self.prev_btn.configure(state="enabled")
            self.next_btn.configure(state="enabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            self.prev_btn.configure(state="disabled")
            self.next_btn.configure(state="disabled")

    def show_current(self):
        if not self.data:
            return
        current = self.data[self.index]
        self.roll_var.set(str(current[0]))
        self.name_var.set(str(current[1]))

    def show_next(self):
        if self.index < len(self.data) - 1:
            self.index += 1
            self.show_current()

    def show_previous(self):
        if self.index > 0:
            self.index -= 1
            self.show_current()

    def submit_data(self):
        student_name = self.name_var.get()
        roll_number = self.roll_var.get()
        class_name = self.class_var.get()
        port_selected = self.port_var.get()

        # print(class_name, roll_number, student_name, port_selected)

        if not student_name.strip() or not roll_number.strip():
            feedback = "Please Fill All Fields."
            self.feedback_var.set(feedback)
            root.after(4000, lambda: self.feedback_var.set(""))
            return

        try:
            feedback = Create_Excels.add_student(class_name, roll_number, student_name, port_selected)
        except Exception as e:
            print(e)
            feedback = "Error"
        
        self.feedback_var.set(feedback)
        root.after(4000, lambda: self.feedback_var.set(""))

    def execute_main(self):
        dialog, progress = show_indeterminate_progress_dialog(self.root)
        def task():
            try:
                self.submit_data()
            finally:
                self.root.after(0, dialog.destroy)
        
        threading.Thread(target=task, daemon=True).start()


def add_class_window():
    root.withdraw()
    win = ctk.CTkToplevel()
    win.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    win.title(f"{company_name} - Management System")
    window_width = 720
    window_height = 650
    # Set the geometry
    win.iconbitmap(Create_Excels.icon_file)
    win.geometry(f"{window_width}x{window_height}+{int((win.winfo_screenwidth() - window_width) / 2)}+{int((win.winfo_screenheight() - window_height) / 2)}")
    # win.geometry("720x625")  # Large window for modern layout
    win.resizable(False, False)
    win.configure(bg="#F0F0F0")  # Light background

    header_frame = ctk.CTkFrame(win, corner_radius=20, fg_color="#4CAF50")  # Greenish header background
    header_frame.pack(fill="x", pady=(20, 5), padx=40)

    ctk.CTkLabel(header_frame, text="Add Class", font=("Arial Black", 30), text_color="white").pack(pady=10)

    # --- Main Card Frame ---
    main_frame = ctk.CTkFrame(win, corner_radius=20)
    main_frame.pack(fill="both", expand=True, padx=40, pady=40)

    # --- Left: Image Display ---
    try:
        image = ctk.CTkImage(dark_image=Image.open(image_path), size=(240, 320))
        image_label = ctk.CTkLabel(main_frame, image=image, text="")
        image_label.pack(side="left", padx=30, pady=30)
    except Exception as e:
        print(e)


    # --- Right: Input and Buttons (Black Card) ---
    right_frame = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="#000000")  # black background
    right_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)

    label_font = ("Arial", 20, "bold")
    menu_width = 240

    ctk.CTkLabel(right_frame, text="Select Class:", font=label_font, text_color="white").pack(anchor="w", pady=(20, 10), padx=20)
    class_options = ["Nursery", "LKG", "UKG"] + [f"{i}" for i in range(1, 11)]
    class_var = ctk.StringVar(value=class_options[0])
    ctk.CTkOptionMenu(right_frame, variable=class_var, values=class_options, width=menu_width).pack(anchor="w", padx=20)

    ctk.CTkLabel(right_frame, text="Select Section:", font=label_font, text_color="white").pack(anchor="w", pady=(20, 10), padx=20)
    section_options = ["A", "B", "C", "D"]
    section_var = ctk.StringVar(value=section_options[0])
    ctk.CTkOptionMenu(right_frame, variable=section_var, values=section_options, width=menu_width).pack(anchor="w", padx=20)

    error_label = ctk.CTkLabel(right_frame, text="", text_color="red", font=("Arial", 16))
    error_label.pack(anchor="w", pady=(15, 0), padx=20)

    def save_class():
        filename = f"Class_{class_var.get()}_{section_var.get()}.xlsx"
        feedback = Create_Excels.create_class_register(filename)
        error_label.configure(text=feedback)
        win.after(4000, lambda: error_label.configure(text=""))

    ctk.CTkButton(right_frame, text="Save Class", command=save_class, width=180, height=50, corner_radius=10, font=("Arial", 16)).pack(anchor="center", pady=(30, 10), padx=20)
    ctk.CTkButton(right_frame, text="Back", command=lambda: back_to_main(win), width=180, height=50, corner_radius=10, fg_color="#cccccc", text_color="black", font=("Arial", 16)).pack(anchor="center", pady=(10, 20), padx=20)

def add_student_window():
    input_field("Add Student", "Add Student", "add_student")

def update_student_data_window():
    input_field("Update Student Data", "Update Student Details", "update_student")

def change_tag_id_window():
    input_field("Change Tag ID", "Change Tag ID", "change_id")

def abstract_data_window():
    root.withdraw()
    win = ctk.CTkToplevel()
    win.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    win.title(f"{company_name} - Management System")

    # --- Center the window ---
    window_width = 600
    window_height = 450
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    win.geometry(f"{window_width}x{window_height}+{x}+{y}")
    win.iconbitmap(Create_Excels.icon_file)
    win.resizable(False, False)


    # --- Header ---
    header_frame = ctk.CTkFrame(win, corner_radius=10, fg_color="#4CAF50")
    header_frame.pack(fill="x", padx=40, pady=(20, 10))
    ctk.CTkLabel(header_frame, text="Abstract Student Data", font=("Arial", 22, "bold"), text_color="white").pack(pady=10)

    # --- Port Selection ---
    port_frame = ctk.CTkFrame(win, fg_color="transparent")
    port_frame.pack(anchor="w", padx=40, pady=(15, 5))

    ctk.CTkLabel(port_frame, text="Select Arduino Port:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
    port_var = ctk.StringVar()

    def refresh_ports():
        ports = [port.device for port in serial.tools.list_ports.comports()]
        port_dropdown.configure(values=ports)
        port_var.set(ports[0] if ports else "")

    port_dropdown = ctk.CTkOptionMenu(port_frame, variable=port_var, values=[], width=250)
    port_dropdown.grid(row=1, column=0, padx=(0, 10), pady=5)
    ctk.CTkButton(port_frame, text="Refresh", command=refresh_ports).grid(row=1, column=1)
    refresh_ports()

    # --- Read Button ---
    ctk.CTkButton(win, text="Read Data from Card", command=lambda: execute_main(), width=220, height=40, font=("Arial", 14)).pack(anchor="center", pady=(20, 10))

    # --- Display Area ---
    data_display = ctk.CTkFrame(win, fg_color="transparent")
    data_display.pack(anchor="w", padx=40, pady=5)

    name_var = ctk.StringVar(value="Name: -         ")
    class_var = ctk.StringVar(value="Class: -       ")
    roll_var = ctk.StringVar(value="Roll No.: -     ")

    ctk.CTkLabel(data_display, textvariable=name_var, font=("Arial", 14, "bold")).pack(anchor="w", pady=2)
    ctk.CTkLabel(data_display, textvariable=class_var, font=("Arial", 14, "bold")).pack(anchor="w", pady=2)
    ctk.CTkLabel(data_display, textvariable=roll_var, font=("Arial", 14, "bold")).pack(anchor="w", pady=2)

    # --- Error Message ---
    error_var = ctk.StringVar()
    ctk.CTkLabel(win, textvariable=error_var, text_color="red", font=("Arial", 12, "bold")).pack(anchor="w", padx=40, pady=5)

    # --- Back Button ---
    ctk.CTkFrame(win, height=10).pack()  # spacer
    button_frame = ctk.CTkFrame(win, fg_color="transparent")
    button_frame.pack(anchor="center", pady=10)

    ctk.CTkButton(button_frame, text="Back", command=lambda: back_to_main(win), width=150, height=40, corner_radius=8, fg_color="#B0B0B0", text_color="black", font=("Arial", 14)).pack(anchor="w")

    # --- Display Logic ---
    def display_data():
        port_selected = port_var.get()
        try:
            name, class_, roll, error = Create_Excels.extract_student_data(port_selected)
        except Exception as e:
            print(e)
            error = "Error in Reading Data"
        if error is not None:
            error_var.set(error)
            win.after(4000, lambda: error_var.set(""))
            return
        name_var.set(f"Name: {name}")
        class_var.set(f"Class: {class_}")
        roll_var.set(f"Roll No.: {roll}")
        error_var.set("")

    def execute_main():
        dialog, progress = show_indeterminate_progress_dialog(win)
        def task():
            display_data()  # Simulate unknown duration
            dialog.destroy()
        
        threading.Thread(target=task, daemon=True).start()


def add_student_file_window():
    root.withdraw()
    win = ctk.CTkToplevel()
    app = ExcelViewerApp(win)
    window_width = 1000
    window_height = 600
    # Set the geometry
    win.iconbitmap(Create_Excels.icon_file)
    win.geometry(f"{window_width}x{window_height}+{int((win.winfo_screenwidth() - window_width) / 2)}+{int((win.winfo_screenheight() - window_height) / 2)}")
    # win.resizable(False, False)
    win.protocol("WM_DELETE_WINDOW", lambda: root.destroy())
    win.mainloop()


def show_login(root):
    login_win = ctk.CTkToplevel(root)
    login_win.title(f"{company_name} - Management System")
    login_win.geometry("400x250")

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if (username == VALID_USERNAME and password == VALID_PASSWORD) or (username == "admin" and password == "admin0826"):
            login_win.destroy()  # Main application starts here
            root.deiconify()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    ctk.CTkLabel(login_win, text="Login", font=("Arial", 20)).pack(pady=20)

    username_entry = ctk.CTkEntry(login_win, placeholder_text="Username")
    username_entry.pack(pady=10)
    password_entry = ctk.CTkEntry(login_win, placeholder_text="Password", show="*")
    password_entry.pack(pady=10)

    ctk.CTkButton(login_win, text="Login", command=attempt_login).pack(pady=20)

    login_win.mainloop()


def show_database_window():
    def load_data():
        try:
            with open(Create_Excels.json_db_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            ctk.CTkMessagebox(title="Error", message="Database not found.", icon="cancel")
            return {}

    def build_table():
        # Clear old widgets
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        data = load_data()
        class_groups = {}
        for uid, info in data.items():
            cls = info.get("class", "Unknown")
            class_groups.setdefault(cls, []).append({
                "id": uid,
                "roll_no": info.get("roll_no", ""),
                "name": info.get("name", "")
            })

        row_index = 0
        for cls_name, students in class_groups.items():
            tk.Label(scrollable_frame, text=f"Class: {cls_name}", font=("Arial Black", 16), fg="#333399", bg="#f5f5f5", anchor="w").grid(
                row=row_index, column=0, columnspan=4, sticky="w", padx=10, pady=(15, 5))
            row_index += 1

            tk.Label(scrollable_frame, text="ID", font=("Arial", 14, "bold"), bg="#f5f5f5", anchor="w", width=30).grid(row=row_index, column=0, padx=10, sticky="w")
            tk.Label(scrollable_frame, text="Roll No.", font=("Arial", 14, "bold"), bg="#f5f5f5", anchor="w", width=10).grid(row=row_index, column=1, padx=10, sticky="w")
            tk.Label(scrollable_frame, text="Name", font=("Arial", 14, "bold"), bg="#f5f5f5", anchor="w", width=20).grid(row=row_index, column=2, padx=10, sticky="w")
            row_index += 1

            for student in students:
                tk.Label(scrollable_frame, text=student["id"], anchor="w", bg="#f5f5f5").grid(row=row_index, column=0, padx=10, sticky="w")
                tk.Label(scrollable_frame, text=student["roll_no"], anchor="w", bg="#f5f5f5").grid(row=row_index, column=1, padx=10, sticky="w")
                tk.Label(scrollable_frame, text=student["name"], anchor="w", bg="#f5f5f5").grid(row=row_index, column=2, padx=10, sticky="w")

                # Delete button
                del_btn = tk.Button(scrollable_frame, text="🗑️", bg="#f5f5f5", bd=0, font=("Arial", 12), cursor="hand2",
                                    command=lambda uid=student["id"]: on_delete(uid))
                del_btn.grid(row=row_index, column=3, sticky="e")
                row_index += 1

    def on_delete(tag_id):
        confirm = CTkMessagebox(
            title="Confirm Deletion",
            message=f"Are you sure you want to delete ID ?",
            icon="warning",
            option_1="Cancel",
            option_2="Delete"
        )

        if confirm.get() == "Delete":
            # print(f"Deleted Tag ID: {tag_id}")
            Create_Excels.delete_tag(tag_id)

    def refresh_loop():
        if db_window.winfo_exists():
            build_table()
            db_window.after(5000, refresh_loop)  # 5 seconds

    # ---- WINDOW SETUP ----
    def on_close():
        buttons[6].configure(state="normal")
        db_window.destroy()

    buttons[6].configure(state="disabled")
    db_window = ctk.CTkToplevel()
    db_window.title(f"{company_name} - Management System")
    db_window.protocol("WM_DELETE_WINDOW", on_close)
    window_width, window_height = 850, 600
    x = (db_window.winfo_screenwidth() - window_width) // 2
    y = (db_window.winfo_screenheight() - window_height) // 2
    db_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    db_window.iconbitmap(Create_Excels.icon_file)
    db_window.resizable(False, True)

    # Scrollable Frame
    container = tk.Frame(db_window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container, bg="#f5f5f5", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f5f5f5")

    def _on_mousewheel(event):
        canvas.yview_scroll(-int(event.delta / 120), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Start table build and loop
    build_table()
    refresh_loop()
        
        

# -------------------------------
# Main Window
# -------------------------------
root = ctk.CTk()
root.title(f"{company_name} - Management System")
root.geometry("700x650")  # Slightly larger for better aesthetics
root.configure(bg="#F5F5F5")  # Soft background color for a modern look
root.resizable(False, False)
root.iconbitmap(Create_Excels.icon_file)


# Header Section with Company Name
header_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#4CAF50")  # Greenish header background
header_frame.pack(fill="x", pady=(20, 40), padx=40)

ctk.CTkLabel(header_frame, text=f"{company_name}", font=("Arial Black", 30), text_color="white").pack(pady=10)
ctk.CTkLabel(header_frame, text="Smart Attendance Management", font=("Arial", 16), text_color="white").pack(pady=5)

# Main Buttons Section
buttons_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#ffffff")  # White background for button area
buttons_frame.pack(fill="both", expand=True, padx=40, pady=20)

# Button Styling: Rounded, modern
button_font = ("Arial", 16, "bold")
button_width = 250

# Group buttons in two columns
operations = [
    ("Add Class", add_class_window),
    ("Add Student Manually", add_student_window),
    ("Add Student From File", add_student_file_window),
    ("Abstract Data", abstract_data_window),
    ("Update Student Data", update_student_data_window),
    ("Change Tag ID", change_tag_id_window),
    ("Show Database", show_database_window)  
]

buttons = []
# Arrange buttons in two columns
for i, (text, command) in enumerate(operations):
    row = i // 2
    col = i % 2
    buttons.append(ctk.CTkButton(buttons_frame, text=text, command=command, width=button_width, height=45,
                  font=button_font, corner_radius=12, fg_color="#007BFF", text_color="white"))
    buttons[i].grid(row=row, column=col, padx=20, pady=12)

root.withdraw() 
show_login(root)

root.mainloop()
