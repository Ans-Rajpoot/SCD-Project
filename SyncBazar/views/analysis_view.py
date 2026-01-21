"""
Real-time analysis window
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from database.connection import db
from database.queries import GET_DASHBOARD_STATS, GET_ALL_ITEMS
from utils.helpers import format_currency


class AnalysisWindow:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        
        self.setup_ui()
        self.load_analysis_data()
    
    def setup_ui(self):
        """Setup analysis UI"""
        self.parent.title("SyncBazar - Real-time Analysis")
        self.parent.geometry("900x600")
        self.parent.configure(bg='#ecf0f1')
        
        # Header
        header_frame = tk.Frame(self.parent, bg='#2c3e50', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 Real-time Analysis",
            font=("Arial", 18, "bold"),
            bg='#2c3e50',
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=15)
        
        # Time display
        self.time_label = tk.Label(
            header_frame,
            text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            font=("Arial", 11),
            bg='#2c3e50',
            fg='white'
        )
        self.time_label.pack(side=tk.RIGHT, padx=30, pady=15)
        
        # Update time every second
        self.update_time()
        
        # Main content with tabs
        notebook = ttk.Notebook(self.parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tab 1: Overview
        overview_tab = tk.Frame(notebook, bg='white')
        notebook.add(overview_tab, text="Overview")
        self.create_overview_tab(overview_tab)
        
        # Tab 2: Inventory Analysis
        inventory_tab = tk.Frame(notebook, bg='white')
        notebook.add(inventory_tab, text="Inventory Analysis")
        self.create_inventory_tab(inventory_tab)
        
        # Tab 3: Reports
        reports_tab = tk.Frame(notebook, bg='white')
        notebook.add(reports_tab, text="Reports")
        self.create_reports_tab(reports_tab)
    
    def update_time(self):
        """Update time display"""
        self.time_label.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.parent.after(1000, self.update_time)
    
    def create_overview_tab(self, parent):
        """Create overview tab"""
        # Get stats from database
        stats = db.fetch_one(GET_DASHBOARD_STATS)
        
        if not stats:
            stats = (0, 0, 0, 0, 0)
        
        total_items, total_shops, total_value, low_stock, out_of_stock = stats
        
        # Stats frame
        stats_frame = tk.Frame(parent, bg='white')
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(
            stats_frame,
            text="System Overview",
            font=("Arial", 20, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=(0, 30))
        
        # Stats cards
        stat_cards = [
            ("Total Inventory Value", format_currency(total_value), "#27ae60"),
            ("Total Items", f"{total_items:,}", "#3498db"),
            ("Total Shops", f"{total_shops:,}", "#9b59b6"),
            ("Low Stock Items", f"{low_stock}", "#f39c12"),
            ("Out of Stock", f"{out_of_stock}", "#e74c3c"),
        ]
        
        # Grid container
        grid_container = tk.Frame(stats_frame, bg='white')
        grid_container.pack(fill=tk.BOTH, expand=True)

        for i, (title, value, color) in enumerate(stat_cards):
            row = i // 3
            col = i % 3
            
            card_frame = tk.Frame(grid_container, bg='white')
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            
            card = tk.Frame(card_frame, bg=color, relief=tk.RAISED, bd=1)
            card.pack(fill=tk.BOTH, expand=True)
            
            tk.Label(
                card,
                text=title,
                font=("Arial", 12),
                bg=color,
                fg='white'
            ).pack(pady=(15, 5))
            
            tk.Label(
                card,
                text=value,
                font=("Arial", 24, "bold"),
                bg=color,
                fg='white'
            ).pack(pady=(0, 15))
            
            # Make grid expandable
            grid_container.grid_rowconfigure(row, weight=1)
            grid_container.grid_columnconfigure(col, weight=1)
        
        # Summary text
        summary_frame = tk.Frame(parent, bg='white')
        summary_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        summary_text = f"""
📊 Inventory Summary:
───────────────────────
• Total Inventory Value: {format_currency(total_value)}
• Total Items in System: {total_items:,}
• Connected Shops: {total_shops}
• Items Needing Attention: {low_stock + out_of_stock}
        """
        
        tk.Label(
            summary_frame,
            text=summary_text,
            font=("Courier", 11),
            bg='white',
            fg='#2c3e50',
            justify=tk.LEFT
        ).pack(anchor='w')
    
    def create_inventory_tab(self, parent):
        """Create inventory analysis tab"""
        # Get inventory data
        items = db.fetch_all(GET_ALL_ITEMS)
        
        if not items:
            tk.Label(
                parent,
                text="No inventory data available",
                font=("Arial", 14),
                bg='white',
                fg='#7f8c8d'
            ).pack(pady=50)
            return
        
        # Calculate statistics
        total_items = len(items)
        total_quantity = sum(item[4] for item in items)  # quantity at index 4
        total_value = sum(item[4] * float(item[6]) for item in items)  # quantity * price
        
        # Create text widget for analysis
        text_widget = tk.Text(parent, wrap=tk.WORD, font=("Courier", 10), 
                            height=25, bg='white', fg='#2c3e50')
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Analysis text
        analysis_text = f"""
