"""
HOTEL MANAGEMENT SYSTEM - MODERN GUI VERSION
A comprehensive hotel management solution with modern Tkinter interface
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime


# ==================== INITIALIZATION ====================

def initialize_files():
    """Initialize all required data files if they don't exist"""
    if not os.path.exists("rooms.txt") or os.path.getsize("rooms.txt") == 0:
        with open("rooms.txt", "w", encoding="utf-8") as f:
            f.write("101,Normal,Available,1000\n")
            f.write("102,Normal,Available,1000\n")
            f.write("103,Normal,Available,1000\n")
            f.write("201,Deluxe,Available,1800\n")
            f.write("202,Deluxe,Available,1800\n")
            f.write("203,Deluxe,Available,1800\n")
            f.write("301,Suite,Available,3000\n")
            f.write("302,Suite,Available,3000\n")

    for file in ["customers.txt", "food_orders.txt", "services.txt",
                 "housekeeping.txt", "grievances.txt", "feedback.txt"]:
        open(file, "a", encoding="utf-8").close()


# ==================== UTILITY FUNCTIONS ====================

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_customer_room(name, id_proof):
    """Get room number for a checked-in customer"""
    try:
        with open("customers.txt", "r", encoding="utf-8") as f:
            for line in f:
                data = line.strip().split(",")
                if len(data) >= 3 and data[0].lower() == name.lower() and data[1] == id_proof:
                    return data[2]
        return None
    except Exception:
        return None


def create_gradient(canvas, width, height, color1, color2):
    """Create a gradient effect on canvas"""
    try:
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)
    except Exception:
        # Fallback to simple background if colors invalid
        canvas.create_rectangle(0, 0, width, height, fill=color1, outline=color1)
        return

    r_ratio = (r2 - r1) / max(1, height)
    g_ratio = (g2 - g1) / max(1, height)
    b_ratio = (b2 - b1) / max(1, height)

    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        color = f'#{nr>>8:02x}{ng>>8:02x}{nb>>8:02x}'
        canvas.create_line(0, i, width, i, fill=color, tags=("gradient",))



# ==================== MODERN BUTTON CLASS ====================


class ModernButton(tk.Canvas):
    """Modern rounded button with hover effects"""

    def __init__(self, parent, text, command, bg_color, hover_color, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text

        width = kwargs.get("width", 300)
        height = kwargs.get("height", 60)

        self.configure(width=width, height=height, bg=parent.cget("bg"))

        # Draw rounded rectangle
        self.rect = self.create_rounded_rect(5, 5, width - 5, height - 5, radius=15, fill=bg_color)
        self.text_id = self.create_text(width // 2, height // 2, text=text,
                                        font=("Segoe UI", 14, "bold"), fill="white")

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", lambda e: self.command())

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, e):
        self.itemconfig(self.rect, fill=self.hover_color)
        self.config(cursor="hand2")

    def on_leave(self, e):
        self.itemconfig(self.rect, fill=self.bg_color)



# ==================== MAIN APPLICATION ====================


