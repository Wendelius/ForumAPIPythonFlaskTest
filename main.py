# This will make the API "work" without us needing to write hundreds of line of code
from flask import Flask, request # help us handle the API requests
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with # help us handle the API requests
from flask_sqlalchemy import SQLAlchemy # let us save data in a mini local DB rather than in memory

# This line is required to work with Flask. 
app = Flask(__name__)
api = Api(app)

# Configure the local DB to be used and the models (tables) within it
# Where is the d atabase?
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackathonprototypeforumdb.db'
db = SQLAlchemy(app)

# Define the tables (models) we are going to store data in

# The application users
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self): # If we represent the user as a simple string, we show the user name
        return f'<User (user_name={user_name})'

# The topics started in chat
class TopicModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=True)

    def __repr__(self): # Represent the topic as a string
        return f'<Topic (title={title})'

# The messages in a topic
class MessageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=True) # For now.... While we don't have topics and stuff
    body = db.Column(db.String(4096), unique=False, nullable=False)
    views = db.Column(db.Integer, unique=False, nullable=False)
    likes = db.Column(db.Integer, unique=False, nullable=False) # To do. Will be a list of users who liked the message at some point...

    # topic_id = db.Column(db.Integer, db.ForeignKey('TopicModel.id'), nullable=False)
    # topic = db.relationship('TopicModel', backref=db.backref('messages', lazy=True))

    # user_id = db.Column(db.Integer, db.ForeignKey('UserModel.id'), nullable=False)
    # user = db.relationship('UserModel', backref=db.backref('usermessages', lazy=True))

    def __repr__(self): # Represent the message as a string. TODO: , author={user_id}
        return f'<Message (id={id}, views={views}, likes={likes})'

# Once we have defined all the data to save in the database, create it. DO THIS ONCE!
# db.create_all() # This can only run once or it will override all the data in the DB

# Define the data format of our message when passed from client to API (aka Dto)
message_put_args = reqparse.RequestParser()
message_put_args.add_argument("message_id", type=int, help="the identifier of the message is required", required=True)
message_put_args.add_argument("topic", type=str, help="Topic of the message is required", required=True)
message_put_args.add_argument("body", type=str, help="Body  of the message is required", required=True)
message_put_args.add_argument("author", type=str, help="Author  of the message")
message_put_args.add_argument("views", type=int, help="Views  of the message")

# When we retrieve data from the database, describe how to serialise it into JSON so we can return it to the caller
resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Functions to check for issues with the requests

# def abort_if_message_id_not_found(message_id):
#     if message_id not in messages:
#         abort(404, message="Message id is not valid")

# def abort_if_message_id_exists(message_id):
#     if message_id in messages:
#         abort(409, message="Message with that id already created")

# Our forum deals with the following resources:

class Messages(Resource):
    @marshal_with(resource_fields) # use this information to turn the data we retrieved into JSON
    def get(self, message_id): # Define what happens when Messages receives a "GET" request with a message_id parameter
        result = MessageModel.query.get(id=message_id) # get is used for a single row by primary key. filter or filter_by for traditional WHERE clauses
        # Increment the view count
        # message = messages[message_id]
        # message["views"] = message["views"] + 1
        # messages[message_id] = message
        # then return the message
        return result

    @marshal_with(resource_fields) # use this information to turn the data we retrieved into JSON
    def post(self):
        args = message_put_args.parse_args()
        message = MessageModel(title=args['title'], body=args['body'], views=0, likes=0)
        db.session.add(message)
        db.session.commit()
        return message, 201 # return added data with Created status code

    @marshal_with(resource_fields) # use this information to turn the data we retrieved into JSON
    def put(self, message_id):
        args = message_put_args.parse_args()
        message = MessageModel(id=message_id, title=args['title'], body=args['body'], views=0, likes=0)
        db.session.add(message)
        db.session.commit()
        return message, 200

    def delete(self, message_id):
        abort_if_message_id_not_found(message_id)
        del messages[message_id]
        return "", 204


# Define the resources that the API knows about and what route(s) (URL) they are found at. Add your own here.
api.add_resource(Messages, "/messages", "/messages/<int:message_id>")

# Used to start the program when calling python main.py on the command line
if __name__ == "__main__":
    app.run(debug=True) # Remove debug = True for production
