# This lets us try out our methods without needing another tool or having to go to the browser every time.
# It is not required. 
# To test it:
# - Go to the directory where your project files are saved
# - Run python main.py in one command line window
# - Run python test.py in a separate command line window. 
# If everything works, you should see the results of your call appear.
# Or try the address below + resource name in your browser.
import requests

BASE = "http://127.0.0.1:5000/"

# Test Invalid Messages GET
print("GET: ")
response = requests.get(BASE + "messages/6")
print(response.status_code)
print(response.json())

# Test Invalid Messages DEL
print("DEL: ")
response = requests.delete(BASE + "messages/6")
print(response.status_code)
print(response.json())

# Test Messages POST
test_data = [{"message_id":1, "topic": "Test", "body": "A clever post", "author": "soso", "views":0},
            {"message_id":2, "topic": "Test2", "body": "A clever post2", "author": "soso", "views":10},
            {"message_id":3, "topic": "Test3", "body": "A clever post3", "author": "soso", "views":20}]

print("POST: ")
for i in range(len(test_data)):
    response = requests.post(BASE + "messages", test_data[i])
    print(response.json())

# Test Messages PUT
print("PUT: ")
response = requests.put(BASE + "messages/4", {"message_id":4, "topic": "Test", "body": "A clever post", "author": "soso", "views":0})
print(response.json())

# Test Valid Messages GET
print("GET: ")
response = requests.get(BASE + "messages/4")
print(response.json())

print("GET: ")
response = requests.get(BASE + "messages/4")
print(response.json())

# Test Messages PUT
print("PUT (Update): ")
response = requests.put(BASE + "messages/4", {"message_id":4, "topic": "New", "body": "A new clever post", "author": "soso", "views":2})
print(response.json())

# Test Valid Messages GET
print("GET: ")
response = requests.get(BASE + "messages/4")
print(response.json())

# Test Valid Messages DEL
print("DEL: ")
response = requests.delete(BASE + "messages/1")
print(response.status_code)

