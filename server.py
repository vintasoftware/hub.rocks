from flask import Flask, request, jsonify, abort

app = Flask(__name__)

tracks = {}

@app.route("/api/tracks/", methods=['GET'])
def get_tracks():
    track_list = sorted(tracks.values(), key=lambda x: x['priority'], reverse=True)
    return jsonify({'tracks': track_list})

@app.route("/api/tracks/<track_id>/", methods=['PUT'])
def vote(track_id):
    if track_id not in tracks:
        tracks[track_id] = {
            'name': 'test name',
            'album': 'test album',
            'priority': 0
        }

    tracks[track_id]['priority'] += 1

    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
