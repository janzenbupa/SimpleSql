import pyodbc
import abc



class SqlConnect(object):
    
    __connection = None
    __cursor = None
    __server: str = None
    __database: str = None

    __metaclass__ = abc.ABCMeta

    def __init__(self, server: str, database: str):
        self.__connection = None
        self.__server = server
        self.__database = database

    def connect(self, server: str = None, database: str = None):
        # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
        self.__connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
        self.__cursor = self.__connection.cursor()
        


    def run_query(self, table: str):
        self.__cursor.execute(f'select * from {table}')
        row = self.__cursor.fetchall()
        return row
        

    @abc.abstractmethod
    def read_query(self):
        pass


    def execute_command(self, stored_procedure: str, parameters):

        command = f'exec {stored_procedure} '
        for i in range(0, len(parameters)):
            command += '?, '

        if len(parameters) > 0:
            command = command[:len(command) - 2]

        self.__cursor.execute(command, (parameters))
        row = self.__cursor.fetchall()

        self.__cursor.commit()
        return row


    def close_connection(self):
        self.__connection.close()
