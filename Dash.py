from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from datetime import *
import time
from database import get_db_connection
from tkinter import ttk
import mysql.connector
import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

mydb = get_db_connection()
mycursor = mydb.cursor()

class Dashboard2:
    def __init__(self, window):
        self.window = window
        self.window.title("System Management Dashboard")
        self.window.geometry("1366x744")
        self.window.resizable(False, False)
        self.window.config(background='#38003c')
        self.create_header()
        self.create_sidebar()
        self.create_date_time_display()

        self.dashboard_text.config(command=self.show_teams_page)
        self.manage_text.config(command=self.show_players_page)
        self.settings_text.config(command=self.show_matches_page)
        self.Exit_text.config(command=self.show_league_page)
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

        self.Exit_text = Button(self.sidebar, text="League", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                cursor='hand2', activebackground='#00ff85')
        self.Exit_text.place(x=85, y=462)


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
        self.heading = Label(self.window, text='Teams', font=("", 15, "bold"), fg='#ffffff', bg='#38003c')
        self.heading.place(x=325, y=70)
        
        # Team and Season Selection
         # Season Selection
        self.selected_season = StringVar(self.window)
        self.seasons = ['2021', '2022']
        self.selected_season.set('2021')
        self.season_dropdown = OptionMenu(self.window, self.selected_season, *self.seasons, command=self.on_season_select)
        self.season_dropdown.place(x=400, y=100)
        

        # Initialize team dropdown but do not populate it yet
        self.selected_team = StringVar(self.window)
        self.teams = self.fetch_teams(self.selected_season.get())  # Fetch teams for the selected season
        self.selected_team.set(self.teams[0])  # Set the default team
        self.team_dropdown = OptionMenu(self.window, self.selected_team, *self.teams, command=self.update_team_stats)
        self.team_dropdown.place(x=800, y=100)

        # Normal Button
        self.normal_button = Button(self.window, text="Normal", fg='#340040', bg='#F2055C', command=self.on_normal_button_pressed)
        self.normal_button.place(x=400, y=150)

        # Graph Button
        self.graph_button = Button(self.window, text="Graph", fg='#340040', bg='white', command=self.on_graph_button_pressed)
        self.graph_button.place(x=400, y=200)
        
        

        # Labels for Statistics
        self.stat_labels = {
            "Wins": StringVar(),
            "Draw": StringVar(),
            "Losses": StringVar(),
            "Goal Scored": StringVar(),
            "Goal Conceded": StringVar(),
            "Goal Difference": StringVar(),
            "Clean Sheets": StringVar(),
            "Average Possession": StringVar(),
            "Shots": StringVar(),
        }

        label_x = 600  # Starting x position for labels
        value_x = label_x + 500  # label_value_spacing = 500
        initial_y = 150  # Starting y position for the first statistic label
        y_increment = 50  
        for i, (label_text, var) in enumerate(self.stat_labels.items()):
            Label(self.window, text=label_text, font=("", 12), fg='white', bg='#38003c').place(x=label_x, y=initial_y + i*y_increment)
            Label(self.window, textvariable=var, font=("", 12), fg='white', bg='#38003c').place(x=value_x, y=initial_y + i*y_increment)

        # Initially populate stats for the default team and season
        self.update_team_stats()

    def on_season_select(self, initial=False):
        season = self.selected_season.get()
        teams = self.fetch_teams(season)

        if initial:
            default_team = 'Arsenal FC' if season == '2021' else 'AFC Bournemouth'
            self.selected_team.set(default_team)
        elif teams:
            # On user-triggered year change, select the first team in the list
            self.selected_team.set(teams[0])

        if teams:
            self.team_dropdown['menu'].delete(0, 'end')
            for team in teams:
                self.team_dropdown['menu'].add_command(label=team, command=lambda value=team: self.update_team_selection(value))

        # Update stats after setting the default team
        self.update_team_stats()

    
    def update_team_selection(self, team):
        self.selected_team.set(team)
        self.update_team_stats()
    
    def on_normal_button_pressed(self):
        # Change button colors to indicate selection
        self.normal_button.config(bg='#F2055C')
        self.graph_button.config(bg='white')
        # Handle any additional functionality for the Normal view
        self.show_teams_page()
       

    def on_graph_button_pressed(self):
        # Change button colors to indicate selection
        self.normal_button.config(bg='white')
        self.graph_button.config(bg='#F2055C')
        # Open the new page for the Graph view
        self.show_graph_page()




    def fetch_teams(self, season):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SELECT DISTINCT team_name FROM teams{season} ORDER BY team_name"
        mycursor.execute(query)
        result = mycursor.fetchall()
        teams = [team[0] for team in result]
        mycursor.close()
        mydb.close()
        return teams

    def update_team_stats(self, *args):
        # Get the selected team and season
        team = self.selected_team.get()
        season = self.selected_season.get()

        # Fetch and display the statistics for the selected team and season
        stats = self.get_team_stats_from_db(team, season)
        for stat_name, var in self.stat_labels.items():
            var.set(stats.get(stat_name, 'N/A')) # Use 'N/A' if the stat is not found

    def get_team_stats_from_db(self, team, season):
        table_name = f"teams{season}"
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name} WHERE team_name = %s"
        mycursor.execute(query, (team,))
        stats_row = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if stats_row:
            return {
                # Use the correct column names as per your table schema
                'Wins': stats_row['wins_home'] + stats_row['wins_away'],
                'Draw': stats_row['draws_home'] + stats_row['draws_away'],
                'Losses': stats_row['losses_home'] + stats_row['losses_away'],
                'Goal Scored': stats_row['goals_scored'],
                'Goal Conceded': stats_row['goals_conceded'],
                'Goal Difference': stats_row['goal_difference'],
                'Clean Sheets': stats_row['clean_sheets'],
                'Average Possession': f"{stats_row['average_possession']}%",  # Adjust this if your column has a different name
                'Shots': stats_row['shots_on_target'] + stats_row['shots_off_target'],  # Adjust if your columns have different names
            }
        else:
            return {stat: 'N/A' for stat in self.stat_labels}
    def fetch_column_names(self, season):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SHOW COLUMNS FROM teams{season}"
        mycursor.execute(query)
        # Replace underscores with spaces in the column names
        columns = [column[0].replace('_', ' ') for column in mycursor.fetchall()
                if column[0].lower() not in ('id', 'team_name', 'common_name', 'season', 'country', 'suspended_matches')]
        mycursor.close()
        mydb.close()
        return columns

        
    def show_graph_page(self):
        self.clear_window()

        # Heading
        self.heading = Label(self.window, text='Teams', font=("", 15, "bold"), fg='#ffffff', bg='#38003c')
        self.heading.place(x=325, y=70)
        
        # Team and Season Selection
        # Season Dropdown
        self.selected_season = StringVar(self.window)
        self.seasons = ['2021', '2022']
        self.selected_season.set('2021')
        self.season_dropdown = OptionMenu(self.window, self.selected_season, *self.seasons, command=self.on_season_select)
        self.season_dropdown.place(x=400, y=100)

    

        self.column_names = self.fetch_column_names('2021')

        self.selected_column = StringVar(self.window)
        self.selected_column.set(self.column_names[0])  # set default value
        self.column_dropdown = OptionMenu(self.window, self.selected_column, *self.column_names)
        self.column_dropdown.place(x=1200, y=100)

        # Normal Button
        self.normal_button = Button(self.window, text="Normal", fg='#340040', bg='white', command=self.on_normal_button_pressed)
        self.normal_button.place(x=400, y=150)

        # Graph Button
        self.graph_button = Button(self.window, text="Graph", fg='#340040', bg='#F2055C', command=self.on_graph_button_pressed)
        self.graph_button.place(x=400, y=200)

        self.generate_graph_button = Button(self.window, text="Generate Graph", fg='#340040', command=self.generate_graph)
        self.generate_graph_button.place(x=1200, y=150)
        self.on_season_select(initial=True)


    def generate_graph(self):
        # Fetch the data for the selected column and season
        column = self.selected_column.get().replace('_', ' ')  # Replace underscores with spaces
        season = self.selected_season.get()
        data = self.fetch_data_for_graph(column.replace(' ', '_'), season)  # Replace spaces back to underscore for SQL query

        # Sort the data by the second item in the tuple (which is assumed to be the value)
        data.sort(key=lambda x: x[1], reverse=True)

        # Now generate the bar chart

        teams = [item[0] for item in data]
        values = [item[1] for item in data]

        # Create the bar chart
        fig, ax = plt.subplots(figsize=(8, 6))  # Adjust the figure size as needed
        bars = ax.barh(teams, values, color='skyblue')
        ax.set_xlabel('Values')
        ax.set_title(f'{column} for Season {season}')

        # Set the background color
        fig.patch.set_facecolor('#38003c')  # Set the outer background color
        ax.set_facecolor('#38003c')  # Set the inner background color

        # Set the color of the text and labels to contrast against the dark background
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

        # Adjust the margins
        plt.subplots_adjust(left=0.3)  # Adjust this value as needed to fit the team names

        # Add the values on the bars and adjust their position based on the bar length
        for bar in bars:
            width = bar.get_width()
            bar_height = bar.get_height()
            y = bar.get_y() + bar_height / 2
            if width != 0:
                ax.text(width / 2, y, f'{width}', ha='center', va='center', color='black')

        ax.tick_params(axis='y', labelsize=8) 
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=105)

        self.season_dropdown.place(x=400, y=100)
        self.column_dropdown.place(x=1200, y=100)
        self.normal_button.place(x=400, y=150)
        self.graph_button.place(x=400, y=200)
        self.generate_graph_button.place(x=1200, y=150)

        self.season_dropdown.lift()
        self.column_dropdown.lift()
        self.normal_button.lift()
        self.graph_button.lift()
        self.generate_graph_button.lift()

    def fetch_data_for_graph(self, column, season):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SELECT team_name, {column} FROM teams{season}"
        mycursor.execute(query)
        result = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return result


    

    def show_players_page(self):
        self.clear_window()
        self.heading = Label(self.window, text='Players', font=("", 15, "bold"), fg='#ffffff', bg='#38003c')
        self.heading.place(x=325, y=70)

    def show_matches_page(self):
        self.clear_window()
        self.heading = Label(self.window, text='Matches', font=("", 15, "bold"), fg='#ffffff', bg='#38003c')
        self.heading.place(x=325, y=70)

    def show_league_page(self):
        self.clear_window()

        sidebar_width = 300  
        content_padding = 50  
        dropdown_width = 10
        label_value_spacing = 500 

        pl_logo = Image.open('images/pl_logo.png')  
        pl_logo = pl_logo.resize((350, 300), Image.ANTIALIAS)  # Resize the image if needed and preserve aspect ratio
        pl_logo = ImageTk.PhotoImage(pl_logo)

        pl_logo_label = Label(self.window, image=pl_logo, bg='#38003c')
        pl_logo_label.image = pl_logo  
        pl_logo_label.place(x=300, y=120)

        Label(self.window, text="Select Season", font=("", 18, "bold"), fg='white', bg='#38003c').place(x=683, y=65)

        dropdown_y = 140

        winner = self.get_winner_from_db('2021') 
        Label(self.window, text="WINNER", font=("", 15, "bold"), fg='white', bg='#38003c').place(x=sidebar_width + content_padding, y=430)
        Label(self.window, text=winner, font=("", 15, "bold"), fg='white', bg='#38003c').place(x=sidebar_width + content_padding, y=470)

        self.selected_season = StringVar(self.window)
        self.seasons = self.fetch_seasons()
        self.selected_season.set(self.seasons[0])
        self.season_dropdown = OptionMenu(self.window, self.selected_season, *self.seasons, command=self.update_stats)
        self.season_dropdown.config(width=dropdown_width)
        # Adjust x position to the right, place the dropdown below the header
        self.season_dropdown.place(x=715, y=105)

        # Place labels and values
        self.stat_labels = {
            "Number of Teams Participated": StringVar(),
            "Matches Conducted": StringVar(),
            "Total Game Week": StringVar(),
            "Average Goals per Match": StringVar(),
            "Clean Sheets Percentage": StringVar(),
            "Average Corners per Match": StringVar(),
            "Total Corners": StringVar(),
            "Average Cards per Match": StringVar(),
            "Total Cards": StringVar(),
        }
        
        label_x = 650  # Increase padding to move to the right
        value_x = label_x + label_value_spacing
        initial_y = dropdown_y + 40  # Start below the dropdown
        y_increment = 50

        for i, (label_text, var) in enumerate(self.stat_labels.items()):
            # Adjust x position to the right
            Label(self.window, text=label_text, font=("", 12), fg='white', bg='#38003c', anchor='w').place(x=label_x, y=initial_y + (i * y_increment))
            Label(self.window, textvariable=var, font=("", 12), fg='white', bg='#38003c', anchor='e').place(x=value_x, y=initial_y + (i * y_increment))
        
        # Initially populate stats for the default season
        self.update_stats(self.selected_season.get())


    def fetch_seasons(self):
        # Function to fetch available seasons from the database
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SHOW TABLES LIKE 'league%'")  # Query to fetch tables with league stats
        result = mycursor.fetchall()
        seasons = [season[0].replace('league', '') for season in result]  # Extract season years
        mycursor.close()
        mydb.close()
        return seasons

    def update_stats(self, season):
        year = season.split(' - ')[0]
        stats = self.get_stats_from_db(year)
        if stats:
            self.stat_labels["Number of Teams Participated"].set(stats['number_of_clubs'])
            self.stat_labels["Matches Conducted"].set(stats['matches_completed'])
            self.stat_labels["Total Game Week"].set(stats['total_game_week'])
            self.stat_labels["Average Goals per Match"].set(stats['average_goals_per_match'])
            self.stat_labels["Clean Sheets Percentage"].set(stats['clean_sheets_percentage'])
            self.stat_labels["Average Corners per Match"].set(stats['average_corners_per_match'])
            self.stat_labels["Total Corners"].set(stats['total_corners_for_season'])
            self.stat_labels["Average Cards per Match"].set(stats['average_cards_per_match'])
            self.stat_labels["Total Cards"].set(stats['total_cards_for_season'])

    def get_winner_from_db(self, year):
        table_name = f"teams{year}"  
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        query = f"SELECT team_name FROM {table_name} WHERE league_position = 1"
        mycursor.execute(query)
        winner = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if winner:
            return winner['team_name']
        else:
            return "Winner Not Found"

    def get_stats_from_db(self, season):
        # Function to query the database and return stats for the selected season
        table_name = f"league{season.replace(' - ', '')}"  # Convert season to table name
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name}"
        mycursor.execute(query)
        stats_row = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if stats_row:
            # Assuming the column names in the database match the stat_labels keys
            return {key: stats_row[key.replace(' ', '_').lower()] for key in self.stat_labels}
        else:
            return {key: "N/A" for key in self.stat_labels}  # Return "N/A" if no data is found

# Rest of your Tkinter setup and main loop

    def get_stats_from_db(self, year):
        table_name = f"league{year}"  # Construct the table name based on the year
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        query = f"SELECT * FROM {table_name} LIMIT 1"  # Assuming there's only one row per season table
        mycursor.execute(query)
        stats_row = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        if stats_row:
            # Return the stats row if data was found
            return stats_row
        else:
            # Return a dictionary with None values if no data was found
            return {
                'number_of_clubs': None,
                'matches_completed': None,
                'total_game_week': None,
                'average_goals_per_match': None,
                'clean_sheets_percentage': None,
                'average_corners_per_match': None,
                'total_corners_for_season': None,
                'average_cards_per_match': None,
                'total_cards_for_season': None
            }




   

def wind():
    window = Tk()
    Dashboard2(window)
    window.mainloop()

if __name__ == '__main__':
    wind()

