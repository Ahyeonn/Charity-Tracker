from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.CharityTracker
feeds = db.feeds
animals = db.animals
homes = db.homes
comments = db.comments
commentsanimal = db.commentsanimal
commentshome = db.commentshome

app = Flask(__name__)

@app.route('/')
def charity_index():
    """Show all charitylists"""
    return render_template('donation.html')

@app.route('/charityhome')
def home_index():
    return render_template('charityhome.html')

@app.route('/charityfeed')
def feed_index():
    return render_template('charityfeed.html')

@app.route('/charityanimal')
def animal_index():
    """Show all playlists."""
    return render_template('charityanimal.html')

@app.route('/feeddonate')
def feed_index_new():
    """show & create dbs for the form"""
    return render_template('feeddonate_index&new.html', feeds=feeds.find())
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
    feeds.insert_one(feed)
    return redirect(url_for('feed_show', feed_id=feed['_id']))

@app.route('/feed/<feed_id>')
def feed_show(feed_id):
    """Show a single donation by a user."""
    feed = feeds.find_one({'_id': ObjectId(feed_id)})
    feed_comments = comments.find({'feed_id': ObjectId(feed_id)})
    return render_template('feeddonate_show.html', feed=feed, comments = feed_comments)

@app.route('/feed/<feed_id>/edit')
def feed_edit(feed_id):
    """Edit a single donation."""
    feed = feeds.find_one({'_id': ObjectId(feed_id)}) 
    return render_template('feeddonate_edit.html', feed=feed, title='Edit Donation')

@app.route('/feed/<feed_id>', methods=['POST'])
def feed_update(feed_id):
    """Update an edited donation history of a user."""
    updated_feed = {
            'feed_date': request.form.get('feed_date'),
            'feed_donation': request.form.get('feed_donation'),
            'feed_name': request.form.get('feed_name')
    }
    feeds.update_one(
        {'_id': ObjectId(feed_id)},
        {'$set': updated_feed})
    return redirect(url_for('feed_show', feed_id=feed_id))

@app.route('/feed/<feed_id>/delete', methods=['POST'])
def feed_delete(feed_id):
    """Delete donation history."""
    feeds.delete_one({'_id': ObjectId(feed_id)})
    return redirect(url_for('feed_index_new'))

@app.route('/animaldonate')
def animal_index_new():
    return render_template('animaldonate_index&new.html', animals=animals.find())

@app.route('/animaldonate', methods=['POST'])
def animal_submit():
    animal = {
        'animal_name': request.form.get('animal_name'),
        'animal_donation': request.form.get('animal_donation'),
        'animal_date': request.form.get('animal_date')
    }
    animals.insert_one(animal)
    return redirect(url_for('animal_show', animal_id=animal['_id']))

@app.route('/animal/<animal_id>')
def animal_show(animal_id):
    animal = animals.find_one({'_id': ObjectId(animal_id)})
    animal_comments = commentsanimal.find({'animal_id': ObjectId(animal_id)})
    return render_template('animaldonate_show.html', animal=animal, comments=animal_comments)

@app.route('/animal/<animal_id>/edit')
def animal_edit(animal_id):
    animal = animals.find_one({'_id': ObjectId(animal_id)}) 
    return render_template('animaldonate_edit.html', animal=animal, title='Edit Donation')

@app.route('/animal/<animal_id>', methods=['POST'])
def animal_update(animal_id):
    updated_animal = {
            'animal_date': request.form.get('animal_date'),
            'animal_donation': request.form.get('animal_donation'),
            'animal_name': request.form.get('animal_name')
    }
    animals.update_one(
        {'_id': ObjectId(animal_id)},
        {'$set': updated_animal})
    return redirect(url_for('animal_show', animal_id=animal_id))

@app.route('/animal/<animal_id>/delete', methods=['POST'])
def animal_delete(animal_id):
    animals.delete_one({'_id': ObjectId(animal_id)})
    return redirect(url_for('animal_index_new'))

@app.route('/homedonate')
def home_index_new():
    return render_template('homedonate_index&new.html', homes=homes.find())

@app.route('/homedonate', methods=['POST'])
def home_submit():
    home = {
        'home_name': request.form.get('home_name'),
        'home_donation': request.form.get('home_donation'),
        'home_date': request.form.get('home_date')
    }
    homes.insert_one(home)
    return redirect(url_for('home_show', home_id=home['_id']))

@app.route('/home/<home_id>')
def home_show(home_id):
    home = homes.find_one({'_id': ObjectId(home_id)})
    home_comments = commentshome.find({'home_id': ObjectId(home_id)})
    return render_template('homedonate_show.html', home=home, comments=home_comments)

@app.route('/home/<home_id>/edit')
def home_edit(home_id):
    """Edit a single donation."""
    home = homes.find_one({'_id': ObjectId(home_id)}) 
    return render_template('homedonate_edit.html', home=home, title='Edit Donation')

@app.route('/home/<home_id>', methods=['POST'])
def home_update(home_id):
    updated_home = {
            'home_date': request.form.get('home_date'),
            'home_donation': request.form.get('home_donation'),
            'home_name': request.form.get('home_name')
    }
    homes.update_one(
        {'_id': ObjectId(home_id)},
        {'$set': updated_home})
    return redirect(url_for('home_show', home_id=home_id))

@app.route('/home/<home_id>/delete', methods=['POST'])
def home_delete(home_id):
    homes.delete_one({'_id': ObjectId(home_id)})
    return redirect(url_for('home_index_new'))

@app.route('/charities/comments', methods=['POST'])
def comments_new():
    comment = {
        'feed_id':ObjectId(request.form.get('feed_id')),
        'title': request.form.get('title'),
        'content': request.form.get('content')
    }
    comments.insert_one(comment) 
    return redirect(url_for('feed_show', feed_id=request.form.get('feed_id')))

@app.route('/charities/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('feed_show', feed_id=request.form.get('feed_id')))


@app.route('/animals/comments', methods=['POST'])
def animalcomments_new():
    comment = {
        'animal_id':ObjectId(request.form.get('animal_id')),
        'title': request.form.get('title'),
        'content': request.form.get('content')
    }
    commentsanimal.insert_one(comment) 
    return redirect(url_for('animal_show', animal_id=request.form.get('animal_id')))

@app.route('/animals/comments/<comment_id>', methods=['POST'])
def animalcomments_delete(comment_id):
    commentsanimal.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('animal_show', animal_id=request.form.get('animal_id')))

@app.route('/homes/comments', methods=['POST'])
def homecomments_new():
    comment = {
        'home_id':ObjectId(request.form.get('home_id')),
        'title': request.form.get('title'),
        'content': request.form.get('content')
    }
    commentshome.insert_one(comment) 
    return redirect(url_for('home_show', home_id=request.form.get('home_id')))

@app.route('/homes/comments/<comment_id>', methods=['POST'])
def homecomments_delete(comment_id):
    commentshome.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('home_show', home_id=request.form.get('home_id')))

if __name__ == '__main__':
  app.run(debug=True)  