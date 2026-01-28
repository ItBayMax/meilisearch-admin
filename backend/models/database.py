"""
Database configuration and session management
"""
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from backend.utils.config import config


Base = declarative_base()


class Database:
    """Database manager for SQLAlchemy connections"""
    
    _instance = None
    _engine = None
    _session_factory = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._engine is None:
            self._init_engine()
    
    def _init_engine(self):
        """Initialize database engine"""
        db_config = config.database
        db_type = db_config.get("type", "sqlite")
        
        if db_type == "sqlite":
            db_path = db_config.get("path", "./data/meilisearch_admin.db")
            # Ensure directory exists
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            connection_string = f"sqlite:///{db_path}"
        elif db_type == "mysql":
            host = db_config.get("host", "localhost")
            port = db_config.get("port", 3306)
            username = db_config.get("username", "root")
            password = db_config.get("password", "")
            database = db_config.get("database", "meilisearch_admin")
            connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        pool_size = db_config.get("pool_size", 10)
        pool_recycle = db_config.get("pool_recycle", 3600)
        
        if db_type == "sqlite":
            self._engine = create_engine(
                connection_string,
                echo=config.app.get("debug", False),
            )
        else:
            self._engine = create_engine(
                connection_string,
                pool_size=pool_size,
                pool_recycle=pool_recycle,
                echo=config.app.get("debug", False),
            )
        
        self._session_factory = scoped_session(
            sessionmaker(bind=self._engine, autocommit=False, autoflush=False)
        )
    
    @property
    def engine(self):
        return self._engine
    
    @property
    def session(self):
        return self._session_factory()
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(self._engine)
    
    def close_session(self):
        """Close the current session"""
        self._session_factory.remove()


# Global database instance
db = Database()
