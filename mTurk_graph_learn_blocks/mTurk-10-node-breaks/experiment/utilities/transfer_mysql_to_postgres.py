# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# postgres_engine = create_engine('postgresql://ari@localhost:5432/mydb')
# postgres_Session = sessionmaker(bind=postgres_engine)
# postgres_session = postgres_Session()

# mysql_engine = create_engine('mysql://localhost:3306/mydb')
# mysql_Session = sessionmaker(bind=mysql_engine)
# mysql_session = mysql_Session()

# engine = create_engine(DATABASE, echo=False, pool_recycle=3600) 
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.dialects.postgresql import JSON, ARRAY

# class City(Base):
#     __tablename__ = 'city'
#     name = Column(String(100), primary_key=True)
#     desc = Column(JSON)
#     temps = Column(ARRAY(Integer))




from psiturk.models import Participant