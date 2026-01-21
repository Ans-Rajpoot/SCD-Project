"""
Login window for SyncBazar
"""
import tkinter as tk
from tkinter import messagebox
from database.connection import db
from utils.validators import validate_password


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("SyncBazar - Login")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Setup UI
        self.setup_ui()
        
        # Connect to database
        if not db.connect():
            messagebox.showerror("Database Error", 
                               "Cannot connect to database. Please check SQL Server.")
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Setup login UI"""
        # Background color
        self.root.configure(bg='#2c3e50')
        
        # Header frame
        header_frame = tk.Frame(self.root, bg='#3498db', height=150)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        tk.Label(
            header_frame,
            text="SyncBazar",
            font=("Arial", 28, "bold"),
            bg='#3498db',
            fg='white'
        ).pack(expand=True, pady=(30, 5))
        
        tk.Label(
            header_frame,
            text="Inventory Management System",
            font=("Arial", 14),
            bg='#3498db',
            fg='white'
        ).pack(pady=(0, 20))
        
        # Login form frame
        form_frame = tk.Frame(self.root, bg='#ecf0f1')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Username field
        tk.Label(
            form_frame,
            text="Username",
            font=("Arial", 11),
            bg='#ecf0f1',
            anchor='w'
        ).pack(fill=tk.X, pady=(10, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=30
        )
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.insert(0, "admin")  # Default username
        self.username_entry.focus()
        
        # Password field
        tk.Label(
            form_frame,
            text="Password",
            font=("Arial", 11),
            bg='#ecf0f1',
            anchor='w'
        ).pack(fill=tk.X, pady=(5, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 12),
            width=30,
            show="•"
        )
        self.password_entry.pack(pady=(0, 10))
        self.password_entry.insert(0, "admin123")  # Default password
        
        # Remember me checkbox
        self.remember_var = tk.IntVar(value=1)
        tk.Checkbutton(
            form_frame,
            text="Remember me",
            variable=self.remember_var,
            bg='#ecf0f1',
            font=("Arial", 10)
        ).pack(anchor='w', pady=(5, 20))
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg='#3498db',
            fg='white',
            command=self.login,
            width=20,
            height=2,
            cursor='hand2',
            relief=tk.FLAT
        )
        login_btn.pack(pady=(10, 15))
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
        
        # Signup link
        signup_frame = tk.Frame(form_frame, bg='#ecf0f1')
        signup_frame.pack()
        
        tk.Label(
            signup_frame,
            text="Don't have an account?",
            font=("Arial", 10),
            bg='#ecf0f1'
        ).pack(side=tk.LEFT)
        
        signup_link = tk.Label(
            signup_frame,
            text="Sign Up",
            font=("Arial", 10, "bold"),
            bg='#ecf0f1',
            fg='#3498db',
            cursor='hand2'
        )
        signup_link.pack(side=tk.LEFT, padx=(5, 0))
        signup_link.bind("<Button-1>", lambda e: self.open_signup())
        
        # Version label
        tk.Label(
            self.root,
            text="SyncBazar v1.0 | © 2025",
            font=("Arial", 8),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.BOTTOM, pady=10)
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        # Check credentials in database
        from database.queries import CHECK_LOGIN
        result = db.fetch_one(CHECK_LOGIN, (username, password))
        
        if result:
            user_id, username, full_name, role = result
            messagebox.showinfo("Success", f"Welcome, {full_name or username}!")
            
            # Close login window
            self.root.destroy()
            
            # Open dashboard
            self.open_dashboard(user_id, full_name or username, role)
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def open_signup(self):
        """Open signup window"""
        # For now, show message
        messagebox.showinfo("Sign Up", 
                          "Sign up feature will be available in next version.")
    
    def open_dashboard(self, user_id, username, role):
        """Open dashboard window"""
        from views.dashboard import DashboardWindow
        
        dashboard_root = tk.Tk()
        app = DashboardWindow(dashboard_root, user_id, username, role)
        dashboard_root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
