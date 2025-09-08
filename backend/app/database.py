"""
Database configuration and connection setup
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://autosell_user:autosell_password@localhost:5432/autosell_mx"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=os.getenv("DEBUG", "false").lower() == "true"
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata for database operations
metadata = MetaData()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """
    Initialize database tables
    """
    try:
        # Import all models to ensure they are registered
        from .models import Vehicle, Photo, StatusHistory, SocialPost, MarketplaceListing
        from .models import User, ApiKey, AutomationWorkflow, WorkflowExecution
        from .models import AnalyticsData, MarketIntelligence
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def check_db_connection() -> bool:
    """
    Check if database connection is working
    """
    try:
        with engine.connect() as connection:
            from sqlalchemy import text
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def get_db_stats() -> dict:
    """
    Get database statistics
    """
    try:
        with engine.connect() as connection:
            from sqlalchemy import text
            # Get table counts
            result = connection.execute(text("""
                SELECT 
                    schemaname,
                    relname as tablename,
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes
                FROM pg_stat_user_tables 
                WHERE schemaname = 'public'
                ORDER BY relname
            """))
            
            stats = {}
            for row in result.fetchall():
                stats[row.tablename] = {
                    "inserts": row.inserts,
                    "updates": row.updates,
                    "deletes": row.deletes
                }
            
            return stats
            
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return {}

# Database health check
def health_check() -> dict:
    """
    Perform database health check
    """
    connection_ok = check_db_connection()
    
    if connection_ok:
        try:
            stats = get_db_stats()
            return {
                "status": "healthy",
                "connection": "ok",
                "tables": len(stats),
                "stats": stats
            }
        except Exception as e:
            return {
                "status": "degraded",
                "connection": "ok",
                "error": str(e)
            }
    else:
        return {
            "status": "unhealthy",
            "connection": "failed",
            "error": "Cannot connect to database"
        }
