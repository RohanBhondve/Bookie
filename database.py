from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dbUrl = "mysql+pymysql://root:mysql%401234@localhost:3306/ticket_booking"
engine = create_engine(dbUrl)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)