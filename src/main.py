import tkinter as tk
from ui.app_window import AppWindow

def main():
    # Create the main application window
    root = tk.Tk()
    # Create the AppWindow (your main GUI)
    AppWindow(root)
    root.geometry("1000x1000")  # Set the window size
    root.title("Desktop AI")  # Set the window title
    root.configure(bg="#FFFFFF")  # Clean white background
    # Start the Tkinter event loop
    AppWindow.wish(1)  # Call the wish method to greet the user
    root.mainloop()

if __name__ == "__main__":
    main()