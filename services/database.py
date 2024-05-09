import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

class MySQLSingleton:
    _instance = None

    def ensure_connection(self):
        try:
            self._connection.ping(reconnect=True, attempts=3, delay=5)  
        except mysql.connector.Error as err:
            self._connection = self._connect()  

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = cls._instance._connect(*args, **kwargs)
        return cls._instance

    def _connect(self, user, password, host, database,port):
        try:
            connection = mysql.connector.connect(user=user, password=password,
                                                  host=host, database=database,port=port)
            print("Connected to MySQL database")
            return connection
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access denied. Check your username and password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Error:", err)
            return None

    def disconnect(self):
        if self._connection:
            self._connection.close()
            print("Disconnected from MySQL database")
        else:
            print("Not connected to any database")

    def insert_temperature(self, value, date):
        try:
            cursor = self._connection.cursor()
            cursor.execute("INSERT INTO temperature (value, date) VALUES (%s, %s)", (value, date))
            self._connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error:", err)
            if err.errno == errorcode.CR_SERVER_LOST:
                 self.ensure_connection()
            else:
                 raise

    def insert_humidity(self, value, date):
        try:
            cursor = self._connection.cursor()
            cursor.execute("INSERT INTO humidity (value, date) VALUES (%s, %s)", (value, date))
            self._connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error:", err)
            if err.errno == errorcode.CR_SERVER_LOST:
                 self.ensure_connection()
            else:
                 raise

    def insert_gas(self, value, date):
        try:
            cursor = self._connection.cursor()
            cursor.execute("INSERT INTO gas (value, date) VALUES (%s, %s)", (value, date))
            self._connection.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Error:", err)
            if err.errno == errorcode.CR_SERVER_LOST:
                 self.ensure_connection()
            else:
                 raise
    
    def get_temperature_values(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT value, date FROM temperature")
            values = cursor.fetchall()
            cursor.close()
            result = []
            for row in values:
                result.append({
                    'value': row[0],
                    'date': row[1],  # Assuming the column name is 'value'
                    # Add other columns as needed
                })
            return result
        except mysql.connector.Error as err:
            print("Error:", err)
            if err.errno == errorcode.CR_SERVER_LOST:
                 self.ensure_connection()
            else:
                 raise
            return []

    def get_humidity_values(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT value, date FROM humidity")
            values = cursor.fetchall()
            cursor.close()
            result = []
            for row in values:
                result.append({
                    'value': row[0],
                    'date': row[1],  # Assuming the column name is 'value'
                    # Add other columns as needed
                })
            return result
        except mysql.connector.Error as err:
            print("Error:", err)
            if err.errno == errorcode.CR_SERVER_LOST:
                 self.ensure_connection()
            else:
                 raise
            return []

    def get_gas_values(self):
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT value, date FROM gas")
            values = cursor.fetchall()
            cursor.close()
            result = []
            for row in values:
                result.append({
                    'value': row[0],
                    'date': row[1],  # Assuming the column name is 'value'
                    # Add other columns as needed
                })
            return result
        except mysql.connector.Error as err:
            print("Error:", err)
            if err.errno == errorcode.CR_SERVER_LOST:
                 self.ensure_connection()
            else:
                 raise
            return []
        