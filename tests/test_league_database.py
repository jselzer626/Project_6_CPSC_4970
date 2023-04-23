import csv
import unittest
import os
import yagmail
from test_league import LeagueTests
from models.league_database import LeagueDatabase
from models.league import League
from models.emailer import Emailer
from models.competition import Competition


class LeagueDatabaseTests(unittest.TestCase):
    """to test functionality of singleton class LeagueDatabase"""
    def test_create(self):
        ld1 = LeagueDatabase()
        self.assertEqual([], ld1.leagues)
        self.assertEqual(0, ld1.last_oid)
        self.assertTrue(isinstance(ld1, LeagueDatabase))

    def test_add_remove_league(self):
        ld1 = LeagueDatabase()
        l1 = LeagueTests.build_league()
        l2 = League(2, "League 2")
        # league list should be empty after object creation
        self.assertEqual([], ld1.leagues)
        ld1.add_league(l1)
        ld1.add_league(l2)
        self.assertEqual([l1, l2], ld1.leagues)
        ld1.remove_league(l2)
        self.assertEqual([l1], ld1.leagues)

    def test_load_valid_backup_reference(self):
        ld1 = LeagueDatabase.instance()
        l1 = LeagueTests.build_league()
        l2 = League(10, "other league")
        ld1.add_league(l1)
        ld1.add_league(l2)
        ld1.save("test")
        ld1.remove_league(l1)
        ld1.remove_league(l2)
        # real file containing backup
        LeagueDatabase.load("test_backup")
        ld2 = LeagueDatabase.instance()
        # Both LD objects should be different instances
        self.assertNotEqual(ld1, ld2)
        # second LD object should have the league that was removed from the first
        self.assertNotIn(l1, ld1.leagues)
        self.assertNotIn(l2, ld1.leagues)
        self.assertIn(l1, ld2.leagues)
        self.assertIn(l2, ld2.leagues)

    def test_load_invalid_backup_reference(self):
        ld1 = LeagueDatabase.instance()
        l1 = LeagueTests.build_league()
        l2 = League(10, "other league")
        ld1.add_league(l1)
        ld1.add_league(l2)
        ld1.save("test")
        ld1.remove_league(l1)
        ld1.remove_league(l2)
        # fake backup file reference - should load stored backup
        LeagueDatabase.load("fake_file_name")
        ld2 = LeagueDatabase.instance()
        # Both LD objects should be different instances
        self.assertNotEqual(ld1, ld2)
        # second LD object should have the league that was removed from the first
        self.assertNotIn(l1, ld1.leagues)
        self.assertNotIn(l2, ld1.leagues)
        self.assertIn(l1, ld2.leagues)
        self.assertIn(l2, ld2.leagues)

    def test_import_league_teams(self):
        ld1 = LeagueDatabase.instance()
        l1 = League(100, "Awesome League")
        ld1.import_league_teams(l1, 'Teams.csv')
        self.assertEqual(1, len(ld1.leagues))
        # if object other than league is provided
        error_msg = "Process aborted. Invalid league object provided."
        self.assertEqual(error_msg, ld1.import_league_teams("fake_league", 'Teams.csv'))
        # if nonexistent file is provided
        error_msg = "Process aborted. Invalid file reference provided."
        self.assertEqual(error_msg, ld1.import_league_teams(l1, 'fake.csv'))
        # if file of incorrect format is provided
        error_msg = "Error reading file. Please try again."
        self.assertEqual(error_msg, ld1.import_league_teams(l1, 'invalid_input.txt'))

    def test_export_league_teams(self):
        l1 = LeagueTests.build_league()
        ld1 = LeagueDatabase.instance()
        ld1.add_league(l1)
        # test normal
        ld1.export_league_teams(l1, "test_export")
        self.assertTrue(os.path.isfile("exports/test_export.csv"))
        f = open('exports/test_export.csv', mode="r")
        csv_reader = csv.DictReader(f)
        # confirm header names
        self.assertEqual(['Team name', 'Member name', 'Member email'], csv_reader.fieldnames)
        test_names = [row['Member name'] for row in csv_reader]
        f.seek(0)   # return to just below header line
        test_emails = [row['Member email'] for row in csv_reader]
        self.assertEqual('Betty', test_names[3])
        self.assertEqual('dino', test_emails[7])
        f.close()
        os.remove("exports/test_export.csv")
        # test with incorrect object parameter
        error_msg = "Process aborted. Invalid league object provided."
        self.assertEqual(error_msg, ld1.export_league_teams(ld1, "test_export_2"))

    def test_import_and_export(self):
        ld1 = LeagueDatabase.instance()
        l1 = League(100, "Awesome League")
        ld1.import_league_teams(l1, 'Teams.csv')
        self.assertEqual(1, len(ld1.leagues))
        ld1.export_league_teams(l1, "test_export")
        self.assertTrue(os.path.isfile("exports/test_export.csv"))
        f = open('exports/test_export.csv', encoding='utf-8', mode="r")
        csv_reader = csv.DictReader(f)
        test_teams = {row['Team name'] for row in csv_reader}
        self.assertEqual({team.name for team in l1.teams}, test_teams)
        f.close()
        os.remove('exports/test_export.csv')

    def test_email_send(self):
        e1 = Emailer()
        single_recip = 'testAuburnModule5@gmail.com'
        multiple_recip = ['fred@curlingleague.awsapps.com', 'wilma@curlingleague.awsapps.com',
                          'barney@curlingleague.awsapps.com', 'betty@curlingleague.awsapps.com',
                          'pebbles@curlingleague.awsapps.com', 'bamm-bamm@curlingleague.awsapps.com']
        error_address = 'fake@mistake_domain.error'
        test_subject = "This is a test!"
        test_body = "Testing testing testing 123."
        # test valid email addresses
        self.assertEqual("Success - process complete.", e1.send_plain_email(single_recip, test_subject, test_body))
        self.assertEqual("Success - process complete.", e1.send_plain_email(multiple_recip, test_subject, test_body))
        self.assertEqual("Error - send not successful.", e1.send_plain_email(error_address, test_subject, test_body))

    def test_league_team_email_send(self):
        e1 = Emailer()
        ld1 = LeagueDatabase.instance()
        l1 = League(100, "Flintstones League")
        ld1.import_league_teams(l1, 'email_test_teams.csv')
        t1 = ld1.leagues[0].teams[0]
        t2 = ld1.leagues[0].teams[1]
        c1 = Competition(10, [t1, t2], 'Somewhere', None)
        ld1.leagues[0].add_competition(c1)
        # confirm competition was created
        self.assertTrue(1, len(ld1.leagues[0].competitions))
        test_subject = "This is a test!"
        test_body = "Testing testing testing 123."
        # competition email method
        self.assertEqual("Success - process complete.", c1.send_email(e1, test_subject, test_body))
        # team email method
        self.assertEqual("Success - process complete.", t1.send_email(e1, test_subject, test_body))







