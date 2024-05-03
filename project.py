import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from PIL import ImageTk


root = tk.Tk()
root.geometry("1366x766")

image = ImageTk.PhotoImage(file="bus.jpeg")
background_label = tk.Label(root, image=image)
background_label.place(x=0, y=0, relheight=1, relwidth=1)

test = tk.Label(root, text="School Bus Reservation", font=("Times New Roman", 25, "bold"), bg="white", foreground="red")
test.pack(padx=10, pady=10)

# Create the login function

import mysql.connector

# Establish a connection to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="clement"
)


# login form
def login():
    # Get the entered username and password
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username and password match for each dashboard
    if user_type_var.get() == "Lecturer":
        # Check if the username and password match in the user_registration table
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM lecturer_registration WHERE username=%s AND password=%s", (username, password))
        result = mycursor.fetchone()
        if result:
            # Hide the login frame
            login_frame.pack_forget()
            # Open the user dashboard
            lecturer_dashboard()
        else:
            # Show an error message
            messagebox.showerror("login", "Invalid username or password !")

    elif user_type_var.get() == "Admin" and username == "2" and password == "2":

        admin_dashboard()
def admin_dashboard():


    admin_frame = tk.Frame(root)
    admin_frame.pack(side="top", fill="both", expand=True)

    # Create a label for the page title
    title_label = tk.Label(admin_frame, text="Admin Dashboard", font=("Arial", 24, "bold"), pady=10)
    title_label.pack()

    # Create a frame for the bookings table
    bookings_frame = tk.Frame(admin_frame, bd=1, relief="solid")
    bookings_frame.pack(padx=20, pady=10)

    # Create a label for the bookings table
    bookings_label = tk.Label(bookings_frame, text="Trips Requests", font=("Arial", 16, "bold"), padx=10, pady=10)
    bookings_label.pack(side="top", fill="x")

    # Create a scrollbar for the bookings table
    scrollbar = tk.Scrollbar(bookings_frame)
    scrollbar.pack(side="right", fill="y")

    # Create a table for the bookings
    trips_table = ttk.Treeview(bookings_frame, yscrollcommand=scrollbar.set)
    trips_table["columns"] = ("trip_type", "name", "email", "phone", "num_people", "date", "time")
    trips_table.column("#0", width=0, stretch="no")
    trips_table.column("trip_type", anchor="w", width=150)
    trips_table.column("name", anchor="w", width=150)
    trips_table.column("email", anchor="w", width=200)
    trips_table.column("phone", anchor="w", width=100)
    trips_table.column("num_people", anchor="center", width=80)
    trips_table.column("date", anchor="center", width=100)
    trips_table.column("time", anchor="center", width=80)


    trips_table.heading("#0", text="", anchor="w")
    trips_table.heading("trip_type", text="Trip_type", anchor="w")
    trips_table.heading("name", text="Name Of Lecturer ", anchor="w")
    trips_table.heading("email", text="Email", anchor="w")
    trips_table.heading("phone", text="Phone", anchor="w")
    trips_table.heading("num_people", text="Number Of people", anchor="center")
    trips_table.heading("date", text="Date Of Trip", anchor="center")
    trips_table.heading("time", text="Time", anchor="center")


    trips_table.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=trips_table.yview)

    # Retrieve the bookings from the database
    def retrieve_bookings():
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clement"
        )
        # Clear the current contents of the bookings table
        for row in trips_table.get_children():
            trips_table.delete(row)

        # Retrieve the bookings from the database
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM trips")

        # Insert the bookings into the table
        for row in mycursor.fetchall():
            trips_table.insert("", "end", text="", values=row)

    retrieve_bookings()

    import smtplib
    from email.mime.text import MIMEText


    # Create the email entry fields
    email_frame = tk.Frame(admin_frame)
    email_frame.pack()

    send_approval_email_label = tk.Label(email_frame, text="Send email for approval", font=("Arial", 16, "bold"),
                                         fg="blue")
    send_approval_email_label.pack()

    email_label = tk.Label(email_frame, text="Enter Email To Approve:", font=("elephant", 12, "bold"), fg="green")
    email_label.pack(side="left", padx=5)

    email_entry = tk.Entry(email_frame, width=50)
    email_entry.pack(side="left", padx=5)

    # Create the email body entry field
    body_label = tk.Label(email_frame, text="Enter Email Body:", font=("elephant", 12, "bold"), fg="green")
    body_label.pack(side="left", padx=5, pady=5)

    body_entry = tk.Text(email_frame, width=50, height=10)
    body_entry.pack(padx=5, pady=5)

    # Create the send email button
    def send_approval_email():
        email = email_entry.get()
        body = body_entry.get("1.0", tk.END)

        if email == "" or body == "":
            messagebox.showerror("email", "please fill in all fields!")
            return

        # Set up the message content
        message = MIMEText(body)
        message["Subject"] = "Booking Approval"
        message["From"] = "clementngabirano99@gmail.com"
        message["To"] = email

        # Connect to the SMTP server and send the message
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("clementngabirano99@gmail.com", "tislcfswpgfykblj")
            server.send_message(message)

        # Show a message indicating that the email has been sent successfully
        messagebox.showinfo("Success", "Email sent successfully")

    send_button = tk.Button(email_frame, text="Send Email", command=send_approval_email, font=("elephant", 14, "bold"), fg="blue")
    send_button.pack(pady=5)

    def logout():
        navbar_frame = tk.Frame(root)
        navbar_frame.pack(side="top", fill="x")
        # Hide content frame
        admin_frame.pack_forget()
        navbar_frame.destroy()
        # Destroy navigation bar
        # Show login interface
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Button to logout
    admin_logout_button = tk.Button(admin_frame, text="Logout", fg="red", font=("Arial", 14), command=logout)
    admin_logout_button.place(relx=1.0, x=-10, y=10, anchor="ne")




