import json
from flask import Flask, Response, jsonify, redirect, render_template, request, abort, url_for
from db.init_db import initialize_database
from db.accessor import create_review, get_song_by_id, get_songs_with_reactions

app = Flask(__name__)

initialize_database()

@app.route('/', methods = ['GET'])
@app.route('/songs', methods = ['GET'])
def reactions():
    if request.method == "GET":
        songs = get_songs_with_reactions()
        return render_template("songs.html", songs=songs)

    return abort(404)

@app.route('/review/<int:id>', methods = ['GET', 'POST'])
def review(id):
    if id <= 0: 
        abort(404)

    song = get_song_by_id(id)

    if song == None:
        abort(404)
    
    if request.method == 'GET':
        return render_template('review.html', song=song)

    elif request.method == 'POST':

        user = request.form.get("user")
        score = request.form.get("score")
        review = request.form.get("review")

        try:
            create_review(user, score, review, id)
        except: 
            abort(Response("Unable to create review"))

        return redirect(url_for(reactions.__name__))

    else:
        abort(404)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

