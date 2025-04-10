import configparser, os, sys, pandas as pd

from sqlalchemy.orm import sessionmaker
import sqlalchemy
# from model.models import Demographics, Waveforms, Leads, Base
import cx_Oracle, pyodbc, mysql.connector


class DBConnector:
    def __init__(self, sqlAlchemy=False, connectionType="Oracle"):
        try:
            config=self.readconfig()
            if sqlAlchemy:
                connection_string = self.createURLString(config, connectionType)
                engine = sqlalchemy.create_engine(connection_string)
                self.connection = self.startConnection_alchemy(engine)
            elif not sqlAlchemy:
                self.connection = self.createRawConnection(config, connectionType)

        except Exception as e:
            print("unable to create connection: ",str(e))
            raise e

    def readconfig(self):
        if getattr(sys, 'frozen', False):  # Check if running from a bundled executable
            base_dir = os.path.dirname(sys.executable)  # Directory of the exe
        else:
            base_dir = os.path.dirname(
                os.path.abspath(__file__))  # for current working directory in development mode

        # base_dir = os.getcwd()  # for current working directory in scientific mode

        config_path = os.path.join(base_dir, 'config', 'config.ini')
        config = configparser.ConfigParser()
        if os.path.exists(config_path):
            config.read(config_path)
        else:
            raise FileNotFoundError(f"Configuration file not found at {config_path}")
        return config

    def createURLString(self, config, database_type):
        dialect = config[database_type]["dialect"]  # e.g., oracle, mysql, postgresql
        driver = config[database_type]["driver"]  # e.g., cx_oracle, pymysql, psycopg2
        host = config[database_type]["host"]
        port = config[database_type]["port"]
        user = config[database_type]["user"]
        password = config[database_type]["password"]
        database = config[database_type]["database"]

        if database_type == "Oracle":
            connection_string = f"{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}"
        elif database_type == "MSSQL":
            connection_string = f"mssql+pyodbc://@{host}/{database}?integrated_security=true&driver={driver}"
        else:
            raise ValueError("Database type not supported: {database_type}")

        return connection_string

    def createRawConnection(self,config, database_type):
        driver = config[database_type]["driver"]  # e.g., cx_oracle, pymysql, psycopg2
        host = config[database_type]["host"]
        port = config[database_type]["port"]
        user = config[database_type]["user"]
        password = config[database_type]["password"]  # env set as password
        database = config[database_type]["database"]
        if database_type == "Oracle":
            oracle_client_path = r"C:\drivers\oracle\instantclient\instantclient_23_7"
            cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)
            dsn_tns = cx_Oracle.makedsn(host, port, database)
            return cx_Oracle.connect(user, password, dsn_tns)

        elif database_type == "MSSQL":
            return pyodbc.connect(
                f"DRIVER={driver};"
                f"SERVER={host};"
                f"DATABASE={database};"
                "Trusted_Connection=yes;"  # Use Windows Authentication
            )
        elif database_type == "MySQL":
            return mysql.connector.connect(
                host=host,  # Replace with your MySQL server host
                user=user,  # Replace with your MySQL username
                password=password,  # Replace with your MySQL password
                database=database
            )
        else:
            raise ValueError("Unsupported database type")

    def startConnection_alchemy(self, engine):
        try:
            Session = sessionmaker(bind=engine)
            Base.metadata.create_all(engine)
            session = Session()
            result = session.execute(sqlalchemy.text("SELECT SYSDATE FROM DUAL"))
            print("Current time:", result.fetchone()[0])
            return session
        except Exception as e:
            print("Database connection failed:", e)

    def getConnection(self):
        return self.connection