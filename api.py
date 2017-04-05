# things.py

# Let's get this party started!
import falcon
from resources import FeedsResource

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
rochesterFeed = FeedsResource('rochester')
usatFeed = FeedsResource('usat')


# things will handle all requests to the '/things' URL path
app.add_route('/rochester/', rochesterFeed)
app.add_route('/usat/', usatFeed)
#app.add_route('/clean/', cleanup)

#instructions

# 1. pip install falcon

# 2. in the HurlStack.java file make sure this is uncommented. (or add it line 89)
'''
boolean isImage = url.contains(".jpg") || url.contains("thumb") || url.contains(".png") || url.contains(".jpeg");

if(!isImage) {
    url = "http://10.0.2.2:8000/usat?url=" + url;
}
'''
# 3. start the api. in the terminal
#  gunicorn api:app

# 4. start the app in an emulator and browse the app.

# 5. copy the json files add it to the raw directory in the app. copy the contents of filefeed.txt and add it to TestMyApplication

