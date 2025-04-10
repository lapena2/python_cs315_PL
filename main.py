# import configparser, os, sys, pandas as pd
# from sqlalchemy.orm import sessionmaker
# import sqlalchemy
# # from model.models import Demographics, Waveforms, Leads, Base
# import cx_Oracle, pyodbc
import DBConnector, pandas as pd


def getSQLScript(fileLocation):
    with open(fileLocation, 'r') as file:
        return file.read()

def main():
    # Your main logic here
    conn = DBConnector.DBConnector(connectionType="MySQL").getConnection()
    cursor = conn.cursor()
    cursor.execute(getSQLScript('sql/query1.sql'))
    cols = [column[0] for column in cursor.description] #Extract column names
    data = cursor.fetchall()

    df = pd.DataFrame.from_records(data, columns=cols)

# Ensures main() runs only when this script is executed directly, not when imported
if __name__ == "__main__":
    main()