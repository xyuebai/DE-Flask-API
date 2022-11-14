import pandas as pd
import numpy as np
import os
from configparser import ConfigParser


class DataTransformation:

    config_object = ConfigParser()
    config_object.read("../config.ini")

    # Get environemnt parameters
    config = config_object["SETTINGS"]
    NORMALIZATION_MAX = int(config["normalization_max"])
    INPUT_DIR = config["data_input"]
    OUTPUT_DIR = config["data_output"]

    def __init__(self, df) -> None:
        self.df = df
    
    def __get_numeric_cols(self):
        """Get numerical cols from dataframe return a list of numerical cols nam

        Keyword arguments:
        df -- dataframe
        """
        self.num_cols = self.df.select_dtypes(include=np.number).columns.to_list()
        return self.num_cols

    def df_clean(self):
        """Clean data frame and fill na value and return a dataframe
        Keyword arguments:
        df -- dataframe
        """
        self.df[['followed_by']] = self.df[['followed_by']].apply(
            pd.to_numeric, errors='coerce')   # force datatype conversion

        self.df["name"] = self.df["name"].fillna(
            "NameEmpty")  # fill null value in col "name"
        self.df = self.df.dropna()  # drop rows contain null value


    def remove_outliers(self):
        """Remove outliers from the dataframe and return a dataframe

        Keyword arguments:
        df -- dataframe
        num_cols -- lists of numerical columns
        """
        num_cols = self.__get_numeric_cols()
        for cols in num_cols:
            Q1 = self.df[cols].quantile(0.02)
            Q3 = self.df[cols].quantile(0.98)
            IQR = Q3 - Q1
            self.df = self.df[~(
                (self.df[cols] < (Q1 - 1.5 * IQR)) | (self.df[cols] > (Q3 + 1.5 * IQR)))]


    def normalization(self):
        """normalize numerical coloums in dataframe from 0-factor
        return the normalized dataframe

        Keyword arguments:
        df -- dataframe
        normalization_factor -- the power for normalization
        """
        num_cols = self.__get_numeric_cols()
        for feature_name in num_cols:
            max_value = self.df[feature_name].max()
            min_value = self.df[feature_name].min()
            self.df[feature_name] = (
                (self.df[feature_name] - min_value) / (max_value - min_value)) * DataTransformation.NORMALIZATION_MAX
        return self.df
    
    
    @staticmethod
    def read_csv(filename, sep=";"):
        """Read csv and return a dataframe

        Keyword arguments:
        filename -- filename
        sep -- separator
        """
        df = pd.read_csv(DataTransformation.INPUT_DIR+filename, sep=sep)
        return df

    @staticmethod
    def write_df_to_csv(df, filename, sep=";"):
        """Save dataframe to csv

        Keyword arguments:
        df -- dataframe
        filename -- output filename
        sep -- separator
        """
        
        if not os.path.exists(DataTransformation.OUTPUT_DIR):
            os.makedirs(DataTransformation.OUTPUT_DIR)
        df.to_csv(DataTransformation.OUTPUT_DIR+filename, sep=sep, index=False)