def lecturer_dashboard():
    # Create the content frame for displaying page content
    lecturer_frame = tk.Frame(root)
    lecturer_frame.pack(side="top", fill="both", expand=True)

    # Create a left frame for navigation buttons
    left_frame = tk.Frame(lecturer_frame, bg="white", width=200, height=root.winfo_height())
    left_frame.pack(side="left", fill="y")

    # Create a right frame for form input
    right_frame = tk.Frame(lecturer_frame, bg="lightgray", width=root.winfo_width()-200, height=root.winfo_height())
    right_frame.pack(side="right", fill="both", expand=True)

    title = tk.Label(left_frame, text="Welcome To Lecturer Dashboard", font=("Arial", 20, "bold"), fg="orange")
    title.pack(pady=20, padx=10)

    # creating navigation bars
    academic_trip_button = tk.Button(left_frame, text="Academic Trip", font=("Arial", 14), command=lambda: open_form(right_frame, "Academic Trip"))
    academic_trip_button.pack(pady=10, padx=10, fill="x")

    transportation_button = tk.Button(left_frame, text="Transportation", font=("Arial", 14), command=lambda: open_form(right_frame, "Transportation"))
    transportation_button.pack(pady=10, padx=10, fill="x")

    clinical_trip_button = tk.Button(left_frame, text="Clinical Trip", font=("Arial", 14), command=lambda: open_form(right_frame, "Clinical Trip"))
    clinical_trip_button.pack(pady=10, padx=10, fill="x")

    def logout():
        navbar_frame = tk.Frame(root)
        navbar_frame.pack(side="top", fill="x")
        # Hide content frame
        lecturer_frame.pack_forget()
        navbar_frame.destroy()
        # Destroy navigation bar
        # Show login interface
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Button to logout
    admin_logout_button = tk.Button(lecturer_frame, text="Logout", fg="red", font=("Arial", 14), command=logout)
    admin_logout_button.place(relx=1.0, x=-10, y=10, anchor="ne")



import mysql.connector

# Create a connection to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="clement"
)

