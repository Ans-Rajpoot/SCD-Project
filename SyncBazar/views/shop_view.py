"""
Shop network management window
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import db
from database.queries import GET_ALL_SHOPS


class ShopWindow:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        
        self.setup_ui()
        self.load_shops()
    
    def setup_ui(self):
        """Setup shop network UI"""
        self.parent.title("SyncBazar - Shop Network")
        self.parent.geometry("900x600")
        self.parent.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🏪 Shop Network Management",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=15)
        
        # Control panel
        control_frame = tk.Frame(self.parent, bg='#ecf0f1', height=50)
        control_frame.pack(fill=tk.X)
        control_frame.pack_propagate(False)
        
        # Search
        search_frame = tk.Frame(control_frame, bg='#ecf0f1')
        search_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        tk.Label(search_frame, text="Search:", font=("Arial", 11), 
                bg='#ecf0f1').pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_shops())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                              width=30, font=("Arial", 11))
        search_entry.pack(side=tk.LEFT)
        
        # Add shop button
        tk.Button(
            control_frame,
            text="➕ Add New Shop",
            font=("Arial", 10, "bold"),
            bg='#27ae60',
            fg='white',
            command=self.add_shop,
            cursor='hand2'
        ).pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main content
        content_frame = tk.Frame(self.parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create treeview
        columns = ("ID", "Shop Name", "Location", "Manager", "Phone", "Email", "Status")
        self.tree = ttk.Treeview(
            content_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Define headings
        column_configs = [
            ("ID", "ID", 50),
            ("Shop Name", "Shop Name", 150),
            ("Location", "Location", 200),
            ("Manager", "Manager", 120),
            ("Phone", "Phone", 100),
            ("Email", "Email", 150),
            ("Status", "Status", 80),
        ]
        
        for col_name, heading, width in column_configs:
            self.tree.heading(col_name, text=heading)
            self.tree.column(col_name, width=width, minwidth=50)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Stats frame
        self.stats_label = tk.Label(
            self.parent,
            text="Loading shop data...",
            font=("Arial", 11),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.stats_label.pack(side=tk.BOTTOM, pady=10)
    
    def load_shops(self):
        """Load shops from database"""
        self.shops = db.fetch_all(GET_ALL_SHOPS)
        self.display_shops()
    
    def display_shops(self):
        """Display shops in treeview"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_shops = 0
        active_shops = 0
        
        # Add shops
        for shop in self.shops:
            shop_id, name, location, manager, phone, email, status = shop
            
            total_shops += 1
            if status == 'Active':
                active_shops += 1
            
            self.tree.insert("", tk.END, values=(
                shop_id,
                name,
                location or "Not specified",
                manager or "Not assigned",
                phone or "N/A",
                email or "N/A",
                status
            ))
        
        # Update stats
        self.stats_label.config(
            text=f"Total Shops: {total_shops} | Active: {active_shops} | "
                 f"Inactive: {total_shops - active_shops}"
        )
    
    def search_shops(self):
        """Search shops by name or location"""
        search_term = self.search_var.get().strip().lower()
        
        if not search_term:
            self.display_shops()
            return
        
        filtered_shops = []
        for shop in self.shops:
            shop_id, name, location, manager, phone, email, status = shop
            
            if (search_term in name.lower() or 
                search_term in (location or "").lower() or 
                search_term in (manager or "").lower()):
                filtered_shops.append(shop)
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Display filtered shops
        for shop in filtered_shops:
            shop_id, name, location, manager, phone, email, status = shop
            
            self.tree.insert("", tk.END, values=(
                shop_id,
                name,
                location or "Not specified",
                manager or "Not assigned",
                phone or "N/A",
                email or "N/A",
                status
            ))
        
        self.stats_label.config(
            text=f"Found {len(filtered_shops)} shops for '{search_term}'"
        )
    
    def add_shop(self):
        """Add new shop dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Shop")
        dialog.geometry("500x500")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Title
        tk.Label(dialog, text="➕ Add New Shop", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, padx=30, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Shop Name*", "entry", ""),
            ("Location", "entry", ""),
            ("Manager Name", "entry", ""),
            ("Phone", "entry", ""),
            ("Email", "entry", ""),
            ("Status", "combo", ["Active", "Inactive"]),
        ]
        
        entries = {}
        
        for label, field_type, values in fields:
            frame = tk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label, font=("Arial", 11), 
                    width=15, anchor='w').pack(side=tk.LEFT)
            
            if field_type == "combo":
                entry = ttk.Combobox(frame, values=values, state="readonly", 
                                   width=32)
                entry.set(values[0])
                entry.pack(side=tk.LEFT, padx=(10, 0))
            else:
                entry = tk.Entry(frame, width=35)
                if values:
                    entry.insert(0, values)
                entry.pack(side=tk.LEFT, padx=(10, 0))
            
            entries[label.replace('*', '').strip()] = entry
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        def save_shop():
            # Get values
            name = entries["Shop Name"].get().strip()
            location = entries["Location"].get().strip()
            manager = entries["Manager Name"].get().strip()
            phone = entries["Phone"].get().strip()
            email = entries["Email"].get().strip()
            status = entries["Status"].get()
            
            # Validate
            if not name:
                messagebox.showerror("Error", "Shop name is required")
                return
            
            # Save to database
            query = """
            INSERT INTO shops (shop_name, location, manager_name, phone, email, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            if db.execute_query(query, (name, location, manager, phone, email, status)):
                messagebox.showinfo("Success", "Shop added successfully!")
                dialog.destroy()
                self.load_shops()  # Refresh list
            else:
                messagebox.showerror("Error", "Failed to add shop")
        
        tk.Button(button_frame, text="Save", command=save_shop, 
                 bg='#27ae60', fg='white', width=10).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, 
                 bg='#7f8c8d', fg='white', width=10).pack(side=tk.RIGHT, padx=5)
