import sqlite3
from sqlite3 import Error
import logging


class DbMgr:
    def __init__(self, file_path):
        self.file_path = file_path
        self.conn = None
        self.cursor = None

    def create_conn(self):
        try:
            self.conn = sqlite3.connect(self.file_path)
        except Error as e:
            logging.error(e)
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql_create_patient_table = """
            CREATE TABLE IN NOT EXISTS patients (
                id integer PRIMARY KEY,
                hospital_id integer NOT NULL,
                name text,
                gender_id integer
            )
        """

        sql_create_gender_table = """
            CREATE TABLE IN NOT EXISTS gender (
                id integer PRIMARY KEY,
                gender_name text
            )
        """

        sql_create_patient_time_table = """
            CREATE TABLE IN NOT EXISTS patient_time (
                id integer PRIMARY KEY,
                patient_id integer NOT NULL,
                gender_id integer NOT NULL,
                consult_time integer,
                date text,
                recording_file text
                FOREIGN KEY (gender_id) REFERENCES gender (id),
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        """

        try:
            self.cursor.execute(sql_create_patient_time_table)
        except Error as e:
            logging.error(e)

    def insert_gender(self):
        sql = ''' INSERT INTO gender (gender_name) VALUES(?,?,?) '''
        for g in ["M", "F"]:
            self.cursor.execute(sql, g)
        self.cursor.commit()


if __name__ == "__main__":
    db_mgr = DbMgr()