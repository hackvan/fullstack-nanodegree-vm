from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine, func, distinct
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            # Query all the restaurants into the table:
            restaurants = session.query(Restaurant).\
                            order_by(Restaurant.name.asc()).\
                            all()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Restaurants:</h1>"
            output += '''<h3>
                           <a href='/restaurants/new'>Make a New Restaurant Here</a>
                           </br>
                         </h3>'''
            output += "<ul>"
            for restaurant in restaurants:
                output += '''<li> %s </li> 
                             <a href='/restaurants/%s/edit'>Edit</a>
                             <a href='/restaurants/%s/delete'>Delete</a>''' \
                             % (restaurant.name, restaurant.id, restaurant.id)
            
            output += "</ul>"
            output += "</body></html>"
            self.wfile.write(output)
            return

        elif self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Make a New Restaurant:</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                           <input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name' >
                           <input type='submit' value='Create'> 
                         </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            return

        elif self.path.endswith("/edit"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).\
                                    filter_by(id=restaurantIDPath).\
                                    one()
            if myRestaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)

        elif self.path.endswith("/delete"):
            restaurantIDPath = self.path.split("/")[2]
            myRestaurantQuery = session.query(Restaurant).\
                                    filter_by(id=restaurantIDPath).\
                                    one()
            if myRestaurantQuery:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1> Are you sure you want to delete %s? </h1>" \
                            % myRestaurantQuery.name
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/delete' >" % restaurantIDPath
                output += "<input type = 'submit' value = 'Delete'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)

        elif self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>Hello!</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                           <h2>What would you like me to say?</h2>
                           <input name="message" type="text" >
                           <input type="submit" value="Submit"> 
                         </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return

        elif self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            output = ""
            output += "<html><body>"
            output += "<h1>&#161 Hola !</h1>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                           <h2>What would you like me to say?</h2>
                           <input name="message" type="text" >
                           <input type="submit" value="Submit"> 
                         </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
            return

        else:
            self.send_error(404, 'File Not Found: %s' % self.path)
    
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    
                    # Create new restaurant object:
                    myNewRestaurant = Restaurant(name = messagecontent[0])
                    session.add(myNewRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print "Insert complete!"

            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    # Search the restaurant to update:
                    myRestaurantQuery = session.query(Restaurant).\
                                            filter_by(id=restaurantIDPath).\
                                            one()
                    if myRestaurantQuery != []:
                        # Update the values of the restaurant:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        print "Update complete!"

            elif self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                # Search the restaurant to delete:
                myRestaurantQuery = session.query(Restaurant).\
                                        filter_by(id=restaurantIDPath).\
                                        one()
                #if myRestaurantQuery != []:
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print "Delete complete!"

            else:
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                               <h2>What would you like me to say?</h2>
                               <input name="message" type="text" >
                               <input type="submit" value="Submit"> 
                             </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except: 
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()