import os
import sqlite3
from sqlite3 import Error
from db_statements import (
    CREATE_PATIENT_TABLE,
    CREATE_GENDER_TABLE,
    CREATE_PATIENT_TIME_TABLE,
    GENDER_INSERT
)
import logging
from typing import List


class DbMgr:
    def __init__(self, file_path):
        self.create_file(file_path)
        self.conn = None
        self.cursor = None
        self.create_conn()
        self.create_table()

    def create_file(self, file_path, times=None):
        fhandle = open(file_path, 'a')
        try:
            os.utime(file_path, times)
        finally:
            fhandle.close()

    def create_conn(self):
        try:
            self.conn = sqlite3.connect(self.file_path)
        except Error as e:
            logging.error(e)
        self.cursor = self.conn.cursor()

    def create_table(self):
        statements = [
            CREATE_PATIENT_TABLE,
            CREATE_GENDER_TABLE,
            CREATE_PATIENT_TIME_TABLE,
            GENDER_INSERT
        ]
        try:
            for statement in statements:
                self.cursor.execute(statement)
        except Error as e:
            logging.error(e)

    def query(self, q_statements: List[str]):
        try:
            self.cursor.execute(q_statements)
            self.cursor.fetchrow()
        except Error as e:
            logging.error(e)

    def clos(self):
        self.conn.close()


if __name__ == "__main__":
    db_mgr = DbMgr('clinic.db')
    db_mgr.insert_gender()
    db_mgr.close()
