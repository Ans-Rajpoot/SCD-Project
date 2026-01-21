"""
Main dashboard window for SyncBazar
"""
import tkinter as tk
from tkinter import messagebox
import datetime
from database.connection import db
from database.queries import GET_DASHBOARD_STATS, GET_RECENT_ACTIVITY
from utils.helpers import format_currency


class DashboardWindow:
    """
    [SW Engineering] Process Model (Agile/Iterative):
    - The modular structure of this application (Views, Controllers, Database) supports an Agile workflow.
    - Features like Inventory, Shop, and Analysis were developed in iterations.
    
    [SW Engineering] Deployment:
    - The application is deployed as a standalone desktop executable (Python + SQL Server).
    - 'config.py' handles environment-specific settings for easy deployment across different machines.
    
    [SW Engineering] Team Roles:
    - Frontend Developer: Implemented Tkinter UI (Dashboard, Inventory Views).
    - Backend Developer: Managed SQL Server integration and Controller logic.
    - Tester: Created Unit Tests (test_database.py) and performed system testing.
    """
    def __init__(self, root, user_id, username, role):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.role = role
        
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        self.root.title(f"SyncBazar - Welcome {self.username}")
        self.root.geometry("1200x700")
        self.root.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="SyncBazar Inventory System",
            font=("Arial", 22, "bold"),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # User info and logout
        user_frame = tk.Frame(header_frame, bg='#2c3e50')
        user_frame.pack(side=tk.RIGHT, padx=30, pady=20)
        
        user_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.username} ({self.role})",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='white'
        )
        user_label.pack(side=tk.LEFT, padx=(0, 20))
        
        logout_btn = tk.Button(
            user_frame,
            text="Logout",
            font=("Arial", 10, "bold"),
            bg='#e74c3c',
            fg='white',
            command=self.logout,
            cursor='hand2',
            relief=tk.FLAT
        )
        logout_btn.pack(side=tk.LEFT)
        
        # Main container
        main_container = tk.Frame(self.root, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Stats
        left_panel = tk.Frame(main_container, bg='white', width=350, 
                            relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Stats title
        tk.Label(
            left_panel,
            text="📊 Dashboard Statistics",
            font=("Arial", 18, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=20)
        
        # Stats frame
        self.stats_frame = tk.Frame(left_panel, bg='white')
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Right panel - Features
        right_panel = tk.Frame(main_container, bg='white', 
                             relief=tk.RAISED, bd=1)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Features title
        tk.Label(
            right_panel,
            text="🎯 Main Features",
            font=("Arial", 20, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=30)
        
        # Features grid
        features_frame = tk.Frame(right_panel, bg='white')
        features_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        features = [
            ("📦", "Smart Inventory", self.open_inventory),
            ("🏪", "Shop Network", self.open_shop_network),
            ("🔍", "Network Search", self.open_network_search),
            ("📊", "Real-time Analysis", self.open_analysis),
        ]
        
        for i, (icon, title, command) in enumerate(features):
            row = i // 2
            col = i % 2
            
            # Create card
            card = tk.Frame(
                features_frame,
                bg='white',
                relief=tk.RAISED,
                bd=2,
                cursor='hand2'
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            card.bind("<Button-1>", lambda e, cmd=command: cmd())
            
            # Make grid expandable
            features_frame.grid_rowconfigure(row, weight=1)
            features_frame.grid_columnconfigure(col, weight=1)
            
            # Card content
            tk.Label(
                card,
                text=icon,
                font=("Arial", 40),
                bg='white'
            ).pack(pady=(30, 10))
            
            tk.Label(
                card,
                text=title,
                font=("Arial", 16, "bold"),
                bg='white',
                fg='#2c3e50'
            ).pack(pady=(0, 10))
            
            tk.Label(
                card,
                text="Click to open",
                font=("Arial", 11),
                bg='white',
                fg='#7f8c8d'
            ).pack(pady=(0, 30))
            
            # Hover effects
            def on_enter(e, card=card):
                card.config(bg='#f8f9fa')
            
            def on_leave(e, card=card):
                card.config(bg='white')
            
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#34495e', height=50)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(
            footer_frame,
            text="© 2025 SyncBazar Inventory Management System",
            font=("Arial", 10),
            bg='#34495e',
            fg='white'
        ).pack(pady=15)
    
    def load_dashboard_data(self):
        """Load dashboard statistics"""
        # Clear existing stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Get stats from database
        stats = db.fetch_one(GET_DASHBOARD_STATS)
        
        if stats:
            total_items, total_shops, total_value, low_stock, out_of_stock = stats
        else:
            total_items = total_shops = total_value = low_stock = out_of_stock = 0
        
        # Display stats
        stat_cards = [
            ("Total Items", f"{total_items:,}", "#3498db"),
            ("Total Shops", f"{total_shops:,}", "#9b59b6"),
            ("Total Value", format_currency(total_value), "#27ae60"),
            ("Low Stock", f"{low_stock}", "#f39c12"),
            ("Out of Stock", f"{out_of_stock}", "#e74c3c"),
        ]
        
        for label, value, color in stat_cards:
            card = tk.Frame(self.stats_frame, bg=color, height=70)
            card.pack(fill=tk.X, pady=5)
            card.pack_propagate(False)
            
            tk.Label(
                card,
                text=label,
                font=("Arial", 12),
                bg=color,
                fg='white',
                anchor='w'
            ).pack(fill=tk.X, padx=15, pady=(10, 0))
            
            tk.Label(
                card,
                text=value,
                font=("Arial", 18, "bold"),
                bg=color,
                fg='white'
            ).pack(pady=(0, 10))
        
        # Recent activity
        tk.Label(
            self.stats_frame,
            text="Recent Activity",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w', pady=(20, 10))
        
        activities = db.fetch_all(GET_RECENT_ACTIVITY)
        
        if activities:
            for desc, timestamp in activities[:3]:  # Show only 3
                frame = tk.Frame(self.stats_frame, bg='white')
                frame.pack(fill=tk.X, pady=2)
                
                tk.Label(
                    frame,
                    text=f"• {desc}",
                    font=("Arial", 9),
                    bg='white',
                    fg='#2c3e50',
                    anchor='w'
                ).pack(side=tk.LEFT, fill=tk.X, expand=True)
                
                # Format date
                if isinstance(timestamp, datetime.datetime):
                    date_str = timestamp.strftime("%m/%d")
                else:
                    date_str = str(timestamp)[:10]
                
                tk.Label(
                    frame,
                    text=date_str,
                    font=("Arial", 8),
                    bg='white',
                    fg='#7f8c8d',
                    anchor='e'
                ).pack(side=tk.RIGHT)
        else:
            tk.Label(
                self.stats_frame,
                text="No recent activity",
                font=("Arial", 10),
                bg='white',
                fg='#7f8c8d'
            ).pack(anchor='w', pady=5)
    
    def open_inventory(self):
        """Open inventory management"""
        from views.inventory_view import InventoryWindow
        
        inventory_window = tk.Toplevel(self.root)
        inventory_window.title("Smart Inventory Management")
        inventory_window.geometry("1000x600")
        
        inventory_app = InventoryWindow(inventory_window, self.user_id)
    
    def open_shop_network(self):
        """Open shop network"""
        from views.shop_view import ShopWindow
        
        shop_window = tk.Toplevel(self.root)
        shop_window.title("Shop Network Management")
        shop_window.geometry("900x600")
        
        shop_app = ShopWindow(shop_window, self.user_id)
    
    def open_network_search(self):
        """Open network search"""
        from views.search_view import SearchWindow
        
        search_window = tk.Toplevel(self.root)
        search_window.title("Network Search")
        search_window.geometry("900x600")
        
        search_app = SearchWindow(search_window, self.user_id)
    
    def open_analysis(self):
        """Open real-time analysis"""
        from views.analysis_view import AnalysisWindow
        
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Real-time Analysis")
        analysis_window.geometry("900x600")
        
        analysis_app = AnalysisWindow(analysis_window, self.user_id)
    
    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            db.close()
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardWindow(root, 1, "Admin", "admin")
    root.mainloop()
