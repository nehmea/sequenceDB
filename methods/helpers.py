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
        connection = mysql.connector.connect(
            host=host, user=username, passwd=password, database=database
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def get_k_substrings(string: str, k: int = 2, with_repition=False):
    # Extract K length substrings using for loop
    if len(string) <= k:
        return string

    res = [string[i : i + k] for i in range(len(string) - k + 1)]
    if with_repition:
        return res
    else:
        return set(res)
