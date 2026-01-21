"""
Network search window
"""
import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import db
from database.queries import SEARCH_ITEMS, GET_ALL_SHOPS
from utils.helpers import format_currency


class SearchWindow:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup network search UI"""
        self.parent.title("SyncBazar - Network Search")
        self.parent.geometry("900x600")
        self.parent.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔍 Network Search",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=15)
        
        # Search panel
        search_panel = tk.Frame(self.parent, bg='#3498db', height=100)
        search_panel.pack(fill=tk.X)
        search_panel.pack_propagate(False)
        
        tk.Label(
            search_panel,
            text="Search Across All Stores",
            font=("Arial", 16, "bold"),
            bg='#3498db',
            fg='white'
        ).pack(pady=(20, 10))
        
        # Search controls
        search_frame = tk.Frame(search_panel, bg='#3498db')
        search_frame.pack(pady=(0, 20))
        
        tk.Label(search_frame, text="Search:", font=("Arial", 12), 
                bg='#3498db', fg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = tk.Entry(search_frame, width=40, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="Search",
            font=("Arial", 12, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.perform_search,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            search_frame,
            text="Clear",
            font=("Arial", 12),
            bg='#95a5a6',
            fg='white',
            command=self.clear_search,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Bind Enter key
        self.parent.bind('<Return>', lambda event: self.perform_search())
        
        # Results frame
        results_frame = tk.Frame(self.parent, bg='white')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Results label
        self.results_label = tk.Label(
            results_frame,
            text="Enter search term to find items across all stores",
            font=("Arial", 12),
            bg='white',
            fg='#7f8c8d'
        )
        self.results_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create treeview
        columns = ("Item", "Category", "Store", "Quantity", "Price", "Status")
        self.tree = ttk.Treeview(
            results_frame,
            columns=columns,
            show="headings",
            height=15
        )
        
        # Define headings
        column_configs = [
            ("Item", "Item Name", 200),
            ("Category", "Category", 120),
            ("Store", "Store", 150),
            ("Quantity", "Quantity", 80),
            ("Price", "Price", 100),
            ("Status", "Status", 100),
        ]
        
        for col_name, heading, width in column_configs:
            self.tree.heading(col_name, text=heading)
            self.tree.column(col_name, width=width)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, 
                                 command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Stats frame
        self.stats_label = tk.Label(
            self.parent,
            text="Ready to search",
            font=("Arial", 11),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        self.stats_label.pack(side=tk.BOTTOM, pady=10)
    
    def perform_search(self):
        """Perform network search"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Warning", "Please enter a search term")
            return
        
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Update results label
        self.results_label.config(text=f"Search results for: '{search_term}'")
        
        # Search in database
        results = db.fetch_all(SEARCH_ITEMS, 
                             (f'%{search_term}%', f'%{search_term}%', 
                              f'%{search_term}%', f'%{search_term}%'))
        
        # Display results
        if results:
            for item in results:
                item_id, name, category, sku, quantity, price, location, supplier = item
                
                # Determine status
                if quantity == 0:
                    status = "Out of Stock"
                elif quantity < 10:  # Default reorder level
                    status = "Low Stock"
                else:
                    status = "In Stock"
                
                self.tree.insert("", tk.END, values=(
                    name,
                    category or "Uncategorized",
                    location or "Main Store",
                    quantity,
                    format_currency(price),
                    status
                ))
            
            self.stats_label.config(text=f"Found {len(results)} results for '{search_term}'")
        else:
            self.tree.insert("", tk.END, values=("No results found", "", "", "", "", ""))
            self.stats_label.config(text=f"No results found for '{search_term}'")
    
    def clear_search(self):
        """Clear search results"""
        self.search_entry.delete(0, tk.END)
        self.results_label.config(text="Enter search term to find items across all stores")
        
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.stats_label.config(text="Ready to search")
