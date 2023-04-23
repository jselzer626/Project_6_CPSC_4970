import sys
import os

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog, QInputDialog
from models.league_database import LeagueDatabase, League, Team, TeamMember
from ui_control.team_edit import TeamEditDialog, create_msg_box

Ui_MainWindow, QtBaseWindow = uic.loadUiType("ui_control/league_edit.ui")


class LeagueEditDialog(QtBaseWindow, Ui_MainWindow):
    def __init__(self, league_db, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.league_selected = league
        self.league_db = league_db
        self.edit_team_title.setText(f"Edit {league.name}")
        self.update_league_edit_ui()
        self.edit_team_button.clicked.connect(self.edit_team_clicked)
        self.delete_team_button.clicked.connect(self.delete_team_clicked)
        self.add_team_button.clicked.connect(self.add_team_clicked)
        self.import_team_button.clicked.connect(self.import_team_clicked)
        self.export_team_button.clicked.connect(self.export_team_clicked)

    def import_team_clicked(self):
        dialog = QFileDialog(self, 'Select File to Import', os.getcwd(), 'All Files(*.*)')
        if dialog.exec():
            selected_file = dialog.selectedFiles()[0]
            try:
                return_msg = self.league_db.import_league_teams(self.league_selected, selected_file)
                self.update_league_edit_ui()
                icon = "w" if return_msg != "Team data successfully imported." else "i"
            except:
                return_msg = "Process aborted. Error reading file."
                icon = None
            result_dialog = create_msg_box("Import Result", return_msg, icon)
            if result_dialog.exec() == QMessageBox.StandardButton.Ok:
                result_dialog.close()

    def export_team_clicked(self):
        export_dialog = create_msg_box(f"Confirm Export",
                                       f"Are you sure you want to export data for {self.league_selected.name}?",
                                       "i")
        export_dialog.addButton(QMessageBox.StandardButton.Cancel)
        export_dialog.addButton(QMessageBox.StandardButton.Yes)
        try:
            if export_dialog.exec() == QMessageBox.StandardButton.Yes:
                return_msg = self.league_db.export_league_teams(self.league_selected,
                                                                f"{self.league_selected.name}_data")
                icon = "i" if return_msg == "League data successfully exported!" else "w"
                export_result = create_msg_box("Export Result", return_msg, icon)
                if export_result.exec() == QMessageBox.StandardButton.Ok:
                    export_result.close()
        except:
            export_result = create_msg_box("Export Error", "Operation could not be completed.", "c")
            if export_result.exec() == QMessageBox.StandardButton.Ok:
                export_result.close()


    def edit_team_clicked(self):
        try:
            team_edit_name = self.teams_in_league.selectedItems()[0].text()
            team_obj = None
            for team in self.league_selected.teams:
                if team.name == team_edit_name:
                    team_obj = team
            team_edit = TeamEditDialog(team_obj, self.league_db)
            if team_edit.exec() == QDialog.DialogCode.Rejected:
                team_edit.close()
        except:
            dialog = create_msg_box("Oops!", "Either no available teams to edit or no team selected", "c")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

    def add_team_clicked(self):
        if self.team_to_add.text() != "":
            team_to_add = Team(self.league_db.next_oid(), self.team_to_add.text())
            self.league_selected.add_team(team_to_add)
            self.update_league_edit_ui()
        else:
            dialog = create_msg_box("Oops!", "Please enter a value in the team name field")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

    def delete_team_clicked(self):
        try:
            team_to_delete = self.teams_in_league.selectedItems()[0].text()
            confirm_delete_team = create_msg_box("Please Confirm", f"Are you sure you want to delete {team_to_delete}?", "q")
            confirm_delete_team.addButton(QMessageBox.StandardButton.Yes)
            confirm_delete_team.addButton(QMessageBox.StandardButton.No)
            result = confirm_delete_team.exec()
            return_message = ""
            if result == QMessageBox.StandardButton.Yes:
                for team in self.league_selected.teams:
                    if team.name == team_to_delete:
                        team_obj = self.league_selected.team_named(team.name)
                        return_message = self.league_selected.remove_team(team_obj)
                confirm_delete_team.close()
                self.update_league_edit_ui()
                team_delete_result = create_msg_box("Success!", return_message)
                team_delete_result.exec()
                if team_delete_result == QMessageBox.StandardButton.Ok:
                    team_delete_result.close()
            else:
                confirm_delete_team.close()
        except Exception as e:
            if type(e) == ValueError:
                error_msg = "Cannot delete selected team because they are still participating in competitions."
            else:
                error_msg = "Either no available teams to delete or no league selected"
            dialog = create_msg_box("Oops", error_msg, "c")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

    def update_league_edit_ui(self):
        self.teams_in_league.clear()
        self.team_to_add.clear()
        for team in self.league_selected.teams:
            self.teams_in_league.addItem(team.name)