class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1300x750")
        self.root.configure(bg="#f5f7fa")

        # Initialize files
        initialize_files()

        # Configure modern styles
        self.setup_styles()

        # Create main container
        self.create_main_menu()

    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Configure Treeview
        style.configure("Modern.Treeview",
                        background="#ffffff",
                        foreground="#2c3e50",
                        rowheight=35,
                        fieldbackground="#ffffff",
                        borderwidth=0)
        style.configure("Modern.Treeview.Heading",
                        background="#34495e",
                        foreground="white",
                        relief="flat",
                        font=("Segoe UI", 11, "bold"))
        style.map("Modern.Treeview", background=[("selected", "#3498db")])

        # Configure Combobox
        style.configure("Modern.TCombobox",
                        fieldbackground="#ffffff",
                        background="#3498db",
                        borderwidth=1)

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_gradient_header(self, parent, title, color1, color2):
        """Create modern gradient header"""
        header_frame = tk.Frame(parent, height=120)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        canvas = tk.Canvas(header_frame, height=120, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Create gradient
        create_gradient(canvas, 1300, 120, color1, color2)

        # Title with shadow effect
        canvas.create_text(652, 62, text=title,
                           font=("Segoe UI", 32, "bold"), fill="#2c3e50", anchor="center")
        canvas.create_text(650, 60, text=title,
                           font=("Segoe UI", 32, "bold"), fill="white", anchor="center")

        return header_frame, canvas

    def create_main_menu(self):
        """Create modern main menu interface"""
        self.clear_window()

        # Gradient Header
        header_frame, canvas = self.create_gradient_header(
            self.root, "🏨 HOTEL LUXURY", "#3498db", "#9b59b6"
        )

        # Subtitle on canvas
        canvas.create_text(650, 95, text="Premium Hotel Management System",
                           font=("Segoe UI", 14), fill="white", anchor="center")

        # Main content with card-like design
        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=60, pady=40)

        # Create cards grid
        buttons_data = [
            ("📋\nShow Rooms", self.show_rooms, "#3498db", "#2980b9"),
            ("✅\nCheck-In", self.check_in, "#27ae60", "#229954"),
            ("🚪\nCheck-Out", self.check_out, "#e67e22", "#d35400"),
            ("💰\nView Bill", self.view_bill, "#16a085", "#138d75"),
            ("🍽️\nServices", self.services_menu, "#9b59b6", "#8e44ad"),
            ("⚠️\nGrievance", self.submit_grievance, "#e74c3c", "#c0392b"),
            ("⭐\nFeedback", self.submit_feedback, "#f39c12", "#e67e22"),
        ]

        for i, (text, command, color, hover) in enumerate(buttons_data):
            row = i // 3
            col = i % 3

            # Card frame
            card = tk.Frame(content, bg="white", relief="solid", bd=1)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            # Add subtle shadow effect by placing a gray frame behind
            shadow = tk.Frame(content, bg="#d0d0d0", relief="flat")
            shadow.place(in_=card, x=3, y=3, relwidth=1, relheight=1)
            card.lift()

            # Button inside card
            btn = ModernButton(card, text.replace("\n", " "), command,
                               color, hover, width=280, height=120)
            btn.pack(padx=10, pady=10)

            content.grid_rowconfigure(row, weight=1)
            content.grid_columnconfigure(col, weight=1)

        # Exit button at bottom
        exit_frame = tk.Frame(content, bg="#f5f7fa")
        exit_frame.grid(row=2, column=0, columnspan=3, pady=20)

        exit_btn = ModernButton(exit_frame, "❌ Exit Application", self.root.quit,
                               "#95a5a6", "#7f8c8d", width=300, height=50)
        exit_btn.pack()

        # Footer with modern styling
        footer = tk.Frame(self.root, bg="#34495e", height=40)
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, text="© 2024 Hotel Luxury Management System | All Rights Reserved",
                 font=("Segoe UI", 10), bg="#34495e", fg="white").pack(pady=10)

    def create_back_button(self, canvas, command):
        """Create modern back button on canvas"""
        back_btn_id = canvas.create_text(50, 60, text="← Back",
                                         font=("Segoe UI", 14, "bold"),
                                         fill="white", anchor="w", tags="back_btn")

        def on_click(e):
            command()

        def on_enter(e):
            canvas.itemconfig(back_btn_id, fill="#ecf0f1")
            canvas.config(cursor="hand2")

        def on_leave(e):
            canvas.itemconfig(back_btn_id, fill="white")
            canvas.config(cursor="")

        canvas.tag_bind("back_btn", "<Button-1>", on_click)
        canvas.tag_bind("back_btn", "<Enter>", on_enter)
        canvas.tag_bind("back_btn", "<Leave>", on_leave)

    def show_rooms(self):
        """Display all rooms with modern styling"""
        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "📋 ROOM STATUS", "#3498db", "#2ecc71"
        )
        self.create_back_button(canvas, self.create_main_menu)

        # Content frame with modern card
        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=40, pady=30)

        # Card for treeview
        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # Title
        tk.Label(card, text="Available & Booked Rooms",
                 font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

        # Treeview
        tree_frame = tk.Frame(card, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = ("Room No", "Type", "Status", "Price/Night")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                            height=15, style="Modern.Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=280, anchor="center")

        try:
            with open("rooms.txt", "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")
                    if len(data) >= 4:
                        status_color = "available" if data[2] == "Available" else "booked"
                        tree.insert("", "end", values=(data[0], data[1], data[2], f"₹{data[3]}"),
                                    tags=(status_color,))

            tree.tag_configure("available", foreground="#27ae60", font=("Segoe UI", 10, "bold"))
            tree.tag_configure("booked", foreground="#e74c3c", font=("Segoe UI", 10, "bold"))
        except Exception:
            messagebox.showerror("Error", "Room data not found!")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def check_in(self):
        """Modern check-in interface"""
        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "✅ CHECK-IN", "#27ae60", "#16a085"
        )
        self.create_back_button(canvas, self.create_main_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=60, pady=40)

        # Modern card
        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(pady=20, padx=50)

        # Add padding inside card
        form = tk.Frame(card, bg="white")
        form.pack(padx=40, pady=30)

        tk.Label(form, text="Book Your Perfect Stay",
                 font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").grid(
            row=0, column=0, columnspan=2, pady=(0, 25))

        fields = []

        # Modern styled labels and entries
        labels_data = [
            ("Room Type:", None),
            ("Customer Name:", None),
            ("ID Proof (Aadhaar/PAN):", None),
            ("Number of Days:", None),
            ("Phone Number:", None),
        ]

        room_var = tk.StringVar()

        for i, (label, _) in enumerate(labels_data):
            # Label with modern styling
            lbl = tk.Label(form, text=label, font=("Segoe UI", 12),
                           bg="white", fg="#34495e", anchor="w")
            lbl.grid(row=i + 1, column=0, sticky="w", padx=10, pady=12)

            if i == 0:
                # Room type combobox
                room_combo = ttk.Combobox(form, textvariable=room_var,
                                          font=("Segoe UI", 11),
                                          values=["Normal - ₹1000/night",
                                                  "Deluxe - ₹1800/night",
                                                  "Suite - ₹3000/night"],
                                          state="readonly", width=32,
                                          style="Modern.TCombobox")
                room_combo.grid(row=i + 1, column=1, padx=10, pady=12)
                room_combo.current(0)
            else:
                # Modern entry
                entry = tk.Entry(form, font=("Segoe UI", 11), width=35,
                                 relief="solid", bd=1, bg="#f8f9fa")
                entry.grid(row=i + 1, column=1, padx=10, pady=12)
                fields.append(entry)

        def process_booking():
            room_type = room_var.get().split(" - ")[0]
            name = fields[0].get().strip()
            id_proof = fields[1].get().strip()
            days = fields[2].get().strip()
            phone = fields[3].get().strip()

            if not all([name, id_proof, days, phone]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                days = int(days)
                if days <= 0:
                    raise ValueError()
            except Exception:
                messagebox.showerror("Error", "Invalid number of days!")
                return

            try:
                with open("rooms.txt", "r", encoding="utf-8") as f:
                    rooms = f.readlines()

                booked = False
                new_data = []

                for line in rooms:
                    data = line.strip().split(",")

                    if len(data) >= 4 and data[1] == room_type and data[2] == "Available" and not booked:
                        total = int(data[3]) * days

                        confirm = messagebox.askyesno(
                            "Confirm Booking",
                            f"Room: {data[0]} ({room_type})\n"
                            f"Price: ₹{data[3]}/night\n"
                            f"Days: {days}\n"
                            f"Total: ₹{total}\n\n"
                            f"Confirm booking?"
                        )

                        if not confirm:
                            return

                        timestamp = get_timestamp()
                        with open("customers.txt", "a", encoding="utf-8") as c:
                            c.write(f"{name},{id_proof},{data[0]},{data[1]},{days},{total},{phone},{timestamp}\n")

                        data[2] = "Booked"
                        booked = True

                        messagebox.showinfo(
                            "Success",
                            f"✓ Room booked successfully!\n\n"
                            f"Room Number: {data[0]}\n"
                            f"Check-in Time: {timestamp}"
                        )
                        self.create_main_menu()

                    new_data.append(",".join(data) + "\n")

                if not booked:
                    messagebox.showerror("Sorry", f"No {room_type} rooms available!")
                    return

                with open("rooms.txt", "w", encoding="utf-8") as f:
                    f.writelines(new_data)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Modern button
        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=25)

        book_btn = ModernButton(btn_frame, "Book Room Now", process_booking,
                                "#27ae60", "#229954", width=250, height=50)
        book_btn.pack()

    def check_out(self):
        """Modern check-out interface"""
        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "🚪 CHECK-OUT", "#e67e22", "#d35400"
        )
        self.create_back_button(canvas, self.create_main_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=60, pady=60)

        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(pady=20, padx=100)

        form = tk.Frame(card, bg="white")
        form.pack(padx=50, pady=40)

        tk.Label(form, text="Complete Your Check-Out",
                 font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").grid(
            row=0, column=0, columnspan=2, pady=(0, 30))

        tk.Label(form, text="Customer Name:", font=("Segoe UI", 12),
                 bg="white", fg="#34495e").grid(row=1, column=0, sticky="w", padx=10, pady=15)
        name_entry = tk.Entry(form, font=("Segoe UI", 11), width=35,
                              relief="solid", bd=1, bg="#f8f9fa")
        name_entry.grid(row=1, column=1, padx=10, pady=15)

        tk.Label(form, text="ID Proof:", font=("Segoe UI", 12),
                 bg="white", fg="#34495e").grid(row=2, column=0, sticky="w", padx=10, pady=15)
        id_entry = tk.Entry(form, font=("Segoe UI", 11), width=35,
                            relief="solid", bd=1, bg="#f8f9fa")
        id_entry.grid(row=2, column=1, padx=10, pady=15)

        def process_checkout():
            name = name_entry.get().strip()
            id_proof = id_entry.get().strip()

            if not name or not id_proof:
                messagebox.showerror("Error", "Both fields are required!")
                return

            try:
                with open("customers.txt", "r", encoding="utf-8") as f:
                    customers = f.readlines()

                new_customers = []
                found = False
                freed_room = ""
                customer_data = None

                for line in customers:
                    data = line.strip().split(",")
                    if len(data) >= 6 and data[0].lower() == name.lower() and data[1] == id_proof:
                        found = True
                        freed_room = data[2]
                        customer_data = data
                    else:
                        new_customers.append(line)

                if found:
                    with open("customers.txt", "w", encoding="utf-8") as f:
                        f.writelines(new_customers)

                    with open("rooms.txt", "r", encoding="utf-8") as f:
                        rooms = f.readlines()

                    updated_rooms = []
                    for line in rooms:
                        data = line.strip().split(",")
                        if len(data) >= 3 and data[0] == freed_room:
                            data[2] = "Available"
                        updated_rooms.append(",".join(data) + "\n")

                    with open("rooms.txt", "w", encoding="utf-8") as f:
                        f.writelines(updated_rooms)

                    # Calculate complete bill
                    bill_data = self.calculate_bill(name, id_proof)

                    # Create detailed bill message
                    bill_message = f"✓ Thank you for staying with us!\n\n"
                    bill_message += f"Customer: {customer_data[0]}\n"
                    bill_message += f"Room: {customer_data[2]}\n"
                    bill_message += f"Check-out Time: {get_timestamp()}\n"
                    bill_message += f"\n{'=' * 40}\n"
                    bill_message += f"BILL SUMMARY\n"
                    bill_message += f"{'=' * 40}\n\n"

                    if bill_data["room_total"] > 0:
                        bill_message += f"Room Charges: ₹{bill_data['room_total']}\n"
                    if bill_data["food_total"] > 0:
                        bill_message += f"Food Orders: ₹{bill_data['food_total']}\n"
                    if bill_data["services_total"] > 0:
                        bill_message += f"Services: ₹{bill_data['services_total']}\n"
                    if bill_data["housekeeping_total"] > 0:
                        bill_message += f"Housekeeping: ₹{bill_data['housekeeping_total']}\n"

                    bill_message += f"\n{'=' * 40}\n"
                    bill_message += f"GRAND TOTAL: ₹{bill_data['grand_total']}\n"
                    bill_message += f"{'=' * 40}"

                    messagebox.showinfo("Check-out Complete", bill_message)
                    self.create_main_menu()
                else:
                    messagebox.showerror("Error", "Customer not found!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=25)

        checkout_btn = ModernButton(btn_frame, "Complete Check-Out", process_checkout,
                                    "#e67e22", "#d35400", width=250, height=50)
        checkout_btn.pack()

    def view_bill(self):
        """View current bill for a customer"""
        customer = self.verify_customer()
        if not customer["room"]:
            return

        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "💰 YOUR CURRENT BILL", "#16a085", "#138d75"
        )
        self.create_back_button(canvas, self.create_main_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=40, pady=30)

        # Calculate bill
        bill_data = self.calculate_bill(customer["name"], customer["id"])

        # Card for bill
        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        # Title
        tk.Label(card, text=f"Bill for Room {customer['room']}",
                 font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        # Customer info
        info_frame = tk.Frame(card, bg="#ecf0f1", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=30, pady=(0, 20))

        tk.Label(info_frame, text=f"Guest Name: {customer['name']}",
                 font=("Segoe UI", 12), bg="#ecf0f1", fg="#2c3e50").pack(
            anchor="w", padx=20, pady=5)
        tk.Label(info_frame, text=f"Room: {customer['room']}",
                 font=("Segoe UI", 12), bg="#ecf0f1", fg="#2c3e50").pack(
            anchor="w", padx=20, pady=5)

        # Scrollable bill details
        canvas_frame = tk.Canvas(card, bg="white", highlightthickness=0, height=300)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas_frame.yview)
        scrollable_frame = tk.Frame(canvas_frame, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))
        )

        canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar.set)

        # Room charges
        if bill_data["room_total"] > 0:
            section_frame = tk.Frame(scrollable_frame, bg="white")
            section_frame.pack(fill="x", padx=30, pady=10)

            tk.Label(section_frame, text="🏨 ROOM CHARGES",
                     font=("Segoe UI", 13, "bold"), bg="white", fg="#3498db").pack(
                anchor="w", pady=(0, 10))

            for item in bill_data["room_items"]:
                item_frame = tk.Frame(section_frame, bg="#f8f9fa", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2)

                tk.Label(item_frame, text=item["desc"], font=("Segoe UI", 10),
                         bg="#f8f9fa", fg="#2c3e50").pack(side="left", padx=15, pady=8)
                tk.Label(item_frame, text=f"₹{item['amount']}", font=("Segoe UI", 10, "bold"),
                         bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=15, pady=8)

            total_frame = tk.Frame(section_frame, bg="#3498db")
            total_frame.pack(fill="x", pady=(5, 0))
            tk.Label(total_frame, text=f"Subtotal: ₹{bill_data['room_total']}",
                     font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white").pack(
                side="right", padx=15, pady=5)

        # Food orders
        if bill_data["food_total"] > 0:
            section_frame = tk.Frame(scrollable_frame, bg="white")
            section_frame.pack(fill="x", padx=30, pady=10)

            tk.Label(section_frame, text="🍽️ FOOD ORDERS",
                     font=("Segoe UI", 13, "bold"), bg="white", fg="#e74c3c").pack(
                anchor="w", pady=(0, 10))

            for item in bill_data["food_items"]:
                item_frame = tk.Frame(section_frame, bg="#f8f9fa", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2)

                tk.Label(item_frame, text=item["desc"], font=("Segoe UI", 10),
                         bg="#f8f9fa", fg="#2c3e50").pack(side="left", padx=15, pady=8)
                tk.Label(item_frame, text=f"₹{item['amount']}", font=("Segoe UI", 10, "bold"),
                         bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=15, pady=8)

            total_frame = tk.Frame(section_frame, bg="#e74c3c")
            total_frame.pack(fill="x", pady=(5, 0))
            tk.Label(total_frame, text=f"Subtotal: ₹{bill_data['food_total']}",
                     font=("Segoe UI", 11, "bold"), bg="#e74c3c", fg="white").pack(
                side="right", padx=15, pady=5)

        # Services
        if bill_data["services_total"] > 0:
            section_frame = tk.Frame(scrollable_frame, bg="white")
            section_frame.pack(fill="x", padx=30, pady=10)

            tk.Label(section_frame, text="🛍️ SERVICES",
                     font=("Segoe UI", 13, "bold"), bg="white", fg="#3498db").pack(
                anchor="w", pady=(0, 10))

            for item in bill_data["service_items"]:
                item_frame = tk.Frame(section_frame, bg="#f8f9fa", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2)

                tk.Label(item_frame, text=item["desc"], font=("Segoe UI", 10),
                         bg="#f8f9fa", fg="#2c3e50").pack(side="left", padx=15, pady=8)
                tk.Label(item_frame, text=f"₹{item['amount']}", font=("Segoe UI", 10, "bold"),
                         bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=15, pady=8)

            total_frame = tk.Frame(section_frame, bg="#3498db")
            total_frame.pack(fill="x", pady=(5, 0))
            tk.Label(total_frame, text=f"Subtotal: ₹{bill_data['services_total']}",
                     font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white").pack(
                side="right", padx=15, pady=5)

        # Housekeeping
        if bill_data["housekeeping_total"] > 0:
            section_frame = tk.Frame(scrollable_frame, bg="white")
            section_frame.pack(fill="x", padx=30, pady=10)

            tk.Label(section_frame, text="🧹 HOUSEKEEPING",
                     font=("Segoe UI", 13, "bold"), bg="white", fg="#27ae60").pack(
                anchor="w", pady=(0, 10))

            for item in bill_data["housekeeping_items"]:
                item_frame = tk.Frame(section_frame, bg="#f8f9fa", relief="solid", bd=1)
                item_frame.pack(fill="x", pady=2)

                tk.Label(item_frame, text=item["desc"], font=("Segoe UI", 10),
                         bg="#f8f9fa", fg="#2c3e50").pack(side="left", padx=15, pady=8)
                tk.Label(item_frame, text=f"₹{item['amount']}", font=("Segoe UI", 10, "bold"),
                         bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=15, pady=8)

            total_frame = tk.Frame(section_frame, bg="#27ae60")
            total_frame.pack(fill="x", pady=(5, 0))
            tk.Label(total_frame, text=f"Subtotal: ₹{bill_data['housekeeping_total']}",
                     font=("Segoe UI", 11, "bold"), bg="#27ae60", fg="white").pack(
                side="right", padx=15, pady=5)

        canvas_frame.pack(side="left", fill="both", expand=True, padx=30)
        scrollbar.pack(side="right", fill="y")

        # Grand total
        total_card = tk.Frame(card, bg="#2c3e50", relief="solid", bd=2)
        total_card.pack(fill="x", padx=30, pady=20)

        tk.Label(total_card, text=f"GRAND TOTAL: ₹{bill_data['grand_total']}",
                 font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="#f39c12").pack(pady=15)

        # Note
        tk.Label(card, text="Note: This is a current bill. Final bill will be generated at checkout.",
                 font=("Segoe UI", 9, "italic"), bg="white", fg="#7f8c8d").pack(pady=(0, 15))

    def services_menu(self):
        """Modern services menu"""
        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "🍽️ IN-HOUSE SERVICES", "#9b59b6", "#8e44ad"
        )
        self.create_back_button(canvas, self.create_main_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, pady=60)

        buttons_data = [
            ("🍔\nOrder Food", self.order_food, "#e74c3c", "#c0392b"),
            ("🛍️\nNon-Food Items", self.order_non_food, "#3498db", "#2980b9"),
            ("🧹\nHousekeeping", self.request_housekeeping, "#27ae60", "#229954"),
        ]

        for text, command, color, hover in buttons_data:
            card = tk.Frame(content, bg="white", relief="solid", bd=1)
            card.pack(pady=15)

            btn = ModernButton(card, text.replace("\n", " - "), command,
                               color, hover, width=400, height=80)
            btn.pack(padx=10, pady=10)

    def calculate_bill(self, name, id_proof):
        """Calculate complete bill for a customer"""
        bill_data = {
            "room_total": 0,
            "food_total": 0,
            "services_total": 0,
            "housekeeping_total": 0,
            "grand_total": 0,
            "room_items": [],
            "food_items": [],
            "service_items": [],
            "housekeeping_items": [],
        }

        # Room charges
        try:
            with open("customers.txt", "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")
                    if len(data) >= 6 and data[0].lower() == name.lower() and data[1] == id_proof:
                        room_total = int(data[5])
                        bill_data["room_total"] = room_total
                        nights = int(data[4]) if data[4].isdigit() else 1
                        per_night = int(room_total // max(1, nights))
                        bill_data["room_items"].append({
                            "desc": f"{data[3]} Room - {nights} day(s) @ ₹{per_night}/night",
                            "amount": room_total,
                        })
                        break
        except Exception:
            pass

        # Food orders
        try:
            with open("food_orders.txt", "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")
                    if len(data) >= 7 and data[0].lower() == name.lower() and data[1] == id_proof:
                        item_total = int(data[6])
                        bill_data["food_total"] += item_total
                        bill_data["food_items"].append({
                            "desc": f"{data[3]} x{data[4]}",
                            "amount": item_total,
                        })
        except Exception:
            pass

        # Services (non-food items)
        try:
            with open("services.txt", "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")
                    if len(data) >= 7 and data[0].lower() == name.lower() and data[1] == id_proof:
                        item_total = int(data[6])
                        bill_data["services_total"] += item_total
                        bill_data["service_items"].append({
                            "desc": f"{data[3]} x{data[4]}",
                            "amount": item_total,
                        })
        except Exception:
            pass

        # Housekeeping
        try:
            with open("housekeeping.txt", "r", encoding="utf-8") as f:
                for line in f:
                    data = line.strip().split(",")
                    if len(data) >= 5 and data[0].lower() == name.lower() and data[1] == id_proof:
                        service_cost = int(data[4])
                        bill_data["housekeeping_total"] += service_cost
                        bill_data["housekeeping_items"].append({
                            "desc": data[3],
                            "amount": service_cost,
                        })
        except Exception:
            pass

        bill_data["grand_total"] = (
            bill_data["room_total"]
            + bill_data["food_total"]
            + bill_data["services_total"]
            + bill_data["housekeeping_total"]
        )

        return bill_data

    def verify_customer(self):
        """Modern customer verification dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Customer Verification")
        dialog.geometry("450x280")
        dialog.configure(bg="white")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"450x280+{x}+{y}")

        result = {"name": None, "id": None, "room": None}

        tk.Label(dialog, text="🔐 Verify Your Identity",
                 font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=25)

        frame = tk.Frame(dialog, bg="white")
        frame.pack(pady=15)

        tk.Label(frame, text="Name:", font=("Segoe UI", 12),
                 bg="white", fg="#34495e").grid(row=0, column=0, padx=15, pady=10, sticky="w")
        name_entry = tk.Entry(frame, font=("Segoe UI", 11), width=28,
                              relief="solid", bd=1, bg="#f8f9fa")
        name_entry.grid(row=0, column=1, padx=15, pady=10)

        tk.Label(frame, text="ID Proof:", font=("Segoe UI", 12),
                 bg="white", fg="#34495e").grid(row=1, column=0, padx=15, pady=10, sticky="w")
        id_entry = tk.Entry(frame, font=("Segoe UI", 11), width=28,
                            relief="solid", bd=1, bg="#f8f9fa")
        id_entry.grid(row=1, column=1, padx=15, pady=10)

        def verify():
            name = name_entry.get().strip()
            id_proof = id_entry.get().strip()

            if not name or not id_proof:
                messagebox.showerror("Error", "Both fields required!")
                return

            room = get_customer_room(name, id_proof)
            if room:
                result["name"] = name
                result["id"] = id_proof
                result["room"] = room
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Customer not found! Please check-in first.")

        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=20)

        verify_btn = ModernButton(btn_frame, "✓ Verify", verify,
                                   "#27ae60", "#229954", width=200, height=45)
        verify_btn.pack()

        self.root.wait_window(dialog)
        return result

    def order_food(self):
        """Modern food ordering interface"""
        customer = self.verify_customer()
        if not customer["room"]:
            return

        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "🍔 FOOD MENU", "#e74c3c", "#c0392b"
        )
        canvas.create_text(650, 95, text=f"Room: {customer['room']}",
                           font=("Segoe UI", 14, "bold"), fill="white", anchor="center")
        self.create_back_button(canvas, self.services_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=30, pady=20)

        menu = {
            "Breakfast Combo": 250, "Lunch Thali": 350, "Dinner Combo": 400,
            "Sandwich": 150, "Pizza": 450, "Pasta": 300, "Biryani": 350,
            "Chinese Combo": 400, "South Indian": 200, "Dessert": 150,
        }

        selections = {}

        # Card for menu
        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(card, text="Select Your Items",
                 font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

        canvas_frame = tk.Canvas(card, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas_frame.yview)
        scrollable_frame = tk.Frame(canvas_frame, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")),
        )

        canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar.set)

        for i, (item, price) in enumerate(menu.items()):
            item_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
            item_frame.pack(fill="x", padx=20, pady=8)

            tk.Label(item_frame, text=item, font=("Segoe UI", 12, "bold"),
                     bg="#f8f9fa", fg="#2c3e50", width=18, anchor="w").pack(side="left", padx=15, pady=12)

            tk.Label(item_frame, text=f"₹{price}", font=("Segoe UI", 12),
                     bg="#f8f9fa", fg="#27ae60", width=8).pack(side="left", padx=5)

            qty_var = tk.IntVar(value=0)
            selections[item] = (price, qty_var)

            tk.Label(item_frame, text="Qty:", font=("Segoe UI", 11),
                     bg="#f8f9fa", fg="#34495e").pack(side="right", padx=(0, 10))

            qty_spin = tk.Spinbox(item_frame, from_=0, to=10, textvariable=qty_var,
                                 font=("Segoe UI", 11), width=5, relief="solid", bd=1)
            qty_spin.pack(side="right", padx=10)

        canvas_frame.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def place_order():
            orders = [(item, qty.get(), price) for item, (price, qty) in selections.items() if qty.get() > 0]

            if not orders:
                messagebox.showwarning("No Items", "Please select at least one item!")
                return

            total = sum(price * qty for _, qty, price in orders)
            order_text = "\n".join([f"{item} x{qty} = ₹{price * qty}" for item, qty, price in orders])

            confirm = messagebox.askyesno(
                "Confirm Order",
                f"{order_text}\n\nTotal: ₹{total}\n\nConfirm order?",
            )

            if confirm:
                timestamp = get_timestamp()
                with open("food_orders.txt", "a", encoding="utf-8") as f:
                    for item, qty, price in orders:
                        f.write(f"{customer['name']},{customer['id']},{customer['room']},"
                                f"{item},{qty},{price},{price * qty},{timestamp}\n")

                messagebox.showinfo(
                    "Success",
                    f"✓ Order placed successfully!\n\n"
                    f"Total: ₹{total}\n"
                    f"Delivery time: 30-45 minutes",
                )
                self.services_menu()

        btn_frame = tk.Frame(self.root, bg="#f5f7fa")
        btn_frame.pack(pady=15)

        order_btn = ModernButton(btn_frame, "🛒 Place Order", place_order,
                                 "#27ae60", "#229954", width=250, height=50)
        order_btn.pack()

    def order_non_food(self):
        """Modern non-food items ordering"""
        customer = self.verify_customer()
        if not customer["room"]:
            return

        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "🛍️ NON-FOOD ITEMS", "#3498db", "#2980b9"
        )
        canvas.create_text(650, 95, text=f"Room: {customer['room']}",
                           font=("Segoe UI", 14, "bold"), fill="white", anchor="center")
        self.create_back_button(canvas, self.services_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=30, pady=20)

        items = {
            "Extra Towels": 50, "Toiletries Kit": 100, "Mineral Water (1L)": 30,
            "Newspaper": 10, "Laundry Bag": 20, "Iron": 100, "Hair Dryer": 100,
            "Extra Pillows": 80, "Blanket": 150, "Room Slippers": 120,
        }

        selections = {}

        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(card, text="Select Items You Need",
                 font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=15)

        canvas_frame = tk.Canvas(card, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas_frame.yview)
        scrollable_frame = tk.Frame(canvas_frame, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_frame.configure(scrollregion=canvas_frame.bbox("all")),
        )

        canvas_frame.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_frame.configure(yscrollcommand=scrollbar.set)

        for item, price in items.items():
            item_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
            item_frame.pack(fill="x", padx=20, pady=8)

            tk.Label(item_frame, text=item, font=("Segoe UI", 12, "bold"),
                     bg="#f8f9fa", fg="#2c3e50", width=18, anchor="w").pack(side="left", padx=15, pady=12)

            tk.Label(item_frame, text=f"₹{price}", font=("Segoe UI", 12),
                     bg="#f8f9fa", fg="#27ae60", width=8).pack(side="left", padx=5)

            qty_var = tk.IntVar(value=0)
            selections[item] = (price, qty_var)

            tk.Label(item_frame, text="Qty:", font=("Segoe UI", 11),
                     bg="#f8f9fa", fg="#34495e").pack(side="right", padx=(0, 10))

            qty_spin = tk.Spinbox(item_frame, from_=0, to=10, textvariable=qty_var,
                                 font=("Segoe UI", 11), width=5, relief="solid", bd=1)
            qty_spin.pack(side="right", padx=10)

        canvas_frame.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def place_order():
            orders = [(item, qty.get(), price) for item, (price, qty) in selections.items() if qty.get() > 0]

            if not orders:
                messagebox.showwarning("No Items", "Please select at least one item!")
                return

            total = sum(price * qty for _, qty, price in orders)
            order_text = "\n".join([f"{item} x{qty} = ₹{price * qty}" for item, qty, price in orders])

            confirm = messagebox.askyesno(
                "Confirm Order",
                f"{order_text}\n\nTotal: ₹{total}\n\nConfirm order?",
            )

            if confirm:
                timestamp = get_timestamp()
                with open("services.txt", "a", encoding="utf-8") as f:
                    for item, qty, price in orders:
                        f.write(f"{customer['name']},{customer['id']},{customer['room']},"
                                f"{item},{qty},{price},{price * qty},{timestamp}\n")

                messagebox.showinfo(
                    "Success",
                    f"✓ Order placed successfully!\n\n"
                    f"Total: ₹{total}\n"
                    f"Delivery time: 15-20 minutes",
                )
                self.services_menu()

        btn_frame = tk.Frame(self.root, bg="#f5f7fa")
        btn_frame.pack(pady=15)

        order_btn = ModernButton(btn_frame, "🛒 Place Order", place_order,
                                 "#27ae60", "#229954", width=250, height=50)
        order_btn.pack()

    def request_housekeeping(self):
        """Modern housekeeping service request"""
        customer = self.verify_customer()
        if not customer["room"]:
            return

        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "🧹 HOUSEKEEPING", "#27ae60", "#229954"
        )
        canvas.create_text(650, 95, text=f"Room: {customer['room']}",
                           font=("Segoe UI", 14, "bold"), fill="white", anchor="center")
        self.create_back_button(canvas, self.services_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=60, pady=40)

        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(pady=20, padx=50)

        form = tk.Frame(card, bg="white")
        form.pack(padx=40, pady=30)

        tk.Label(form, text="Select Housekeeping Services",
                 font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

        services = {
            "Room Cleaning": (tk.BooleanVar(), 200),
            "Bed Sheet Change": (tk.BooleanVar(), 150),
            "Towel Replacement": (tk.BooleanVar(), 150),
            "Bathroom Cleaning": (tk.BooleanVar(), 400),
            "Full Service": (tk.BooleanVar(), 700),
        }

        for service, (var, price) in services.items():
            check_frame = tk.Frame(form, bg="#f8f9fa", relief="solid", bd=1)
            check_frame.pack(fill="x", pady=5)

            service_frame = tk.Frame(check_frame, bg="#f8f9fa")
            service_frame.pack(fill="x")

            tk.Checkbutton(service_frame, text=service, variable=var,
                           font=("Segoe UI", 12), bg="#f8f9fa",
                           activebackground="#f8f9fa", fg="#2c3e50").pack(
                side="left", pady=8, padx=20)

            tk.Label(service_frame, text=f"₹{price}", font=("Segoe UI", 11, "bold"),
                     bg="#f8f9fa", fg="#27ae60").pack(side="right", padx=20, pady=8)

        tk.Label(form, text="Preferred Time:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#34495e").pack(pady=(20, 5), anchor="w")
        time_entry = tk.Entry(form, font=("Segoe UI", 11), width=40,
                              relief="solid", bd=1, bg="#f8f9fa")
        time_entry.insert(0, "Now")
        time_entry.pack(pady=(0, 15))

        tk.Label(form, text="Special Requirements (Optional):",
                 font=("Segoe UI", 12, "bold"), bg="white", fg="#34495e").pack(
            pady=(10, 5), anchor="w")
        req_text = tk.Text(form, font=("Segoe UI", 11), width=45, height=4,
                          relief="solid", bd=1, bg="#f8f9fa", wrap=tk.WORD)
        req_text.pack(pady=(0, 20))

        def submit_request():
            selected = [(s, p) for s, (v, p) in services.items() if v.get()]

            if not selected:
                messagebox.showwarning("No Services", "Please select at least one service!")
                return

            pref_time = time_entry.get().strip()
            special_req = req_text.get("1.0", "end-1c").strip()

            total_cost = sum(price for _, price in selected)

            timestamp = get_timestamp()
            with open("housekeeping.txt", "a", encoding="utf-8") as f:
                for service, price in selected:
                    f.write(f"{customer['name']},{customer['id']},{customer['room']},"
                            f"{service},{price},{pref_time},{special_req},{timestamp},Pending\n")

            messagebox.showinfo(
                "Success",
                f"✓ Housekeeping request submitted!\n\n"
                f"Services: {', '.join([s for s, _ in selected])}\n"
                f"Total Cost: ₹{total_cost}\n"
                f"Preferred Time: {pref_time}",
            )
            self.services_menu()

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.pack(pady=10)

        submit_btn = ModernButton(btn_frame, "Submit Request", submit_request,
                                  "#27ae60", "#229954", width=250, height=50)
        submit_btn.pack()

    def submit_grievance(self):
        """Modern grievance submission"""
        customer = self.verify_customer()
        if not customer["room"]:
            return

        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "⚠️ GRIEVANCE", "#e74c3c", "#c0392b"
        )
        canvas.create_text(650, 95, text=f"Room: {customer['room']}",
                           font=("Segoe UI", 14, "bold"), fill="white", anchor="center")
        self.create_back_button(canvas, self.create_main_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=60, pady=30)

        card = tk.Frame(content, bg="white", relief="solid", bd=1)
        card.pack(fill="both", expand=True, padx=50, pady=10)

        form = tk.Frame(card, bg="white")
        form.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(form, text="Submit Your Grievance",
                 font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))

        tk.Label(form, text="Category:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#34495e").pack(pady=(10, 5), anchor="w")

        category_var = tk.StringVar()
        categories = ["Room Cleanliness", "Staff Behavior", "Amenities Issue",
                      "Noise Complaint", "Food Quality", "Maintenance Issue", "Other"]

        category_combo = ttk.Combobox(form, textvariable=category_var,
                                      font=("Segoe UI", 11), values=categories,
                                      state="readonly", width=48, style="Modern.TCombobox")
        category_combo.pack(pady=(0, 15))
        category_combo.current(0)

        tk.Label(form, text="Priority:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#34495e").pack(pady=(10, 5), anchor="w")

        priority_var = tk.StringVar()
        priority_combo = ttk.Combobox(form, textvariable=priority_var,
                                      font=("Segoe UI", 11),
                                      values=["High", "Medium", "Low"],
                                      state="readonly", width=48, style="Modern.TCombobox")
        priority_combo.pack(pady=(0, 15))
        priority_combo.current(1)

        tk.Label(form, text="Description:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#34495e").pack(pady=(10, 5), anchor="w")

        desc_text = scrolledtext.ScrolledText(form, font=("Segoe UI", 11),
                                             width=55, height=8, wrap=tk.WORD,
                                             relief="solid", bd=1, bg="#f8f9fa")
        desc_text.pack(pady=(0, 20))

        def submit():
            category = category_var.get()
            priority = priority_var.get()
            description = desc_text.get("1.0", "end-1c").strip()

            if not description:
                messagebox.showerror("Error", "Please provide a description!")
                return

            timestamp = get_timestamp()
            with open("grievances.txt", "a", encoding="utf-8") as f:
                f.write(f"{customer['name']},{customer['id']},{customer['room']},"
                        f"{category},{priority},{description},{timestamp},Open\n")

            messagebox.showinfo(
                "Success",
                "✓ Grievance submitted successfully!\n\n"
                "Our team will address your concern shortly.",
            )
            self.create_main_menu()

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.pack(pady=10)

        submit_btn = ModernButton(btn_frame, "Submit Grievance", submit,
                                  "#e74c3c", "#c0392b", width=250, height=50)
        submit_btn.pack()

    def submit_feedback(self):
        """Modern feedback submission"""
        self.clear_window()

        header_frame, canvas = self.create_gradient_header(
            self.root, "⭐ FEEDBACK", "#f39c12", "#e67e22"
        )
        self.create_back_button(canvas, self.create_main_menu)

        content = tk.Frame(self.root, bg="#f5f7fa")
        content.pack(fill="both", expand=True, padx=50, pady=30)

        # Scrollable card
        canvas_main = tk.Canvas(content, bg="#f5f7fa", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas_main.yview)
        card = tk.Frame(canvas_main, bg="white", relief="solid", bd=1)

        card.bind(
            "<Configure>",
            lambda e: canvas_main.configure(scrollregion=canvas_main.bbox("all")),
        )

        canvas_main.create_window((0, 0), window=card, anchor="nw")
        canvas_main.configure(yscrollcommand=scrollbar.set)

        form = tk.Frame(card, bg="white")
        form.pack(padx=40, pady=30, fill="both", expand=True)

        tk.Label(form, text="We Value Your Feedback",
                 font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 25))

        # Name and ID
        info_frame = tk.Frame(form, bg="white")
        info_frame.pack(fill="x", pady=(0, 20))

        tk.Label(info_frame, text="Your Name:", font=("Segoe UI", 12),
                 bg="white", fg="#34495e").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        name_entry = tk.Entry(info_frame, font=("Segoe UI", 11), width=35,
                             relief="solid", bd=1, bg="#f8f9fa")
        name_entry.grid(row=0, column=1, padx=10, pady=8)

        tk.Label(info_frame, text="ID Proof (Optional):", font=("Segoe UI", 12),
                 bg="white", fg="#34495e").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        id_entry = tk.Entry(info_frame, font=("Segoe UI", 11), width=35,
                           relief="solid", bd=1, bg="#f8f9fa")
        id_entry.grid(row=1, column=1, padx=10, pady=8)

        # Ratings
        tk.Label(form, text="Rate Your Experience (1-5 stars)",
                 font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50").pack(
            pady=(15, 10), anchor="w")

        ratings = {}
        categories = ["Room Quality", "Staff Service", "Food Quality", "Overall Experience"]

        for category in categories:
            rating_card = tk.Frame(form, bg="#f8f9fa", relief="solid", bd=1)
            rating_card.pack(fill="x", pady=5)

            tk.Label(rating_card, text=f"{category}:", font=("Segoe UI", 11),
                     bg="#f8f9fa", fg="#2c3e50", width=18, anchor="w").pack(
                side="left", padx=15, pady=10)

            rating_var = tk.IntVar(value=5)
            ratings[category] = rating_var

            star_frame = tk.Frame(rating_card, bg="#f8f9fa")
            star_frame.pack(side="left", padx=20)

            for j in range(1, 6):
                tk.Radiobutton(star_frame, text="⭐" * j, variable=rating_var,
                              value=j, font=("Segoe UI", 10), bg="#f8f9fa",
                              activebackground="#f8f9fa", fg="#f39c12").pack(
                    side="left", padx=3)

        # Comments
        tk.Label(form, text="Additional Comments:", font=("Segoe UI", 12, "bold"),
                 bg="white", fg="#34495e").pack(pady=(20, 5), anchor="w")

        comments_text = tk.Text(form, font=("Segoe UI", 11), width=50, height=5,
                                wrap=tk.WORD, relief="solid", bd=1, bg="#f8f9fa")
        comments_text.pack(pady=(0, 15))

        # Recommendation
        rec_frame = tk.Frame(form, bg="#f8f9fa", relief="solid", bd=1)
        rec_frame.pack(fill="x", pady=10)

        tk.Label(rec_frame, text="Would you recommend us to others?",
                 font=("Segoe UI", 12), bg="#f8f9fa", fg="#2c3e50").pack(
            side="left", padx=20, pady=12)

        recommend_var = tk.StringVar(value="Yes")

        radio_frame = tk.Frame(rec_frame, bg="#f8f9fa")
        radio_frame.pack(side="left", padx=20)

        tk.Radiobutton(radio_frame, text="👍 Yes", variable=recommend_var,
                      value="Yes", font=("Segoe UI", 11), bg="#f8f9fa",
                      activebackground="#f8f9fa", fg="#27ae60").pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text="👎 No", variable=recommend_var,
                      value="No", font=("Segoe UI", 11), bg="#f8f9fa",
                      activebackground="#f8f9fa", fg="#e74c3c").pack(side="left", padx=10)

        def submit():
            name = name_entry.get().strip()
            id_proof = id_entry.get().strip()
            comments = comments_text.get("1.0", "end-1c").strip()
            recommend = recommend_var.get()

            if not name:
                messagebox.showerror("Error", "Name is required!")
                return

            room_no = "N/A"
            if id_proof:
                room_no = get_customer_room(name, id_proof) or "N/A"

            rating_values = [str(var.get()) for var in ratings.values()]

            timestamp = get_timestamp()
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(f"{name},{id_proof},{room_no},{','.join(rating_values)},"
                        f"{recommend},{comments},{timestamp}\n")

            messagebox.showinfo(
                "Thank You!",
                "✓ Thank you for your valuable feedback!\n\n"
                "Your feedback helps us improve our services.",
            )
            self.create_main_menu()

        btn_frame = tk.Frame(form, bg="white")
        btn_frame.pack(pady=20)

        submit_btn = ModernButton(btn_frame, "Submit Feedback", submit,
                                  "#f39c12", "#e67e22", width=250, height=50)
        submit_btn.pack()

        canvas_main.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


# ==================== MAIN EXECUTION ====================


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = HotelManagementSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()