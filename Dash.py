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
        self.normal_button = Button(self.window, text="Normal", fg='#F2055C', bg='#38003c', bd=0,
                                cursor='hand2', activebackground='#38003c', font=("", 18, "bold"), 
                                command=self.on_normal_button_pressed)
        self.normal_button.place(x=400, y=200)

        # Graph Button
        self.graph_button = Button(self.window, text="Graph", fg='#ffffff', bg='#38003c', bd=0,
                               cursor='hand2', activebackground='#38003c', font=("", 18, "bold"), 
                               command=self.on_graph_button_pressed)
        self.graph_button.place(x=400, y=280)
        
        

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

        self.graph_type_var = StringVar(self.window)
        self.graph_types = ['Vertical Bar', 'Horizontal Bar', 'Scatter Plot']
        self.graph_type_var.set(self.graph_types[0]) 
        self.graph_type_dropdown = OptionMenu(self.window, self.graph_type_var, *self.graph_types)
        self.graph_type_dropdown.place(x=1050, y=100)

        self.normal_button = Button(self.window, text="Normal", fg='#ffffff', bg='#38003c', bd=0,
                                cursor='hand2', activebackground='#38003c', font=("", 18, "bold"), 
                                command=self.on_normal_button_pressed)
        self.normal_button.place(x=400, y=200)

        # Graph Button
        self.graph_button = Button(self.window, text="Graph", fg='#F2055C', bg='#38003c', bd=0,
                               cursor='hand2', activebackground='#38003c', font=("", 18, "bold"), 
                               command=self.on_graph_button_pressed)
        self.graph_button.place(x=400, y=280)

        self.generate_graph_button = Button(self.window, text="Generate Graph", fg='#340040', command=self.generate_graph)
        self.generate_graph_button.place(x=1200, y=150)
        self.on_season_select(initial=True)


    def generate_graph(self):
        column = self.selected_column.get().replace('_', ' ')
        season = self.selected_season.get()
        graph_type = self.graph_type_var.get()
        data = self.fetch_data_for_graph(column.replace(' ', '_'), season)

        data.sort(key=lambda x: x[1], reverse=True)
        teams = [item[0] for item in data]
        values = [item[1] for item in data]
        team_colors = {
            'Arsenal FC': '#EF0107',
            'Aston Villa FC': '#670E36',
            'Brentford FC': '#FF0000',
            'Brighton & Hove Albion FC': '#0057B8',
            'Burnley FC': '#6C1D45',
            'Chelsea FC': '#034694',
            'Crystal Palace FC': '#C4122E',  # Primary color Red
            'Everton FC': '#003399',
            'Fulham FC': '#FFFFFF',
            'Leeds United FC': '#FFFFFF',
            'Leicester City FC': '#003090',
            'Liverpool FC': '#C8102E',
            'Manchester City FC': '#6CABDD',
            'Manchester United FC': '#DA291C',
            'Newcastle United FC': '#241F20',  # Primary color Black
            'Norwich City FC': '#FFF200',  # Primary color Yellow
            'Southampton FC': '#D71920',  # Primary color Red
            'Tottenham Hotspur FC': '#FFFFFF',
            'Watford FC': '#FBEE23',
            'West Ham United FC': '#7A263A',  # Primary color Claret
            'Wolverhampton Wanderers FC': '#FDB913',
            'AFC Bournemouth FC': '#DA291C',  # Primary color Red
            'Nottingham Forest FC': '#D50000',
        }

        team_abbreviations = {
            'Arsenal FC': 'ARS',
            'Aston Villa FC': 'AVL',
            'Brentford FC': 'BRE',
            'Brighton & Hove Albion FC': 'BHA',
            'Burnley FC': 'BUR',
            'Chelsea FC': 'CHE',
            'Crystal Palace FC': 'CRY',
            'Everton FC': 'EVE',
            'Fulham FC': 'FUL',
            'Leeds United FC': 'LEE',
            'Leicester City FC': 'LEI',
            'Liverpool FC': 'LIV',
            'Manchester City FC': 'MCI',
            'Manchester United FC': 'MUN',
            'Newcastle United FC': 'NEW',
            'Norwich City FC': 'NOR',
            'Southampton FC': 'SOU',
            'Tottenham Hotspur FC': 'TOT',
            'Watford FC': 'WAT',
            'West Ham United FC': 'WHU',
            'Wolverhampton Wanderers FC': 'WOL',
            'AFC Bournemouth FC': 'BOU',
            'Nottingham Forest FC': 'NFO',
        }

        abbreviated_teams = [team_abbreviations.get(team, 'UNK') for team in teams]  # UNK for Unknown


        fig, ax = plt.subplots(figsize=(8, 6))
        bar_colors = [team_colors.get(team, '#FFFFFF') for team in teams]

        if graph_type == 'Horizontal Bar':
            bars = ax.barh(teams, values, color=bar_colors)
            for bar in bars:
                width = bar.get_width()
                label_x_pos = bar.get_x() + width / 2
                ax.text(label_x_pos, bar.get_y() + bar.get_height() / 2, str(width), va='center', ha='center')

        elif graph_type == 'Vertical Bar':
            bars = ax.bar(range(len(abbreviated_teams)), values, color=bar_colors)
            ax.set_xticks(range(len(abbreviated_teams)))
            ax.set_xticklabels(abbreviated_teams, rotation=90)
            for bar in bars:
                height = bar.get_height()
                label_y_pos = bar.get_y() + height / 2
                ax.text(bar.get_x() + bar.get_width() / 2, label_y_pos, str(height), va='center', ha='center')

        elif graph_type == 'Scatter Plot':
            for i, (abbr, value) in enumerate(zip(abbreviated_teams, values)):
                ax.scatter(i, value, color=team_colors.get(teams[i], '#FFFFFF'))
                ax.text(i, value, abbr, ha='center', va='bottom', fontsize=8, rotation=45, color='white')

        # Common graph settings
        ax.set_xlabel('Values')
        ax.set_title(f'{column} for Season {season}')
        ax.set_facecolor('#38003c')
        fig.patch.set_facecolor('#38003c')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        plt.subplots_adjust(left=0.3 if graph_type == 'Horizontal Bar' else 0.1)

        # Embedding the graph in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.draw()
        canvas.get_tk_widget().place(x=470, y=105)

        self.season_dropdown.place(x=400, y=100)
        self.column_dropdown.place(x=1200, y=100)
        self.normal_button.place(x=400, y=200)
        self.graph_button.place(x=400, y=280)
        self.generate_graph_button.place(x=1200, y=150)
        self.graph_type_dropdown.place(x=1050, y=100)

        self.season_dropdown.lift()
        self.column_dropdown.lift()
        self.graph_type_dropdown.lift()
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

        self.selected_year = StringVar(self.window)
        self.years = ['2021', '2022']  # Update this list as needed
        self.selected_year.set('2021')  # Set default year to 2021
        self.year_dropdown = OptionMenu(self.window, self.selected_year, *self.years, command=self.on_year_select)
        self.year_dropdown.place(x=400, y=100)  # Adjust position as needed

        # Initialize empty dropdowns for team and player, to be populated later
        self.selected_team = StringVar(self.window)
        self.team_dropdown = OptionMenu(self.window, self.selected_team, '')
        self.team_dropdown.place(x=480, y=100)  # Adjust position as needed

        self.selected_player = StringVar(self.window)
        self.player_dropdown = OptionMenu(self.window, self.selected_player, '')
        self.player_dropdown.place(x=685, y=100)  # Adjust position as needed

        self.on_year_select('2021')
        self.create_scrollable_stat_area()

    def on_year_select(self, selected_year):
        teams = self.fetch_teams_for_year(selected_year)
        self.selected_team.set(teams[0] if teams else '')  # Set the first team as default
        self.team_dropdown['menu'].delete(0, 'end')
        for team in teams:
            self.team_dropdown['menu'].add_command(label=team, command=lambda value=team: self.update_team_selection(value))
        self.update_team_selection(teams[0] if teams else '')  # Update player dropdown
    
    def fetch_teams_for_year(self, year):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SELECT DISTINCT current_club FROM players{year}"
        mycursor.execute(query)
        teams = [team[0] for team in mycursor.fetchall()]
        mycursor.close()
        mydb.close()
        return teams
    
    def update_team_selection(self, team):
        self.selected_team.set(team)
        players = self.fetch_players_for_team(self.selected_year.get(), team)
        self.selected_player.set(players[0] if players else '')  # Set the first player as default
        self.player_dropdown['menu'].delete(0, 'end')
        for player in players:
            self.player_dropdown['menu'].add_command(label=player, command=lambda value=player: self.display_player_stats(value))
    
    def update_player_dropdown(self):
        team = self.selected_team.get()
        year = self.selected_year.get()
        players = self.fetch_players_for_team(year, team)
        self.selected_player.set('')  # Clear previous selection
        self.player_dropdown['menu'].delete(0, 'end')
        for player in players:
            self.player_dropdown['menu'].add_command(label=player, command=lambda value=player: self.selected_player.set(value))

    def display_player_stats(self, player_name):
        self.selected_player.set(player_name)
        player_stats = self.fetch_player_stats(player_name, self.selected_year.get())

        # Clear previous stats
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if player_stats:
            # Display new stats in the scrollable frame
            for i, (key, value) in enumerate(player_stats.items()):
                Label(self.scrollable_frame, text=f"{key.replace('_', ' ').title()}: {value}", bg='#38003c', fg='white').grid(row=i, column=0, sticky="w", padx=10, pady=5)

    def fetch_players_for_team(self, year, team):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SELECT full_name FROM players{year} WHERE current_club = %s"
        mycursor.execute(query, (team,))
        players = [player[0] for player in mycursor.fetchall()]
        mycursor.close()
        mydb.close()
        return players
    
    def fetch_player_stats(self, player_name, year):
        mydb = get_db_connection()
        mycursor = mydb.cursor(dictionary=True)
        query = f"SELECT * FROM players{year} WHERE full_name = %s"
        mycursor.execute(query, (player_name,))
        player_stats = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        return player_stats
    
    def create_scrollable_stat_area(self):
        # Create a canvas and a scrollbar
        self.stats_canvas = Canvas(self.window, bg='#38003c')
        self.stats_scrollbar = Scrollbar(self.window, orient="vertical", command=self.stats_canvas.yview)
        self.scrollable_frame = Frame(self.stats_canvas, bg='#38003c')

        # Add the scrollable frame to the canvas
        self.stats_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.stats_canvas.configure(yscrollcommand=self.stats_scrollbar.set)

        # Bind the configuration event to update the scroll region
        self.scrollable_frame.bind("<Configure>", lambda e: self.stats_canvas.configure(scrollregion=self.stats_canvas.bbox("all")))

        # Place the canvas and scrollbar in the window
        self.stats_canvas.place(x=400, y=200, width=560, height=500)  # Adjust size and position as needed
        self.stats_scrollbar.place(x=960, y=200, height=500)  # Adjust to align with the canvas


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
        pl_logo = pl_logo.resize((350, 300))  # Resize the image if needed and preserve aspect ratio
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
    window.state('zoomed')
    Dashboard2(window)
    window.mainloop()

if __name__ == '__main__':
    wind()

