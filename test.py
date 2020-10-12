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

# Test HellowWorld GET
response = requests.get(BASE + "helloworld")
print(response.status_code)
print(response.json())

# Test HellowWorld POST
response = requests.post(BASE + "helloworld")
print(response.status_code)
print(response.json())