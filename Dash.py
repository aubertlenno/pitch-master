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
from tkinter import messagebox



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
        self.fantasy_text.config(command=self.show_fpl_page)
        self.players_in_position = {'Def': 0, 'Mid': 0, 'Fwd': 0, 'Gk': 0, 'Sub': 0}
        self.inserted_players = []
        self.total_points = 0



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

        self.fantasyImage = ImageTk.PhotoImage(file='images/settings-icon.png')
        self.fantasy = Label(self.sidebar, image=self.fantasyImage, bg='#00ff85')
        self.fantasy.place(x=35, y=512)

        self.fantasy_text = Button(self.sidebar, text="Fantasy Draft", bg='#00ff85', font=("", 13, "bold"), bd=0,
                                    cursor='hand2', activebackground='#00ff85')
        self.fantasy_text.place(x=90, y=512)


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
        
    def show_fpl_page(self):
        self.clear_window()

    

        welcome_text = "Welcome to the\nFantasy Draft\nSimulator"
        welcome_label = Label(self.window, text=welcome_text, font=("Helvetica", 50, "bold"), fg='white', bg='#38003c').place(x=570, y=200)
        start_button = Button(self.window, text="Start", command=self.start_simulation, font=("Helvetica", 30, "bold") , fg='white', bg='#38003c').place(x=760,y=450)


    def start_simulation(self):
        self.clear_window()

        fg_color = 'white'
        bg_color = '#38003c'

        self.team_name_var = StringVar()
        team_name_label = Label(self.window, text="Team Name:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        team_name_label.place(x=350, y=50)
        team_name_entry = Entry(self.window, textvariable=self.team_name_var, font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        team_name_entry.place(x=450, y=50)

        self.formation_var = StringVar(value="4-3-3")  # set default formation
        formation_label = Label(self.window, text="Formation:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        formation_label.place(x=350, y=95)
        formation_menu = OptionMenu(self.window, self.formation_var, "4-3-3", "3-4-3", "4-4-2")
        formation_menu.config(fg=fg_color, bg=bg_color)
        formation_menu.place(x=450, y=95)

        save_team_button = Button(self.window, text="Save Team", command=self.save_team, font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        save_team_button.place(x=350, y=140)
        reset_team_button = Button(self.window, text="Reset Team", command=self.reset_team, font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        reset_team_button.place(x=480, y=140)


        self.selected_load_team = StringVar(self.window)
        self.load_team_dropdown = OptionMenu(self.window, self.selected_load_team, 'Select a team to load')
        self.load_team_dropdown.config(fg=fg_color, bg=bg_color)
        self.load_team_dropdown.place(x=610, y=140)
        self.update_load_team_dropdown()
        # Year selection dropdown
        self.selected_year = StringVar(self.window)
        self.selected_year.set("2021")  # default value
        year_label = Label(self.window, text="Select Year:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        year_label.place(x=350, y=185)
        self.year_dropdown = OptionMenu(self.window, self.selected_year, "2021", "2022")  # Assign to self.year_dropdown
        self.year_dropdown.config(fg=fg_color, bg=bg_color)
        self.year_dropdown.place(x=450, y=185)

        # Update teams dropdown when a year is selected
        self.selected_year.trace('w', self.update_teams_dropdown)

        # Team selection dropdown
        self.selected_team = StringVar(self.window)
        team_label = Label(self.window, text="Select Team:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        team_label.place(x=350, y=230)
        self.team_dropdown = OptionMenu(self.window, self.selected_team, 'Select year first')  # Placeholder until year is selected
        self.team_dropdown.config(fg=fg_color, bg=bg_color)
        self.team_dropdown.place(x=450, y=230)
        self.selected_team.set('Select team')

        # Position selection dropdown
        self.selected_position = StringVar(self.window)
        positions = ["Forward", "Goalkeeper", "Midfielder", "Defender"]
        position_label = Label(self.window, text="Position:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        position_label.place(x=350, y=270)
        self.position_dropdown = OptionMenu(self.window, self.selected_position, *positions)
        self.position_dropdown.config(fg=fg_color, bg=bg_color)
        self.position_dropdown.place(x=450, y=270)
        self.selected_position.set('Select position')

        # Player selection dropdown
        self.selected_player = StringVar(self.window)
        player_label = Label(self.window, text="Select Player:", font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        player_label.place(x=350, y=310)  # Adjust the y-coordinate as needed to align with your layout
        self.player_dropdown = OptionMenu(self.window, self.selected_player, 'Select team and position first')
        self.player_dropdown.config(fg=fg_color, bg=bg_color)
        self.player_dropdown.place(x=450, y=310)  # Adjust the y-coordinate to match the label
        self.player_dropdown['state'] = 'disabled'

        self.insert_button = Button(self.window, text="Insert 1st Player", command=self.insert_player, font=("Helvetica", 12), fg=fg_color, bg=bg_color)
        self.insert_button.place(x=350, y=350)

        # Update position dropdown when a team is selected
        self.selected_team.trace('w', self.update_position_dropdown)

        # Update player dropdown when a position is selected
        self.selected_position.trace('w', self.update_player_dropdown)

            # Make sure to bind update_player_dropdown to both team and position dropdown changes
        self.selected_team.trace('w', self.update_player_dropdown)
        self.selected_position.trace('w', self.update_player_dropdown)

        # Also bind it to the year dropdown if it's not already bound
        self.selected_year.trace('w', self.update_player_dropdown)  


        total_points_label = Label(self.window, text="Total Points:", font=("Helvetica", 20), fg='white', bg=bg_color)
        total_points_label.place(x=1050, y=100 )  
        self.total_points_value_label = Label(self.window, text="0", font=("Helvetica", 20), fg='white', bg=bg_color)
        self.total_points_value_label.place(x=1200, y=100)

        remove_team_button= Button(self.window, text="Remove Team", command=self.remove_team, font=("Helvetica", 15), fg=fg_color, bg=bg_color)
        remove_team_button.place(x=350, y=550)


        formation_positions = {
            'Gk1': (900, 100),  
            'Def1': (710, 250), 'Def2': (835, 250), 'Def3': (960, 250), 'Def4': (1095, 250),
            'Mid1': (770, 400), 'Mid2': (900, 400), 'Mid3': (1030, 400),
            'Fwd1': (770, 550), 'Fwd2': (900, 550), 'Fwd3': (1030, 550),
        }
        # Size of the buttons
        button_width, button_height = 80, 80

        # Create buttons for each position
        for position, (x, y) in formation_positions.items():
            btn = Button(self.window, text=position, font=("Helvetica", 12), fg='white', bg='black')
            btn.place(x=x, y=y, width=button_width, height=button_height)

            # Label for the substitutes section
        sub_label = Label(self.window, text="Subsitutes", font=("Helvetica", 20), fg='white', bg='#38003c')
        sub_label.place(x=350, y=400)  # Adjust the coordinates as necessary

        # Coordinates for substitute buttons, aligned horizontally
        subs_positions = {
            'Sub1': (350, 450),
            'Sub2': (430, 450),
            'Sub3': (510, 450),
            'Sub4': (590, 450),
        }

        # Create buttons for each type of substitute
        for sub_pos, (x, y) in subs_positions.items():
            sub_btn = Button(self.window, text=sub_pos[3:], font=("Helvetica", 10), fg='white', bg='black')
            sub_btn.place(x=x, y=y, width=60, height=60)

        # Dictionary to hold the labels for player names
        self.player_name_labels = {}

        # Create labels for each position to hold the player names
        for position, (x, y) in formation_positions.items():
            name_label = Label(self.window, text="", font=("Helvetica", 10), fg='white', bg='#38003c')
            name_label.place(x=x, y=y+85)  # Place it below the position button
            self.player_name_labels[position] = name_label

        # Substitutes labels
        for sub_pos, (x, y) in subs_positions.items():
            sub_name_label = Label(self.window, text="", font=("Helvetica", 10), fg='white', bg='#38003c')
            sub_name_label.place(x=x, y=y+65)  # Place it below the substitute button
            self.player_name_labels[sub_pos] = sub_name_label

        # Initialize the current player count and the insert button text
        self.current_player_count = 1
        self.update_insert_button()
        self.players_in_position = {'Def': 0, 'Mid': 0, 'Fwd': 0, 'Gk': 0, 'Sub': 0}


    def update_insert_button(self):
        if self.current_player_count > 15:
            self.insert_button['state'] = 'disabled'  # Disable button if team is full
            self.insert_button['text'] = 'Team Full'
            return

        self.insert_button['text'] = f'Insert {self.ordinal(self.current_player_count)} Player'

    def ordinal(self, n):
        return "%d%s" % (n, "tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

        
    def update_teams_dropdown(self, *args):
        year = self.selected_year.get()
        team_names = self.fetch_teams_fpl(year)
        self.team_dropdown['menu'].delete(0, 'end')
        self.team_dropdown['state'] = 'normal'
        for team in team_names:
            self.team_dropdown['menu'].add_command(label=team, command=lambda value=team: self.selected_team.set(value))
        self.selected_team.set('')  # Clear the current selection

    def fetch_players(self, team_name, position, season):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SELECT full_name FROM players{season} WHERE current_club = %s AND position = %s ORDER BY full_name"
        try:
            mycursor.execute(query, (team_name, position))
            result = mycursor.fetchall()
            players = [player[0] for player in result]
        except Exception as e:
            print(f"An error occurred: {e}")
            players = []  # Return an empty list in case of an error
        finally:
            mycursor.close()
            mydb.close()
        return players
    
    def fetch_players_data(self, team_name, position, season):
        mydb = get_db_connection()
        mycursor = mydb.cursor()

        query = f"""
        SELECT id, full_name, age, league, season, position, current_club, minutes_played_overall, nationality,
            appearances_overall, goals_overall, assists_overall, penalty_goals, penalty_misses,
            clean_sheets_overall, conceded_overall, yellow_cards_overall, red_cards_overall,
            goals_involved_per_90_overall, goals_per_90_overall, conceded_per_90_overall,
            cards_per_90_overall, min_per_match, min_per_assist_overall
        FROM players{season}
        WHERE current_club = %s AND position = %s
        ORDER BY full_name
        """

        try:
            mycursor.execute(query, (team_name, position))
            result = mycursor.fetchall()
            player_data_dicts = [
                {
                    'id': row[0],
                    'full_name': row[1],
                    'age': row[2],
                    'league': row[3],
                    'season': row[4],
                    'position': row[5],
                    'current_club': row[6],
                    'minutes_played_overall': row[7],
                    'nationality': row[8],
                    'appearances_overall': row[9],
                    'goals_overall': row[10],
                    'assists_overall': row[11],
                    'penalty_goals': row[12],
                    'penalty_misses': row[13],
                    'clean_sheets_overall': row[14],
                    'conceded_overall': row[15],
                    'yellow_cards_overall': row[16],
                    'red_cards_overall': row[17],
                    'goals_involved_per_90_overall': row[18],
                    'goals_per_90_overall': row[19],
                    'conceded_per_90_overall': row[20],
                    'cards_per_90_overall': row[21],
                    'min_per_match': row[22],
                    'min_per_goal_assist_overall': row[23]
                } for row in result
            ]
        except Exception as e:
            print(f"An error occurred: {e}")
            player_data_dicts = []  # Return an empty list in case of an error
        finally:
            mycursor.close()
            mydb.close()

        return player_data_dicts




    def fetch_teams_fpl(self, season):
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        query = f"SELECT DISTINCT common_name FROM teams{season} ORDER BY common_name"
        mycursor.execute(query)
        result = mycursor.fetchall()
        teams = [team[0] for team in result]
        mycursor.close()
        mydb.close()
        return teams
    
    def update_player_dropdown(self, *args):
        # Make sure that the team name and position are not the initial prompts
        if self.selected_team.get() not in ('Select year first', 'Select team') and \
        self.selected_position.get() not in ('Select position',):
            team_name = self.selected_team.get()
            position = self.selected_position.get()
            season = self.selected_year.get()
            
            # Fetch players based on the selected team, position, and season
            player_names = self.fetch_players(team_name, position, season)
            
            self.player_dropdown['menu'].delete(0, 'end')
            if player_names:
                for name in player_names:
                    self.player_dropdown['menu'].add_command(label=name, command=lambda value=name: self.selected_player.set(value))
                self.player_dropdown['state'] = 'normal'
                self.selected_player.set('Select player')
            else:
                self.player_dropdown['state'] = 'disabled'
                self.selected_player.set('No players found')
        else:
            self.player_dropdown['state'] = 'disabled'
            self.selected_player.set('Select team and position first')

            

    



    def update_position_dropdown(self, *args):
        positions = ["Forward", "Goalkeeper", "Midfielder", "Defender"]
        menu = self.position_dropdown['menu']
        menu.delete(0, 'end')
        for position in positions:
            menu.add_command(label=position, command=lambda value=position: self.selected_position.set(value))
        self.position_dropdown['state'] = 'normal'
        self.update_player_dropdown()



    def save_team_to_database(self):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            database='pitch-master'
        )
        mycursor = mydb.cursor()

        team_name = self.team_name_var.get()
        formation = self.formation_var.get()
        season = self.selected_year.get()

        position_keys = ['Gk1', 'Def1', 'Def2', 'Def3', 'Def4', 'Mid1', 'Mid2', 'Mid3', 'Fwd1', 'Fwd2', 'Fwd3', 'Sub1', 'Sub2', 'Sub3', 'Sub4']
        player_names = [self.player_name_labels[position].cget('text') if position in self.player_name_labels else '' for position in position_keys]

        total_points = str(self.total_points)

        insert_query = """
        INSERT INTO Userdata (Team_name, Formation, Player1, Player2, Player3, Player4, Player5, Player6, 
        Player7, Player8, Player9, Player10, Player11, Player12, Player13, Player14, Player15, Total_Points, Season) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            mycursor.execute(insert_query, (team_name, formation, *player_names, total_points, season))
            mydb.commit()  # Commit the transaction
            messagebox.showinfo("Success", "Team saved successfully!")
            self.update_load_team_dropdown()  # Update the dropdown with the new team
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")
        finally:
            mycursor.close()
            mydb.close()

    def save_team(self):
        if not self.inserted_players:
            messagebox.showerror("Empty Team", "You cannot save an empty team.")
            return
        if len(self.inserted_players) < 11:
            messagebox.showerror("Incomplete Team", "Please insert at least 11 players before saving.")
            return

        team_name = self.team_name_var.get()
        formation = self.formation_var.get()
        season = self.selected_year.get()
        position_keys = ['Gk1', 'Def1', 'Def2', 'Def3', 'Def4', 'Mid1', 'Mid2', 'Mid3', 'Fwd1', 'Fwd2', 'Fwd3', 'Sub1', 'Sub2', 'Sub3', 'Sub4']
        player_names = [self.player_name_labels[position].cget('text') for position in position_keys]

        if not self.is_duplicate_team(team_name, formation, player_names, season):
            self.save_team_to_database()
            self.update_load_team_dropdown()
        else:
            messagebox.showerror("Duplicate Team", "A team with the same details already exists.")

            self.save_team_to_database()


        team_name = self.team_name_var.get()
        formation = self.formation_var.get()
        season = self.selected_year.get()
        position_keys = ['Gk1', 'Def1', 'Def2', 'Def3', 'Def4', 'Mid1', 'Mid2', 'Mid3', 'Fwd1', 'Fwd2', 'Fwd3', 'Sub1', 'Sub2', 'Sub3', 'Sub4']
        player_names = [self.player_name_labels[position].cget('text') for position in position_keys]

        if self.is_duplicate_team(team_name, formation, player_names, season):
            messagebox.showerror("Duplicate Team", "A team with the same details already exists.")
            return

        self.save_team_to_database()

    def insert_player(self):
        selected_player_name = self.selected_player.get()
        selected_position = self.selected_position.get()
        selected_team = self.selected_team.get()
        season = self.selected_year.get()
        
        if selected_player_name in ('Select Player', ''):
            messagebox.showinfo("Invalid Selection", "Please select a player.")
            return

        if selected_player_name in self.inserted_players:
            messagebox.showerror("Duplicate Player", "This player has already been inserted.")
            return

        player_data_list = self.fetch_players_data(selected_team, selected_position, season)
        player_data = next((data for data in player_data_list if data['full_name'] == selected_player_name), None)
        if not player_data:
            messagebox.showerror("Player Not Found", "The selected player's data could not be found.")
            return

        # Calculate points only for the first 11 players
        if self.current_player_count <= 11:
            player_points = self.calculate_player_points(player_data)
        else:
            player_points = 0

        position_prefixes = {"Goalkeeper": "Gk", "Defender": "Def", "Midfielder": "Mid", "Forward": "Fwd"}
        selected_position_prefix = position_prefixes.get(selected_position, "Sub")

        max_players = {"Gk": 1, "Def": 4, "Mid": 3, "Fwd": 3, "Sub": 4}
        if self.current_player_count <= 11:
            if self.players_in_position[selected_position_prefix] >= max_players[selected_position_prefix]:
                messagebox.showerror("Position Full", f"All {selected_position} positions are filled.")
                return
        else:
            selected_position_prefix = "Sub"
            position_number = self.players_in_position[selected_position_prefix]
            if position_number >= max_players[selected_position_prefix]:
                messagebox.showerror("Substitutes Full", "No more substitutes can be added.")
                self.insert_button['state'] = 'disabled'
                self.insert_button['text'] = 'Full Squad'
                return

        position_number = self.players_in_position[selected_position_prefix] + 1
        position_label = f'{selected_position_prefix}{position_number}'
        
        self.player_name_labels[position_label]['text'] = selected_player_name
        self.players_in_position[selected_position_prefix] = position_number

        self.total_points += player_points
        self.total_points_value_label.config(text=str(self.total_points))

        self.inserted_players.append(selected_player_name)
        self.current_player_count += 1
        self.update_insert_button()

        if self.current_player_count > 15:
            self.insert_button['state'] = 'disabled'
            self.insert_button['text'] = 'Full Squad'
        elif self.current_player_count > 0:
            self.year_dropdown['state'] = 'disabled'
            self.year_dropdown['text'] = 'Locked'



    def reset_team(self):
        self.team_name_var.set("")
        self.formation_var.set("4-3-3")

        self.selected_year.set("2021")
        self.selected_team.set('Select team')
        self.selected_position.set('Select position')

        self.selected_player.set('Select team and position first')
        self.player_dropdown['state'] = 'disabled'

        self.insert_button['state'] = 'normal'
        self.insert_button['text'] = "Insert 1st Player"

        self.inserted_players.clear()

        self.players_in_position = {'Def': 0, 'Mid': 0, 'Fwd': 0, 'Gk': 0, 'Sub': 0}
        self.current_player_count = 1

        self.total_points = 0
        self.total_points_value_label.config(text=str(self.total_points))

        for label in self.player_name_labels.values():
            label['text'] = ""

        # Refresh the  and player dropdowns (if necessary)
        self.update_teams_dropdown()
        self.update_player_dropdown()
        self.year_dropdown['state'] = 'normal'


    def calculate_player_points(self, player_data):
        POINTS_PER_GOAL = {'Goalkeeper': 4, 'Defender': 4, 'Midfielder': 5, 'Forward': 4}
        POINTS_CLEAN_SHEET = {'Goalkeeper': 4, 'Defender': 4, 'Midfielder': 1, 'Forward': 0}
        POINTS_PER_ASSIST = 3
        POINTS_PER_YELLOW = -1
        POINTS_PER_RED = -3
        POINTS_PER_MISSED_PEN = -2
        POINTS_CONCEDED = -1  # For every 2 goals conceded by their team

        # Calculate points
        def safe_int(value):
            try:
                return int(value)
            except ValueError:
                return 0
        points = 0
        minutes = safe_int(player_data['minutes_played_overall']) / 38
        goals = safe_int(player_data['goals_overall']) / 38
        assists = safe_int(player_data['assists_overall']) / 38
        conceded = safe_int(player_data['conceded_overall']) / 38
        yellow_cards = safe_int(player_data['yellow_cards_overall']) / 38
        red_cards = safe_int(player_data['red_cards_overall']) / 38
        missed_penalties = safe_int(player_data['penalty_misses']) / 38
        clean_sheets = safe_int(player_data['clean_sheets_overall']) / 38

        position = player_data['position']


        #playing time
        if minutes > 0:
            points += 1  # Played up to 60 minutes
        if minutes >= 60:
            points += 1  # Played 60 minutes or more

        #goals scored
        points += goals * POINTS_PER_GOAL.get(position, 0)

        #clean sheets
        if minutes >= 60:  # Only if played 60 minutes or more
            points += clean_sheets * POINTS_CLEAN_SHEET.get(position, 0)

        #goals conceded by goalkeepers and defenders
        if position in ['Goalkeeper', 'Defender']:
            points += (conceded - 1) // 2 * POINTS_CONCEDED

        # Points  
        points += assists * POINTS_PER_ASSIST

        # Penalty 
        points += yellow_cards * POINTS_PER_YELLOW
        points += red_cards * POINTS_PER_RED
        points += missed_penalties * POINTS_PER_MISSED_PEN

        return round(points)

    def is_duplicate_team(self, team_name, formation, player_names, season):
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            database='pitch-master'
        )
        mycursor = mydb.cursor()

        # Ensure team_name, formation, and season are stripped of whitespace and standardized
        team_name = team_name.strip().lower()
        formation = formation.strip().lower()
        season = season.strip()

        # Check for duplicate team based on team name, formation, and season
        check_query = """
        SELECT Team_name, Formation, Season
        FROM Userdata
        WHERE Team_name = %s AND Formation = %s AND Season = %s
        """
        mycursor.execute(check_query, (team_name, formation, season))
        existing_teams = mycursor.fetchall()

        for existing_team in existing_teams:
            print(f"Existing team data: {existing_team}")  # Debugging print

        # Check if any retrieved team has the same player details
        for existing_team in existing_teams:
            existing_team_name = existing_team[0].strip().lower()
            existing_formation = existing_team[1].strip().lower()
            existing_season = str(existing_team[2]).strip()

            if existing_team_name == team_name and existing_formation == formation and existing_season == season:
                # Now we check if all the player names are the same
                existing_player_names = [existing_team[i+3].strip() for i in range(15) if existing_team[i+3]]
                if set(existing_player_names) == set(player_names):
                    mycursor.close()
                    mydb.close()
                    return True  # A duplicate team exists

        mycursor.close()
        mydb.close()
        return False  # No duplicate team exists


    
    def update_load_team_dropdown(self):
        # Fetch team names from the database
        team_names = self.fetch_team_names()
        menu = self.load_team_dropdown['menu']
        menu.delete(0, 'end')

        # Define a new command that will set the selected_load_team and load the team
        def command(value):
            self.selected_load_team.set(value)
            self.load_team()

        for name in team_names:
            menu.add_command(label=name, command=lambda value=name: command(value))
        self.selected_load_team.set('Select a team to load')

    def fetch_team_names(self):
        # Establish a database connection
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            database='pitch-master'
        )
        mycursor = mydb.cursor()

        # SQL query to fetch team names
        query = "SELECT DISTINCT Team_name FROM Userdata ORDER BY Team_name"
        try:
            mycursor.execute(query)
            result = mycursor.fetchall()
            team_names = [name[0] for name in result]
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            team_names = []  # Return an empty list in case of an error
        finally:
            mycursor.close()
            mydb.close()
        return team_names

    def load_team(self):
        try:
            # Get the selected team name from the dropdown
            selected_team_name = self.selected_load_team.get()
            print(f"Loading team: {selected_team_name}")  # Debugging print

            # Validate the selection
            if selected_team_name == 'Select a team to load':
                messagebox.showinfo("Selection Needed", "Please select a team to load.")
                return

            # Fetch the team data from the database
            team_data = self.fetch_team_data(selected_team_name)
            print(f"Team data fetched: {team_data}")  # Debugging print

            if not team_data:
                messagebox.showerror("Not Found", "The selected team could not be found in the database.")
                return

            # Load the team data onto the form
            self.team_name_var.set(team_data['Team_name'])
            self.formation_var.set(team_data['Formation'])
            self.selected_year.set(team_data['Season'])

            # Iterate over the positions and assign the player names to the labels
            for position_key in ['Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'Player6', 'Player7', 'Player8', 'Player9', 'Player10', 'Player11', 'Player12', 'Player13', 'Player14', 'Player15']:
                player_label_key = self.map_player_to_position(position_key, team_data['Formation'])
                player_name = team_data.get(position_key, '')
                print(f"Mapping {position_key} to {player_label_key} with name {player_name}")  # Debugging print
                if player_name:
                    self.player_name_labels[player_label_key].config(text=player_name)

            # Update total points label
            self.total_points_value_label.config(text=str(team_data['Total_Points']))
        except Exception as e:
            print(f"An error occurred in load_team: {e}")  # Print any exception


    def fetch_team_data(self, team_name):
        # Establish a database connection
        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            database='pitch-master'
        )
        mycursor = mydb.cursor()

        # SQL query to fetch team data
        query = "SELECT * FROM Userdata WHERE Team_name = %s"
        try:
            mycursor.execute(query, (team_name,))
            result = mycursor.fetchone()
            if result:
                columns = [desc[0] for desc in mycursor.description]
                return dict(zip(columns, result))
            else:
                return None
        except mysql.connector.Error as err:
            print(f"An error occurred: {err}")
            return None
        finally:
            mycursor.close()
            mydb.close()
    def map_player_to_position(self, player_key, formation):
        
        formation_map = {
            '4-3-3': {
                'Player1': 'Gk1',
                'Player2': 'Def1',
                'Player3': 'Def2',
                'Player4': 'Def3',
                'Player5': 'Def4',
                'Player6': 'Mid1',
                'Player7': 'Mid2',
                'Player8': 'Mid3',
                'Player9': 'Fwd1',
                'Player10': 'Fwd2',
                'Player11': 'Fwd3',
                'Player12': 'Sub1',
                'Player13': 'Sub2',
                'Player14': 'Sub3',
                'Player15': 'Sub4'
            }
            # Other formations would be added here
        }
        return formation_map[formation].get(player_key, '')
        

    def remove_team(self):
        team_name = self.selected_load_team.get()
        if team_name == 'Select a team to load':
            messagebox.showwarning("No team selected", "Please select a team to remove.")
            return

        mydb = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            passwd='',
            database='pitch-master'
        )
        mycursor = mydb.cursor()

        delete_query = "DELETE FROM Userdata WHERE Team_name = %s"

        try:
            mycursor.execute(delete_query, (team_name,))
            mydb.commit()
            messagebox.showinfo("Success", f"Team '{team_name}' removed successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred while removing the team: {err}")
        finally:
            mycursor.close()
            mydb.close()

        self.update_load_team_dropdown()  

def wind():
    window = Tk()
    Dashboard2(window)
    window.mainloop()

if __name__ == '__main__':
    wind()

