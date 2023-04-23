import datetime
import unittest

from module5.competition import Competition
from module5.team import Team
from module5.emailer import Emailer
from module5.team_member import TeamMember

class CompetitionTests2(unittest.TestCase):
    """First class of competition tested create. 
    Tests below will cover methods of superclass as well as str and email_send"""
    def test_equality_based_on_id_competition(self):
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "Here", now)
        c3 = Competition(1, [t1, t3], "Nowhere", None)

        #competitions are equal to themselves
        self.assertTrue(c1 == c1)
        self.assertTrue(c2 == c2)

        #competitions with different IDs are equal
        self.assertTrue(c1 == c3)

        #competitions with same location but different IDs are different
        self.assertTrue(t1 != t2)

    def test_hash_competition(self):
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "Here", now)
        c3 = Competition(1, [t1, t3], "Nowhere", None)

         # hash depends only on id
        self.assertTrue(hash(c1) == hash(c3))
        self.assertTrue(hash(c1) != hash(c2))

    @staticmethod
    def build_competitions():
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        tm3 = TeamMember(7, "h", "h")
        tm4 = TeamMember(8, "j", "j")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm3)
        t2.add_member(tm4)
        t3.add_member(tm3)
        t3.add_member(tm1)
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "Here", now)
        c3 = Competition(3, [t1, t3], "Over there", now)
        return [c1, c2, c3, now]

    def test_email_send_competition(self):
        test_competition_list = self.build_competitions()
        c1 = test_competition_list[0]
        c2 = test_competition_list[1]
        c3 = test_competition_list[2]
        fe = Emailer()
        
        # all team members receive emails
        c1.send_email(fe, "Title", "body of email")
        self.assertEqual(['f','g','h','j'], fe.recipients)
        self.assertEqual("Title", fe.subject)
        self.assertEqual("body of email", fe.message)
        
        # duplicate team members on competing teams are ignored
        c3.send_email(fe, "Important!", "Important information here")
        self.assertEqual(['f','g','h'], fe.recipients)
        self.assertEqual("Important!", fe.subject)
        self.assertEqual("Important information here", fe.message)

        # check that email list gets updated when member is added
        t1 = TeamMember(9, "k", "k")
        c1.teams_competing[1].add_member(t1)
        c1.send_email(fe, "Hurray!" , "Players added")
        self.assertEqual(['f', 'g', 'h', 'j', 'k'], fe.recipients)
        self.assertEqual("Hurray!", fe.subject)
        self.assertEqual("Players added", fe.message)
    
        # check that email list gets updated when member is removed
        t1 = c3.teams_competing[0].members[1]
        c3.teams_competing[0].remove_member(t1)
        c3.send_email(fe, "Warning!", "Players have quit")
        self.assertEqual(['f', 'h'], fe.recipients)
        self.assertEqual("Warning!", fe.subject)
        self.assertEqual("Players have quit", fe.message)

    def test_str_competition(self):
        test_competition_list = self.build_competitions()
        c1 = test_competition_list[0]
        c2 = test_competition_list[1]
        c3 = test_competition_list[2]
        now = test_competition_list[3]

        # check to see datetime is omitted is printed when no time is given
        self.assertNotEqual(f"Competition at Here on {now} with Team 1 and Team 2", str(c1))

        # check strings print as expected
        self.assertEqual("Competition at Here with Team 1 and Team 2", str(c1))
        self.assertEqual(f"Competition at Here on {now} with Team 2 and Team 3", str(c2))
        self.assertEqual(f"Competition at Over there on {now} with Team 1 and Team 3", str(c3))
        
    
if __name__ == '__main__':
    unittest.main()