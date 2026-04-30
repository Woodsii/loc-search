import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
PG_URL = os.getenv("PG_URL")

print('Creating search tables...')

engine = create_engine(PG_URL)

with open("search.sql", "r") as file:
    query = file.read()

with engine.connect() as conn:
    conn.execute(text(query))
    conn.commit()

print('Finished making search tables!')