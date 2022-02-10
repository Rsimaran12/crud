from flask import Flask
from flask_pymongo import PyMongo
import gridfs
app = Flask(__name__)
app.secret_key = "secret key"
app.config["MONGO_URI"] = "mongodb://localhost:8080"
mongo = PyMongo(app)
if "__name__" == "__main__":
    app.run(debug=True)