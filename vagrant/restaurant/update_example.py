from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

"""
Update with SQLAlchemy:
1. Find entry
2. Reset values
3. Add to session
4. Commit the session
"""
print "Show all the Veggie Burgers:"
veggieBurguers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for veggieBurguer in veggieBurguers:
	print veggieBurguer.id
	print veggieBurguer.price
	print veggieBurguer.restaurant.name
	print "\n"

print "Find and print the price:"
UrbanVeggieBurguer = session.query(MenuItem).filter_by(id = 9).one()
print UrbanVeggieBurguer.price

print "Update only the values that found:"
UrbanVeggieBurguer.price = '$2.99'
session.add(UrbanVeggieBurguer)
session.commit()

print "Update all the Veggie Burguers and show them:"
veggieBurguers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

for veggieBurguer in veggieBurguers:
	if veggieBurguer.price != '$2.99':
		veggieBurguer.price = '$2.99'
		session.add(veggieBurguer)
		session.commit()

for veggieBurguer in veggieBurguers:
	print veggieBurguer.id
	print veggieBurguer.price
	print veggieBurguer.restaurant.name
	print "\n"
