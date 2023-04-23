import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from models.league_database import LeagueDatabase, League, Team, TeamMember
from models.duplicate_email import DuplicateEmail

Ui_MainWindow, QtBaseWindow = uic.loadUiType("ui_control/team_edit.ui")


def create_msg_box(title, text, icon=None):
    dialog = QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setText(text)
    if icon:
        if icon == "c":
            dialog.setIcon(QMessageBox.Critical)
        elif icon == "q":
            dialog.setIcon(QMessageBox.Question)
        elif icon == "i":
            dialog.setIcon(QMessageBox.Information)
        elif icon == "w":
            dialog.setIcon(QMessageBox.Warning)
    return dialog


class TeamEditDialog(QtBaseWindow, Ui_MainWindow):
    def __init__(self, team, league_db, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.team = team
        self.league_db = league_db
        self.edit_members_title.setText(f"Edit {team.name}")
        self.update_team_edit_ui()
        self.add_member_button.clicked.connect(self.add_member_clicked)
        self.delete_member_button.clicked.connect(self.delete_member_clicked)
        self.update_member_button.clicked.connect(self.update_member_clicked)

    def update_team_edit_ui(self):
        self.members_in_team.clear()
        self.member_to_add_name.clear()
        self.member_to_add_email.clear()
        for member in self.team.members:
            self.members_in_team.addItem(str(member))

    def delete_member_clicked(self):
        try:
            member_to_delete = self.members_in_team.selectedItems()[0].text().split("<")[0]
            confirm_delete_member = create_msg_box("Please Confirm",
                                                   f"Are you sure you want to delete {member_to_delete}?", "q")
            confirm_delete_member.addButton(QMessageBox.StandardButton.Yes)
            confirm_delete_member.addButton(QMessageBox.StandardButton.No)
            result = confirm_delete_member.exec()
            return_message = ""
            if result == QMessageBox.StandardButton.Yes:
                for member in self.team.members:
                    if member.name == member_to_delete:
                        return_message = self.team.remove_member(member)
                confirm_delete_member.close()
                self.update_team_edit_ui()
                member_delete_result = create_msg_box("Success!", return_message)
                member_delete_result.exec()
                if member_delete_result == QMessageBox.StandardButton.Ok:
                    member_delete_result.close()
            else:
                confirm_delete_member.close()
        except Exception as e:
            print(e)
            dialog = create_msg_box("Oops", "Either no available members to delete or no member selected", "c")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

    def add_member_clicked(self):
        try:
            if self.member_to_add_name.text() != "" and self.member_to_add_email.text() != "":
                member_to_add = TeamMember(self.league_db.next_oid(), self.member_to_add_name.text(),
                                           self.member_to_add_email.text())
                return_msg = self.team.add_member(member_to_add)
                self.update_team_edit_ui()
                dialog = create_msg_box("Success!", return_msg)
                result = dialog.exec()
                if result == QMessageBox.StandardButton.Ok:
                    dialog.close()
            else:
                raise ValueError
        except Exception as e:
            if type(e) == ValueError:
                error_msg = "Either name or email field is blank. Please enter data in both fields and try again."
            elif type(e) == DuplicateEmail:
                error_msg = "Member with that email already exists."
            else:
                error_msg = "Error adding member. Please try again"
            dialog = create_msg_box("Oops", error_msg, "c")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

    def update_member_clicked(self):
        try:
            member_to_update = self.members_in_team.selectedItems()[0].text()
            member_to_update = member_to_update.split("<")[0]
            if self.member_to_add_name.text() == "" and self.member_to_add_email.text() == "":
                raise ValueError
            member_obj = self.team.member_named(member_to_update)
            for member in self.team.members:
                if member.__eq__(member_obj):
                    if self.member_to_add_name.text() != "":
                        member.name = self.member_to_add_name.text()
                    if self.member_to_add_email.text() != "":
                        member.email = self.member_to_add_email.text()
            self.update_team_edit_ui()
            dialog = create_msg_box("Success!", f"{member.name} successfully updated!")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()
        except Exception as e:
            if type(e) == ValueError:
                error_msg = "Please enter a new name or a new email for the selected member"
            else:
                error_msg = "Either no available members to delete or no member selected"
            dialog = create_msg_box("Oops", error_msg, "c")
            result = dialog.exec()
            if result == QMessageBox.StandardButton.Ok:
                dialog.close()

