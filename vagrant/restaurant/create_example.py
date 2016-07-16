from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
# Lets our program know which database engine we want to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')
# Let's bind the engine to the base class
Base.metadata.bind = engine
# Establishes a link communication beetwen our code executions and the engine
DBSession = sessionmaker(bind = engine)
# In order to create, read, update or delete information on our database
# A session allows us to write down all the commands we want to execute 
# But not send them to the database until we call a commit
session = DBSession()
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
# print session.query(Restaurant).all()
cheesepizza = MenuItem(name = "Cheese Pizza",
					   description = "Mase with all natural ingredients and fresh mozzarela",
					   course = "Entree",
					   price = "$8.99",
					   restaurant = myFirstRestaurant
					  )
session.add(cheesepizza)
session.commit()
# print session.query(MenuItem).all()