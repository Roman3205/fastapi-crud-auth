from database import Base, engine
from sqlalchemy import Column, Integer, VARCHAR

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255))
    author = Column(VARCHAR(255))

Base.metadata.create_all(bind=engine)