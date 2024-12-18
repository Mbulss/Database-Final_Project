import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

# Koneksi ke database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Ganti dengan username MySQL Anda
            password="cikemewing",  # Ganti dengan password MySQL Anda
            database="eventmanagement"  # Ganti dengan nama database Anda
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

# Ambil data dari database dengan opsi pencarian
def fetch_data(query, params=None):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        data = cursor.fetchall()
        connection.close()
        return data
    return []

# Isi TreeView dengan data
def populate_treeview(tree, data):
    for row in tree.get_children():
        tree.delete(row)
    for item in data:
        tree.insert("", "end", values=list(item.values()))

# Variabel global untuk melacak tampilan aktif
current_view = None

# Navigasi antar halaman
def switch_frame(frame_func, active_button_text):
    global current_view
    for widget in main_frame.winfo_children():
        widget.destroy()
    frame_func()

    # Atur visibilitas tombol CRUD
    if frame_func == dashboard_view:
        hide_crud_buttons()
    else:
        show_crud_buttons()

    # Highlight tombol navigasi yang aktif
    highlight_nav_button(active_button_text)

# Halaman Dashboard Utama
def dashboard_view():
    global current_view
    current_view = None  # Tidak ada tabel aktif

    counts = {
        "Total Clients": "SELECT COUNT(clientId) AS count FROM client",
        "Total Events": "SELECT COUNT(eventId) AS count FROM event",
        "Total Categories": "SELECT COUNT(categoryId) AS count FROM eventCategory",
        "Total Venues": "SELECT COUNT(venueId) AS count FROM venue",
        "Total Tasks": "SELECT COUNT(taskId) AS count FROM eventTask",
        "Total Bookings": "SELECT COUNT(bookingId) AS count FROM booking",
        "Total Payments": "SELECT COUNT(paymentId) AS count FROM payment"
    }

    stats = {title: fetch_data(query)[0]['count'] for title, query in counts.items()}

    tk.Label(main_frame, text="Dashboard", font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=20)

    stats_frame = tk.Frame(main_frame, bg="#f8f9fa")
    stats_frame.pack(pady=20, padx=10, fill="both", expand=True)

    # Container untuk stat cards agar bisa diposisikan di tengah
    cards_container = tk.Frame(stats_frame, bg="#f8f9fa")
    cards_container.pack(expand=True)

    for title, value in stats.items():
        # Tentukan warna berdasarkan title
        if "Clients" in title:
            color = "#007BFF"
        elif "Events" in title:
            color = "#28a745"
        elif "Categories" in title:
            color = "#6f42c1"
        elif "Venues" in title:
            color = "#fd7e14"
        elif "Tasks" in title:
            color = "#17a2b8"
        elif "Bookings" in title:
            color = "#ffc107"
        elif "Payments" in title:
            color = "#dc3545"
        else:
            color = "#343a40"  # Default color

        create_stat_card(cards_container, title, value, color)

