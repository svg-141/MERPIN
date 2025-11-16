from fastapi import FastAPI, HTTPException, Response, Path
from fastapi.responses import StreamingResponse, FileResponse
from starlette.background import BackgroundTask
from pydantic import BaseModel
import pandas as pd
import io
import matplotlib
matplotlib.use('Agg') # Must be called before import pyplot as plt

import matplotlib.pyplot as plt
import base64
import os
import json

# Import ETL and Model Training functions
from etl_pipeline import run_etl_pipeline
from model_training import train_and_evaluate_model

# Initialize FastAPI app
app = FastAPI(
    title="Sales Prediction API",
    description="API for predicting sales of technological equipment and providing analytical insights.",
    version="1.0.0"
)

# Global variables to hold processed data and trained model
# These will be loaded on startup
processed_data_df: pd.DataFrame = pd.DataFrame()
trained_prophet_model = None
# Placeholder for the full historical data (before aggregation) for bestsellers analysis
full_historical_df: pd.DataFrame = pd.DataFrame() 

# Define Pydantic models for request/response
class PredictionResponse(BaseModel):
    ds: str
    yhat: float
    yhat_lower: float
    yhat_upper: float

class ForecastResponse(BaseModel):
    forecast: list[PredictionResponse]
    metrics: dict | None = None

class Bestseller(BaseModel):
    product: str
    total_sales_revenue: float

class BestsellersResponse(BaseModel):
    bestsellers: list[Bestseller]

class ChartBase64Response(BaseModel):
    image_base64: str
    media_type: str = "image/png"
    metrics: dict | None = None

@app.on_event("startup")
async def load_data_and_train_model():
    """
    Load data, run ETL, and train the model on application startup.
    """
    global processed_data_df, trained_prophet_model, full_historical_df
    
    current_dir = os.path.dirname(__file__)
    csv_data_path = os.path.join(current_dir, '..', 'CSV')

    try:
        print("API Startup: Running ETL pipeline...")
        processed_data_df, full_historical_df = run_etl_pipeline(csv_data_path)
        print("API Startup: ETL pipeline completed.")

        print("API Startup: Training model...")
        # Train model with a reasonable forecast period and test size
        trained_prophet_model, _, _, _ = train_and_evaluate_model(processed_data_df, periods_to_forecast=90, test_size_months=3)
        print("API Startup: Model training completed.")

    except Exception as e:
        print(f"API Startup Error: Failed to load data or train model: {e}")
        # Depending on criticality, you might want to exit or set a flag
        # indicating the API is not fully functional.
        raise HTTPException(status_code=500, detail=f"Failed to initialize API: {e}")

@app.get("/predict/sales/{days}", response_model=ForecastResponse)
async def predict_sales(days: int = Path(..., gt=0, description="Number of days to forecast")):
    """
    Predicts sales for the next 'days' using the trained Prophet model.
    """
    if trained_prophet_model is None or processed_data_df.empty:
        raise HTTPException(status_code=503, detail="Model not loaded or data not processed yet.")

    # Create future dataframe for prediction
    future = trained_prophet_model.make_future_dataframe(periods=days, include_history=False)
    forecast = trained_prophet_model.predict(future)

    # Extract relevant forecast columns
    predictions = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
    
    # Convert datetime objects to string for JSON serialization
    for p in predictions:
        p['ds'] = p['ds'].strftime('%Y-%m-%d')

    return ForecastResponse(forecast=predictions)

@app.get("/analysis/bestsellers/{top_n}", response_model=BestsellersResponse)
async def get_bestsellers(top_n: int = Path(..., gt=0, description="Number of top-selling products to retrieve")):
    """
    Identifies the top N best-selling products based on historical sales revenue.
    """
    if full_historical_df.empty:
        raise HTTPException(status_code=503, detail="Historical data not loaded yet for analysis.")

    bestsellers_df = full_historical_df.groupby('Product')['Sales Revenue'].sum().nlargest(top_n).reset_index()
    bestsellers = bestsellers_df.rename(columns={'Product': 'product', 'Sales Revenue': 'total_sales_revenue'}).to_dict(orient='records')

    return BestsellersResponse(bestsellers=bestsellers)

@app.get("/chart/forecast/{days}", response_class=Response)
async def get_forecast_chart(days: int = Path(..., description="Number of days to forecast for the chart")):
    """
    Generates and returns a PNG image of the sales forecast chart.
    """
    if trained_prophet_model is None or processed_data_df.empty:
        raise HTTPException(status_code=503, detail="Model not loaded or data not processed yet.")

    future = trained_prophet_model.make_future_dataframe(periods=days, include_history=True)
    forecast = trained_prophet_model.predict(future)

    fig, ax = plt.subplots(figsize=(10, 6))
    trained_prophet_model.plot(forecast, ax=ax)
    ax.set_title('Sales Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales Revenue')
    fig.canvas.draw() # Explicitly draw the canvas

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    plt.close(fig) # Close the figure to free memory
    img_buf.seek(0)
    return StreamingResponse(img_buf, media_type="image/png")

@app.get("/chart/forecast_base64", response_model=ChartBase64Response)
async def get_forecast_chart_base64(days: int = 90): # Default to 90 days if not specified
    """
    Generates a sales forecast chart and returns it as a Base64 encoded string.
    """
    if trained_prophet_model is None or processed_data_df.empty:
        raise HTTPException(status_code=503, detail="Model not loaded or data not processed yet.")

    if days <= 0:
        raise HTTPException(status_code=400, detail="Days must be a positive integer.")

    future = trained_prophet_model.make_future_dataframe(periods=days, include_history=True)
    forecast = trained_prophet_model.predict(future)

    fig, ax = plt.subplots(figsize=(10, 6))
    trained_prophet_model.plot(forecast, ax=ax)
    ax.set_title('Sales Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales Revenue')
    fig.canvas.draw() # Explicitly draw the canvas

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    plt.close(fig) # Close the figure to free memory
    img_buf.seek(0)

    img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')

    # Optionally, include metrics here if desired, but for simplicity, we'll omit for now
    # metrics = {"MAPE": 10.5, "RMSE": 200.0} # Placeholder

    return ChartBase64Response(image_base64=img_base64, media_type="image/png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)