# This will make the API "work" without us needing to write hundreds of line of code
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

# This line is required to work with Flask. 
app = Flask(__name__)
api = Api(app)

# Define the data format of our message put requests
message_put_args = reqparse.RequestParser()
message_put_args.add_argument("message_id", type=int, help="the identifier of the message is required", required=True)
message_put_args.add_argument("topic", type=str, help="Topic of the message is required", required=True)
message_put_args.add_argument("body", type=str, help="Body  of the message is required", required=True)
message_put_args.add_argument("author", type=str, help="Author  of the message")
message_put_args.add_argument("views", type=int, help="Views  of the message")

# Sample data testing parameters to GET
# message {"id": 0, "topic":"?", "body":"?", "author":"?", "likedBy": [], "views": 0}
messages = {}

# Functions to check for issues with the requests

def abort_if_message_id_not_found(message_id):
    if message_id not in messages:
        abort(404, message="Message id is not valid")

def abort_if_message_id_exists(message_id):
    if message_id in messages:
        abort(409, message="Message with that id already created")

# Our forum deals with the following resources:

class Messages(Resource):
    def get(self, message_id): # Define what happens when Messages receives a "GET" request with a message_id parameter
        abort_if_message_id_not_found(message_id)
        # Increment the view count
        message = messages[message_id]
        message["views"] = message["views"] + 1
        messages[message_id] = message
        # then return the message
        return messages[message_id]

    def post(self):
        args = message_put_args.parse_args()
        id = args["message_id"]
        abort_if_message_id_exists(id)
        messages[id] = args
        return messages[id], 201 # return added data with Created status code

    def put(self, message_id):
        # Parse the arguments received and ensure they match the expected format
        args = message_put_args.parse_args()
        messages[message_id] = args
        return messages[message_id], 201 # return added data with Created status code

    def delete(self, message_id):
        abort_if_message_id_not_found(message_id)
        del messages[message_id]
        return "", 204


# Define the resources that the API knows about and what route(s) (URL) they are found at. Add your own here.
api.add_resource(Messages, "/messages", "/messages/<int:message_id>")

# Used to start the program when calling python main.py on the command line
if __name__ == "__main__":
    app.run(debug=True) # Remove debug = True for production
