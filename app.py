# Import dependencies for Flask, Mongo and scraping
from flask import Flask, render_template
from flask_pymongo import PyMongo
import Scraping

#Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" #mongo connection string
mongo = PyMongo(app)

# Set up App Routes
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Set up scraping route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars  # Assigning variable mars for MongoDB
    mars_data = Scraping.scrape_all()  # Calling scrape_all and assigning return to mars_data variable
    mars.update({}, mars_data, upsert=True) # Appending mars data with new scraping results
    return "Scraping Successful!"
    
#Tell Flask to run
if __name__ == "__main__":
    app.run()

