from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

"""
Delete with SQLAlchemy:
1. Find entry
2. Session delete to entry
3. Commit the session
"""
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print spinach.restaurant.name
session.delete(spinach)
session.commit()

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()