# Membuat Statistik Card
def create_stat_card(parent, title, value, color):
    card = tk.Frame(parent, bg=color, width=200, height=100, bd=2, relief="raised")
    card.pack(side="left", padx=20, pady=10, anchor='n')
    tk.Label(card, text=title, bg=color, fg="white", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(card, text=value, bg=color, fg="white", font=("Arial", 18, "bold")).pack(pady=5)

# Table Definitions for CRUD Operations
table_definitions = {
    "Clients": {
        "table": "client",
        "primary_key": "clientId",
        "fields": {
            "clientName": "Name",
            "PhoneNumber": "Phone",
            "email": "Email",
            "address": "Address",
            "dateOfBirth": "Date of Birth",
            "balance": "Balance"
            # 'createdAt' biasanya diatur otomatis, jadi tidak termasuk di form
        },
        "search_fields": ["clientId", "clientName"]  # Menambahkan field pencarian
    },
    "Event Categories": {
        "table": "eventCategory",
        "primary_key": "categoryId",
        "fields": {
            "categoryName": "Category",
            "description": "Description"
        },
        "search_fields": ["categoryId", "categoryName"]
    },
    "Events": {
        "table": "event",
        "primary_key": "eventId",
        "fields": {
            "categoryId": "Category ID",
            "title": "Title",
            "description": "Description",
            "pricePerPax": "Price Per Pax"
        },
        "search_fields": ["eventId", "title"]
    },
    "Venues": {
        "table": "venue",
        "primary_key": "venueId",
        "fields": {
            "venueName": "Name",
            "address": "Address",
            "capacity": "Capacity",
            "pricePerHour": "Price Per Hour"
        },
        "search_fields": ["venueId", "venueName"]
    },
    "Bookings": {
        "table": "booking",
        "primary_key": "bookingId",
        "fields": {
            "clientId": "Client ID",
            "eventId": "Event ID",
            "venueId": "Venue ID",
            "numberOfGuest": "Guests",
            "status": "Status",
            "totalAmount": "Total Amount",
            "bookedAt": "Booked At"
        },
        "search_fields": ["bookingId", "clientId"]  # Tidak ada 'name' field langsung
    },
    "Event Tasks": {
        "table": "eventTask",
        "primary_key": "taskId",
        "fields": {
            "taskName": "Task",
            "taskPrice": "Task Price"
        },
        "search_fields": ["taskId", "taskName"]
    },
    "Schedules": {
        "table": "schedule",
        "primary_key": "id",
        "fields": {
            "bookingId": "Booking ID",
            "startDate": "Start Date",
            "endDate": "End Date",
            "startTime": "Start Time",
            "endTime": "End Time"
        },
        "search_fields": ["id", "bookingId"]
    },
    "Booking History": {
        "table": "bookingHistory",
        "primary_key": "id",
        "fields": {
            "clientId": "Client ID",
            "clientName": "Client Name",
            "eventId": "Event ID",
            "eventTitle": "Event Title",
            "categoryId": "Category ID",
            "categoryName": "Category Name",
            "venueId": "Venue ID",
            "venueName": "Venue Name",
            "venueTotalPrice": "Venue Total Price",
            "scheduleId": "Schedule ID",
            "startDate": "Start Date",
            "endDate": "End Date",
            "numberOfGuest": "Guests",
            "totalPaxAmount": "Total Pax Amount",
            "bookedAt": "Booked At"
        },
        "search_fields": ["id", "clientName"]
    },
    "Booking History Details": {
        "table": "bookingHistoryDetails",
        "primary_key": "id",
        "fields": {
            "historyId": "History ID",
            "taskId": "Task ID",
            "taskName": "Task",
            "taskPrice": "Task Price",
            "totalTaskPrice": "Total Task Price",
            "totalPaidAmount": "Total Paid Amount"
        },
        "search_fields": ["id", "taskName"]
    },
    "Booked Task": {
        "table": "bookedTask",
        "primary_key": "id",
        "fields": {
            "bookingId": "Booking ID",
            "taskId": "Task ID"
        },
        "search_fields": ["id", "taskId"]
    },
    "Payment": {
        "table": "payment",
        "primary_key": "paymentId",
        "fields": {
            "bookingId": "Booking ID",
            "paymentDate": "Payment Date",
            "paymentStatus": "Payment Status",
            "paidAmount": "Paid Amount"
        },
        "search_fields": ["paymentId", "paymentStatus"]
    }
}

# Fungsi Helper untuk Membuat Search Bar
def create_search_bar(parent, view_name, query, tree):
    """
    Menambahkan widget search bar ke dalam frame yang sudah ada.

    Parameters:
    - parent: Frame tempat search bar akan ditempatkan.
    - view_name: Nama tampilan untuk menentukan kolom pencarian.
    - query: Query dasar tanpa filter pencarian.
    - tree: TreeView yang akan difilter.
    """
    search_label = tk.Label(parent, text="Search:", font=("Arial", 12), bg="#f8f9fa")
    search_label.pack(side="left", padx=(0,5))

    search_var = tk.StringVar()
    search_entry = tk.Entry(parent, textvariable=search_var, font=("Arial", 12))
    search_entry.pack(side="left", fill="x", expand=True, padx=(0,5))

    search_button = tk.Button(parent, text="Search", font=("Arial", 12), bg="#007BFF", fg="white",
                              command=lambda: perform_search(view_name, query, tree, search_var))
    search_button.pack(side="left", padx=(0,5))

    reset_button = tk.Button(parent, text="Reset", font=("Arial", 12), bg="#6c757d", fg="white",
                             command=lambda: reset_search(query, tree, search_var))
    reset_button.pack(side="left")

def perform_search(view_name, base_query, tree, search_var):
    """
    Melakukan pencarian berdasarkan ID dan Nama yang dimasukkan.

    Parameters:
    - view_name: Nama tampilan untuk menentukan kolom pencarian.
    - base_query: Query dasar tanpa filter pencarian.
    - tree: TreeView yang akan difilter.
    - search_var: StringVar yang berisi kata kunci pencarian.
    """
    keyword = search_var.get().strip()
    if keyword:
        search_fields = table_definitions[view_name].get('search_fields', [])
        if not search_fields:
            messagebox.showerror("Search Error", f"No search fields defined for {view_name}")
            return

        # Membuat klausa LIKE untuk setiap field dalam search_fields
        like_clauses = " OR ".join([f"{field} LIKE %s" for field in search_fields])
        search_query = f"{base_query} WHERE {like_clauses}"
        params = [f"%{keyword}%" for _ in search_fields]
        data = fetch_data(search_query, params)
        populate_treeview(tree, data)
    else:
        # Jika keyword kosong, tampilkan semua data
        data = fetch_data(base_query)
        populate_treeview(tree, data)

def reset_search(base_query, tree, search_var):
    """
    Mengembalikan tampilan TreeView ke semua data tanpa filter pencarian dan mengosongkan entry pencarian.

    Parameters:
    - base_query: Query dasar tanpa filter pencarian.
    - tree: TreeView yang akan dikembalikan.
    - search_var: StringVar yang berisi kata kunci pencarian.
    """
    search_var.set("")
    data = fetch_data(base_query)
    populate_treeview(tree, data)

# Halaman Tabel Generik dengan Search Bar
def create_table_view(view_name, query, columns, title):
    global current_view
    current_view = view_name  # Set tampilan aktif

    tk.Label(main_frame, text=title, font=("Arial", 20, "bold"), bg="#f8f9fa").pack(pady=10)

    # Frame untuk Search Bar
    search_frame = tk.Frame(main_frame, bg="#f8f9fa")
    search_frame.pack(fill="x", padx=10, pady=5)

    # Frame untuk TreeView
    tree_frame = tk.Frame(main_frame, bg="#f8f9fa")
    tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

    # Membuat TreeView dengan scrollbar horizontal khusus untuk Booking History
    if view_name == "Booking History":
        tree = create_treeview_with_horizontal_scroll(tree_frame, columns)
    else:
        tree = create_treeview(tree_frame, columns)

    # Isi TreeView dengan data
    data = fetch_data(query)
    populate_treeview(tree, data)

    # Membuat Search Bar dengan referensi TreeView
    create_search_bar(search_frame, view_name, query, tree)

# Membuat TreeView dengan Scrollbar Vertikal dan Horizontal
def create_treeview(parent, columns):
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
    style.configure("Treeview", font=("Arial", 10), rowheight=25)

    # Buat Frame untuk TreeView dan Scrollbars menggunakan pack layout
    tree_frame = tk.Frame(parent, bg="#f8f9fa")
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        # Atur lebar kolom yang cukup agar teks terlihat
        tree.column(col, anchor="center", width=150, minwidth=100, stretch=True)

    # Scrollbar Vertikal
    scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    # Scrollbar Horizontal
    scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.pack(side="bottom", fill="x")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    return tree

# Membuat TreeView khusus dengan Scrollbar Horizontal menggunakan grid layout
def create_treeview_with_horizontal_scroll(parent, columns):
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 10, "bold"))  # Mengurangi ukuran font
    style.configure("Treeview", font=("Arial", 9), rowheight=20)  # Mengurangi ukuran font dan tinggi baris

    # Set ukuran frame yang menampung TreeView
    fixed_width = 1000  # Sesuaikan sesuai kebutuhan
    fixed_height = 400  # Sesuaikan sesuai kebutuhan
    parent.config(width=fixed_width, height=fixed_height)
    parent.grid_propagate(False)  # Mencegah frame mengubah ukuran sesuai konten

    # Konfigurasi grid
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    # Membuat TreeView
    tree = ttk.Treeview(parent, columns=columns, show="headings")
    total_col_width = 0
    for col in columns:
        tree.heading(col, text=col)
        # Lebar kolom yang lebih kecil untuk memastikan total lebar > frame width
        tree.column(col, anchor="center", width=80, minwidth=60, stretch=False)
        total_col_width += 80  # Total lebar kolom

    # Debugging: Pastikan total lebar kolom melebihi fixed_width
    print(f"Total kolom width: {total_col_width}, Frame width: {fixed_width}")

    # Scrollbar Vertikal
    scrollbar_y = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky='ns')

    # Scrollbar Horizontal
    scrollbar_x = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=1, column=0, sticky='ew')

    # Tempatkan TreeView
    tree.grid(row=0, column=0, sticky='nsew')

    return tree

