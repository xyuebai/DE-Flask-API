from transformation import (
    df_transformation,
    remove_outliers,
    normalization,
    get_numeric_cols,
    read_csv
)
from transformation import NORMALIZATION_MAX
import pandas as pd
import unittest

file_playlists = "playlists.csv"

class TestTransformationMethods(unittest.TestCase):
    def setUp(self):
        self.df = read_csv(file_playlists)
        self.assertEqual(self.df.shape[0],12667)
        self.assertEqual(self.df.shape[1],26)
    
    def test_df_transformation(self):
        df = df_transformation(self.df)
        self.assertEqual(df.isnull().sum().sum(),0)
    
    def test_df_normalization(self):
        numeric_cols = get_numeric_cols(self.df)
        df_numeric = (self.df[numeric_cols])
        df_numeric = normalization(df_numeric, NORMALIZATION_MAX)
        # Value range check after normalization
        assert df_numeric.max().max() <= NORMALIZATION_MAX
        assert df_numeric.min().min() >= 0

if __name__ == '__main__':
    unittest.main()




