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

redis_cli = redis.from_url(os.environ.get('REDISCLOUD_URL'))

tracks = Dict(redis=redis_cli, key='tracks')
now_playing = Dict(redis=redis_cli, key='now_playing')


def _get_request_user():
    authorization = request.headers.get('Authorization')
    split = authorization.split(' ')
    if len(split) == 2:
        token_name, token = split
        if token_name == 'Token':
            return token


@app.route("/api/tracks/", methods=['GET'])
def tracks_get():
    track_list = tracks.values()
    track_list.sort(key=lambda x: len(x['votes']), reverse=True)
    
    return jsonify({
        'now_playing': dict(now_playing),
        'tracks': track_list,
    })


def _fetch_track_from_deezer(deezer_id):
    response = requests.get('http://api.deezer.com/track/{0}'.format(deezer_id))
    if response.status_code == 200:
        response_json = response.json()
        if 'error' not in response_json:
            return {
                'deezer_id': deezer_id,
                'title': response_json['title'],
                'artist': response_json['artist']['name'],
                'votes': []
            }


@app.route("/api/tracks/<deezer_id>/vote/", methods=['PUT'])
def track_vote_put(deezer_id):
    user = _get_request_user()

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

    pusher['tracks'].trigger('updated')

    return '', 204


@app.route("/api/tracks/<deezer_id>/vote/", methods=['DELETE'])
def track_vote_delete(deezer_id):
    user = _get_request_user()
    
    if not (deezer_id in tracks and user):
        abort(400)

    try:
        track = tracks[deezer_id]
        track['votes'].remove(user)
        
        if len(track['votes']) == 0:
            del tracks[deezer_id]
        else:
            tracks[deezer_id] = track

        pusher['tracks'].trigger('updated')

        return '', 204
    except ValueError:
        abort(400)


@app.route("/api/tracks/next/", methods=['GET'])
def track_next_get():
    if tracks:
        next = max(tracks.values(), key=lambda x: len(x['votes']))
    else:
        next = None
    
    return jsonify({'next': next})


@app.route("/api/tracks/<deezer_id>/", methods=['DELETE'])
def track_delete(deezer_id):
    if deezer_id not in tracks:
        abort(400)

    del tracks[deezer_id]

    pusher['tracks'].trigger('updated')

    return '', 204


@app.route("/api/tracks/<deezer_id>/now-playing/", methods=['PUT'])
def track_now_playing_put(deezer_id):
    if deezer_id not in tracks:
        abort(400)

    now_playing.update(tracks[deezer_id])

    pusher['tracks'].trigger('updated')

    return '', 204


@app.route("/api/tracks/<deezer_id>/now-playing/", methods=['DELETE'])
def track_now_playing_delete(deezer_id):
    if deezer_id != now_playing['deezer_id']:
        abort(400)

    now_playing.clear()

    pusher['tracks'].trigger('updated')

    return '', 204


@app.route("/")
def vote_html():
    return render_template('vote.html', PUSHER_API_KEY=pusher.key)


@app.route("/player/")
def deezer_html():
    return render_template('player.html')


@app.route('/static/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    app.run(debug=not os.environ.get('IN_HEROKU'))
