import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Date, MetaData, Table

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/procedure_db")
engine = create_engine(DATABASE_URL, echo=True)
metadata = MetaData()

procedures_table = Table(
    'procedures', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('procedure_dat', Date, nullable=False),
    Column('person_id', Integer, nullable=False),
    Column('provider_id', Integer),
    Column('procedure_source_concept_id', Integer, nullable=False),
)

def init_db():
    # create table
    metadata.create_all(engine)


    # load csv
    csv_file_path = "data/procedure_occurrence.csv"
    if os.path.exists(csv_file_path):
        data = pd.read_csv(csv_file_path, usecols=["procedure_dat", "person_id", "provider_id", "procedure_source_concept_id"])
        data["procedure_dat"] = pd.to_datetime(data["procedure_dat"], format="%d/%m/%Y")
        data.to_sql("procedures", engine, if_exists="replace", index=False)
        print("loaded ")
    else:
        print(f"data not found at {csv_file_path}")

if __name__ == "__main__":
    init_db()
