import mysql.connector
from mysql.connector import Error


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
        connection = mysql.connector.connect(host=host, user=username, passwd=password)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        connection.commit()
        connection.close()
        connection = mysql.connector.connect(
            host=host, user=username, passwd=password, database=database
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"Database Connection Error: '{e}'")

    return connection


def get_k_substrings(string: str, k: int = 2):
    """
    Gets the list of substrings with length k from a string

    Arguments:
        string: string to extract substrings from
        k: length of substrings

    return:
        set of unique substrings with length k
    """
    # Extract K length substrings using for loop
    if len(string) <= k:
        return string

    return set([string[i : i + k] for i in range(len(string) - k + 1)])