def open_form(frame, form_title):
    # Remove previous content in the frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a form for the selected trip
    form_title_label = tk.Label(frame, text=form_title + " Form", font=("elephant", 16, "bold"), fg="blue")
    form_title_label.grid(row=0, column=0, columnspan=2, pady=20)

    # Lecture name field
    name_label = tk.Label(frame, text="Lecture Name:")
    name_label.grid(row=1, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=1, column=1, padx=5, pady=5)

    # Email field
    email_label = tk.Label(frame, text="Email:")
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(frame)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    # Phone number field
    phone_label = tk.Label(frame, text="Phone Number:")
    phone_label.grid(row=3, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(frame)
    phone_entry.grid(row=3, column=1, padx=5, pady=5)

    # Number of students/lecturers going for the trip field
    num_people_label = tk.Label(frame, text="Number of People Going:")
    num_people_label.grid(row=4, column=0, padx=5, pady=5)
    num_people_entry = tk.Entry(frame)
    num_people_entry.grid(row=4, column=1, padx=5, pady=5)

    # Date for the trip field
    date_label = tk.Label(frame, text="Date for the Trip:")
    date_label.grid(row=5, column=0, padx=5, pady=5)
    date_entry = tk.Entry(frame)
    date_entry.grid(row=5, column=1, padx=5, pady=5)

    # Time for the trip field
    time_label = tk.Label(frame, text="Time for the Trip:")
    time_label.grid(row=6, column=0, padx=5, pady=5)
    time_entry = tk.Entry(frame)
    time_entry.grid(row=6, column=1, padx=5, pady=5)

    # Submit button
    submit_button = tk.Button(frame, text="Submit",
                              command=lambda: submit_form(form_title, name_entry.get(), email_entry.get(), phone_entry.get(),
                                                          num_people_entry.get(), date_entry.get(), time_entry.get()))
    submit_button.grid(row=7, column=0, columnspan=2, pady=20)


def submit_form(trip_type, name, email, phone, num_people, date, time):
    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Define the SQL query to insert the form data into the database
    sql = "INSERT INTO trips (trip_type, name, email, phone, num_people, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (trip_type, name, email, phone, num_people, date, time)
    # Execute the query and commit the changes to the database
    cursor.execute(sql, values)
    db.commit()

    # Print a message to confirm that the data was successfully submitted
    messagebox.showinfo("trip", "Submitted To Admin for approval\n successfully!")




# login form
login_frame = tk.Frame(root, bg="white", pady=100, padx=70)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

title_login = tk.Label(login_frame, text="login form", font=("elephant", 18, "bold"), fg="blue")
title_login.pack()

# options to login as either as Lecturer or Admin

user_type_label = tk.Label(login_frame, text="Select User Type:")
user_type_label.pack(pady=5)
user_type_options = ["Lecturer", "Admin"]
user_type_var = tk.StringVar(value=user_type_options[0])
user_type_dropdown_menu = ttk.Combobox(login_frame, textvariable=user_type_var, values=user_type_options)
user_type_dropdown_menu.pack()

username_lable = tk.Label(login_frame, text="Username")
username_lable.pack()
username_entry = tk.Entry(login_frame)
username_entry.pack(pady=10)

password_lable = tk.Label(login_frame, text="Password")
password_lable.pack()
password_entry = tk.Entry(login_frame)
password_entry.pack(pady=10)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.pack(pady=10)

# don't have the account
register_lable = tk.Label(login_frame, text="Don't have an account", fg="blue")
register_lable.pack()


# for registration
def open_registration_window():
    # create registration window
    registration = tk.Toplevel()
    registration.title("Registration")
    registration.geometry("400x500")
    registration.configure(bg="white")

    # create labels and entry widgets
    username_label = tk.Label(registration, text="Username:", font=("Arial", 12), bg="white")
    username_label.pack(pady=10)

    username_entry = tk.Entry(registration, font=("Arial", 12))
    username_entry.pack(pady=10)

    password_label = tk.Label(registration, text="Password:", font=("Arial", 12), bg="white")
    password_label.pack(pady=10)

    password_entry = tk.Entry(registration, show="*", font=("Arial", 12))
    password_entry.pack(pady=10)

    cpassword_label = tk.Label(registration, text="Confirm Password:", font=("Arial", 12), bg="white")
    cpassword_label.pack(pady=10)

    cpassword_entry = tk.Entry(registration, show="*", font=("Arial", 12))
    cpassword_entry.pack(pady=10)

    def register_lecturer():
        # Get the values from the input fields
        username = username_entry.get()
        password = password_entry.get()
        cpassword = cpassword_entry.get()
        # Connect to the database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clement"
        )

        # Check if the passwords match
        if password != cpassword:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Insert the data into the database
        cursor = mydb.cursor()
        query = "INSERT INTO lecturer_registration (username, password) VALUES (%s, %s)"
        values = (username, password)
        cursor.execute(query, values)
        mydb.commit()
        cursor.close()

        # Show success message
        messagebox.showinfo("Success", "User registration successful!")

    # Submit buttons
    submit_user_button = tk.Button(registration, text="Register as User", command=register_lecturer, font=("Arial", 12),
                                   bg="#4CAF50", fg="white", padx=10)
    submit_user_button.pack(pady=10)

    register_button.pack(pady=10)


register_button = tk.Button(login_frame, text="Register", bg="green", command=open_registration_window)
register_button.pack(pady=8)

root.mainloop()
