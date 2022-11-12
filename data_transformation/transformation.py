from configparser import ConfigParser
import csv
import pandas as pd
import numpy as np
import json

config_object = ConfigParser()
config_object.read("../config.ini")

file_playlists = "playlists.csv"
file_palylisttracks = "playlist_tracks.csv"

# Get environemnt parameters
config = config_object["ENV-VAR"]
NORMALIZATION_MAX = int(config["normalization_max"])
INPUT_DIR = config["data_input"]
OUTPUT_DIR = config["data_output"]


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def remove_outliers(df, num_cols):
    """Remove outliers from the dataframe and return a dataframe

    Keyword arguments:
    df -- dataframe
    num_cols -- lists of numerical columns
    """
    result_df = df.copy()
    for cols in num_cols:
        Q1 = result_df[cols].quantile(0.02)
        Q3 = result_df[cols].quantile(0.98)
        IQR = Q3 - Q1
        result_df = result_df[~(
            (result_df[cols] < (Q1 - 1.5 * IQR)) | (result_df[cols] > (Q3 + 1.5 * IQR)))]
    return result_df


def df_transformation(df):
    """Clean data frame and fill na value and return a dataframe

    Keyword arguments:
    df -- dataframe
    """
    result_df = df.copy()
    result_df[['followed_by']] = result_df[['followed_by']].apply(
        pd.to_numeric, errors='coerce')   # force datatype conversion
    result_df["name"] = result_df["name"].fillna(
        "NameEmpty")  # fill null value in col "name"
    result_df = result_df.dropna()  # drop rows contain null value
    return result_df


def normalization(df, normalization_factor=100):
    """normalize numerical coloums in dataframe from 0-factor
    return the normalized dataframe

    Keyword arguments:
    df -- dataframe
    normalization_factor -- the power for normalization
    """
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (
            (df[feature_name] - min_value) / (max_value - min_value)) * normalization_factor
    return result


def play_tracks_summary(df):
    """Print staticis for table 
    return a dictionary of stats

    Keyword arguments:
    df -- dataframe
    """
    tracks_summary_dict = {"no_unique_playlists": "", "no_unique_tracks": "", "min_tracks": "",
                           "avg_tracks": "", "max_tracks": ""}

    tracks_summary_dict["no_unique_playlists"] = len(
        pd.unique(df["playlist_id"]))
    print("Total number of playlists:", str(
        tracks_summary_dict["no_unique_playlists"]))

    tracks_summary_dict["no_unique_tracks"] = len(pd.unique(df["track_id"]))
    print("Total number of unique tracks:", str(
        tracks_summary_dict["no_unique_tracks"]))

    tracks_summary_dict["min_tracks"] = df.groupby(
        ['playlist_id'])['playlist_id'].count().min()
    print("Minimum number of tracks of all playlists",
          str(tracks_summary_dict["min_tracks"]))

    tracks_summary_dict["avg_tracks"] = df.groupby(
        ['playlist_id'])['playlist_id'].count().mean()
    print("Average number of tracks of all playlists",
          str(tracks_summary_dict["avg_tracks"]))

    tracks_summary_dict["max_tracks"] = df.groupby(
        ['playlist_id'])['playlist_id'].count().max()
    print("Maximum number of tracks of all playlists",
          str(tracks_summary_dict["max_tracks"]))
    return tracks_summary_dict


def write_df_to_csv(df, filename, sep=";"):
    """Save dataframe to csv

    Keyword arguments:
    df -- dataframe
    filename -- output filename
    sep -- separator
    """
    df.to_csv(OUTPUT_DIR+filename, sep=sep, index=False)


def read_csv(filename, sep=";"):
    """Read csv and return a dataframe

    Keyword arguments:
    filename -- filename
    sep -- separator
    """
    df = pd.read_csv(INPUT_DIR+filename, sep=sep)
    return df


def get_numeric_cols(df):
    """Get numerical cols from dataframe return a list of numerical cols nam

    Keyword arguments:
    df -- dataframe
    """
    return df.select_dtypes(include=np.number).columns.to_list()


def main():
    # Load csv file into pandas dataframe
    play_lists_raw_df = read_csv(file_playlists, ";")
    # Clean dataframe
    play_lists_df = df_transformation(play_lists_raw_df)
    
    # Remove outliers from dataframe
    numeric_cols = get_numeric_cols(play_lists_df)
    play_lists_df = remove_outliers(play_lists_df, numeric_cols)
    
    # Apply normalization on dataframe with numerical cols
    df_numeric = play_lists_df[numeric_cols]
    df_numeric = normalization(df_numeric, NORMALIZATION_MAX)
    
    # save the result for question 1.1: playlists_normalized.csv
    write_df_to_csv(df_numeric, "playlists_normalized.csv")

    # save the result for question 1.1: playlists_normalized.csv
    play_lists_df[numeric_cols] = df_numeric
    play_lists_df = play_lists_df.drop(columns=["name"])
    write_df_to_csv(play_lists_df, "playlists_normalized_id.csv")

    df_average = df_numeric.mean().to_frame().transpose()
    # save the result for question 1.2: playlists_average.csv
    write_df_to_csv(df_average, "playlists_average.csv")

    tracks_raw_df = read_csv(file_palylisttracks, sep=";")
    tracks_summary_dict = play_tracks_summary(tracks_raw_df)
    tracks_summary_json = json.dumps(tracks_summary_dict, cls=NpEncoder)
    with open(OUTPUT_DIR + "playlist_tracks_stats.json", 'w') as fp:
        # save the result for question 2.1: playlist_tracks_stats.json
        fp.write(tracks_summary_json)

    play_lists_join_df = play_lists_raw_df[["playlist_id", "name"]]
    tracks_lists_join = pd.merge(
        tracks_raw_df, play_lists_join_df, on=["playlist_id"])
    # save the result for question 2.2: list_tracks_join.csv
    write_df_to_csv(tracks_lists_join, "list_tracks_join.csv")


if __name__ == "__main__":
    main()
