from models.identified_object import IdentifiedObject


class Competition(IdentifiedObject):
    """This class will represent competitions, which will have a location, date/time, as
    well as a list of teams competing. Each team in the team list will have members, who
    will effectively be who is participating in the competition"""

    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams_competing = teams
        self.date_time = datetime
        self.location = location

    def send_email(self, emailer, subject, message):
        email_recipients = []
        for team in self.teams_competing:
            [email_recipients.append(member) for member in team.members if member not in email_recipients]
        return emailer.send_plain_email([member.email for member in email_recipients], subject, message)
        

    @property
    def teams_competing(self):
        return self._teams_competing

    def __str__(self):
        date_time_str = f" on {self.date_time}" if self.date_time is not None else ""
        return f"Competition at {self.location}{date_time_str} with {self._teams_competing[0].name} and {self._teams_competing[1].name}"
    
