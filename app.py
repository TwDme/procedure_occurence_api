from flask import Flask, request
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.dialects import postgresql


DATABASE_URL = "postgresql://postgres:password@db:5432/procedure_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)
Base = declarative_base()

app = Flask(__name__)
app.config["SQLALCHEMY_ECHO"] = True 
# procedure table
class Procedure(Base):
    __tablename__ = 'procedures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    procedure_dat = Column(Date, nullable=False)
    person_id = Column(Integer, nullable=False)
    provider_id = Column(Integer)
    procedure_source_concept_id = Column(Integer, nullable=False)




@app.route('/unique-persons', methods=['POST'])
def get_unique_persons():
    """
    Get the count of unique persons for the last N days.
    """
    try:
        data = request.get_json()
        days = data.get('days')
        if not days:
            return {"error": "days parameter is required"}, 400
        
        with Session.begin() as session:
            stmt = select(func.count(func.distinct(Procedure.person_id))).where(
                func.date(Procedure.procedure_dat) >= func.date(func.current_date() - days))
 
            # app.logger.info(stmt.compile(dialect=postgresql.dialect()))
            
            result = session.execute(stmt).scalar()

        return {"unique_person_count": result}
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/unique-providers-by-procedure-type', methods=['POST'])
def get_summary_by_procedure_type():
    """
    Get the total number of unique providers and persons for a specified procedure type,
    grouped by procedure date.
    """
    try:
        data = request.get_json()
        procedure_type = data.get('procedure_type')
        if not procedure_type:
            return {"error": "Procedure type is required"}, 400
        
        with Session.begin() as session:
            stmt = select(Procedure.procedure_dat,
            func.count(func.distinct(Procedure.provider_id)).label('unique_providers'),
            func.count(func.distinct(Procedure.person_id)).label('unique_persons')
        ).where(
            Procedure.procedure_source_concept_id == procedure_type
        ).group_by(Procedure.procedure_dat)
 
            # app.logger.info(stmt.compile(dialect=postgresql.dialect()))
            
            results = session.execute(stmt).all()

        return [
            {
                "procedure_date": str(row[0]),
                "unique_providers": row[1],
                "unique_persons": row[2],
                "total_unique": row[1] + row[2]
            }
            for row in results
        ]
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
