import pandas as pd
import os
import sys
import unittest

# Add the src directory to the Python path to allow importing etl_pipeline
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from etl_pipeline import run_etl_pipeline

class TestEtlPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up for test methods."""
        cls.test_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'test_data'))
        cls.dummy_csv_path = os.path.join(cls.test_data_dir, 'Sales_Test.csv')

    def test_run_etl_pipeline_basic(self):
        """Test if the pipeline runs and returns two DataFrames with expected columns."""
        df_ts, df_full = run_etl_pipeline(self.test_data_dir)
        self.assertIsInstance(df_ts, pd.DataFrame)
        self.assertIn('ds', df_ts.columns)
        self.assertIn('y', df_ts.columns)
        self.assertGreater(len(df_ts), 0)

        self.assertIsInstance(df_full, pd.DataFrame)
        self.assertIn('Order ID', df_full.columns)
        self.assertIn('Product', df_full.columns)
        self.assertIn('Sales Revenue', df_full.columns)
        self.assertGreater(len(df_full), 0)

    def test_run_etl_pipeline_data_types(self):
        """Test if the 'ds' column is datetime and 'y' is numeric in the aggregated DF."""
        df_ts, _ = run_etl_pipeline(self.test_data_dir)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_ts['ds']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df_ts['y']))

    def test_run_etl_pipeline_sales_revenue_calculation(self):
        """Test if sales revenue is correctly aggregated."""
        df_ts, _ = run_etl_pipeline(self.test_data_dir)
        # Expected sales for 01/01/2023: (2*10.00) + (1*25.50) = 20 + 25.50 = 45.50
        # Expected sales for 01/02/2023: (3*10.00) = 30.00
        # Expected sales for 01/03/2023: (1*50.00) + (1*10.00) = 50 + 10 = 60.00
        # Expected sales for 01/04/2023: (2*25.50) = 51.00

        self.assertAlmostEqual(df_ts[df_ts['ds'] == '2023-01-01']['y'].iloc[0], 45.50)
        self.assertAlmostEqual(df_ts[df_ts['ds'] == '2023-01-02']['y'].iloc[0], 30.00)
        self.assertAlmostEqual(df_ts[df_ts['ds'] == '2023-01-03']['y'].iloc[0], 60.00)
        self.assertAlmostEqual(df_ts[df_ts['ds'] == '2023-01-04']['y'].iloc[0], 51.00)

    def test_run_etl_pipeline_continuity(self):
        """Test if the time series is continuous and missing days are filled with 0."""
        df_ts, _ = run_etl_pipeline(self.test_data_dir)
        # The dummy data has sales on 01/01, 01/02, 01/03, 01/04
        # The range should be from 2023-01-01 to 2023-01-04, inclusive.
        expected_dates = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'])
        
        # Check if all expected dates are present
        for date in expected_dates:
            self.assertIn(date, df_ts['ds'].values)
        
        # Check if the length of the DataFrame matches the number of days in the range
        self.assertEqual(len(df_ts), len(expected_dates))

    def test_run_etl_pipeline_no_csv_files(self):
        """Test behavior when no CSV files are found."""
        empty_dir = os.path.join(self.test_data_dir, 'empty_folder')
        os.makedirs(empty_dir, exist_ok=True)
        with self.assertRaises(ValueError) as cm:
            run_etl_pipeline(empty_dir)
        self.assertIn("No CSV files found", str(cm.exception))
        os.rmdir(empty_dir) # Clean up empty directory

if __name__ == '__main__':
    unittest.main()
