"""
Developed by Ali Nehme
Date: 2023-04-14
"""

import uuid
from mysql.connector import Error
from methods import helpers


class SequenceDb:
    def __init__(self, host: str, username: str, password: str, database: str):
        """
        Connects to a specific
        The __init__ method creates a connection to the database and a "sequences" table if it does not already exist.

        parameters:
            host, username, password, database: used as arguments for to create a connection using create_connection() method.

        returns:
            None. It creates a connection attribute in Class SequenceDb.
        """
        try:
            self.connection = helpers.create_connection(
                host, username, password, database
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS sequences (id VARCHAR(36) NOT NULL PRIMARY KEY, sequence TEXT NOT NULL UNIQUE)"
            )
            self.connection.commit()
        except Error as e:
            print(f"{e}")

    @staticmethod
    def valid_sequence(sequence: str):
        """
        checks if the sequence is a valid DNA sequence that only include A,T,C or G.
        """
        if isinstance(sequence, str):
            return set(sequence).issubset({"A", "C", "G", "T"})
        else:
            print(f"'{sequence}' is not a string")
            return False

    def insert(self, sequence: str):
        """
        The insert method checks if the sequence already exists in the database and returns its unique identifier if it does.
        If the sequence does not exist in the database, a new unique identifier is generated using the uuid library,
        and the sequence is inserted into the database.

        parameters:
            sequence: a string containing the DNA sequence.

        returns:
            sequence_id: string uuid.
        """
        # check if sequence is valid
        if not self.valid_sequence(sequence):
            print(
                f"Error: Invalid Sequence; sequences should only include A, T, C and G"
            )
            return None

        # Check if sequence already exists in database
        self.cursor.execute("SELECT id FROM sequences WHERE sequence = %s", (sequence,))
        result = self.cursor.fetchone()
        if result:
            print(f"Sequence already exist in the DB")
            return str(result[0])
        else:
            # Generate a unique identifier for the sequence
            sequence_id = str(uuid.uuid4())
            # Insert sequence into database
            self.cursor.execute(
                "INSERT INTO sequences (id, sequence) VALUES (%s, %s)",
                (sequence_id, sequence),
            )
            self.connection.commit()
            return sequence_id

    def bulk_insert(self, sequence_list: list):
        """
        inserts multiple sequences if they don't exist in the DB.
        implements the insert method

        parameters:
            sequence_list: kist of DNA sequences

        returns:
            dictionary: key = sequence; value = id
        """
        if len(sequence_list) == 0:
            print(f"Error: list is empty")
            return None

        id_list = dict()
        for sequence in sequence_list:
            id_list[sequence] = self.insert(sequence)
        return id_list

    def get(self, sequence_id):
        """
        The get method retrieves a sequence from the database by its unique identifier.

        parameters:
            sequence_id: uuid of the sequence to be retrieved.

        returns:
            sequence (string) or None.
        """
        # Retrieve sequence from database by its unique identifier
        self.cursor.execute(
            "SELECT sequence FROM sequences WHERE id = %s", (sequence_id,)
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def find(self, sample):
        """
        The find method searches for sequences containing a specified sample sequence using the LIKE operator in SQL.

        parameters:
            sample: sample sequence to find in the sequences in the database.

        returns:
            list of sequences or empty list.
        """
        # check if the sequence is valid
        if not self.valid_sequence(sample):
            print(
                f"Error: Invalid Sequence; sequences should only include A, T, C and G"
            )
            return []

        # Search for sequences containing the sample sequence
        self.cursor.execute(
            "SELECT id FROM sequences WHERE sequence LIKE %s", ("%" + sample + "%",)
        )
        results = self.cursor.fetchall()
        return [str(result[0]) for result in results]

    def overlap(self, sample, sequence_id):
        """
        This method first checks if the sample and sequence are exact matches, or if one is contained within the other.
        If not, it checks for partial overlaps by comparing substrings of the sequence to the sample.
        If a partial overlap is found, the method returns True. If no overlap is found, it returns False.
        """
        # check if the sample is valid
        if not self.valid_sequence(sample):
            print(
                f"Error: Invalid Sequence; sequences should only include A, T, C and G"
            )
            return False

        db_sequence = self.get(sequence_id)
        if not db_sequence:
            print(f"sequence with id '{sequence_id}' does not exist in DB")
            return False

        # check if they are the same sequence
        if sample == db_sequence:
            return True

        # check if one sequence is a subset of the other one
        if sample in db_sequence or db_sequence in sample:
            return True

        # Get all subsequences of length >= 2 for both sample and DB sequence
        sample_subsequences = helpers.get_k_substrings(sample, 2)
        sequence_subsequences = helpers.get_k_substrings(db_sequence, 2)

        # Check if there is any overlap between the two sets of substrings
        if sample_subsequences.intersection(sequence_subsequences):
            return True
        else:
            return False

    def close_connection(self):
        self.connection.close()
