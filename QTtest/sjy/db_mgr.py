import sqlite3
from sqlite3 import Error
import logging


class DbMgr:
    def __init__(self, file_path):
        self.file_path = file_path
        self.conn = None
        self.cursor = None
        self.create_conn()
        self.create_table()

    def create_conn(self):
        try:
            self.conn = sqlite3.connect(self.file_path)
        except Error as e:
            logging.error(e)
        self.cursor = self.conn.cursor()

    def create_table(self):
        sql_create_patient_table = """
            CREATE TABLE IF NOT EXISTS patients (
                id integer PRIMARY KEY,
                hospital_id integer NOT NULL,
                name text,
                gender_id integer
            )
        """

        sql_create_gender_table = """
            CREATE TABLE IF NOT EXISTS gender (
                id integer PRIMARY KEY,
                gender_name text,
                UNIQUE (gender_name)
            )
        """

        sql_create_patient_time_table = """
            CREATE TABLE IF NOT EXISTS patient_time (
                id integer PRIMARY KEY,
                patient_id integer NOT NULL,
                gender_id integer NOT NULL,
                consult_time integer,
                date text,
                recording_file text,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (gender_id) REFERENCES gender(id)
            )
        """

        try:
            self.cursor.execute(sql_create_patient_table)
            self.cursor.execute(sql_create_gender_table)
            self.cursor.execute(sql_create_patient_time_table)
        except Error as e:
            logging.error(e)

    def insert_gender(self):
        try:
            sql = ''' INSERT INTO gender (gender_name) VALUES(?) '''
            for g in ["M", "F"]:
                self.cursor.execute(sql, g)
            self.conn.commit()
        except Error as e:
            logging.error(e)


if __name__ == "__main__":
    db_mgr = DbMgr('clinic.db')
    db_mgr.insert_gender()
