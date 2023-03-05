import pyodbc
import abc



class SqlConnect(object):
    
    connection = None
    cursor = None
    server: str = None
    database: str = None

    __metaclass__ = abc.ABCMeta

    def __init__(self, server: str, database: str):
        self.connection = None
        self.server = server
        self.database = database

    def connect(self, server: str = None, database: str = None):
        # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        self.cursor = self.connection.cursor()
        


    def run_query(self, table: str):
        self.cursor.execute(f'select * from {table}')
        row = self.cursor.fetchall()
        return row
        

    @abc.abstractmethod
    def read_query(self):
        return


    def execute_command(self, stored_procedure: str, parameters):

        com = f'exec {stored_procedure} '
        for i in range(0, len(parameters)):
            com += '?, '

        if len(parameters) > 0:
            com = com[:len(com) - 2]

        self.cursor.execute(com, (parameters))
        row = self.cursor.fetchall()

        self.cursor.commit()
        return row


    def close_connection(self):
        self.connection.close()
