from models.league import League
from models.duplicate_oid import DuplicateOid
from models.team import Team
from models.team_member import TeamMember
import csv
import os
import pickle
import yagmail
import keyring


class LeagueDatabase:
    """docstring"""
    _sole_instance = None

    def __init__(self):
        self._leagues = []
        self._last_oid = 0

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        return_msg = ""
        if '.backup' not in file_name or not os.path.isfile(file_name):
            return_msg = "Invalid backup file selected. Loaded database from most recent saved backup."
            file_name = f"backups/{[file for file in os.listdir('./backups') if '.backup' in file][0]}"
        else:
            return_msg = "File successfully loaded."
        f = open(file_name, mode="rb")
        cls._sole_instance = pickle.load(f)
        f.close()
        return return_msg

    @property
    def leagues(self):
        return self._leagues

    @property
    def last_oid(self):
        return self._last_oid

    def add_league(self, league):
        if league not in self._leagues:
            self._leagues.append(league)

    def remove_league(self, league):
        try:
            for league_check in self._leagues:
                if league_check == league:
                    del self._leagues[self._leagues.index(league)]
                    return f"{league_check.name} successfully removed."
        except:
            return f"Error removing {league_check}"

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        if not file_name:
            return "Process aborted. Invalid file reference."
        file_name = f"backups/{file_name}.backup"
        for file in os.listdir('./backups'):
            if '.backup' in file and file != file_name:
                os.remove(f"./backups/{file}")
        if self.instance() is not None:
            f = open(file_name, mode="wb")
            pickle.dump(self.instance(), f)
            f.close()
            return "League successfully saved."
        else:
            return "Process aborted. No league data to save."

    def import_league_teams(self, league, file_name):
        if not file_name or not os.path.isfile(file_name):
            print("Process aborted. Invalid file reference provided.")
            return "Process aborted. Invalid file reference provided."
        elif type(league) != League:
            print("Process aborted. Invalid league object provided.")
            return "Process aborted. Invalid league object provided."
        try:
            with open(file_name, encoding='utf-8') as csvfile:
                league_data = csv.DictReader(csvfile)
                current_team = None
                # current_oid = 0
                for row in league_data:
                    if not current_team: # first team on list
                        current_team = Team(self.next_oid(), row['Team name'])
                        league.add_team(current_team)
                    elif current_team.name != row['Team name']:
                        current_team = Team(self.next_oid(), row['Team name'])
                        league.add_team(current_team)
                    current_team.add_member(TeamMember(self.next_oid(), row['Member name'], row['Member email']))
                    # current_oid += 1
                self.add_league(league)
                csvfile.close()
                return "Team data successfully imported."
        except Exception as e:
            if type(e) == DuplicateOid:
                return "Duplicate teams found in import file. Please include only new team data and try again."
            return "Error reading file. Please try again."

    def export_league_teams(self, league, file_name):
        if type(league) != League or league not in self.leagues:
            print("Process aborted. Invalid league object provided.")
            return "Process aborted. Invalid league object provided."
        try:
            file_name = "exports/" + file_name
            if ".csv" not in file_name: file_name += ".csv"
            with open(file_name, mode="w", encoding='utf-8', newline='') as csvfile:
                fieldnames = ['Team name', 'Member name', 'Member email']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for team in league.teams:
                    for member in team.members:
                        writer.writerow({fieldnames[0]: team.name, fieldnames[1]: member.name, fieldnames[2]: member.email})
                csvfile.close()
                return "League data successfully exported!"
        except:
            print("Process aborted. Error writing to file")
            return "Process aborted. Error writing to file"






