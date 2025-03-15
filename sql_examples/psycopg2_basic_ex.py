import psycopg2
from psycopg2 import Error

password = input("Enter password: ")
try:
    # Connect to an existing database
    connection = psycopg2.connect(
        user="postgres",
        password=password,
        host="192.168.11.14",
        port="5433",
        database="danaul_inventory",
        connect_timeout=5,
    )

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT version();")
    # Fetch result
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

