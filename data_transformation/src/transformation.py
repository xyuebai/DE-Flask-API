import pandas as pd
import numpy as np
import json
from data_toolkit import DataTransformation
import logging
import os

file_playlists = "playlists.csv"
file_palylisttracks = "playlist_tracks.csv"
file_log = "data_transformation.log"


LOG_DIR = DataTransformation.LOG_DIR
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(filename=LOG_DIR+file_log,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def play_tracks_summary(df):
    """Print staticis for table 
    return a dictionary of stats

    Keyword arguments:
    df -- dataframe
    """
    tracks_summary_dict = {"no_unique_playlists": "", "no_unique_tracks": "", "min_tracks": "",
                           "avg_tracks": "", "max_tracks": ""}

    tracks_summary_dict["no_unique_playlists"] = len(pd.unique(df["playlist_id"]))

    logging.warning("Total number of playlists: %s",
                    str(tracks_summary_dict["no_unique_playlists"]))

    tracks_summary_dict["no_unique_tracks"] = len(pd.unique(df["track_id"]))
    logging.warning("Total number of unique tracks: %s",
                    str(tracks_summary_dict["no_unique_tracks"]))

    tracks_summary_dict["min_tracks"] = df.groupby(
        ['playlist_id'])['playlist_id'].count().min()
    logging.warning("Minimum number of tracks of all playlists: %s",
                    str(tracks_summary_dict["min_tracks"]))

    tracks_summary_dict["avg_tracks"] = df.groupby(
        ['playlist_id'])['playlist_id'].count().mean()
    logging.warning("Average number of tracks of all playlists: %s",
                    str(tracks_summary_dict["avg_tracks"]))

    tracks_summary_dict["max_tracks"] = df.groupby(
        ['playlist_id'])['playlist_id'].count().max()
    logging.warning("Maximum number of tracks of all playlists: %s",
                    str(tracks_summary_dict["max_tracks"]))

    tracks_summary_json = json.dumps(tracks_summary_dict, cls=NpEncoder)

    return tracks_summary_json


def main():
    # Read csv
    play_lists_raw_df = DataTransformation.read_csv(file_playlists)
    logging.warning("Load File: " + file_playlists)

    # Initialize class and read csv file
    dt_pl = DataTransformation(play_lists_raw_df)
    dt_pl.df_clean()    # data frame clean
    dt_pl.remove_outliers()  # reomove outliers
    play_lists_normalized = dt_pl.normalization()   # apply normalization
    logging.warning("Dataframe Normalization Done")

    # save the result for question 1.1: playlists_normalized.csv
    play_lists_normalized_num = play_lists_normalized[dt_pl.num_cols]
    DataTransformation.write_df_to_csv(
        play_lists_normalized_num, "playlists_normalized.csv")
    logging.warning("Normalized Dataframe Saved")

    # save the result for question 1.1: playlists_normalized_id.csv
    play_lists_df = play_lists_normalized.drop(columns=["name"])
    DataTransformation.write_df_to_csv(
        play_lists_df, "playlists_normalized_id.csv")

    # save the result for question 1.2: playlists_average.csv
    df_average = play_lists_normalized_num.mean().to_frame().transpose()
    DataTransformation.write_df_to_csv(df_average, "playlists_average.csv")
    logging.warning("Normalized Dataframe Average Saved")

    # Initialize class and read csv file
    play_track_raw_df = DataTransformation.read_csv(file_palylisttracks)
    logging.warning("Load File: " + file_palylisttracks)

    tracks_summary_json = play_tracks_summary(play_track_raw_df)
    with open(DataTransformation.OUTPUT_DIR + "playlist_tracks_stats.json", 'w') as fp:
        # save the result for question 2.1: playlist_tracks_stats.json
        fp.write(tracks_summary_json)
    logging.warning("Json Saved")

    play_lists_join_df = play_lists_raw_df[["playlist_id", "name"]]
    tracks_lists_join = pd.merge(
        play_track_raw_df, play_lists_join_df, on=["playlist_id"])
    # save the result for question 2.2: list_tracks_join.csv
    DataTransformation.write_df_to_csv(
        tracks_lists_join, "list_tracks_join.csv")
    logging.warning("Joined Result Saved")


if __name__ == "__main__":
    main()
