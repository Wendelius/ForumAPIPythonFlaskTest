# This will make the API "work" without us needing to write hundreds of line of code
from flask import Flask
from flask_restful import Api, Resource

# This line is required to work with Flask. 
app = Flask(__name__)
api = Api(app)

# Here is a sample API "resource" for testing. Remove it once you write the real code
# Each resource should be declared as a class (an object that will group functions and variables and do something for us)
# It inherits from Resource as that gives us access to API methods to keep development easy.
class HelloWorld(Resource):
    def get(self): # Define what happens when HelloWorld receives a "GET" request
        return {"data": "Hello World!"}

    def post(self): # Define what happens when HelloWorld receives a "POST" request
        return {"data": "Posted"}

# Define the resources that the API knows about and what route (URL) they are found at. Add your own here.
api.add_resource(HelloWorld, "/helloworld")

# Used to start the program when calling python main.py on the command line
if __name__ == "__main__":
    app.run(debug=True) # Remove debug = True for production
