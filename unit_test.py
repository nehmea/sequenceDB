import unittest
import mysql.connector
from methods.sequencedb import SequenceDB
import os
from dotenv import load_dotenv

load_dotenv()
host = os.getenv("host")
username = os.getenv("user")
password = os.getenv("password")


class TestSequenceDB(unittest.TestCase):
    def setUp(self):
        # Connect to the database
        self.seqdb = SequenceDB(
            host=os.getenv("host"),
            username=username,
            password=password,
            database="testdb",
            local_filename="test_sequenceDB_local.csv",
        )

    def test_insert_get_sequence(self):
        # Test storing a sequence
        sequence = "ACCCAGA"
        sample_id = self.seqdb.insert(sequence)
        self.assertIsNotNone(sample_id)

        # Test retrieving id if already exist
        sample_id_2 = self.seqdb.insert(sequence)
        self.assertEqual(sample_id_2, sample_id)

        # Test getting a sequence
        retrieved_sequence = self.seqdb.get(sample_id)
        self.assertEqual(sequence, retrieved_sequence)

    def test_find(self):
        # Add some sequences to the database
        id1 = self.seqdb.insert("ACCCAGA")
        id2 = self.seqdb.insert("GAATAACAA")
        id3 = self.seqdb.insert("TCCAAT")

        # Test find
        found_ids = self.seqdb.find("CC")
        self.assertTrue(id1 in found_ids)
        self.assertFalse(id2 in found_ids)
        self.assertTrue(id3 in found_ids)

    def test_overlap(self):
        # Add some sequences to the database
        id1 = self.seqdb.insert("ACCCAGA")
        id2 = self.seqdb.insert("GAATAACAA")
        id3 = self.seqdb.insert("TCCAAT")

        # Test overlaps
        self.assertTrue(self.seqdb.overlap("GAGA", id1))
        self.assertTrue(self.seqdb.overlap("GAGA", id2))
        self.assertFalse(self.seqdb.overlap("GAGA", id3))

    def tearDown(self):
        # Close the database connection
        self.seqdb.connection.close()

        # create new connection and delete the test database
        self.db = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
        )
        cursor = self.db.cursor()
        cursor.execute("DROP DATABASE testdb")
        self.db.close()

        import os

        if os.path.exists("test_sequenceDB_local.csv"):
            os.remove("test_sequenceDB_local.csv")


if __name__ == "__main__":
    unittest.main()
