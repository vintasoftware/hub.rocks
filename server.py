import os
import requests

from flask import Flask, Response, abort, render_template, send_from_directory
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo
from bson import json_util
from pusher import pusher_from_url


app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGOHQ_URL')
CORS(app, resources=r'/api/*', headers='Content-Type')
mongo = PyMongo(app)
pusher = pusher_from_url()


def json_response(data):
    return Response(json_util.dumps(data), mimetype='application/json')


@app.route("/api/tracks/", methods=['GET'])
def tracks_get():
    tracks = list(mongo.db.tracks.find().sort('votes', -1))
    return json_response({'tracks': tracks})


def _fetch_track_from_deezer(deezer_id):
    response = requests.get('http://api.deezer.com/track/{0}'.format(deezer_id))
    if response.status_code == 200:
        response_json = response.json()
        return {
            'deezer_id': deezer_id,
            'title': response_json['title'],
            'artist': response_json['artist']['name'],
            'votes': 0
        }

@app.route("/api/tracks/<deezer_id>/", methods=['PUT'])
def track_put(deezer_id):
    track = mongo.db.tracks.find_one({'deezer_id': deezer_id})
    
    if not track:
        track = _fetch_track_from_deezer(deezer_id)
        if not track:
            abort(400)

        mongo.db.tracks.insert(track)

    mongo.db.tracks.update({'deezer_id': deezer_id}, {'$inc': {'votes': 1}})
    pusher['tracks'].trigger('updated');

    return '', 204


@app.route("/api/tracks/next/", methods=['GET'])
def track_next_get():
    track = mongo.db.tracks.find().sort('votes', -1).limit(1)
    if track.has_next():
        next = track.next()
    else:
        next = None
    
    return json_response({'next': next})


@app.route("/api/tracks/<deezer_id>/", methods=['DELETE'])
def track_delete(deezer_id):
    mongo.db.tracks.remove({'deezer_id' : deezer_id})
    pusher['tracks'].trigger('updated');
    
    return '', 204


@app.route("/")
def vote_html():
    return render_template('vote.html')


@app.route('/static/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    app.run(debug=True)
