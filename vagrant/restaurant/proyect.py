from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def HelloWorld():
	return "Hello World"

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).\
					filter_by(id = restaurant_id).\
					one()
	items = session.query(MenuItem).\
				filter_by(restaurant_id = restaurant.id).\
				order_by(MenuItem.name.asc())
	return render_template('menu.html', restaurant = restaurant, items = items)
	'''
	output = ''
	for i in items:
		output += i.name + '</br>'
		output += i.price + '</br>'
		output += i.description + '</br>'
		output += '</br>'
	return output
	'''

# Access via http://localhost:5000/restaurants/1/new/
@app.route('/restaurant/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:  # It's a GET request.
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Access via http://localhost:5000/restaurants/1/2/edit/
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')	
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a new menu item. Task 2 complete!"

# Access via http://localhost:5000/restaurants/1/2/delete/
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')	
def deleteMenuItem(restaurant_id, menu_id):
	return "page to delete a new menu item. Task 3 complete!"	

''' Flask's Documentation :
> App route decorator: Python use the decorator ...
Flask has the @app.route decorator to specify maps to the URL indicated:
	
	@app.route('/') -- Root directory (http://0.0.0.0:0000/)
	@app.route('/path/') -- Path specified (http://0.0.0.0:0000/path/)
	@app.route('/path1/<type:name_variable>/path2/...) -- Path specified (http://0.0.0.0:0000/path1/1/path2)

	@app.route('/path/', methods = ['GET', 'POST'])

> Templates: Flask uses templates into the folder /templates/ on the root app
to rendering templates.

	render_template('name_of_template.html', args = values [, args = values]) 

into the HTML code we can use Python code and variables using:

	{% logical code %}
	{{ printed code }}

since, from within HTML codes, we cannot use indentations to mark
the beginning and ending of statements and loops, we must use keywords
like endfor and endif.

> URL Building: is a helpful feature to create URLs based on the functions they execute
	
	url_for('function_name', args1 = values [, args2 = values])

for example: If we have functions with the decorator @app.route defined.

	from flask import Flask, url_for
	app = Flask(__name__)
	
	@app.route('/')
	def index(): pass

	@app.route('/login')
	def login(): pass
	
	@app.route('/user/<username>')
	def profile(username): pass

	with app.test_request_context():
		print url_for('index')
		print url_for('login')
		print url_for('login', next='/')
		print url_for('profile', username='John Doe')
	>>> /
	>>> /login
	>>> /login?next=/
	>>> /user/John%20Doe

'''

# This conditional is useful to indicate that the server turn on when
# the Python script is call directly on the console, if it's use by import
# this code doesn't execute.
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
