from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define routes and views here
@app.route('/')
# @cross_origin(origin='your-wix-site.com', headers=['Content- Type', 'Authorization'])
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
