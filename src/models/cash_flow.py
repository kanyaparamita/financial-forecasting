from prophet import Prophet
import pandas as pd
from typing import Dict, Any
import numpy as np


class CashFlowModel:
    def __init__(self):
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05
        )
        self.is_trained = False

    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare data for Prophet model."""
        df = data.copy()
        df = df.rename(columns={
            'monthly_total_month': 'ds',
            'monthly_total_value': 'y'
        })
        return df

    def train(self, data: pd.DataFrame) -> None:
        """Train the Prophet model."""
        prepared_data = self.prepare_data(data)
        self.model.fit(prepared_data)
        self.is_trained = True

    def predict(
        self,
        periods: int = 30,
        include_history: bool = True
    ) -> Dict[str, Any]:
        """Make predictions with the trained model."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        future = self.model.make_future_dataframe(
            periods=periods,
            include_history=include_history
        )
        forecast = self.model.predict(future)

        return {
            'dates': forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
            'predictions': forecast['yhat'].tolist(),
            'lower_bound': forecast['yhat_lower'].tolist(),
            'upper_bound': forecast['yhat_upper'].tolist()
        }

    def evaluate(self, actual: pd.Series, predicted: pd.Series) -> Dict[str, float]:
        """Evaluate model performance."""
        mse = np.mean((actual - predicted) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(actual - predicted))
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae
        } 