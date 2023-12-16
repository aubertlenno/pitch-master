
from pathlib import Path

from tkinter import *
import hashlib
import mysql.connector as mysql
from tkinter import messagebox
import register
import re

from Dash import Dashboard2


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def on_signin_clicked():
    email = email_login.get()
    password = password_login.get()

    if not is_valid_email(email):
        messagebox.showerror("Login Error", "Invalid email format")
        return
    
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Connecting to MySQL
    try:
        conn = mysql.connect(
            host="127.0.0.1",  # replace with your host
            user="root",  # replace with your username
            passwd="",  # replace with your password
            database="pitch-master"  # replace with your database name
        )
        cursor = conn.cursor()

        # Fetch user data from the database
        query = "SELECT password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror("Login Error", "Email not registered")
        else:
            stored_password = result[0]
            # Compare entered password with the hashed password
            if stored_password == hashed_password:
                window.destroy()
                dashboard_root = Tk()
                app = Dashboard2(dashboard_root)  # Instantiate the dashboard
                dashboard_root.mainloop()  # Run the dashboard app
            else:
                messagebox.showerror("Login Error", "Incorrect password")

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
    68.0,
    anchor="nw",
    text="Welcome to Pitch Master",
    fill="#FAFFFD",
    font=("Arial BoldMT", 40 * -1)
)

canvas.create_text(
    52.0,
    123.0,
    anchor="nw",
    text="Please Login to Continue",
    fill="#FAFFFD",
    font=("ArialMT", 24 * -1)
)

canvas.create_text(
    52.0,
    500.0,
    anchor="nw",
    text="Don’t have an account?",
    fill="#FAFFFD",
    font=("ArialMT", 16 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("email_login.png"))
entry_bg_1 = canvas.create_image(
    234.0,
    233.0,
    image=entry_image_1
)
email_login = Entry(
    bd=0,
    bg="#FAFFFD",
    fg="#000716",
    highlightthickness=0
)
email_login.place(
    x=60.0,
    y=210.0,
    width=348.0,
    height=44.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("password_login.png"))
entry_bg_2 = canvas.create_image(
    234.0,
    347.0,
    image=entry_image_2
)
password_login = Entry(
    bd=0,
    bg="#FAFFFD",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
password_login.place(
    x=60.0,
    y=324.0,
    width=348.0,
    height=44.0
)

canvas.create_text(
    52.0,
    180.0,
    anchor="nw",
    text="E-mail",
    fill="#FAFFFD",
    font=("Arial BoldMT", 18 * -1)
)

canvas.create_text(
    52.0,
    294.0,
    anchor="nw",
    text="Password",
    fill="#FAFFFD",
    font=("Arial BoldMT", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("signin_login.png"))
signin_login = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=on_signin_clicked,
    relief="flat"
)
signin_login.place(
    x=52.0,
    y=421.0,
    width=158.0,
    height=46.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("register_login.png"))
register_login = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: [window.destroy(), register.main()],
    relief="flat"
)
register_login.place(
    x=52.0,
    y=531.0,
    width=117.11288452148438,
    height=34.09615707397461
)
window.resizable(False, False)
window.mainloop()