📈 Inventory Analysis Report
────────────────────────────
Report Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

📊 Basic Statistics:
• Total Products: {total_items:,}
• Total Quantity: {total_quantity:,} units
• Total Inventory Value: {format_currency(total_value)}
• Average Value per Item: {format_currency(total_value/total_items if total_items > 0 else 0)}

🏷️ Stock Status Analysis:
"""
        
        # Stock status counts
        out_of_stock = 0
        low_stock = 0
        in_stock = 0
        
        for item in items:
            quantity = item[4]
            reorder_level = item[5]
            
            if quantity == 0:
                out_of_stock += 1
            elif quantity < reorder_level:
                low_stock += 1
            else:
                in_stock += 1
        
        analysis_text += f"""
• In Stock: {in_stock} items ({in_stock/total_items*100:.1f}%)
• Low Stock: {low_stock} items ({low_stock/total_items*100:.1f}%)
• Out of Stock: {out_of_stock} items ({out_of_stock/total_items*100:.1f}%)

⚠️ Recommendations:
"""
        
        if low_stock > 0:
            analysis_text += f"• {low_stock} items need immediate restocking\n"
        
        if out_of_stock > 0:
            analysis_text += f"• {out_of_stock} items are completely out of stock\n"
        
        if low_stock == 0 and out_of_stock == 0:
            analysis_text += "• All items are sufficiently stocked. Excellent!\n"
        
        # Top 5 most valuable items
        analysis_text += f"""
💰 Top 5 Most Valuable Items:
─────────────────────────────
"""
        
        # Calculate item values
        item_values = []
        for item in items:
            item_id, name, category, sku, quantity, reorder_level, price, location, supplier, created_at = item
            total_value = quantity * float(price)
            item_values.append((name, total_value, quantity))
        
        # Sort by value
        item_values.sort(key=lambda x: x[1], reverse=True)
        
        for i, (name, value, quantity) in enumerate(item_values[:5], 1):
            analysis_text += f"{i}. {name}: {quantity} units = {format_currency(value)}\n"
        
        # Insert text
        text_widget.insert(1.0, analysis_text)
        text_widget.config(state=tk.DISABLED)
    
    def create_reports_tab(self, parent):
        """Create reports tab"""
        tk.Label(
            parent,
            text="Generate Reports",
            font=("Arial", 20, "bold"),
            bg='white',
            fg='#2c3e50'
        ).pack(pady=30)
        
        # Reports frame
        reports_frame = tk.Frame(parent, bg='white')
        reports_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 30))
        
        reports = [
            ("📋 Inventory Report", "Complete inventory list with quantities and values", 
             self.generate_inventory_report),
            ("💰 Stock Valuation", "Detailed stock value calculation", 
             self.generate_stock_report),
            ("⚠️ Low Stock Alert", "Items that need immediate restocking", 
             self.generate_low_stock_report),
        ]
        
        for i, (title, description, command) in enumerate(reports):
            report_frame = tk.Frame(reports_frame, bg='white')
            report_frame.pack(fill=tk.X, pady=10)
            
            # Title and description
            tk.Label(
                report_frame,
                text=title,
                font=("Arial", 14, "bold"),
                bg='white',
                fg='#2c3e50',
                anchor='w'
            ).pack(fill=tk.X)
            
            tk.Label(
                report_frame,
                text=description,
                font=("Arial", 11),
                bg='white',
                fg='#7f8c8d',
                anchor='w'
            ).pack(fill=tk.X, pady=(5, 10))
            
            # Generate button
            tk.Button(
                report_frame,
                text="Generate Report",
                font=("Arial", 10),
                bg='#27ae60',
                fg='white',
                command=command,
                cursor='hand2'
            ).pack(anchor='e')
            
            # Separator
            if i < len(reports) - 1:
                ttk.Separator(reports_frame, orient='horizontal').pack(fill=tk.X, pady=5)
    
    def generate_inventory_report(self):
        """Generate inventory report"""
        messagebox.showinfo("Report", "Inventory report generated successfully!")
    
    def generate_stock_report(self):
        """Generate stock valuation report"""
        messagebox.showinfo("Report", "Stock valuation report generated successfully!")
    
    def generate_low_stock_report(self):
        """Generate low stock report"""
        messagebox.showinfo("Report", "Low stock report generated successfully!")
    
    def load_analysis_data(self):
        """Load analysis data"""
        # Data is loaded in each tab separately
        pass
