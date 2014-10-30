from flask import Flask, jsonify, abort
import requests

app = Flask(__name__)

tracks = {}

@app.route("/api/tracks/", methods=['GET'])
def tracks_get():
    track_list = sorted(tracks.values(), key=lambda x: x['priority'], reverse=True)
    return jsonify({'tracks': track_list})

def _fetch_track_from_spotify(track_id):
    response = requests.get('https://api.spotify.com/v1/tracks/{0}'.format(track_id))
    if response.status_code == 200:
        response_json = response.json()
        return {
            'name': response_json['name'],
            'artist': ', '.join(a['name'] for a in response_json['artists']),
            'priority': 0
        }

@app.route("/api/tracks/<track_id>/", methods=['PUT'])
def track_put(track_id):
    if track_id not in tracks:
        track = _fetch_track_from_spotify(track_id)
        if not track:
            abort(400)

        tracks[track_id] = track

    tracks[track_id]['priority'] += 1

    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
