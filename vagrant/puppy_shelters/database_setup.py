# @Configuration
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# @Class
class Shelter(Base):
    # @Table
    __tablename__ = 'shelter'
    # @Mapper
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)

# @Class
class Puppy(Base):
    # @Table
    __tablename__ = 'puppy'
    # @Mapper
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    gender = Column(String(6), nullable = False)
    dateOfBirth = Column(Date)
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    weight = Column(Numeric(10))

# @Configuration
engine = create_engine('sqlite:///puppies.db')
Base.metadata.create_all(engine)