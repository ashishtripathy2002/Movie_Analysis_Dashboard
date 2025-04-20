from sqlalchemy.engine import create_engine

class PostgresqlDB:
    _instance = None  # Class variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostgresqlDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, user_name, password, host, port, db_name):
        if not hasattr(self, "initialized"):  # Check if already initialized
            self.user_name = user_name
            self.password = password
            self.host = host
            self.port = port
            self.db_name = db_name
            self.engine = self.create_db_engine()
            self.initialized = True  # Mark as initialized to avoid re-running __init__

    def create_db_engine(self):
        try:
            db_uri = f'postgresql+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}'
            return create_engine(db_uri)
        except Exception as err:
            raise RuntimeError(f'Failed to establish connection -- {err}') from err

    def execute_dql_commands(self, stmt, values=None):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(stmt, values) if values else conn.execute(stmt)
            return result
        except Exception as err:
            print(f'Failed to execute DQL commands -- {err}')
            return None

    def execute_ddl_and_dml_commands(self, stmt, values=None):
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            result = connection.execute(stmt, values) if values else connection.execute(stmt)
            trans.commit()
            connection.close()
            return result
        except Exception as err:
            trans.rollback()
            print(f'Failed to execute DDL/DML commands -- {err}')
            return None
