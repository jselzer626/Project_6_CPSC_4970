# Curling League Manager

**************************************************************
### Overview
This is the final project for CSPC 4970. The goal of this project was to practice interfacing with python objects using a GUI framework. It is an interface to manage imaginary curling leagues, built in PyQt5.

*************************************************************
### Functionality
Users can view and edit leagues, add/delete teams from those leagues, and add/delete members from those teams, or update information for a selected member, via a multi window display. 

Each object (teams, leagues, players) is edited in separate windows. To access detailed data for a specific object, it is necessary to select that object (league/team/player) and click on edit. Leagues can be accessed for edit from the league editor, or main window, teams can be accessed for edit from the league editor window, and players can be accessed for edit from the team editor window. 

Thus, it is not possible to search for a team or specific player from the main window, first that team's league, or player's team must be selected from the corresponding window and edit must be clicked. 

Users can also save league data, and load saved data to restore previously backed up data related to leagues, teams and players, by clicking on either the load or save option in the top bar menu in the main window of the application. 

Users can also import and export team data for a specific league, by first creating/selecting that league in the main window, clicking on edit, and then clicking on either the import or export button in the league editor window that pops up. Exported files will be sent to the exports folder in the application file directory. 


*************************************************************
### Getting Started
Create a new folder and download this project repository into that folder. Then create and activate a virtual environment where you can install the dependencies for the application. 

The fastest way to do this is to enter `pip install -r requirements.txt` in the command line once you've activated the virtual environment you will be using to run this application. 

Once you've installed dependencies for the project, you will need to open the **main.py** file in the root directory of the project, and **run the main method** _(this is the only method in the file)_. 

This will open the main window for the league manager. From there, you can add or load data, and access the windows for other league objects using instructions provided above in the functionality section.


*************************************************************
### Mock data
There is a CSV file in the tests folder, Teams.csv, which you can use to test the import functionality in the league editor window. 


*************************************************************
### Saving, Loading and Exporting
If you save league data, the file will be saved to the backups folder. If you export team data for a league, the export file will be exported to the exports folder.

A backup file with mock data is currently stored in the backups folder -> if you choose load from the main window, without having first saved any league data, this data will be loaded. 

There can only one backup data file, so if you save data for a set of leagues, it will overwrite whatever the last backup was. There is no limit on exported league information. 
