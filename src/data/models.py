from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime
from .database import AppBase


class ForecastResult(AppBase):
    """Model for storing forecast results."""
    __tablename__ = "forecast_results"

    id = Column(Integer, primary_key=True)
    forecast_type = Column(String, nullable=False)  # cash_flow, revenue, expenses, profit
    prediction_date = Column(DateTime, nullable=False)
    forecast_date = Column(DateTime, nullable=False)
    predicted_value = Column(Float, nullable=False)
    confidence_interval = Column(JSON)  # Store lower and upper bounds
    model_version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModelMetrics(AppBase):
    """Model for storing model performance metrics."""
    __tablename__ = "model_metrics"

    id = Column(Integer, primary_key=True)
    forecast_type = Column(String, nullable=False)
    model_version = Column(String, nullable=False)
    metrics = Column(JSON)  # Store MSE, RMSE, MAE, etc.
    evaluation_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) 