"""
Developed by Ali Nehme
Date: 2023-04-14
"""

import mysql.connector
import uuid
from mysql.connector import Error
import re


def create_connection(host, username, password, database):
    """
    In this implementation, the mysql-connector-python library is used to connect to a MySQL database.
    This module requires that MySQL be installed with available database for connection.

    parameters:
        host: host to connect
        username: username to login
        password: user password
        database: database name

    returns:
        A connection to MySQL database, or None.

    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host, user=username, passwd=password, database=database
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


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
            self.connection = create_connection(host, username, password, database)
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
            return not re.match(r"^[ATCG]*[^ATCG]+[ATCG]*", sequence)
        else:
            print(f"'{sequence}' is not as string")
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
        # Check if sequence already exists in database
        if not self.valid_sequence(sequence):
            print(
                f"Error: Invalid Sequence; sequences should only include A, T, C and G"
            )
            return None

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

        # Search for sequences containing the sample sequence
        self.cursor.execute(
            "SELECT id FROM sequences WHERE sequence LIKE %s", ("%" + sample + "%",)
        )
        results = self.cursor.fetchall()
        return [str(result[0]) for result in results]

    def close_connection(self):
        self.connection.close()
