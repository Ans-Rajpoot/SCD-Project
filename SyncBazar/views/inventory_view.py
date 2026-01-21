"""
Inventory management window
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import db
from database.queries import GET_ALL_ITEMS, ADD_ITEM, UPDATE_ITEM, DELETE_ITEM, SEARCH_ITEMS
from utils.validators import validate_item_data, validate_numeric
from utils.helpers import format_currency


class InventoryWindow:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        
        self.setup_ui()
        self.load_items()
    
    def setup_ui(self):
        """Setup inventory management UI"""
        self.parent.title("SyncBazar - Inventory Management")
        self.parent.geometry("1000x600")
        self.parent.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📦 Smart Inventory Management",
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
        self.search_var.trace('w', lambda *args: self.search_items())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                              width=30, font=("Arial", 11))
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Action buttons
        action_frame = tk.Frame(control_frame, bg='#ecf0f1')
        action_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        buttons = [
            ("➕ Add Item", self.add_item),
            ("✏️ Edit Item", self.edit_item),
            ("🗑️ Delete Item", self.delete_item),
            ("🔄 Refresh", self.load_items),
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                action_frame,
                text=text,
                font=("Arial", 10),
                bg='#3498db',
                fg='white',
                command=command,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Main content
        content_frame = tk.Frame(self.parent, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create treeview
        columns = ("ID", "Name", "Category", "Quantity", "Price", "Location", "Supplier", "Status")
        self.tree = ttk.Treeview(
            content_frame,
            columns=columns,
            show="headings",
            height=20
        )
        
        # Define headings
        column_configs = [
            ("ID", "ID", 50),
            ("Name", "Product Name", 150),
            ("Category", "Category", 100),
            ("Quantity", "Quantity", 80),
            ("Price", "Price", 100),
            ("Location", "Location", 100),
            ("Supplier", "Supplier", 120),
            ("Status", "Status", 100),
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
        
        # Bind double-click for editing
        self.tree.bind("<Double-1>", lambda e: self.edit_item())
        
        # Stats frame
        self.stats_label = tk.Label(
            self.parent,
            text="Loading...",
            font=("Arial", 11),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.stats_label.pack(side=tk.BOTTOM, pady=10)
    
    def load_items(self):
        """Load items from database"""
        self.items = db.fetch_all(GET_ALL_ITEMS)
        self.display_items()
    
    def display_items(self):
        """Display items in treeview"""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        total_items = 0
        total_quantity = 0
        total_value = 0
        
        # Add items
        for item in self.items:
            item_id, name, category, sku, quantity, reorder_level, price, location, supplier, created_at = item
            
            # Calculate totals
            total_items += 1
            total_quantity += quantity
            total_value += quantity * float(price)
            
            # Determine status
            if quantity == 0:
                status = "Out of Stock"
                tags = ('out_of_stock',)
            elif quantity < reorder_level:
                status = "Low Stock"
                tags = ('low_stock',)
            else:
                status = "In Stock"
                tags = ('in_stock',)
            
            self.tree.insert("", tk.END, values=(
                item_id,
                name,
                category or "Uncategorized",
                quantity,
                format_currency(price),
                location or "Main Store",
                supplier or "N/A",
                status
            ), tags=tags)
        
        # Configure tags for coloring
        self.tree.tag_configure('out_of_stock', background='#ffebee')
        self.tree.tag_configure('low_stock', background='#fff3e0')
        self.tree.tag_configure('in_stock', background='#e8f5e9')
        
        # Update stats
        self.stats_label.config(
            text=f"Total: {total_items} items | Quantity: {total_quantity:,} | "
                 f"Value: {format_currency(total_value)} | "
                 f"Showing {len(self.items)} items"
        )
    
    def search_items(self):
        """Search items by name or category"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            self.display_items()
            return
        
        results = db.fetch_all(SEARCH_ITEMS, 
                             (f'%{search_term}%', f'%{search_term}%', 
                              f'%{search_term}%', f'%{search_term}%'))
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Display results
        for item in results:
            item_id, name, category, sku, quantity, price, location, supplier = item
            
            # Determine status
            if quantity == 0:
                status = "Out of Stock"
                tags = ('out_of_stock',)
            elif quantity < 10:  # Default reorder level
                status = "Low Stock"
                tags = ('low_stock',)
            else:
                status = "In Stock"
                tags = ('in_stock',)
            
            self.tree.insert("", tk.END, values=(
                item_id,
                name,
                category or "Uncategorized",
                quantity,
                format_currency(price),
                location or "Main Store",
                supplier or "N/A",
                status
            ), tags=tags)
        
        self.stats_label.config(text=f"Found {len(results)} results for '{search_term}'")
    
    def add_item(self):
        """Add new item dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Item")
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
        tk.Label(dialog, text="➕ Add New Inventory Item", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, padx=30, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        fields = [
            ("Item Name*", "entry", ""),
            ("Category", "entry", "General"),
            ("SKU", "entry", ""),
            ("Quantity*", "entry", "0"),
            ("Price*", "entry", "0.00"),
            ("Location", "entry", "Main Store"),
            ("Supplier", "entry", ""),
        ]
        
        entries = {}
        
        for label, field_type, default in fields:
            frame = tk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label, font=("Arial", 11), 
                    width=15, anchor='w').pack(side=tk.LEFT)
            
            if field_type == "entry":
                entry = tk.Entry(frame, width=35)
                entry.insert(0, default)
                entry.pack(side=tk.LEFT, padx=(10, 0))
                entries[label.replace('*', '').strip()] = entry
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        def save_item():
            # Get values
            name = entries["Item Name"].get().strip()
            category = entries["Category"].get().strip()
            sku = entries["SKU"].get().strip()
            quantity = entries["Quantity"].get().strip()
            price = entries["Price"].get().strip()
            location = entries["Location"].get().strip()
            supplier = entries["Supplier"].get().strip()
            
            # Validate
            if not name:
                messagebox.showerror("Error", "Item name is required")
                return
            
            quantity_valid, quantity_msg = validate_numeric(quantity, "Quantity")
            if not quantity_valid:
                messagebox.showerror("Error", quantity_msg)
                return
            
            price_valid, price_msg = validate_numeric(price, "Price")
            if not price_valid:
                messagebox.showerror("Error", price_msg)
                return
            
            # Save to database
            if db.execute_query(ADD_ITEM, (name, category, sku, 
                                         int(float(quantity)), 10, 
                                         float(price), location, supplier)):
                messagebox.showinfo("Success", "Item added successfully!")
                dialog.destroy()
                self.load_items()  # Refresh list
            else:
                messagebox.showerror("Error", "Failed to add item")
        
        tk.Button(button_frame, text="Save", command=save_item, 
                 bg='#27ae60', fg='white', width=10).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, 
                 bg='#7f8c8d', fg='white', width=10).pack(side=tk.RIGHT, padx=5)
    
    def edit_item(self):
        """Edit selected item"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to edit")
            return
        
        item_id = int(self.tree.item(selected[0])['values'][0])
        
        # Find item details
        item_details = None
        for item in self.items:
            if item[0] == item_id:
                item_details = item
                break
        
        if not item_details:
            messagebox.showerror("Error", "Item not found")
            return
        
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Edit Item: {item_details[1]}")
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
        tk.Label(dialog, text=f"✏️ Edit Item", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(dialog, padx=30, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        item_id, name, category, sku, quantity, reorder_level, price, location, supplier, created_at = item_details
        
        # Form fields with current values
        fields = [
            ("Item Name*", "entry", name),
            ("Category", "entry", category or ""),
            ("SKU", "entry", sku or ""),
            ("Quantity*", "entry", str(quantity)),
            ("Price*", "entry", str(float(price))),
            ("Location", "entry", location or "Main Store"),
            ("Supplier", "entry", supplier or ""),
        ]
        
        entries = {}
        
        for label, field_type, default in fields:
            frame = tk.Frame(form_frame)
            frame.pack(fill=tk.X, pady=10)
            
            tk.Label(frame, text=label, font=("Arial", 11), 
                    width=15, anchor='w').pack(side=tk.LEFT)
            
            if field_type == "entry":
                entry = tk.Entry(frame, width=35)
                entry.insert(0, default)
                entry.pack(side=tk.LEFT, padx=(10, 0))
                entries[label.replace('*', '').strip()] = entry
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=30, pady=20)
        
        def update_item():
            # Get values
            name = entries["Item Name"].get().strip()
            category = entries["Category"].get().strip()
            sku = entries["SKU"].get().strip()
            quantity = entries["Quantity"].get().strip()
            price = entries["Price"].get().strip()
            location = entries["Location"].get().strip()
            supplier = entries["Supplier"].get().strip()
            
            # Validate
            if not name:
                messagebox.showerror("Error", "Item name is required")
                return
            
            quantity_valid, quantity_msg = validate_numeric(quantity, "Quantity")
            if not quantity_valid:
                messagebox.showerror("Error", quantity_msg)
                return
            
            price_valid, price_msg = validate_numeric(price, "Price")
            if not price_valid:
                messagebox.showerror("Error", price_msg)
                return
            
            # Update in database
            if db.execute_query(UPDATE_ITEM, (name, category, sku, 
                                            int(float(quantity)), 10, 
                                            float(price), location, supplier, 
                                            item_id)):
                messagebox.showinfo("Success", "Item updated successfully!")
                dialog.destroy()
                self.load_items()  # Refresh list
            else:
                messagebox.showerror("Error", "Failed to update item")
        
        tk.Button(button_frame, text="Update", command=update_item, 
                 bg='#3498db', fg='white', width=10).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, 
                 bg='#7f8c8d', fg='white', width=10).pack(side=tk.RIGHT, padx=5)
    
    def delete_item(self):
        """Delete selected item"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        item_id = int(self.tree.item(selected[0])['values'][0])
        item_name = self.tree.item(selected[0])['values'][1]
        
        response = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{item_name}'?\n\n"
            "This action cannot be undone."
        )
        
        if response:
            if db.execute_query(DELETE_ITEM, (item_id,)):
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.load_items()  # Refresh list
            else:
                messagebox.showerror("Error", "Failed to delete item")
