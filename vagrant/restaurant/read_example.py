from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Show the first result in the table:
firstResult = session.query(Restaurant).first()
print firstResult.name

# Show all the items into the table:
items = session.query(MenuItem).all()
for item in items:
	print item.name

# count User records, without using a subquery.
session.query(func.count(Restaurant.id))
# return count of user "id" grouped by "name"
session.query(func.count(Restaurant.id)).group_by(Restaurant.name)
# count distinct "name" values
session.query(func.count(distinct(Restaurant.name)))

