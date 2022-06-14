from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



pg_engine = create_engine('postgresql://postgres:postgres@localhost:5438/postgres')
session = sessionmaker(bind=pg_engine)

# import pandas as pd


# pd.read_sql("select * from information_schema.tables where table_schema = 'public'", pg_engine)

# pd.read_sql('select * from test', pg_engine)
