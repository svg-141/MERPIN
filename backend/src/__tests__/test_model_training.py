import pandas as pd
import os
import sys
import unittest
from unittest.mock import patch
import numpy as np

# Add the src directory to the Python path to allow importing model_training
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model_training import train_and_evaluate_model

class TestModelTraining(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up a dummy time series DataFrame for testing."""
        dates = pd.to_datetime(pd.date_range(start='2022-01-01', periods=365 * 2, freq='D')) # 2 years of daily data
        sales = np.random.rand(365 * 2) * 100 + np.sin(np.arange(365 * 2) / 30) * 50 + 100 # Base sales + seasonality
        
        # Add some trend
        sales = sales + np.arange(365 * 2) * 0.1

        # Add a spike for a "holiday"
        sales[30] += 200 # Jan 31st
        sales[365 + 30] += 200 # Jan 31st of next year

        cls.dummy_df_ts = pd.DataFrame({'ds': dates, 'y': sales})

    def test_train_and_evaluate_model_basic(self):
        """Test if the function returns expected outputs and types."""
        model, forecast, metrics, test_df = train_and_evaluate_model(self.dummy_df_ts, periods_to_forecast=30, test_size_months=1)
        
        self.assertIsNotNone(model)
        self.assertIsInstance(forecast, pd.DataFrame)
        self.assertIn('ds', forecast.columns)
        self.assertIn('yhat', forecast.columns)
        self.assertIsInstance(metrics, dict)
        self.assertIn('MAPE', metrics)
        self.assertIn('RMSE', metrics)
        self.assertIsInstance(test_df, pd.DataFrame)

    def test_train_and_evaluate_model_empty_input(self):
        """Test behavior with an empty input DataFrame."""
        with self.assertRaises(ValueError) as cm:
            train_and_evaluate_model(pd.DataFrame({'ds': [], 'y': []}), periods_to_forecast=30, test_size_months=1)
        self.assertIn("Input DataFrame for model training is empty.", str(cm.exception))

    def test_train_and_evaluate_model_not_enough_data_for_test_set(self):
        """Test behavior when not enough data for the specified test set size."""
        small_df = pd.DataFrame({
            'ds': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03']),
            'y': [10, 20, 30]
        })
        with self.assertRaises(ValueError) as cm:
            train_and_evaluate_model(small_df, periods_to_forecast=1, test_size_months=6) # 6 months test size on 3 days data
        self.assertIn("Training DataFrame is empty.", str(cm.exception))

    def test_train_and_evaluate_model_forecast_length(self):
        """Test if the forecast DataFrame has the correct number of future periods."""
        periods = 30
        model, forecast, metrics, test_df = train_and_evaluate_model(self.dummy_df_ts, periods_to_forecast=periods, test_size_months=1)
        
        # Calculate the actual train_df length based on the split logic in model_training.py
        split_date = self.dummy_df_ts['ds'].max() - pd.DateOffset(months=1) # test_size_months=1
        train_df_length = len(self.dummy_df_ts[self.dummy_df_ts['ds'] <= split_date])

        expected_forecast_length = train_df_length + periods
        self.assertEqual(len(forecast), expected_forecast_length)

    def test_train_and_evaluate_model_metrics_calculation(self):
        """Test if metrics are calculated when test_df is not empty."""
        model, forecast, metrics, test_df = train_and_evaluate_model(self.dummy_df_ts, periods_to_forecast=30, test_size_months=1)
        
        self.assertIsNotNone(metrics.get('MAPE'))
        self.assertIsNotNone(metrics.get('RMSE'))
        self.assertIsInstance(metrics['MAPE'], float)
        self.assertIsInstance(metrics['RMSE'], float)

    @patch('model_training.Prophet')
    def test_prophet_model_configuration(self, MockProphet):
        """Test if Prophet is initialized with correct parameters and predict is called."""
        # Configure the mock Prophet instance
        mock_instance = MockProphet.return_value
        
        # Mock the predict method to return a DataFrame with expected columns
        mock_forecast_df = pd.DataFrame({
            'ds': pd.to_datetime(pd.date_range(start='2022-01-01', periods=len(self.dummy_df_ts) + 30, freq='D')),
            'yhat': np.random.rand(len(self.dummy_df_ts) + 30),
            'yhat_lower': np.random.rand(len(self.dummy_df_ts) + 30),
            'yhat_upper': np.random.rand(len(self.dummy_df_ts) + 30)
        })
        mock_instance.predict.return_value = mock_forecast_df

        train_and_evaluate_model(self.dummy_df_ts, periods_to_forecast=30, test_size_months=1)
        
        MockProphet.assert_called_once_with(
            seasonality_mode='multiplicative',
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False
        )
        mock_instance.fit.assert_called_once()
        mock_instance.make_future_dataframe.assert_called_once()
        mock_instance.predict.assert_called_once()

if __name__ == '__main__':
    unittest.main()
