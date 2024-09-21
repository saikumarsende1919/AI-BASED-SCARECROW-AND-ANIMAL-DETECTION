import tkinter as tk
from tkinter import messagebox

# Function to show a popup
def show_popup():
    messagebox.showinfo("Popup", "This is a popup message!")

# Create a Tkinter window
root = tk.Tk()
root.title("Popup Example")

# Create a button to trigger the popup
popup_button = tk.Button(root, text="Show Popup", command=show_popup)
popup_button.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
