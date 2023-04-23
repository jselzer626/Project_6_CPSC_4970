import unittest
from module5.team import Team
from module5.team_member import TeamMember
from module5.duplicate_oid import DuplicateOid
from module5.duplicate_email import DuplicateEmail


class TeamTests2(unittest.TestCase):
    """First class of team member tests tested create, add, remove, member_named and sends_email methods. 
    Tests below will cover methods of superclass as well as str"""

    def test_equality_based_on_id_team(self):
        t1 = Team(10, "Curl Jam")
        t2 = Team(15, "Curl Girls")
        t3 = Team(15, "Curl Jam")
        
        #teams are equal to themselves
        self.assertTrue(t1 == t1)
        self.assertTrue(t2 == t2)
        self.assertTrue(t3 == t3)

        #teams with different IDs are equal
        self.assertTrue(t2 == t3)

        #teams with same name but different IDs are different
        self.assertTrue(t1 != t3)

    def test_hash_team(self):
        t1 = Team(10, "Curl Jam")
        t2 = Team(15, "Curl Girls")
        t3 = Team(15, "Curl Jam")

         # hash depends only on id
        self.assertTrue(hash(t2) == hash(t3))
        self.assertTrue(hash(t1) != hash(t3))

    def test_str_team(self):
        t1 = Team(10, "Curl Jam")
        t2 = Team(15, "Curl Girls")
        t3 = Team(15, "Curl Time")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm1)

        self.assertEqual("Curl Jam: f<f>, g<g>", str(t1))
        self.assertEqual("Curl Girls: f<f>", str(t2))
        self.assertEqual("Curl Time: ", str(t3))

    def test_adding_duplicate_team_member_throws_exception(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        tm3 = TeamMember(5, "h", "h")
        tm4 = TeamMember(7, "j", "g")
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        t.add_member(tm2)
        self.assertIn(tm2, t.members)
        
        #test duplicate oid exception was raised and that member was not added 
        with self.assertRaises(DuplicateOid) as ex:
            t.add_member(tm3)
        self.assertEqual(5, ex.exception.oid)
        self.assertEqual(f"Cannot add {tm3.name}. Someone with that ID is already in {t.name}.", str(ex.exception))
        self.assertEqual(2, len(t.members))

        #test duplicate email exception was raised and that member was not added
        with self.assertRaises(DuplicateEmail) as ex:
            t.add_member(tm4)
        self.assertEqual('g', ex.exception.email)
        self.assertEqual(f"Cannot add {tm4.name}. Someone with email address <{ex.exception.email}> is already in {t.name}.", str(ex.exception))
        self.assertEqual(2, len(t.members))

        #test duplicate email exception was raised even if email has different casing, but is still the same
        tm5 = TeamMember(7, "j", "JjJJjJj")
        tm6 = TeamMember(8, "q", "jjjjjjj")
        t.add_member(tm5)
        with self.assertRaises(DuplicateEmail) as ex:
            t.add_member(tm6)
        self.assertEqual("jjjjjjj", ex.exception.email)
        self.assertEqual(f"Cannot add {tm6.name}. Someone with email address <{ex.exception.email}> is already in {t.name}.", str(ex.exception))
        self.assertEqual(3, len(t.members))

        #if member has duplicated oid and email, DuplicateOid exception should be raised first
        tm5 = TeamMember(6, "k", "g")
        with self.assertRaises(DuplicateOid) as ex:
            t.add_member(tm5)
        self.assertEqual(6, ex.exception.oid)
        self.assertEqual(f"Cannot add {tm5.name}. Someone with that ID is already in {t.name}.", str(ex.exception))
        self.assertEqual(3, len(t.members))

