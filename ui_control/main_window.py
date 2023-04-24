import sys
import os

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QFileDialog, QInputDialog, QLineEdit
from models.league_database import LeagueDatabase, League, Team, TeamMember
from ui_control.league_edit import LeagueEditDialog, create_msg_box


Ui_MainWindow, QtBaseWindow = uic.loadUiType("ui_control/main_window.ui")

class MainWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.league_db = LeagueDatabase.instance()
        self.setupUi(self)
        self.add_league_button.clicked.connect(self.add_league_clicked)
        self.delete_league_button.clicked.connect(self.delete_league_clicked)
        self.edit_league_button.clicked.connect(self.edit_league_clicked)
        self.action_load.triggered.connect(self.action_load_triggered)
        self.action_save.triggered.connect(self.action_save_triggered)

    def action_load_triggered(self):
        dialog = QFileDialog(self, 'Select File to Load', os.getcwd(), 'All Files(*.*)')
        if dialog.exec():
            selected_file = dialog.selectedFiles()[0]
            try:
                return_msg = self.league_db.load(selected_file)
                self.league_db = LeagueDatabase.instance()
                self.update_ui()
            except Exception as e:
                print(e)
                return_msg = "Error reading file. Process aborted"
            icon = "i" if return_msg == "League database successfully loaded." else "w"
            result_dialog = create_msg_box("Loading Result", return_msg, icon)
            if result_dialog.exec() == QMessageBox.StandardButton.Ok:
                result_dialog.close()

    def action_save_triggered(self):
        file_name, ok = QInputDialog().getText(self, "Save League Database",
                                                "Enter file name where league data will be saved:", QLineEdit.Normal)
        if file_name and ok:
            return_msg = self.league_db.save(file_name)
            icon = "i" if return_msg == "League successfully saved." else "w"
            result_dialog = create_msg_box("Save Result", return_msg, icon)
            if result_dialog.exec() == QMessageBox.StandardButton.Ok:
                result_dialog.close()


    def add_league_clicked(self):
        return_msg = "Please enter a value in the name field"
        icon = "i"
        bx_title = "Success!"
        if self.new_league_name_input.text() != "":
            league_to_add = League(self.league_db.next_oid(), self.new_league_name_input.text())
            self.league_db.add_league(league_to_add)
            self.update_ui()
            return_msg = f"{league_to_add.name} successfully added!"
        else:
            bx_title = "Oops"
            icon = "w"
        result = create_msg_box(bx_title, return_msg, icon)
        if result.exec() == QMessageBox.StandardButton.Ok:
            result.close()


    def edit_league_clicked(self):
        try:
            league_edit_name = self.main_league_list.selectedItems()[0].text()
            league_obj = None
            for league in self.league_db.leagues:
                if league.name == league_edit_name:
                    league_obj = league
            league_edit = LeagueEditDialog(self.league_db, league_obj)
            if league_edit.exec() == QDialog.DialogCode.Rejected:
                league_edit.close()
        except Exception as e:
            print(e)
            dialog = QMessageBox()
            dialog.setWindowTitle("Oops!")
            dialog.setIcon(QMessageBox.Critical)
            dialog.setText("Either no available leagues to edit or no league selected")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

    def delete_league_clicked(self):
        try:
            league_to_delete = self.main_league_list.selectedItems()[0].text()
            confirm_delete = create_msg_box("Please Confirm",
                                            f"Are you sure you want to delete {league_to_delete}?", "q")
            confirm_delete.addButton(QMessageBox.StandardButton.Yes)
            confirm_delete.addButton(QMessageBox.StandardButton.No)
            return_message = ""
            if confirm_delete.exec() == QMessageBox.StandardButton.Yes:
                for league in self.league_db.leagues:
                    if league.name == league_to_delete:
                        return_message = self.league_db.remove_league(league)
                confirm_delete.close()
                self.update_ui()
                delete_result = create_msg_box("Success!", return_message)
                if delete_result.exec() == QMessageBox.StandardButton.Ok:
                    delete_result.close()
            else:
                confirm_delete.close()
        except:
            dialog = create_msg_box("Oops!", "Either no available leagues to delete or no league selected", "c")
            if dialog.exec() == QMessageBox.StandardButton.Ok:
                dialog.close()

    def update_ui(self):
        self.main_league_list.clear()
        self.new_league_name_input.clear()
        for league in self.league_db.leagues:
            self.main_league_list.addItem(league.name)


