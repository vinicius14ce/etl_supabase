import os
from dotenv import load_dotenv

load_dotenv()

host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT", 5432)
database = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")

host_web = os.environ.get("DBWEB_HOST")
port_web = os.environ.get("DBWEB_PORT", 5432)
database_web = os.environ.get("DBWEB_NAME")
user_web = os.environ.get("DBWEB_USER")
password_web = os.environ.get("DBWEB_PASSWORD")

class Env:
    """
    Classe para gerenciar variáveis de ambiente.
    """
    def __init__(self):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

        self.host_web = host_web
        self.port_web = port_web
        self.database_web = database_web
        self.user_web = user_web
        self.password_web = password_web
    def load_env(self):
        """
        Carrega as variáveis de ambiente do arquivo .env.
        """
        return {
            "host": self.host,
            "port": self.port,
            "database": self.database,
            "user": self.user,
            "password": self.password,
            "host_web": self.host_web,
            "port_web": self.port_web,
            "database_web": self.database_web,
            "user_web": self.user_web,
            "password_web": self.password_web
        }