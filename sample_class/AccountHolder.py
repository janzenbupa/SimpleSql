from sql_connect import SqlConnect
from pyodbc import Row
from typing import List



class AccountHolder(SqlConnect):

    Id: int
    FirstName: str
    LastName: str
    Pin :str
    ZipCode: str

    def __init__(self, id = 0, first_name = None, last_name = None, pin = None, zip_code = None):
        self.Id = id
        self.FirstName = first_name
        self.LastName = last_name
        self.Pin = pin
        self.ZipCode = zip_code

    def read_query(self, row: Row) -> list():
        data = []
        for r in row:
            account_holder = AccountHolder(r[0], r[1], r[2], r[3], r[4])
            data.append(account_holder)

        return data
        
    def connect(self, server: str, database: str):
        super().connect(server, database)

    def execute_command(self, stored_procedure: str, parameters: List[str]):
        row = super().execute_command(stored_procedure, parameters)
        for i in row:
            return i[0]