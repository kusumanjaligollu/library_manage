import tkinter as tk
from tkinter import messagebox
import ctypes
import os

# ------------------ LOAD C LIBRARY ------------------
lib_path = os.path.abspath("./booking.dll")
lib = ctypes.CDLL(lib_path)

# Updated function with auto ID and phone number
lib.bookTicketAuto.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.bookTicketAuto.restype = ctypes.c_int

lib.cancelTicket.argtypes = [ctypes.c_int]
lib.cancelTicket.restype = ctypes.c_int

lib.viewConfirmedStr.restype = ctypes.c_char_p
lib.viewWaitingStr.restype = ctypes.c_char_p

# ------------------ MAIN GUI ------------------
root = tk.Tk()
root.title("🎟 Online Ticket Booking System")
root.geometry("720x520")
root.config(bg="#f0f4f7")
current_frame = None

def switch_frame(new_frame_func):
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = new_frame_func()
    current_frame.pack(fill="both", expand=True, pady=10)

# ------------------ HOME PAGE ------------------
def home_page():
    frame = tk.Frame(root, bg="#f0f4f7")
    tk.Label(frame, text="🎟 Ticket Booking System", font=("Arial Rounded MT Bold", 18), bg="#f0f4f7").pack(pady=30)

    tk.Button(frame, text="➕ Book New Ticket", width=25, height=2, bg="#4CAF50", fg="white",
              font=("Arial", 11), command=lambda: switch_frame(book_page)).pack(pady=10)
    tk.Button(frame, text="❌ Cancel Ticket", width=25, height=2, bg="#f44336", fg="white",
              font=("Arial", 11), command=lambda: switch_frame(cancel_page)).pack(pady=10)
    tk.Button(frame, text="📋 View Passenger Lists", width=25, height=2, bg="#2196F3", fg="white",
              font=("Arial", 11), command=lambda: switch_frame(view_page)).pack(pady=10)

    tk.Label(frame, text="Developed in C (Backend) + Python (Frontend)",
             font=("Arial", 9, "italic"), bg="#f0f4f7", fg="gray").pack(side="bottom", pady=20)
    return frame

# ------------------ BOOK PAGE ------------------
def book_page():
    frame = tk.Frame(root, bg="#f0f4f7")
    tk.Label(frame, text="Book New Ticket", font=("Arial Rounded MT Bold", 16), bg="#f0f4f7").pack(pady=20)

    tk.Label(frame, text="Passenger Name:", bg="#f0f4f7").pack()
    name_entry = tk.Entry(frame, width=25)
    name_entry.pack(pady=5)

    tk.Label(frame, text="Phone Number:", bg="#f0f4f7").pack()
    phone_entry = tk.Entry(frame, width=25)
    phone_entry.pack(pady=5)

    def book_ticket():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        if not name or not phone:
            messagebox.showwarning("Input Error", "Please enter both name and phone number!")
            return
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showwarning("Invalid Phone", "Enter a valid 10-digit phone number!")
            return

        res = lib.bookTicketAuto(name.encode('utf-8'), phone.encode('utf-8'))
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)

        if res > 0:
            msg = f"✅ Ticket Confirmed!\n🎟 Your Ticket ID: {res}"
        elif res < 0:
            msg = f"⏳ Added to Waiting List!\n🎟 Your Waiting ID: {-res}"
        else:
            msg = "❌ Booking Full. Try again later!"

        switch_frame(lambda: view_page(extra_book_button=True, message=msg))

    tk.Button(frame, text="Book Ticket", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"),
              command=book_ticket).pack(pady=10)
    tk.Button(frame, text="⬅ Back to Menu", bg="#ccc", font=("Arial", 10),
              command=lambda: switch_frame(home_page)).pack(pady=5)

    return frame

