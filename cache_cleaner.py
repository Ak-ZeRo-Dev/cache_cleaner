import os
import shutil
import sys
import tkinter as tk
from tkinter import simpledialog
import getpass  # To get the current system username

def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for both development and packaged mode """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def get_system_username():
    """ Get the current system username """
    return getpass.getuser()

def center_window(window):
    """ Center the window on the screen """
    window.update_idletasks()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_x = int((screen_width - window_width) / 2)
    position_y = int((screen_height - window_height) / 2)
    window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

def show_custom_messagebox(root, title, message, error=False):
    custom_box = tk.Toplevel(root)
    custom_box.title(title)
    
    label = tk.Label(custom_box, text=message, padx=10, pady=10, fg="red" if error else "green")
    label.pack()
    
    tk.Button(custom_box, text="OK", command=custom_box.destroy).pack(pady=5)
    
    # Center the messagebox
    custom_box.update_idletasks()
    center_window(custom_box)

    custom_box.grab_set()
    root.wait_window(custom_box)

def clean_cache(root, text_widget):
    username = get_system_username()

    paths = [
        fr"C:\Users\{username}\AppData\Local\Temp",
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch"
    ]

    for path in paths:
        if os.path.exists(path):
            removed_count = 0
            skip_count = 0
            text_widget.insert(tk.END, f"Cleaning {path}...\n")
            text_widget.update()

            for root_dir, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root_dir, file)
                    try:
                        os.remove(file_path)
                        removed_count += 1
                    except Exception:
                        skip_count += 1
                        text_widget.insert(tk.END, f"Error removing file: {file_path}\n", "error")

                for dir in dirs:
                    dir_path = os.path.join(root_dir, dir)
                    try:
                        shutil.rmtree(dir_path)
                        removed_count += 1
                    except Exception:
                        skip_count += 1
                        text_widget.insert(tk.END, f"Error removing directory: {dir_path}\n", "error")

            # Show removed items count in green
            text_widget.insert(tk.END, f"{removed_count} item(s) removed from {path}.\n", "removed")
            # Show skipped items count in orange
            if skip_count > 0:
                text_widget.insert(tk.END, f"Skipped {skip_count} item(s) from {path}.\n", "skipped")
        else:
            text_widget.insert(tk.END, f"Directory does not exist: {path}\n", "error")
        text_widget.insert(tk.END, "-" * 40 + "\n")
        text_widget.update()

    # Show the completion message in the Text widget
    text_widget.insert(tk.END, "Cache cleaning complete!\n", "removed")

def start_cleaning():
    global root
    root = tk.Tk()
    root.title("Cache Cleaner")

    username = get_system_username()

    icon_path = get_resource_path("assets/ak-zero.ico")
    root.iconbitmap(icon_path)

    text_widget = tk.Text(root, wrap=tk.WORD, width=80, height=20)
    text_widget.pack(padx=10, pady=10)

    text_widget.tag_configure("error", foreground="red")
    text_widget.tag_configure("removed", foreground="green")
    text_widget.tag_configure("skipped", foreground="orange")

    # Aligning all buttons in a single line
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Start Cleaning Button - Default style
    start_button = tk.Button(button_frame, text="Start Cleaning", command=lambda: clean_cache(root, text_widget))
    start_button.pack(side=tk.LEFT, padx=5)

    footer_label = tk.Label(root, text="Created by Ak-ZeRo", font=("Arial", 10))
    footer_label.pack(side=tk.BOTTOM, pady=10)

    # Center the main application window
    root.update_idletasks()
    root.geometry("600x400")  # Set initial size
    center_window(root)

    root.mainloop()

if __name__ == "__main__":
    start_cleaning()
