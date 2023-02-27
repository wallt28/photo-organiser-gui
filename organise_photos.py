import os
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser


class PhotoOrganiserGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.folder_label = None
        self.master = master
        self.master.title("Photo Organiser")
        self.create_widgets()

    def create_widgets(self):

        description_text = "This program helps you organise your photos by creating folders based on the month and " \
                           "year each photo was last modified, and moving the photos into their corresponding " \
                           "folders."
        description_label = tk.Label(self.master, text=description_text, font=("Helvetica", 16), wraplength=500)
        description_label.grid(row=0, column=0, columnspan=3, padx=10, pady=(20, 10))

        self.folder_label = tk.Label(self.master, text="Select folder to organise:")
        self.folder_label.grid(row=1, column=0, padx=10, pady=10)

        self.folder_path = tk.Entry(self.master, width=50)
        self.folder_path.grid(row=1, column=1, padx=10, pady=10)

        self.folder_button = tk.Button(self.master, text="Browse", command=self.select_folder)
        self.folder_button.grid(row=1, column=2, padx=10, pady=10)

        self.organise_button = tk.Button(self.master, text="Organise Photos", command=self.organise_photos)
        self.organise_button.grid(row=2, column=1, padx=10, pady=10, sticky='NS')

        self.progress_label = tk.Label(self.master, text="")
        self.progress_label.grid(row=3, column=1, padx=10, pady=10)

        disclaimer_text = "DISCLAIMER: Please ensure that you have backed up your files before running this program. " \
                          "I am not responsible for any data loss or damage that may occur as a result " \
                          "of using this program."

        disclaimer_label = tk.Label(self.master, text=disclaimer_text, font=("Helvetica", 12, "bold"), wraplength=500)
        disclaimer_label.grid(row=4, column=0, columnspan=3, padx=10, pady=(50, 20))

        github_button = tk.Button(self.master, text="GitHub", command=self.open_github)
        github_button.grid(row=5, column=0, padx=10, pady=10)

        linkedin_button = tk.Button(self.master, text="LinkedIn", command=self.open_linkedin)
        linkedin_button.grid(row=5, column=2, padx=10, pady=10)

    def open_github(self):
        webbrowser.open("https://github.com/wallt28")

    def open_linkedin(self):
        webbrowser.open("https://www.linkedin.com/in/tomwallis28")

    def select_folder(self):
        folder_path = filedialog.askdirectory(initialdir='/', title='Select Folder')
        if folder_path:
            self.folder_path.delete(0, tk.END)
            self.folder_path.insert(0, folder_path)

    def select_destination(self):
        dest_path = filedialog.askdirectory(initialdir='/', title='Select Destination Folder')
        if dest_path:
            self.dest_path.delete(0, tk.END)
            self.dest_path.insert(0, dest_path)

    def organise_photos(self):
        # Get the input and output directory paths
        photo_dir = self.folder_path.get()

        # Check if the input and output directories exist
        if not os.path.exists(photo_dir):
            messagebox.showerror("Error", "Invalid directory path!")
            return

        # Ask for confirmation before proceeding with the file organisation
        confirm = messagebox.askokcancel("Confirmation", "Are you sure you want to organise these files?")
        if not confirm:
            return

        # Collect all files in the input directory and its subdirectories
        files = []
        for root, dirs, filenames in os.walk(photo_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)

        # Sort the files based on their last modified time
        files.sort(key=lambda f: os.path.getmtime(f))

        # Move each file to the appropriate folder based on its modified date
        num_files_organised = 0
        num_folders_created = 0
        last_month = None
        for file_path in files:
            try:
                # Get the last modified date of the file
                modified_time = os.path.getmtime(file_path)
                modified_date = datetime.fromtimestamp(modified_time).date()

                # Create a new folder for each month that has files
                if modified_date.month != last_month:
                    folder_name = modified_date.strftime("%B %Y")
                    folder_path = os.path.join(photo_dir, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    num_folders_created += 1

                # Move the file to the appropriate folder
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(photo_dir, folder_name, file_name)
                shutil.move(file_path, dest_path)
                num_files_organised += 1

                # Update the progress label
                progress_text = f"Organising file {num_files_organised} of {len(files)} ({num_files_organised / len(files):.0%} done)"
                self.progress_label.config(text=progress_text)
                self.progress_label.update()

                last_month = modified_date.month

            except Exception as e:
                # Show a warning message if there was an error moving the file
                messagebox.showwarning("Warning", f"Error organising file {file_path}: {str(e)}")

        # Show a success message when all files have been moved
        summary_text = f"Organised {num_files_organised} files"
        messagebox.showinfo("Success", summary_text)


if __name__ == '__main__':
    root = tk.Tk()
    app = PhotoOrganiserGUI(root)
    app.mainloop()
