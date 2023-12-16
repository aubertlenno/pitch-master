
from pathlib import Path

from tkinter import *
from tkinter import messagebox
import hashlib
import mysql.connector as mysql
import login
import re


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def on_signup_clicked():
    email = email_register.get()
    password = password_register.get()
    confirm_password = confirmpassword_register.get()

    if not email or not password or not confirm_password:
            messagebox.showwarning("Incomplete Form", "Please fill in all fields.")
            return

    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "The email format is not correct.")
        return
    
    if password != confirm_password:
        messagebox.showerror("Password Error", "Passwords do not match.")
        return

    # Hashing the password
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Connecting to MySQL
    try:
        conn = mysql.connect(
            host="127.0.0.1",  # replace with your host, usually 'localhost'
            user="root",  # replace with your username
            passwd="",  # replace with your password
            database="pitch-master"  # replace with your database name
        )
        cursor = conn.cursor()

        # Inserting data into the table
        query = "INSERT INTO users (email, password) VALUES (%s, %s)"
        cursor.execute(query, (email, hashed_password))

        conn.commit()
        messagebox.showinfo("Account Created", "Your account has been successfully created.")
        window.destroy()
        login.main()
    except mysql.Error as err:
        messagebox.showerror("Database Error", str(err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

window = Tk()

window.geometry("577x633")
window.configure(bg = "#340040")


canvas = Canvas(
    window,
    bg = "#340040",
    height = 633,
    width = 577,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    52.0,
    46.0,
    anchor="nw",
    text="Welcome to Pitch Master",
    fill="#FAFFFD",
    font=("Arial BoldMT", 40 * -1)
)

canvas.create_text(
    52.0,
    101.0,
    anchor="nw",
    text="Register to make a new account",
    fill="#FAFFFD",
    font=("ArialMT", 24 * -1)
)

canvas.create_text(
    52.0,
    523.0,
    anchor="nw",
    text="Already have an account?",
    fill="#FAFFFD",
    font=("ArialMT", 16 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("email_register.png"))
entry_bg_1 = canvas.create_image(
    234.0,
    211.0,
    image=entry_image_1
)
email_register = Entry(
    bd=0,
    bg="#FAFFFD",
    fg="#000716",
    highlightthickness=0
)
email_register.place(
    x=60.0,
    y=188.0,
    width=348.0,
    height=44.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("password_register.png"))
entry_bg_2 = canvas.create_image(
    234.0,
    296.0,
    image=entry_image_2
)
password_register = Entry(
    bd=0,
    bg="#FAFFFD",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
password_register.place(
    x=60.0,
    y=273.0,
    width=348.0,
    height=44.0
)

canvas.create_text(
    52.0,
    158.0,
    anchor="nw",
    text="E-mail",
    fill="#FAFFFD",
    font=("Arial BoldMT", 18 * -1)
)

canvas.create_text(
    52.0,
    243.0,
    anchor="nw",
    text="Password",
    fill="#FAFFFD",
    font=("Arial BoldMT", 18 * -1)
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("confirmpassword_register.png"))
entry_bg_3 = canvas.create_image(
    234.0,
    381.0,
    image=entry_image_3
)
confirmpassword_register = Entry(
    bd=0,
    bg="#FAFFFD",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
confirmpassword_register.place(
    x=60.0,
    y=358.0,
    width=348.0,
    height=44.0
)

canvas.create_text(
    52.0,
    328.0,
    anchor="nw",
    text="Confirm Password",
    fill="#FAFFFD",
    font=("Arial BoldMT", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("signup_register.png"))
signup_register = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=on_signup_clicked,
    relief="flat"
)
signup_register.place(
    x=52.0,
    y=444.0,
    width=158.0,
    height=46.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("signin_register.png"))
signin_register = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [window.destroy(), login.main()],
    relief="flat"
)
signin_register.place(
    x=52.0,
    y=554.0,
    width=117.11288452148438,
    height=34.09615707397461
)
window.resizable(False, False)
window.mainloop()
