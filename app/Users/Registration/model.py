from app.Connection.database import Base
import sqlalchemy
import sqlalchemy
from datetime import datetime
from abc import ABC,abstractmethod
class BaseModel(Base):
    __abstract__ = True  # This makes it an abstract class (SQLAlchemy won't create a table for it)
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,autoincrement=True)
    Created_date = sqlalchemy.Column(sqlalchemy.DATETIME,default=datetime.now())
    Updated_date = sqlalchemy.Column(sqlalchemy.DATETIME)
    status = sqlalchemy.Column(sqlalchemy.BOOLEAN ,default=1)
    @abstractmethod
    def ConvertToDict(self):
        pass

class Users(BaseModel):
    __tablename__ = 'Users'
    username = sqlalchemy.Column(sqlalchemy.String(255),nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(255),unique=True)
    phone = sqlalchemy.Column(sqlalchemy.String(255))
    password = sqlalchemy.Column(sqlalchemy.String(255))
    haspwd = sqlalchemy.Column(sqlalchemy.String(255))


    # def __init__(self, id, username, email, phone,password,haspwd,Created_date,Updated_date,status):
    #         self.id = id
    #         self.username = username
    #         self.email = email
    #         self.phone = phone
    #         self.password = password
    #         self.haspwd = haspwd
    #         self.Created_date = Created_date
    #         self.Updated_date = Updated_date
    #         self.status = status

    def ConvertToDict(self):
        dictData =  {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            # "password": self.password,  # Only if safe to include; remove if not
            # "haspwd": self.haspwd, # Only if safe to include; remove if not
            "Created_date": self.Created_date.strftime('%d %B %Y') if self.Created_date else None,
            "Updated_date": self.Updated_date.strftime('%d %B %Y') if self.Updated_date else None,
            "status": self.status
        }
        return dictData
    

