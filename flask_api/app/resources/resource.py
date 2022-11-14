from flask_restful import Resource
from flask import abort
from configparser import ConfigParser
import pandas as pd
import json

config_object = ConfigParser()
config_object.read("../../config.ini")
config = config_object["SETTINGS"]
NORMALIZATION_MAX = int(config["normalization_max"])

df_playlist = pd.read_csv("../../output/playlists_normalized_id.csv", sep= ";")
df_list_track = pd.read_csv("../../output/list_tracks_join.csv", sep= ";")

class PlayList(Resource):
    def get(self, playlist_id):
        result_df = df_playlist[df_playlist["playlist_id"] == playlist_id]
        if result_df.empty:
            abort(404, description="Playlist_id not found")
        result = result_df.to_json(orient='records')
        parsed = json.loads(result)
        return parsed[0]

class TrackList(Resource):
    def get(self, playlist_id):
        result_df = df_list_track[df_list_track["playlist_id"] == playlist_id]
        if result_df.empty:
            abort(404, description="Playlist_id not found")
        result = result_df.to_json(orient='records')
        parsed = json.loads(result)
        response = {"playlist_id": playlist_id, "name": parsed[0]["name"], "track_id":[]}
        for item in parsed: response["track_id"].append(item["track_id"])
        return response

class MaxValue(Resource):
    def get(self):
        return {"max_value": str(NORMALIZATION_MAX)}