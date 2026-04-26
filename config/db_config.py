# config/db_config.py
"""
DBConfig — Singleton database connection manager.
OOP Concept: Singleton Pattern (only one DB connection instance exists at a time)
"""

import mysql.connector
from mysql.connector import Error


class DBConfig:
    """
    Singleton class that manages the MySQL database connection.
    Ensures one connection object reused across the entire application.
    """

    _instance = None  # Class-level variable — Singleton pattern

    # ── Default XAMPP connection settings ──────────────────────────────────
    HOST     = "localhost"
    PORT     = 3306
    USER     = "root"
    PASSWORD = ""          # XAMPP default has no password
    DATABASE = "placetrack_pro"

    def __new__(cls):
        """Override __new__ to enforce Singleton: return existing instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        """Return an active MySQL connection, creating one if needed."""
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=self.HOST,
                    port=self.PORT,
                    user=self.USER,
                    password=self.PASSWORD,
                    database=self.DATABASE,
                    autocommit=False,
                    connection_timeout=10
                )
            except Error as e:
                raise ConnectionError(
                    f"❌ Cannot connect to MySQL.\n"
                    f"Please make sure XAMPP is running and the database exists.\n\n"
                    f"Technical detail: {e}"
                )
        return self._connection

    def execute_query(self, query: str, params: tuple = (), fetch: str = "none"):
        """
        Execute any SQL query safely.
        :param query:  SQL string with %s placeholders
        :param params: Tuple of parameter values
        :param fetch:  'one' | 'all' | 'none' (for INSERT/UPDATE/DELETE)
        :returns:      Row(s) for SELECT, lastrowid for INSERT, None otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Ensure params is always a tuple
            if params is None:
                params = ()
            elif not isinstance(params, tuple):
                params = tuple(params)

            print("SQL DEBUG:", query)
            print("PARAMS:", params)

            cursor.execute(query, params)

            if fetch == "one":
                return cursor.fetchone()
            elif fetch == "all":
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid

        except Error as e:
            conn.rollback()
            raise RuntimeError(f"Database error: {e}\nQuery: {query}")

        finally:
            cursor.close()

    def close(self):
        """Close the DB connection when the application exits."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None


# Convenience global instance
db = DBConfig()
