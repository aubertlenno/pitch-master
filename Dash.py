from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from datetime import *
import time
from database import get_db_connection
from tkinter import ttk

mydb = get_db_connection()
mycursor = mydb.cursor()

class Dashboard2:
    def __init__(self, window):
        self.window = window
        self.window.title("System Management Dashboard")
        self.window.geometry("1366x744")
        self.window.resizable(False, False)
        self.window.config(background='#e90052')
        
        self.create_header()
        self.create_sidebar()
        self.create_date_time_display()

        self.dashboard_text.config(command=self.show_teams_page)
        self.manage_text.config(command=self.show_players_page)
        self.settings_text.config(command=self.show_matches_page)
        self.Exit_text.config(command=self.show_transfers_page)
        self.injuries_text.config(command=self.show_injuries_page)
        self.show_teams_page()


    def create_header(self):
        self.header = Frame(self.window, bg='#38003c')  
        self.header.place(x=300, y=0, width=1070, height=60)

    def create_sidebar(self):
        self.sidebar = Frame(self.window, bg='#00ff85')
        self.sidebar.place(x=0, y=0, width=300, height=750)

        # Complete sidebar setup
        self.logoImage = ImageTk.PhotoImage(file='images/Logos.png')
        self.logo = Label(self.sidebar, image=self.logoImage, bg='#00ff85')
        self.logo.place(x=-120, y=-140)

        self.brandName = Label(self.sidebar, text='Pitch Master', bg='#00ff85', font=("", 15, "bold"))
        self.brandName.place(x=80, y=200)

        self.dashboardImage = ImageTk.PhotoImage(file='images/dashboard-icon.png')
        self.dashboard = Label(self.sidebar, image=self.dashboardImage, bg='#00ff85')
        self.dashboard.place(x=35, y=289)

        self.dashboard_text = Button(self.sidebar, text="Teams", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                     cursor='hand2', activebackground='#00ff85')
        self.dashboard_text.place(x=80, y=287)

        self.manageImage = ImageTk.PhotoImage(file='images/manage-icon.png')
        self.manage = Label(self.sidebar, image=self.manageImage, bg='#00ff85')
        self.manage.place(x=35, y=340)

        self.manage_text = Button(self.sidebar, text="Players", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                  cursor='hand2', activebackground='#00ff85')
        self.manage_text.place(x=80, y=345)

        self.settingsImage = ImageTk.PhotoImage(file='images/settings-icon.png')
        self.settings = Label(self.sidebar, image=self.settingsImage, bg='#00ff85')
        self.settings.place(x=35, y=402)

        self.settings_text = Button(self.sidebar, text="Matches", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#00ff85')
        self.settings_text.place(x=80, y=402)

        self.ExitImage = ImageTk.PhotoImage(file='images/exit-icon.png')
        self.Exit = Label(self.sidebar, image=self.ExitImage, bg='#00ff85')
        self.Exit.place(x=25, y=452)

        self.Exit_text = Button(self.sidebar, text="Transfers", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#00ff85')
        self.Exit_text.place(x=85, y=462)

        self.injuriesImage = ImageTk.PhotoImage(file='images/settings-icon.png')
        self.injuries = Label(self.sidebar, image=self.injuriesImage, bg='#00ff85')
        self.injuries.place(x=35, y=510)

        self.injuries_text = Button(self.sidebar, text="Injuries", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#00ff85')
        self.injuries_text.place(x=80, y=515)

    def create_date_time_display(self):
        self.clock_image = ImageTk.PhotoImage(file="images/time.png")
        self.date_time_image = Label(self.sidebar, image=self.clock_image, bg="#00ff85")
        self.date_time_image.place(x=88, y=20)
    
        self.date_time = Label(self.window)
        self.date_time.place(x=115, y=15)
        self.show_time()

    def show_time(self):
        self.time = time.strftime("%H:%M:%S")
        self.date = time.strftime('%Y/%m/%d')
        set_text = f"  {self.time} \n {self.date}"
        self.date_time.configure(text=set_text, font=("", 13, "bold"), bd=0, bg="#00ff85", fg="black")
        self.date_time.after(100, self.show_time)

    def clear_window(self):
        for widget in self.window.winfo_children():
            if widget not in [self.header, self.sidebar, self.date_time]:
                widget.destroy()

    def show_teams_page(self):
        self.clear_window()

        # Heading
        self.heading = Label(self.window, text='Teams', font=("", 15, "bold"), fg='#ffffff', bg='#e90052')
        self.heading.place(x=325, y=70)

        # Query the database to get the data from the 'teams2021' table
        mycursor.execute("SELECT * FROM teams2021")

        # Get the first team
        self.current_team = mycursor.fetchone()

        # Display the team
        self.display_team()

        # Next button
        self.next_button = Button(self.window, text="Next", command=self.next_team)
        self.next_button.place(x=400, y=250)

        # Previous button
        self.prev_button = Button(self.window, text="Previous", command=self.prev_team)
        self.prev_button.place(x=300, y=250)

    def display_team(self):
        # Clear the previous team
        self.clear_window()

        # Display the current team
        if self.current_team is not None:
            for i, value in enumerate(self.current_team):
                Label(self.window, text=f"{mycursor.description[i][0]}: {value}").place(x=400, y=100 + i*30)

    def next_team(self):
        # Get the next team
        self.current_team = mycursor.fetchone()

        # Display the team
        self.display_team()

    def prev_team(self):
        # Get the previous team
        mycursor.scroll(-1, mode='relative')
        self.current_team = mycursor.fetchone()

        # Display the team
        self.display_team()
        
    def search_teams(self):
        pass

    def show_players_page(self):
        self.clear_window()
        self.heading = Label(self.window, text='Players', font=("", 15, "bold"), fg='#ffffff', bg='#e90052')
        self.heading.place(x=325, y=70)

    def show_matches_page(self):
        self.clear_window()
        self.heading = Label(self.window, text='Matches', font=("", 15, "bold"), fg='#ffffff', bg='#e90052')
        self.heading.place(x=325, y=70)

    def show_transfers_page(self):
        self.clear_window()
        self.heading = Label(self.window, text='Transfers', font=("", 15, "bold"), fg='#ffffff', bg='#e90052')
        self.heading.place(x=325, y=70)

    def show_injuries_page(self):
        self.clear_window()
        self.heading = Label(self.window, text='Injuries', font=("", 15, "bold"), fg='#ffffff', bg='#e90052')
        self.heading.place(x=325, y=70)

def wind():
    window = Tk()
    Dashboard2(window)
    window.mainloop()

if __name__ == '__main__':
    wind()
