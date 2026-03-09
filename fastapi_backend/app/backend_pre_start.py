import logging
from venv import logger
from sqlachemy import Engine
from sqlmodels import Session, select
from app.core.config import engine
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

logging.basicConfig(level=logging.INFO)
loggr = logging.getLogger(__name__)

max_retries = 5 * 60 # 5 minutes
wait_time = 1 # 1 second



@retry(
    stop=stop_after_attempt(max_retries), 
    wait=wait_fixed(wait_time),
    before=before_log(loggr, logging.INFO),
    after = after_log(loggr, logging.INFO)
)
def init_db_with_retry(
    engine: Engine
   ) -> None:
    retries = 0
    while retries < max_retries:
        try:
            with Session(engine) as session:
                session.execute(select(1))
            loggr.info("Database connection successful.")
            
        except Exception as e:
            loggr.warning(f"Database connection failed (attempt {retries + 1}/{max_retries}): {e}") 
            loggr.error("Could not connect to the database after multiple attempts.")
            raise ConnectionError("Failed to connect to the database.")

def main()->None:
    logger.info("Starting database initialization with retry mechanism...") 
    init_db_with_retry(engine)
    logger.info("Database initialization completed successfully.")


if __name__ == "__main__": 
    main()