from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
engine = create_engine("mysql+pymysql://root:Ams_12345@localhost:3306/sanjeev_db")
# Define your base model
Base = declarative_base()
Session = sessionmaker(bind=engine)