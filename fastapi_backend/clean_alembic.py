from sqlalchemy import create_engine, inspect, text

DATABASE_URL = "postgresql+psycopg://postgres_user:123@localhost:5434/fastapi_backend_app"

engine = create_engine(DATABASE_URL)

#check all the tables in the database

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in the database:", tables)

# Check if the alembic_version table exists and drop it if it does

# with engine.connect() as conn:
#     # conn.execute(text("DELETE FROM alembic_version"))
#     conn.execute(text(""))
#     conn.commit()

print("alembic_version cleared")