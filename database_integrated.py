import tkinter as tk
from tkinter import ttk
import mysql.connector

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this if you have a different username
    password="root",  # Replace with your MySQL password
    database="moviebooking"
)
cursor = conn.cursor()

def select_seat(seat_id):
    if seat_id not in selected_seats:
        if len(selected_seats) < num_tickets:
            selected_seats.append(seat_id)
            seat_buttons[seat_id].config(bg="green")

def confirm_selection():
    root.destroy()

def create_seat_layout():
    global seat_buttons
    seat_buttons = {}
    frame = tk.Frame(root)
    frame.pack()
    for row in range(5):
        for col in range(8):
            seat_id = f"{chr(65+row)}{col+1}"
            btn = tk.Button(frame, text=seat_id, width=5, command=lambda s=seat_id: select_seat(s))
            btn.grid(row=row, column=col, padx=5, pady=5)
            seat_buttons[seat_id] = btn
    tk.Button(root, text="Confirm Selection", command=confirm_selection).pack(pady=10)

def start_booking():
    global num_tickets, selected_seats, root
    selected_seats = []
    num_tickets = int(ticket_entry.get())
    root = tk.Tk()
    root.title("Select Your Seats")
    create_seat_layout()
    root.mainloop()
    display_summary()

def display_summary():
    movie_name = movie_var.get()
    price = num_tickets * 150
    summary_label.config(text=f"Movie: {movie_name}\nSeats: {', '.join(selected_seats)}\nTotal Price: ₹{price}")

def confirm_booking():
    movie_name = movie_var.get()
    seats = ", ".join(selected_seats)
    total_price = num_tickets * 150

    # Insert booking into the database
    query = "INSERT INTO data (movie_name, seats, total_price) VALUES (%s, %s, %s)"
    cursor.execute(query, (movie_name, seats, total_price))
    conn.commit()

    print("Booking successful! Data saved in the database.")
    print(f"Movie: {movie_name}")
    print(f"Seats: {seats}")
    print(f"Total Price: ₹{total_price}")
    root_window.quit()

root_window = tk.Tk()
root_window.title("Movie Ticket Booking")

movies = ["Inception", "Interstellar", "Avatar", "Avengers"]
tk.Label(root_window, text="Select a movie:").pack()
movie_var = tk.StringVar()
movie_dropdown = ttk.Combobox(root_window, textvariable=movie_var, values=movies, state="readonly")
movie_dropdown.pack()
movie_dropdown.set(movies[0])

tk.Label(root_window, text="Enter number of tickets:").pack()
ticket_entry = tk.Entry(root_window)
ticket_entry.pack()

tk.Button(root_window, text="Proceed to Seat Selection", command=start_booking).pack(pady=10)

summary_label = tk.Label(root_window, text="")
summary_label.pack()

tk.Button(root_window, text="Confirm Booking", command=confirm_booking).pack(pady=10)

root_window.mainloop()

# Close the database connection when done
cursor.close()
conn.close()
