from flask import Flask, jsonify
from flask_restful import Api
from resources.resource import PlayList, TrackList, MaxValue

app = Flask(__name__)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


api = Api(app)

api.add_resource(PlayList, '/playlist/<string:playlist_id>')
api.add_resource(TrackList, '/tracklist/<string:playlist_id>')
api.add_resource(MaxValue, '/max_value')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)  # important to mention debug=True