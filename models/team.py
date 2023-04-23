from models.identified_object import IdentifiedObject
from models.duplicate_oid import DuplicateOid
from models.duplicate_email import DuplicateEmail


class Team(IdentifiedObject):
    """This class represents teams that will compete in competitions.
    Teams will have a name as well as a list of members"""

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._members = []

    @property
    def members(self):
        return self._members
    
    def add_member(self, member):
        if member not in self.members:
            for member_check in self.members:
                #convert to caps for case insensitive comparision
                if member_check.email.upper() == member.email.upper():
                    raise DuplicateEmail(f"Cannot add {member.name}. Someone with email address <{member.email}> is already in {self.name}.", member.email)
            self.members.append(member)
            return f"{member.name} successfully added!"
        else: 
            raise DuplicateOid(f"Cannot add {member.name}. Someone with that ID is already in {self.name}.", member.oid)

    def member_named(self, s):
        for member in self.members:
            if member.name == s:
                return member
        
    def remove_member(self, member):
        for team_member in self.members:
            if member.__eq__(team_member):
                del self.members[self.members.index(member)]
                return f"{member.name} successfully deleted!"


    def send_email(self, emailer, subject, message):
        return emailer.send_plain_email([member.email for member in self.members if member.email is not None], subject, message)

    def __str__(self):
        member_list = ", ".join([str(member) for member in self.members])
        return f"{self.name}: {member_list}"
        
