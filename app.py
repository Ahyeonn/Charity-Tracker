from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

client = MongoClient()
db = client.CharityTracker
charities = db.charities

app = Flask(__name__)

@app.route('/charitylists')
def charity_index():
    """Show all charitylists"""
    return render_template('donation.html')

@app.route('/feeddonate')
def feed_index_new():
    """show & create dbs for the form"""
    return render_template('feeddonate_index&new.html', charities=charities.find())
#skip feed new because it will be on the same page
#form for new & for loops for index

@app.route('/feeddonate', methods=['POST'])
def feed_submit():
    """Submit the form of a donation for the feed charity"""
    feed = {
        'feed_name': request.form.get('feed_name'),
        'feed_donation': request.form.get('feed_donation'),
        'feed_date': request.form.get('feed_date')
    }
    charities.insert_one(feed)
    return redirect(url_for('feed_show', feed_id=feed['_id']))

@app.route('/charities/<feed_id>')
def feed_show(feed_id):
    """Show a single donation by a user."""
    feed = charities.find_one({'_id': ObjectId(feed_id)})
    return render_template('feeddonate_show.html', feed=feed)

@app.route('/charities/<feed_id>/edit')
def feed_edit(feed_id):
    """Edit a single donation."""
    feed = charities.find_one({'_id': ObjectId(feed_id)}) 
    return render_template('feeddonate_edit.html', feed=feed, title='Edit Donation')

@app.route('/charities/<feed_id>', methods=['POST'])
def feed_update(feed_id):
    """Submit an edited donation by a user."""
    updated_feed = {
            'feed_date': request.form.get('feed_date'),
            'feed_donation': request.form.get('feed_donation'),
            'feed_name': request.form.get('feed_name')
    }
    charities.update_one(
        {'_id': ObjectId(feed_id)},
        {'$set': updated_feed})
    return redirect(url_for('feed_show', feed_id=feed_id))