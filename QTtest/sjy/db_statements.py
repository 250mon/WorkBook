CREATE_PATIENT_TABLE = """
    CREATE TABLE IF NOT EXISTS patients (
        id integer PRIMARY KEY,
        hospital_id integer NOT NULL,
        name text,
        gender_id integer
    );
"""

CREATE_GENDER_TABLE = """
    CREATE TABLE IF NOT EXISTS gender (
        id integer PRIMARY KEY,
        gender_name text,
        UNIQUE (gender_name)
    );
"""

CREATE_PATIENT_TIME_TABLE = """
    CREATE TABLE IF NOT EXISTS patient_time (
        id integer PRIMARY KEY,
        patient_id integer NOT NULL,
        gender_id integer NOT NULL,
        consult_time integer,
        date text,
        recording_file text,
        FOREIGN KEY (patient_id) REFERENCES patients(id),
        FOREIGN KEY (gender_id) REFERENCES gender(id)
    );
"""

GENDER_INSERT = """
   INSERT INTO gender VALUES(1, 'M');
   INSERT INTO gender VALUES(2, 'F');
"""