"""
Main entry point for SyncBazar
"""
import tkinter as tk
from views.login_window import LoginWindow


def main():
    """Main function to start the application"""
    try:
        # Create main window
        root = tk.Tk()
        
        # Create login window
        app = LoginWindow(root)
        
        # Start the application
        root.mainloop()
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
