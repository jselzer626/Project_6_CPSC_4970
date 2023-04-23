from models.identified_object import IdentifiedObject
from models.duplicate_oid import DuplicateOid


class League(IdentifiedObject):
    """This class represents a League, which has a name, teams and competitions. 
    A team in the league doesn't have to participate in any competitions. 
    The team members on the teams in the league comprise those participating in the league."""

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        return self._teams
    
    @property
    def competitions(self):
        return self._competitions

    def add_team(self, team):
        if team not in self.teams:
            self._teams.append(team)
        else: 
            raise DuplicateOid(f"Cannot add {team.name}. There is already a team with ID #{team.oid} in {self.name}.", team.oid)
    
    def remove_team(self, team):
        if team in self.teams:
            for competition in self.competitions:
                if team in competition.teams_competing:
                    raise ValueError(f"Could not remove {team.name} from this league as they are still participating in competitions.")
            del self._teams[self._teams.index(team)]
            return f"{team.name} successfully removed from {self.name}."

    def team_named(self, team_name):
        for team in self.teams:
            if team.name == team_name:
                return team
    
    def add_competition(self, competition):
        if competition not in self.competitions:
            for team in competition.teams_competing:
                if team not in self.teams:
                    raise ValueError(f"Cannot add competition with {team.name} to {self.name} because {team.name} is not part of this league.")
            self._competitions.append(competition)
        else:
            raise DuplicateOid(f"Cannot add competition with ID #{competition.oid} because a competition in {self.name} already has that ID.", competition.oid)

    def teams_for_member(self, member):
        return [team for team in self._teams if member in team.members]
    
    def competitions_for_team(self, team):
        return [competition for competition in self.competitions if team in competition.teams_competing]

    def competitions_for_member(self, member):
        c_list = []
        for competition in self.competitions:
            for team in competition.teams_competing:
                   if member in team.members: 
                       c_list.append(competition)
        return c_list
    
    def __str__(self):
        team_list = "\n".join([str(team) for team in self.teams])
        team_sep = "\n" if len(team_list) > 0 else ""
        competition_list = [competition_1 for competition_1 in {str(competition) for competition in self.competitions}]
        competition_list.sort()
        competition_list = "\n".join(competition_list)
        comp_sep = "\n" if len(competition_list) > 0 else ""
        return f"{self.name}:{team_sep}{team_list}{comp_sep}{competition_list}"