# ------------------ CANCEL PAGE ------------------
def cancel_page():
    frame = tk.Frame(root, bg="#f0f4f7")
    tk.Label(frame, text="Cancel Ticket", font=("Arial Rounded MT Bold", 16), bg="#f0f4f7").pack(pady=20)
    tk.Label(frame, text="Enter Ticket ID to Cancel:", bg="#f0f4f7").pack()
    id_entry = tk.Entry(frame, width=25)
    id_entry.pack(pady=5)

    def cancel_ticket():
        try:
            pid = int(id_entry.get())
            lib.cancelTicket.restype = ctypes.c_char_p  # make sure at top of file
            result = lib.cancelTicket(pid).decode('utf-8')
            if result == "NOT_FOUND":
                messagebox.showwarning("Not Found", "No booking found with that Ticket ID.")
            else:
                id_str, name = result.split(" ", 1)
                msg = f"✅ Ticket Cancelled Successfully!\n🎟 Passenger: {name} (ID: {id_str})"
                switch_frame(lambda: view_page(extra_cancel_button=True, message=msg))

        except ValueError:
            messagebox.showwarning("Input Error", "Enter a valid numeric Ticket ID!")

    tk.Button(frame, text="Cancel Ticket", bg="#f44336", fg="white", font=("Arial", 11, "bold"),
              command=cancel_ticket).pack(pady=10)
    tk.Button(frame, text="⬅ Back to Menu", bg="#ccc", font=("Arial", 10),
              command=lambda: switch_frame(home_page)).pack(pady=5)
    return frame

# ------------------ VIEW PAGE ------------------
def view_page(extra_book_button=False, extra_cancel_button=False, message=None):
    frame = tk.Frame(root, bg="#f0f4f7")
    tk.Label(frame, text="Passenger Lists", font=("Arial Rounded MT Bold", 16), bg="#f0f4f7").pack(pady=10)

    if message:
        tk.Label(frame, text=message, font=("Arial", 12, "bold"), bg="#f0f4f7", fg="green").pack(pady=5)

    container = tk.Frame(frame, bg="#f0f4f7")
    container.pack()

    # Confirmed list
    conf_frame = tk.Frame(container, bg="#f0f4f7")
    conf_frame.pack(side="left", padx=20)
    tk.Label(conf_frame, text="✅ Confirmed", font=("Arial", 12, "bold"), bg="#f0f4f7").pack()
    conf_text = tk.Text(conf_frame, width=40, height=18, font=("Consolas", 10))
    conf_text.pack()

    # Waiting list
    wait_frame = tk.Frame(container, bg="#f0f4f7")
    wait_frame.pack(side="right", padx=20)
    tk.Label(wait_frame, text="⏳ Waiting", font=("Arial", 12, "bold"), bg="#f0f4f7").pack()
    wait_text = tk.Text(wait_frame, width=40, height=18, font=("Consolas", 10))
    wait_text.pack()

    def refresh_lists():
        conf_text.delete(1.0, tk.END)
        wait_text.delete(1.0, tk.END)
        conf = lib.viewConfirmedStr().decode('utf-8')
        wait = lib.viewWaitingStr().decode('utf-8')
        conf_text.insert(tk.END, conf)
        wait_text.insert(tk.END, wait)

    refresh_lists()

    btn_frame = tk.Frame(frame, bg="#f0f4f7")
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="🔄 Refresh", bg="#2196F3", fg="white", font=("Arial", 10),
              command=refresh_lists).pack(side="left", padx=5)

    if extra_book_button:
        tk.Button(btn_frame, text="➕ Book Another Ticket", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                  command=lambda: switch_frame(book_page)).pack(side="left", padx=5)
    if extra_cancel_button:
        tk.Button(btn_frame, text="❌ Cancel Another Ticket", bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                command=lambda: switch_frame(cancel_page)).pack(side="left", padx=5)

    tk.Button(btn_frame, text="⬅ Back to Menu", bg="#ccc", font=("Arial", 10),
              command=lambda: switch_frame(home_page)).pack(side="left", padx=5)

    return frame

# ------------------ START ------------------
switch_frame(home_page)
root.mainloop()