import os
from supabase import create_client, Client
from postgrest import APIError
from dotenv import load_dotenv
from typing import Generator, Optional
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy import URL, text
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

URI = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_SECRET_KEY")

class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.client = create_client(url, key)

    def get_client(self) -> Client:
        return self.client

    def test_connection(self) -> bool:
        try:
            self.client.schema('public').table("test").select("*").execute()
            return print(self.client.schema('public').table("test").select("*").execute())
        except APIError as e:
            print(f"Connection test failed: {e}")
            return False

test = SupabaseClient(URI, KEY)
test.test_connection()  

class Conn:
    """
    Classe modularizada para gerenciamento de conexões com banco de dados via SQLAlchemy.
    """
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int = 5432,
        database: str = "postgres",
        schema: Optional[str] = None,
        dialect: str = "postgresql",
        driver: Optional[str] = "psycopg2",       
        echo: bool = False,
        sql_query: str = 'SELECT 1'
    ):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.schema = schema
        self.dialect = dialect
        self.driver = driver
        self.echo = echo
        self.sql_query = sql_query
        
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None

    @property # Decorator para tornar a função um dado derivado da classe e não um método. 
    def url(self) -> str:
        driver_name = f"{self.dialect}+{self.driver}" if self.driver else self.dialect
        query_params = {}
        if self.schema:
            # Seta o search_path padrão no PostgreSQL
            query_params["options"] = f"-c search_path={self.schema}"

        url_obj = URL.create(
            drivername=driver_name,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
            query=query_params if query_params else None
        )
        return url_obj.render_as_string(hide_password=False)
   

    def get_engine(self) -> Engine:
        """Cria ou retorna a instância singleton da Engine (Pool de conexões)."""
        if self._engine is None:
            self._engine = create_engine(
                self.url,
                echo=self.echo,
                pool_pre_ping=True,  # Verifica se a conexão ainda está viva antes de usar
                pool_size=10,         # Tamanho do pool de conexões
                max_overflow=20      # Conexões extras permitidas em picos
            )
        return self._engine

    def get_session(self) -> Session:
        """Cria uma nova sessão síncrona com o banco."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.get_engine(),
                autocommit=False,
                autoflush=False
            )
        return self._session_factory()

    def get_db_session(self) -> Generator[Session, None, None]:
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def query_text(self, query: Optional[str] = None, params: Optional[dict] = None): 
        query = query or self.sql_query
        with self.get_engine().connect() as connection:
            result = connection.execute(text(query), params or {})
            return result.fetchall()

        