# CRUD Operations

def insert_record():
    if not current_view:
        messagebox.showerror("Error", "Please select a table to insert a record.")
        return

    table_info = table_definitions.get(current_view)
    if not table_info:
        messagebox.showerror("Error", f"No table information found for {current_view}")
        return

    def submit_insert():
        values = {field: var.get() or None for field, var in entries.items()}
        required_fields = [field for field in table_info['fields'] if field != "createdAt"]

        # Validasi input
        for field in required_fields:
            if not values[field]:
                messagebox.showerror("Input Error", f"{table_info['fields'][field]} is required.")
                return

        columns = ", ".join(values.keys())
        placeholders = ", ".join(["%s"] * len(values))
        sql = f"INSERT INTO {table_info['table']} ({columns}) VALUES ({placeholders})"

        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute(sql, list(values.values()))
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Record inserted successfully.")
                insert_window.destroy()
                refresh_current_view(current_view)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    insert_window = tk.Toplevel(root)
    insert_window.title(f"Insert into {current_view}")
    insert_window.geometry("400x600")  # Menyesuaikan ukuran window untuk form yang lebih panjang
    insert_window.configure(bg="#f8f9fa")

    entries = {}
    row = 0
    for field, label in table_info['fields'].items():
        tk.Label(insert_window, text=label, bg="#f8f9fa", font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        var = tk.StringVar()
        if field in ["paymentStatus", "status"]:
            # Dropdown untuk ENUM fields
            options = ['Pending', 'Confirmed', 'Declined'] if field == "paymentStatus" else ['Pending', 'Confirmed']
            dropdown = ttk.Combobox(insert_window, textvariable=var, values=options, state='readonly', font=("Arial", 12))
            dropdown.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            dropdown.current(0)
            entries[field] = var
        elif field in ["categoryId", "eventId", "venueId", "clientId", "bookingId", "taskId", "historyId", "scheduleId", "paymentId"]:
            # Entry untuk foreign keys (bisa dikembangkan lebih lanjut dengan dropdown dari tabel terkait)
            entry = tk.Entry(insert_window, textvariable=var, font=("Arial", 12))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[field] = var
        elif field in ["dateOfBirth", "startDate", "endDate", "bookedAt", "paymentDate"]:
            # Entry khusus untuk tanggal
            entry = tk.Entry(insert_window, textvariable=var, font=("Arial", 12))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[field] = var
        elif field in ["paidAmount", "balance", "pricePerPax", "pricePerHour", "taskPrice", "totalAmount", "venueTotalPrice", "totalPaxAmount", "totalTaskPrice", "totalPaidAmount"]:
            # Entry khusus untuk angka desimal
            entry = tk.Entry(insert_window, textvariable=var, font=("Arial", 12))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[field] = var
        else:
            entry = tk.Entry(insert_window, textvariable=var, font=("Arial", 12))
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[field] = var
        row += 1

    submit_btn = tk.Button(insert_window, text="Submit", font=("Arial", 12), bg="#007BFF", fg="white",
                           command=submit_insert)
    submit_btn.grid(row=row, column=0, columnspan=2, pady=20)

def edit_record():
    if not current_view:
        messagebox.showerror("Error", "Please select a table to edit a record.")
        return

    table_info = table_definitions.get(current_view)
    if not table_info:
        messagebox.showerror("Error", f"No table information found for {current_view}")
        return

    # Mendapatkan referensi TreeView yang aktif
    tree = find_active_treeview()
    if not tree:
        messagebox.showerror("Error", "No active table found.")
        return

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a record to edit.")
        return

    item = tree.item(selected_item)
    record = item['values']

    def submit_edit():
        values = {field: var.get() or None for field, var in entries.items()}
        required_fields = [field for field in table_info['fields'] if field != "createdAt"]

        # Validasi input
        for field in required_fields:
            if not values[field]:
                messagebox.showerror("Input Error", f"{table_info['fields'][field]} is required.")
                return

        set_clause = ", ".join([f"{field} = %s" for field in values.keys()])
        sql = f"UPDATE {table_info['table']} SET {set_clause} WHERE {table_info['primary_key']} = %s"

        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute(sql, list(values.values()) + [record[0]])
                connection.commit()
                connection.close()
                messagebox.showinfo("Success", "Record updated successfully.")
                edit_window.destroy()
                refresh_current_view(current_view)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit {current_view}")
    edit_window.geometry("400x600")  # Menyesuaikan ukuran window untuk form yang lebih panjang
    edit_window.configure(bg="#f8f9fa")

    entries = {}
    row = 0
    for i, (field, label) in enumerate(table_info['fields'].items()):
        tk.Label(edit_window, text=label, bg="#f8f9fa", font=("Arial", 12)).grid(row=row, column=0, padx=10, pady=5, sticky="e")
        var = tk.StringVar()
        if field == "createdAt":
            # Tanggal pembuatan biasanya tidak diubah
            var.set(record[i + 1])
            tk.Label(edit_window, text=var.get(), bg="#f8f9fa", font=("Arial", 12)).grid(row=row, column=1, padx=10, pady=5, sticky="w")
            entries[field] = var
        else:
            var.set(record[i + 1])  # +1 untuk melewati primary key
            if field in ["paymentStatus", "status"]:
                # Dropdown untuk ENUM fields
                options = ['Pending', 'Confirmed', 'Declined'] if field == "paymentStatus" else ['Pending', 'Confirmed']
                dropdown = ttk.Combobox(edit_window, textvariable=var, values=options, state='readonly', font=("Arial", 12))
                dropdown.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries[field] = var
            elif field in ["categoryId", "eventId", "venueId", "clientId", "bookingId", "taskId", "historyId", "scheduleId", "paymentId"]:
                # Entry untuk foreign keys
                entry = tk.Entry(edit_window, textvariable=var, font=("Arial", 12))
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries[field] = var
            elif field in ["dateOfBirth", "startDate", "endDate", "bookedAt", "paymentDate"]:
                # Entry khusus untuk tanggal
                entry = tk.Entry(edit_window, textvariable=var, font=("Arial", 12))
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries[field] = var
            elif field in ["paidAmount", "balance", "pricePerPax", "pricePerHour", "taskPrice", "totalAmount", "venueTotalPrice", "totalPaxAmount", "totalTaskPrice", "totalPaidAmount"]:
                # Entry khusus untuk angka desimal
                entry = tk.Entry(edit_window, textvariable=var, font=("Arial", 12))
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries[field] = var
            else:
                entry = tk.Entry(edit_window, textvariable=var, font=("Arial", 12))
                entry.grid(row=row, column=1, padx=10, pady=5, sticky="w")
                entries[field] = var
        row += 1

    submit_btn = tk.Button(edit_window, text="Update", font=("Arial", 12), bg="#007BFF", fg="white",
                           command=submit_edit)
    submit_btn.grid(row=row, column=0, columnspan=2, pady=20)

def delete_record():
    if not current_view:
        messagebox.showerror("Error", "Please select a table to delete a record.")
        return

    table_info = table_definitions.get(current_view)
    if not table_info:
        messagebox.showerror("Error", f"No table information found for {current_view}")
        return

    # Mendapatkan referensi TreeView yang aktif
    tree = find_active_treeview()
    if not tree:
        messagebox.showerror("Error", "No active table found.")
        return

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a record to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected record?")
    if not confirm:
        return

    item = tree.item(selected_item)
    record = item['values']

    sql = f"DELETE FROM {table_info['table']} WHERE {table_info['primary_key']} = %s"

    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute(sql, (record[0],))
            connection.commit()
            connection.close()
            messagebox.showinfo("Success", "Record deleted successfully.")
            refresh_current_view(current_view)
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def find_active_treeview():
    """
    Mencari dan mengembalikan referensi ke TreeView yang aktif di main_frame secara rekursif.
    """
    def recursive_search(widget):
        for child in widget.winfo_children():
            if isinstance(child, ttk.Treeview):
                return child
            result = recursive_search(child)
            if result:
                return result
        return None

    return recursive_search(main_frame)

def refresh_current_view(view_name):
    # Find the navigation button corresponding to view_name and trigger its command
    for text, command in nav_buttons:
        if text == view_name:
            switch_frame(command, text)
            break

# Menambahkan Tombol CRUD di Sidebar
def add_crud_buttons():
    """
    Menambahkan tombol Insert, Edit, Delete ke sidebar di bawah navigasi.
    """
    crud_frame = tk.Frame(side_nav, bg="#343a40")
    crud_frame.pack(pady=20)
    side_nav.crud_frame = crud_frame  # Simpan referensi frame CRUD

    insert_btn = tk.Button(crud_frame, text="Insert", font=("Arial", 12), bg="#28a745", fg="white",
                           command=insert_record)
    insert_btn.pack(fill="x", pady=5)

    edit_btn = tk.Button(crud_frame, text="Update", font=("Arial", 12), bg="#ffc107", fg="white",
                        command=edit_record)
    edit_btn.pack(fill="x", pady=5)

    delete_btn = tk.Button(crud_frame, text="Delete", font=("Arial", 12), bg="#dc3545", fg="white",
                           command=delete_record)
    delete_btn.pack(fill="x", pady=5)

# Menampilkan Tombol CRUD
def show_crud_buttons():
    try:
        side_nav.crud_frame.pack(pady=20)
    except AttributeError:
        pass

# Menyembunyikan Tombol CRUD
def hide_crud_buttons():
    try:
        side_nav.crud_frame.pack_forget()
    except AttributeError:
        pass

# Highlight tombol navigasi yang aktif
def highlight_nav_utbton(active_button_text):
    """
    Mengubah warna tombol aktif di sidebar.

    Parameters:
    - active_button_text: Teks tombol yang sedang aktif.
    """
    for text, button in nav_button_refs.items():
        if text == active_button_text:
            button.config(bg="#81D4FA", fg="white")
        else:
            button.config(bg="#007BFF", fg="white")

# UI Utama
root = tk.Tk()
root.title("Event Management System Dashboard")
root.geometry("1800x900")  # Menyesuaikan ukuran window untuk menampung lebih banyak kartu statistik
root.configure(bg="#f8f9fa")

# Side Navigation
side_nav = tk.Frame(root, bg="#343a40", width=200)
side_nav.pack(side="left", fill="y")

# Menambahkan Judul di Sidebar dengan Format Dua Baris
title_label1 = tk.Label(
    side_nav,
    text="Event Management",
    font=("Arial", 16, "bold"),
    bg="#343a40",
    fg="white"
)
title_label1.pack(pady=(20,0))

title_label2 = tk.Label(
    side_nav,
    text="    System",  # Tambahkan spasi untuk indentasi "System"
    font=("Arial", 16, "bold"),
    bg="#343a40",
    fg="white",
    anchor='w'  # Anchor kiri untuk memastikan indentasi terlihat
)
title_label2.pack()

# Tombol Navigasi
nav_buttons = [
    ("Dashboard", dashboard_view),
    ("Clients", lambda: create_table_view(
        "Clients",
        "SELECT clientId AS ID, clientName AS Name, PhoneNumber AS Phone, email AS Email, address AS Address, dateOfBirth AS 'Date of Birth', balance AS Balance FROM client",
        ("ID", "Name", "Phone", "Email", "Address", "Date of Birth", "Balance"),
        "Clients"
    )),
    ("Event Categories", lambda: create_table_view(
        "Event Categories",
        "SELECT categoryId AS ID, categoryName AS Category, description AS Description FROM eventCategory",
        ("ID", "Category", "Description"),
        "Event Categories"
    )),
    ("Events", lambda: create_table_view(
        "Events",
        "SELECT eventId AS ID, categoryId AS 'Category ID', title AS Title, description AS Description, pricePerPax AS 'Price Per Pax' FROM event",
        ("ID", "Category ID", "Title", "Description", "Price Per Pax"),
        "Events"
    )),
    ("Venues", lambda: create_table_view(
        "Venues",
        "SELECT venueId AS ID, venueName AS Name, address AS Address, capacity AS Capacity, pricePerHour AS 'Price Per Hour' FROM venue",
        ("ID", "Name", "Address", "Capacity", "Price Per Hour"),
        "Venues"
    )),
    ("Bookings", lambda: create_table_view(
        "Bookings",
        """SELECT bookingId AS ID, clientId AS 'Client ID', eventId AS 'Event ID', 
           venueId AS 'Venue ID', numberOfGuest AS 'Guests', status AS Status, 
           totalAmount AS 'Total Amount', bookedAt AS 'Booked At' FROM booking""",
        ("ID", "Client ID", "Event ID", "Venue ID", "Guests", "Status", "Total Amount", "Booked At"),
        "Bookings"
    )),
    ("Event Tasks", lambda: create_table_view(
        "Event Tasks",
        "SELECT taskId AS ID, taskName AS Task, taskPrice AS 'Task Price' FROM eventTask",
        ("ID", "Task", "Task Price"),
        "Event Tasks"
    )),
    ("Schedules", lambda: create_table_view(
        "Schedules",
        "SELECT id AS ID, bookingId AS 'Booking ID', startDate AS 'Start Date', endDate AS 'End Date', startTime AS 'Start Time', endTime AS 'End Time' FROM schedule",
        ("ID", "Booking ID", "Start Date", "End Date", "Start Time", "End Time"),
        "Schedules"
    )),
    ("Booking History", lambda: create_table_view(
        "Booking History",
        """SELECT id AS ID, clientId AS 'Client ID', clientName AS 'Client Name', eventId AS 'Event ID', eventTitle AS 'Event Title', 
           categoryId AS 'Category ID', categoryName AS 'Category Name', venueId AS 'Venue ID', venueName AS 'Venue Name', 
           venueTotalPrice AS 'Venue Total Price', scheduleId AS 'Schedule ID', startDate AS 'Start Date', endDate AS 'End Date', 
           numberOfGuest AS 'Guests', totalPaxAmount AS 'Total Pax Amount', bookedAt AS 'Booked At' FROM bookingHistory""",
        ("ID", "Client ID", "Client Name", "Event ID", "Event Title", 
         "Category ID", "Category Name", "Venue ID", "Venue Name", 
         "Venue Total Price", "Schedule ID", "Start Date", "End Date", 
         "Guests", "Total Pax Amount", "Booked At"),
        "Booking History"
    )),
    ("Booking History Details", lambda: create_table_view(
        "Booking History Details",
        "SELECT id AS ID, historyId AS 'History ID', taskId AS 'Task ID', taskName AS 'Task', totalTaskPrice AS 'Total Task Price', totalPaidAmount AS 'Total Paid Amount' FROM bookingHistoryDetails",
        ("ID", "History ID", "Task ID", "Task", "Total Task Price", "Total Paid Amount"),
        "Booking History Details"
    )),
    ("Booked Task", lambda: create_table_view(
        "Booked Task",
        "SELECT id AS ID, bookingId AS 'Booking ID', taskId AS 'Task ID' FROM bookedTask",
        ("ID", "Booking ID", "Task ID"),
        "Booked Task"
    )),
    ("Payment", lambda: create_table_view(
        "Payment",
        "SELECT paymentId AS ID, bookingId AS 'Booking ID', paymentDate AS 'Payment Date', paymentStatus AS 'Payment Status', paidAmount AS 'Paid Amount' FROM payment",
        ("ID", "Booking ID", "Payment Date", "Payment Status", "Paid Amount"),
        "Payment"
    ))
]

nav_button_refs = {}  # Simpan referensi tombol

for text, command in nav_buttons:
    btn = tk.Button(
        side_nav,
        text=text,
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        command=lambda cmd=command, b=text: switch_frame_with_highlight(cmd, b)
    )
    btn.pack(fill="x", pady=5)
    nav_button_refs[text] = btn  # Simpan referensi tombol

def switch_frame_with_highlight(frame_func, active_button):
    """
    Ganti tampilan dan ubah warna tombol aktif di sidebar.
    """
    # Reset warna semua tombol
    for button in nav_button_refs.values():
        button.config(bg="#007BFF", fg="white")  # Reset warna default

    # Ubah warna tombol aktif
    nav_button_refs[active_button].config(bg="#81D4FA", fg="white")

    # Panggil fungsi tampilan
    switch_frame(frame_func, active_button)

# Menambahkan Tombol CRUD di Sidebar
def add_crud_buttons():
    """
    Menambahkan tombol Insert, Edit, Delete ke sidebar di bawah navigasi.
    """
    crud_frame = tk.Frame(side_nav, bg="#343a40")
    crud_frame.pack(pady=20)
    side_nav.crud_frame = crud_frame  # Simpan referensi frame CRUD

    insert_btn = tk.Button(crud_frame, text="Insert", font=("Arial", 12), bg="#28a745", fg="white",
                           command=insert_record)
    insert_btn.pack(fill="x", pady=5)

    edit_btn = tk.Button(crud_frame, text="Update", font=("Arial", 12), bg="#ffc107", fg="white",
                        command=edit_record)
    edit_btn.pack(fill="x", pady=5)

    delete_btn = tk.Button(crud_frame, text="Delete", font=("Arial", 12), bg="#dc3545", fg="white",
                           command=delete_record)
    delete_btn.pack(fill="x", pady=5)

# Menampilkan Tombol CRUD
def show_crud_buttons():
    try:
        side_nav.crud_frame.pack(pady=20)
    except AttributeError:
        pass

# Menyembunyikan Tombol CRUD
def hide_crud_buttons():
    try:
        side_nav.crud_frame.pack_forget()
    except AttributeError:
        pass

# Highlight tombol navigasi yang aktif
def highlight_nav_button(active_button_text):
    """
    Mengubah warna tombol aktif di sidebar.

    Parameters:
    - active_button_text: Teks tombol yang sedang aktif.
    """
    for text, button in nav_button_refs.items():
        if text == active_button_text:
            button.config(bg="#81D4FA", fg="white")
        else:
            button.config(bg="#007BFF", fg="white")

# Override command of navigation buttons to include highlight
for text, command in nav_buttons:
    btn = nav_button_refs[text]
    btn.config(command=lambda cmd=command, b=text: switch_frame_with_highlight(cmd, b))

# Menambahkan Tombol CRUD di Sidebar
add_crud_buttons()

# Main Content Area
main_frame = tk.Frame(root, bg="#f8f9fa")
main_frame.pack(side="right", expand=True, fill="both")

# Default View
switch_frame(dashboard_view, "Dashboard")

# Jalankan aplikasi
root.mainloop()
