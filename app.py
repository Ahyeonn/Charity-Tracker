from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.CharityTracker
charities = db.charities

app = Flask(__name__)

@app.route('/feeddonate')
def playlists_index():
    """Show all playlists."""
    return render_template('playlists_index.html', charities=charities.find())