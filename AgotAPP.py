from tkinter import simpledialog
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class Database:
    @staticmethod
    def create_connection():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Hernandez14',
                database='RestaurantDB'
            )
            return connection
        except mysql.connector.Error as err:
            messagebox.showerror("Connection Error", f"Error: {err}")
            return None

class Admin:
    def __init__(self, root):
        self.root = root
        self.admin_window = None

    def open_login(self):
        if self.admin_window and self.admin_window.winfo_exists():
            self.admin_window.destroy()

        self.admin_window = Toplevel(self.root)
        self.admin_window.title("Admin Login")
        self.admin_window.geometry("500x400")
        self.admin_window.configure(bg="#ffffff")

        username_label = Label(self.admin_window, text="Admin Username:", bg="#ffffff")
        username_label.pack(pady=(20, 5))
        username_entry = Entry(self.admin_window)
        username_entry.pack(pady=(0, 10))

        password_label = Label(self.admin_window, text="Admin Password:", bg="#ffffff")
        password_label.pack(pady=(10, 5))
        password_entry = Entry(self.admin_window, show="*")
        password_entry.pack(pady=(0, 10))

        button_frame = Frame(self.admin_window, bg="#ffffff")
        button_frame.pack(pady=(20, 10), fill='x')

        login_button = ttk.Button(button_frame, text="Log In", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(side='left', padx=(20, 5), fill='x', expand=True)

        back_button = ttk.Button(button_frame, text="Back", command=self.admin_window.destroy)
        back_button.pack(side='right', padx=(5, 20), fill='x', expand=True)

        center_window(self.admin_window, 500, 400)

    def login(self, username, password):
        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Admin WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                self.admin_window.destroy()
                self.open_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

            cursor.close()
            connection.close()

    def open_dashboard(self):
        self.admin_window = Toplevel(self.root)
        self.admin_window.title("Admin Dashboard")
        self.admin_window.geometry("800x600")
        self.admin_window.configure(bg="#ffffff")

        welcome_label = Label(self.admin_window, text="Welcome to Admin Dashboard", font=("Arial", 22, "bold"), bg="#ffffff", fg="#333333")
        welcome_label.pack(pady=(20, 10))

        button_frame = Frame(self.admin_window, bg="#ffffff")
        button_frame.pack(pady=(10, 10), fill='x')

        view_button = ttk.Button(button_frame, text="View Book Reservations", command=self.view_book_reservations)
        view_button.pack(side='top', pady=(10, 5), padx=20, fill='x', expand=True)

        alter_button = ttk.Button(button_frame, text="Alter Reservations", command=self.alter_reservations)
        alter_button.pack(side='top', pady=(5, 5), padx=20, fill='x', expand=True)

        logout_button = ttk.Button(button_frame, text="Log Out", command=lambda: self.confirm_logout(self.admin_window))
        logout_button.pack(side='top', pady=(5, 20), padx=20, fill='x', expand=True)

        center_window(self.admin_window, 800, 600)

    def confirm_logout(self, window):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            window.destroy()
            self.root.deiconify()

    def view_book_reservations(self):
        reservations_window = Toplevel(self.root)
        reservations_window.title("Pending Reservations")
        reservations_window.geometry("900x600")
        reservations_window.configure(bg="#ffffff")

        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Reservations WHERE status = 'Pending'"
            cursor.execute(query)
            pending_reservations = cursor.fetchall()

            
            if pending_reservations:
                for reservation in pending_reservations:
                    reservation_frame = Frame(reservations_window, bg="#ffffff")
                    reservation_frame.pack(pady=(5, 0), padx=10, fill='x')

                    reservation_label = Label(reservation_frame, text=f"Reservation ID: {reservation[0]}, Client ID: {reservation[1]}, Date: {reservation[2]}, Time: {reservation[3]}, Place: {reservation[4]}, Event Type: {reservation[5]}, Guests: {reservation[6]}, Status: {reservation[7]}", bg="#ffffff")
                    reservation_label.pack(side='left', padx=(0, 10))

                    approve_button = ttk.Button(reservation_frame, text="Approve", command=lambda res_id=reservation[0]: self.approve_reservation(res_id))
                    approve_button.pack(side='left', padx=(0, 5))

                    reject_button = ttk.Button(reservation_frame, text="Reject", command=lambda res_id=reservation[0]: self.reject_reservation(res_id))
                    reject_button.pack(side='left')

                    separator = ttk.Separator(reservations_window, orient='horizontal')
                    separator.pack(fill='x', pady=(5, 0))

            else:
                messagebox.showinfo("No Pending Reservations", "There are no pending reservations.")

            cursor.close()
            connection.close()

    def approve_reservation(self, reservation_id):
        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE Reservations SET status = 'Approved' WHERE reservation_id = %s"
            cursor.execute(query, (reservation_id,))
            connection.commit()
            messagebox.showinfo("Reservation Approved", "The reservation has been approved.")
            cursor.close()
            connection.close()
        else:
            messagebox.showerror("Error", "Could not connect to the database.")

    def reject_reservation(self, reservation_id):
        rejection_reason = simpledialog.askstring("Rejection Reason", "Please provide a reason for rejection:")
        if rejection_reason:
            connection = Database.create_connection()
            if connection:
                cursor = connection.cursor()
                query = "UPDATE Reservations SET status = 'Rejected', rejection_reason = %s WHERE reservation_id = %s"
                cursor.execute(query, (rejection_reason, reservation_id))
                connection.commit()
                messagebox.showinfo("Reservation Rejected", "The reservation has been rejected.")
                cursor.close()
                connection.close()
            else:
                messagebox.showerror("Error", "Could not connect to the database.")

    def alter_reservations(self):
        alter_window = Toplevel(self.root)
        alter_window.title("Alter Reservations")
        alter_window.geometry("600x400")
        alter_window.configure(bg="#ffffff")

        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Reservations WHERE status IN ('Approved', 'Rejected')"
            cursor.execute(query)
            existing_reservations = cursor.fetchall()

            approved_label = Label(alter_window, text="Approved Reservations:", font=("Arial", 14, "bold"), bg="#ffffff")
            approved_label.pack(pady=(10, 5))

            for reservation in existing_reservations:
                if reservation[7] == 'Approved':
                    reservation_frame = Frame(alter_window, bg="#ffffff")
                    reservation_frame.pack(pady=(5, 0), padx=10, fill='x')

                    reservation_label = Label(reservation_frame, text=f"Reservation ID: {reservation[0]}, Client ID: {reservation[1]}, Date: {reservation[2]}, Time: {reservation[3]}, Place: {reservation[4]}, Event Type: {reservation[5]}, Guests: {reservation[6]}, Status: {reservation[7]}", bg="#ffffff")
                    reservation_label.pack(side='left', padx=(0, 10))

                    edit_button = ttk.Button(reservation_frame, text="Edit", command=lambda res_id=reservation[0]: self.edit_reservation(reservation))
                    edit_button.pack(side='left', padx=(0, 5))

                    separator = ttk.Separator(alter_window, orient='horizontal')
                    separator.pack(fill='x', pady=(5, 0))

            rejected_label = Label(alter_window, text="Rejected Reservations:", font=("Arial", 14, "bold"), bg="#ffffff")
            rejected_label.pack(pady=(10, 5))

            for reservation in existing_reservations:
                if reservation[7] == 'Rejected':
                    reservation_frame = Frame(alter_window, bg="#ffffff")
                    reservation_frame.pack(pady=(5, 0), padx=10, fill='x')

                    reservation_label = Label(reservation_frame, text=f"Reservation ID: {reservation[0]}, Client ID: {reservation[1]}, Date: {reservation[2]}, Time: {reservation[3]}, Place: {reservation[4]}, Event Type: {reservation[5]}, Guests: {reservation[6]}, Status: {reservation[7]}, Reason: {reservation[8]}", bg="#ffffff")
                    reservation_label.pack(side='left', padx=(0, 10))

                    edit_button = ttk.Button(reservation_frame, text="Edit", command=lambda res_id=reservation[0]: self.edit_reservation(reservation))
                    edit_button.pack(side='left', padx=(0, 5))

                    separator = ttk.Separator(alter_window, orient='horizontal')
                    separator.pack(fill='x', pady=(5, 0))

            cursor.close()
            connection.close()

    def edit_reservation(self, reservation):
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Reservation")
        edit_window.geometry("400x400")
        edit_window.configure(bg="#ffffff")

        date_label = Label(edit_window, text="Date (YYYY-MM-DD):", bg="#ffffff")
        date_label.pack(pady=(20, 5))
        date_entry = Entry(edit_window)
        date_entry.insert(0, reservation[2])
        date_entry.pack(pady=(0, 10))

        time_label = Label(edit_window, text="Time (HH:MM):", bg="#ffffff")
        time_label.pack(pady=(10, 5))
        time_entry = Entry(edit_window)
        time_entry.insert(0, reservation[3])
        time_entry.pack(pady=(0, 10))

        place_label = Label(edit_window, text="Place:", bg="#ffffff")
        place_label.pack(pady=(10, 5))
        place_entry = Entry(edit_window)
        place_entry.insert(0, reservation[4])
        place_entry.pack(pady=(0, 10))

        event_type_label = Label(edit_window, text="Type of Event:", bg="#ffffff")
        event_type_label.pack(pady=(10, 5))
        event_type_entry = Entry(edit_window)
        event_type_entry.insert(0, reservation[5])
        event_type_entry.pack(pady=(0, 10))

        guest_count_label = Label(edit_window, text="Guest Count:", bg="#ffffff")
        guest_count_label.pack(pady=(10, 5))
        guest_count_entry = Entry(edit_window)
        guest_count_entry.insert(0, reservation[6])
        guest_count_entry.pack(pady=(0, 10))

        submit_button = ttk.Button(edit_window, text="Update Reservation", 
            command=lambda: self.update_reservation(reservation[0], date_entry.get(), time_entry.get(), 
                                                    place_entry.get(), event_type_entry.get(), 
                                                    guest_count_entry.get(), edit_window))
        submit_button.pack(pady=(20, 5), padx=20, fill='x')

    def update_reservation(self, reservation_id, date, time, place, event_type, guest_count, edit_window):
        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "UPDATE Reservations SET date = %s, time = %s, place = %s, event_type = %s, guest_count = %s WHERE reservation_id = %s"
            cursor.execute(query, (date, time, place, event_type, guest_count, reservation_id))
            connection.commit()
            messagebox.showinfo("Reservation Updated", "The reservation has been updated.")
            edit_window.destroy()
            cursor.close()
            connection.close()
        else:
            messagebox.showerror("Error", "Could not connect to the database.")

class Client:
    def __init__(self, root):
        self.root = root
        self.client_window = None

    def open_login(self):
        if self.client_window and self.client_window.winfo_exists():
            self.client_window.destroy()

        self.client_window = Toplevel(self.root)
        self.client_window.title("Client Login")
        self.client_window.geometry("600x400")
        self.client_window.configure(bg="#ffffff")

        username_label = Label(self.client_window, text="Username:", bg="#ffffff")
        username_label.pack(pady=(20, 5))
        username_entry = Entry(self.client_window)
        username_entry.pack(pady=(0, 10))

        password_label = Label(self.client_window, text="Password:", bg="#ffffff")
        password_label.pack(pady=(10, 5))
        password_entry = Entry(self.client_window, show="*")
        password_entry.pack(pady=(0, 10))

        login_button = ttk.Button(self.client_window, text="Log In", command=lambda: self.login(username_entry.get(), password_entry.get()))
        login_button.pack(pady=(10, 5), padx=20, fill='x')

        signup_button = ttk.Button(self.client_window, text="Sign Up", command=self.open_signup_window)
        signup_button.pack(pady=(0, 10), padx=20, fill='x')

        back_button = ttk.Button(self.client_window, text="Back", command=lambda: self.back_to_main(self.client_window))
        back_button.pack(pady=(10, 20), padx=20, fill='x')

        center_window(self.client_window, 500, 300)

    def login(self, username, password):
        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM Client WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                client_id = result[0]
                client_name = result[1]
                messagebox.showinfo("Login Successful", "Welcome, Client!")
                self.client_window.destroy()
                self.open_dashboard(client_name, client_id)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

            cursor.close()
            connection.close()

    def open_dashboard(self, client_name, client_id):
        self.client_window = Toplevel(self.root)
        self.client_window.title("Client Dashboard")
        self.client_window.geometry("800x400")
        self.client_window.configure(bg="#ffffff")

        welcome_label = Label(self.client_window, text=f"Welcome, {client_name}!", font=("Arial", 22, "bold"), bg="#ffffff", fg="#333333")
        welcome_label.pack(pady=(20, 10))

        button_frame = Frame(self.client_window, bg="#ffffff")
        button_frame.pack(pady=(10, 5), fill='x')

        book_button = ttk.Button(button_frame, text="Book a Reservation", command=lambda: self.book_reservation(client_id))
        book_button.pack(side='top', pady=(10, 5), padx=20, fill='x', expand=True)

        view_pending_button = ttk.Button(button_frame, text="View Pending Requests", command=lambda: self.view_pending_requests(client_id))
        view_pending_button.pack(side='top', pady=(5, 5), padx=20, fill='x', expand=True)

        view_existing_button = ttk.Button(button_frame, text="View Existing Reservations", command=lambda: self.view_existing_reservations(client_id))
        view_existing_button.pack(side='top', pady=(5, 5), padx=20, fill='x', expand=True)

        logout_button = ttk.Button(button_frame, text="Log Out", command=lambda: self.confirm_logout(self.client_window))
        logout_button.pack(side='top', pady=(5, 20), padx=20, fill='x', expand=True)

        center_window(self.client_window, 800, 400)

    def confirm_logout(self, window):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            window.destroy()
            self.root.deiconify()

    def book_reservation(self, client_id):
        booking_window = Toplevel(self.root)
        booking_window.title("Book a Reservation")
        booking_window.geometry("600x500")
        booking_window.configure(bg="#ffffff")

        date_label = Label(booking_window, text="Date (YYYY-MM-DD):", bg="#ffffff")
        date_label.pack(pady=(20, 5))
        date_entry = Entry(booking_window)
        date_entry.pack(pady=(0, 10))

        time_label = Label(booking_window, text="Time (HH:MM):", bg="#ffffff")
        time_label.pack(pady=(10, 5))
        time_entry = Entry(booking_window)
        time_entry.pack(pady=(0, 10))

        place_label = Label(booking_window, text="Place:", bg="#ffffff")
        place_label.pack(pady=(10, 5))
        place_entry = Entry(booking_window)
        place_entry.pack(pady=(0, 10))

        event_type_label = Label(booking_window, text="Type of Event:", bg="#ffffff")
        event_type_label.pack(pady=(10, 5))
        event_type_entry = Entry(booking_window)
        event_type_entry.pack(pady=(0, 10))

        guest_count_label = Label(booking_window, text="Guest Count:", bg="#ffffff")
        guest_count_label.pack(pady=(10, 5))
        guest_count_entry = Entry(booking_window)
        guest_count_entry.pack(pady=(0, 10))

        submit_button = ttk.Button(booking_window, text="Submit Reservation", command=lambda: self.submit_reservation(client_id, date_entry.get(), time_entry.get(), place_entry.get(), event_type_entry.get(), guest_count_entry.get(), booking_window))
        submit_button.pack(pady=(20, 5), padx=20, fill='x')

    def submit_reservation(self, client_id, date, time, place, event_type, guest_count, booking_window):
        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO Reservations (client_id, date, time, place, event_type, guest_count, status) VALUES (%s, %s, %s, %s, %s, %s, 'Pending')"
            try:
                cursor.execute(query, (client_id, date, time, place, event_type, guest_count))
                connection.commit()
                messagebox.showinfo("Reservation Successful", "Your reservation has been submitted and is pending approval.")
                booking_window.destroy()
                self.view_pending_requests(client_id)
            except mysql.connector.Error as err:
                messagebox.showerror("Reservation Failed", f"Error: {err}")
            finally:
                cursor.close()
                connection.close()

    def view_pending_requests(self, client_id):
        pending_window = Toplevel(self.root)
        pending_window.title("Pending Requests")
        pending_window.geometry("600x400")
        pending_window.configure(bg="#ffffff")

        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT reservation_id, event_type, place, time, status FROM Reservations WHERE client_id = %s AND status = 'Pending'"
            cursor.execute(query, (client_id,))
            pending_requests = cursor.fetchall()

            if pending_requests:
                for request in pending_requests:
                    request_label = Label(pending_window, text=f"Reservation ID: {request[0]}, Event Type: {request[1]}, Place: {request[2]}, Time: {request[3]}, Status: {request[4]}", bg="#ffffff")
                    request_label.pack(pady=(5, 0))
                    separator = ttk.Separator(pending_window, orient='horizontal')
                    separator.pack(fill='x', pady=(5, 0))
            else:
                messagebox.showinfo("No Pending Requests", "You have no pending reservation requests.")

            cursor.close()
            connection.close()

    def view_existing_reservations(self, client_id):
        existing_window = Toplevel(self.root)
        existing_window.title("Existing Reservations")
        existing_window.geometry("600x400")
        existing_window.configure(bg="#ffffff")

        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT reservation_id, date, time, place, event_type, guest_count, status, rejection_reason FROM Reservations WHERE client_id = %s AND status IN ('Approved', 'Rejected')"
            cursor.execute(query, (client_id,))
            existing_reservations = cursor.fetchall()

            if existing_reservations:
                for reservation in existing_reservations:
                    reservation_label = Label(existing_window, text=f"Reservation ID: {reservation[0]}, Date: {reservation[1]}, Time: {reservation[2]}, Place: {reservation[3]}, Event Type: {reservation[4]}, Guests: {reservation[5]}, Status: {reservation[6]}, Rejection Reason: {reservation[7] if reservation[6] == 'Rejected' else 'N/A'}", bg="#ffffff")
                    reservation_label.pack(pady=(5, 0))
                    separator = ttk.Separator(existing_window, orient='horizontal')
                    separator.pack(fill='x', pady=(5, 0))
            else:
                messagebox.showinfo("No Existing Reservations", "You have no existing reservations.")

            cursor.close()
            connection.close()

    def open_signup_window(self):
        signup_window = Toplevel(self.root)
        signup_window.title("Sign Up")
        signup_window.geometry("500x600")
        signup_window.configure(bg="#ffffff")

        full_name_label = Label(signup_window, text="Full Name:", bg="#ffffff")
        full_name_label.pack(pady=(20, 5))
        full_name_entry = Entry(signup_window)
        full_name_entry.pack(pady=(0, 10))

        address_label = Label(signup_window, text="Address:", bg="#ffffff")
        address_label.pack(pady=(10, 5))
        address_entry = Entry(signup_window)
        address_entry.pack(pady=(0, 10))

        contact_label = Label(signup_window, text="Contact Number:", bg="#ffffff")
        contact_label.pack(pady=(10, 5))
        contact_entry = Entry(signup_window)
        contact_entry.pack(pady=(0, 10))

        email_label = Label(signup_window, text="Email:", bg="#ffffff")
        email_label.pack(pady=(10, 5))
        email_entry = Entry(signup_window)
        email_entry.pack(pady=(0, 10))

        username_label = Label(signup_window, text="Username:", bg="#ffffff")
        username_label.pack(pady=(10, 5))
        username_entry = Entry(signup_window)
        username_entry.pack(pady=(0, 10))

        password_label = Label(signup_window, text="Password:", bg="#ffffff")
        password_label.pack(pady=(10, 5))
        password_entry = Entry(signup_window, show="*")
        password_entry.pack(pady=(0, 10))

        signup_button = ttk.Button(signup_window, text="Sign Up", command=lambda: self.signup(full_name_entry.get(), address_entry.get(), contact_entry.get(), email_entry.get(), username_entry.get(), password_entry.get(), signup_window))
        signup_button.pack(pady=(20, 5), padx=20, fill='x')

        back_button = ttk.Button(signup_window, text="Back", command=signup_window.destroy)
        back_button.pack(pady=(10, 20), padx=20, fill='x')

        center_window(signup_window, 400, 500)

    def signup(self, full_name, address, contact, email, username, password, signup_window):
        connection = Database.create_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO Client (full_name, address, contact_number, email, username, password) VALUES (%s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(query, (full_name, address, contact, email, username, password))
                connection.commit()
                messagebox.showinfo("Sign Up Successful", "You have successfully signed up!")
                signup_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Sign Up Failed", f"Error: {err}")
            finally:
                cursor.close()
                connection.close()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Main application window
root = Tk()
root.title("Restaurant Management System")
root.geometry("600x400")
root.configure(bg="#ffffff")

welcome_label = Label(root, text="Welcome to Restaurant Management System", font=("Arial", 16, "bold"), bg="#ffffff", fg="#333333")
welcome_label.pack(pady=(20, 10))

admin = Admin(root)
client = Client(root)

admin_button = ttk.Button(root, text="Admin Login", command=admin.open_login)
admin_button.pack(pady=(10, 5), padx=20, fill='x')

client_button = ttk.Button(root, text="Client Login", command=client.open_login)
client_button.pack(pady=(10, 5), padx=20, fill='x')

center_window(root, 600, 150)

root.mainloop()