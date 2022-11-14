from src.data_toolkit import DataTransformation
import unittest

file_playlists = "playlists.csv"

class TestTransformationMethods(unittest.TestCase):
    def setUp(self):
        # Load data check
        df = DataTransformation.read_csv(file_playlists)
        self.dt = DataTransformation(df)
        self.assertEqual(df.shape[0],12667)
        self.assertEqual(df.shape[1],26)
    
    def test_df_clean(self):
        # Null value check
        self.dt.df_clean()
        self.assertEqual(self.dt.df.isnull().sum().sum(),0)
    
    def test_df_normalization(self):
        # Value range check after normalization
        self.dt.df_clean()
        self.dt.normalization()
        play_lists_normalized_num = self.dt.df[self.dt.num_cols]
        assert play_lists_normalized_num.max().max() <= int(DataTransformation.NORMALIZATION_MAX)
        assert play_lists_normalized_num.min().min() >= 0

if __name__ == '__main__':
    unittest.main()




