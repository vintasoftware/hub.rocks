from flask import Flask, jsonify, abort, render_template, send_from_directory
from flask.ext.cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources=r'/api/*', headers='Content-Type')

tracks = {u'3134062': {'priority': 1, 'artist': u'Eric Serra', 'id': u'3134062', 'title': u'Leeloominai'}, u'3124869': {'priority': 1, 'artist': u'The Auteurs', 'id': u'3124869', 'title': u'Bailed Out'}, u'3134869': {'priority': 1, 'artist': u'Roxy Music', 'id': u'3134869', 'title': u'True To Life (1999 Digital Remaster)'}, u'3134862': {'priority': 1, 'artist': u'Roxy Music', 'id': u'3134862', 'title': u'The Space Between (1999 Digital Remaster)'}, u'3134860': {'priority': 1, 'artist': u'Roxy Music', 'id': u'3134860', 'title': u'Running Wild (1999 Digital Remaster)'}, u'3134762': {'priority': 2, 'artist': u'Afro Celt Sound System', 'id': u'3134762', 'title': u'Even In My Dreams'}}

@app.route("/api/tracks/", methods=['GET'])
def tracks_get():
    print tracks
    track_list = sorted(tracks.values(), key=lambda x: x['priority'], reverse=True)
    return jsonify({'tracks': track_list})

def _fetch_track_from_deezer(track_id):
    response = requests.get('http://api.deezer.com/track/{0}'.format(track_id))
    if response.status_code == 200:
        response_json = response.json()
        return {
            'id': track_id,
            'title': response_json['title'],
            'artist': response_json['artist']['name'],
            '.priority': 0
        }

@app.route("/api/tracks/<track_id>/", methods=['PUT'])
def track_put(track_id):
    if track_id not in tracks:
        track = _fetch_track_from_deezer(track_id)
        if not track:
            abort(400)

        tracks[track_id] = track

    tracks[track_id]['.priority'] += 1

    return '', 204

@app.route("/api/tracks/next/", methods=['GET'])
def track_next_get():
    if tracks:
        next = max(tracks.values(), key=lambda x: x['.priority'])
    else:
        next = None
    
    return jsonify({'next': next})

@app.route("/api/tracks/<track_id>/", methods=['DELETE'])
def track_delete(track_id):
    if track_id not in tracks:
        abort(400)

    del tracks[track_id]

    return '', 204

@app.route("/")
def vote_html():
    return render_template('vote.html')

@app.route('/static/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)
