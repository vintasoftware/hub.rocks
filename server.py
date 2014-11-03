import os
import requests

from flask import (
    Flask, jsonify, request,
    abort, render_template,
    send_from_directory)
from flask.ext.cors import CORS
from pusher import pusher_from_url
import redis
from redis_collections import Dict

app = Flask(__name__)
CORS(app, resources=r'/api/*', headers='Content-Type')
pusher = pusher_from_url()

redis_cli = redis.from_url(os.environ.get('OPENREDIS_URL'))
tracks = Dict(redis=redis_cli, key='tracks')


@app.route("/api/tracks/", methods=['GET'])
def tracks_get():
    now_playing = tracks.get('now_playing')
    track_list = [track for key, track in tracks.items() if key != 'now_playing']
    track_list.sort(key=lambda x: len(x['votes']), reverse=True)
    
    return jsonify({
        'now_playing': now_playing,
        'tracks': track_list,
    })


def _fetch_track_from_deezer(deezer_id):
    response = requests.get('http://api.deezer.com/track/{0}'.format(deezer_id))
    if response.status_code == 200:
        response_json = response.json()
        return {
            'deezer_id': deezer_id,
            'title': response_json['title'],
            'artist': response_json['artist']['name'],
            'votes': []
        }

@app.route("/api/tracks/<deezer_id>/vote/", methods=['PUT'])
def track_vote_put(deezer_id):
    user = request.headers.get('Authorization')

    if not user:
        abort(400)

    if deezer_id not in tracks:
        track = _fetch_track_from_deezer(deezer_id)
        if not track:
            abort(400)
    else:
        track = tracks[deezer_id]
    
    if user not in track['votes']:
        track['votes'].append(user)
    tracks[deezer_id] = track

    pusher['tracks'].trigger('updated');

    return '', 204


@app.route("/api/tracks/<deezer_id>/vote/", methods=['DELETE'])
def track_vote_delete(deezer_id):
    user = request.headers.get('Authorization')
    
    if not (deezer_id in tracks and user):
        abort(400)

    del tracks['deezer_id']

    pusher['tracks'].trigger('updated');

    return '', 204


@app.route("/api/tracks/next/", methods=['GET'])
def track_next_get():
    if tracks:
        next = max(tracks.values(), key=lambda x: len(x['votes']))
    else:
        next = None
    
    return jsonify({'next': next})


@app.route("/api/tracks/<deezer_id>/now-playing/", methods=['PUT'])
def track_now_playing_put(deezer_id):
    if deezer_id not in tracks:
        abort(400)

    tracks['now_playing'] = tracks[deezer_id]

    pusher['tracks'].trigger('updated');

    return '', 204


@app.route("/")
def vote_html():
    return render_template('vote.html', PUSHER_API_KEY=pusher.key)


@app.route('/static/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    app.run(debug=True)