from models.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):
    """This class will represent a team member, who has a name and an email. 
    Team members will be part of teams, who will participate in competitions, both of which
    will be part of a League."""

    def __init__(self, oid, name, email):
        super().__init__(oid)
        self.name = name
        self.email = email

    def send_email(self, emailer, subject, message):
        return emailer.send_plain_email([self.email], subject, message)

    def __str__(self):
        return f"{self.name}<{self.email}>"
    

