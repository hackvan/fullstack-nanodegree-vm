from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy
from datetime import date
from dateutil.relativedelta import relativedelta

engine = create_engine('sqlite:///puppies.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
width = 70
"""
1. Query all of the puppies and return the results 
in ascending alphabetical order.
"""
def query_1():
	print "1. Query:", "*"*width
	puppies = session.query(Puppy.id, Puppy.name).order_by(Puppy.name.asc()).all()
	for puppie in puppies:
		print puppie.id, " - ", puppie.name

"""
2. Query all of the puppies that are less than 6 months
old organized by the youngest first.

Require: dateutil library
win32: python -m pip install python-dateutil
linux: sudo pip install python-dateutil
"""
def query_2():
	print "2. Query:", "*"*width
	six_months_ago = date.today() + relativedelta(months=-6)
	puppies = session.query(Puppy).filter(Puppy.dateOfBirth >= six_months_ago)\
				.order_by(Puppy.dateOfBirth.desc())
	for puppie in puppies:
		print puppie.id, " - ", puppie.name, " - ", puppie.dateOfBirth

"""
3. Query all puppies by ascending weight
"""
def query_3():
	print "3. Query:", "*"*width
	puppies = session.query(Puppy).order_by(Puppy.weight.asc()).all()
	for puppie in puppies:
		print puppie.id, " - ", puppie.name, " - ", puppie.weight

"""
4. Query all puppies grouped by the shelter in which they are staying
"""
def query_4():
	print "4. Query:", "*"*width
	result = session.query(Shelter, func.count(Puppy.id)).join(Puppy)\
				.group_by(Shelter.id).all()
	for item in result:
		print item[0].id, item[0].name, item[1]

query_1()
query_2()
query_3()
query_4()