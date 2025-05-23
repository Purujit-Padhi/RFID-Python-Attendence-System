import customtkinter as ctk
import serial.tools.list_ports
import helper1 as ua
from tkinter import messagebox
import threading
from datetime import datetime
import os


# Initial Values
company_name = "Company Name"
color_theme = "light"


ctk.set_appearance_mode(color_theme)
ctk.set_default_color_theme("blue")



# Create the main window
root = ctk.CTk()
root.title(f"{company_name} - Management System")
window_width = 800
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.iconbitmap(ua.icon_file)
# root.resizable(False, False)


header_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#4CAF50")  # Greenish header background
header_frame.pack(fill="x", pady=(20, 40), padx=40)

ctk.CTkLabel(header_frame, text=f"{company_name}", font=("Arial Black", 30), text_color="white").pack(pady=10)
ctk.CTkLabel(header_frame, text="Smart Attendance Management", font=("Arial", 16), text_color="white").pack(pady=5)


port_frame = ctk.CTkFrame(root, fg_color="transparent")
port_frame.pack(anchor="w", padx=40, pady=(15, 5))

ctk.CTkLabel(port_frame, text="Select Device Port:", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
port_var = ctk.StringVar()

def refresh_ports():
    ports = [port.device for port in serial.tools.list_ports.comports()]
    port_dropdown.configure(values=ports)
    port_var.set(ports[0] if ports else "")

port_dropdown = ctk.CTkOptionMenu(port_frame, variable=port_var, values=[], width=250)
port_dropdown.grid(row=1, column=0, padx=(0, 10), pady=5)
ctk.CTkButton(port_frame, text="Refresh", command=refresh_ports).grid(row=1, column=1)
refresh_ports()

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

def update_time():
    current_time = datetime.now().strftime("%I:%M:%S %p")
    time_label.configure(text=current_time)
    time_label.after(1000, update_time)  # Update every second

def open_folder():
    folder_path = ua.attendance_folder  # Change to your folder path
    if os.path.exists(folder_path):
        os.startfile(folder_path)  # For Windows
    else:
        messagebox.showerror("Error", f"Error in openening the folder path:\n{folder_path}")

def update_attendence_student(ser):
    status_label.configure(text="Device Online.. ✅", text_color="green")
    feedback = ua.listen_for_cards(ser)
    if not feedback:
        connect_button.configure(state="enabled")
        port_dropdown.configure(state="enabled")
        status_label.configure(text="Device Offline.. ❌", text_color="red")
    else:
        connect_button.configure(state="enabled")
        port_dropdown.configure(state="enabled")
        status_label.configure(text="Device Offline.. ❌", text_color="red")
        messagebox.showerror("Error", feedback)

def connect_device():
    port_selected = port_var.get()
    feedback, ser = ua.connect_arduino(port_selected)
    print(feedback)
    if feedback:
        connect_button.configure(state="disabled")
        port_dropdown.configure(state="disabled")
        threading.Thread(target=update_attendence_student, args=(ser,), daemon=True).start()
    else:
        messagebox.showerror("Error", f"Wrong Port Selected")
        status_label.configure(text="Device Offline.. ❌", text_color="red")
        return


def execute_connect():
    dialog, progress = show_indeterminate_progress_dialog(root)
    def task():
        connect_device()  # Simulate unknown duration
        dialog.destroy()
    
    threading.Thread(target=task, daemon=True).start()


connect_frame = ctk.CTkFrame(root, fg_color="transparent")
connect_frame.pack(fill="x", padx=20)
# Connect Button
connect_button = ctk.CTkButton(connect_frame, text="Connect", command=execute_connect, width=180, height=50, corner_radius=10, font=("Arial", 16))
connect_button.grid(row=1, column=0, padx = 20, pady=(30, 10))

# Status Label
status_label = ctk.CTkLabel(connect_frame, text="Device Offline.. ❌", text_color="red", font=("Arial", 14, "bold"))
status_label.grid(row=1, column=1, padx = (50,20), pady=(30, 10))

open_folder_button = ctk.CTkButton(
    connect_frame,
    text="Open Attendance Folder",
    command=open_folder,
    width=200,
    height=40,
    font=("Arial", 14)
)
open_folder_button.grid(row=2, column=0, columnspan=2, pady=(10, 5))

#Time Showing
time_label = ctk.CTkLabel(root, font=("Arial", 18, "bold"), text_color="black")
time_label.place(relx=0.88, rely=0.5, anchor="center")  # Approximately 3 o’clock position
update_time()

root.mainloop()
