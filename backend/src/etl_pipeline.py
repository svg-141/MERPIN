import pandas as pd
import glob
import os

def run_etl_pipeline(csv_folder_path: str) -> pd.DataFrame:
    """
    Executes the ETL pipeline to process raw sales data from CSV files.

    Args:
        csv_folder_path (str): The absolute path to the folder containing the CSV files.

    Returns:
        pd.DataFrame: A DataFrame with the processed time series data,
                      containing 'ds' (date) and 'y' (daily sales revenue) columns.
    """
    # 1. Ingesta Masiva y Consolidación de Archivos
    all_files = glob.glob(os.path.join(csv_folder_path, "*.csv"))
    
    if not all_files:
        raise ValueError(f"No CSV files found in the specified folder: {csv_folder_path}")

    df_list = []
    for f in all_files:
        df = pd.read_csv(f)
        df_list.append(df)

    df_consolidated = pd.concat(df_list, ignore_index=True)

    # 2. Limpieza y Normalización de Datos
    # Drop rows with any NaN values that might interfere with conversion
    df_consolidated.dropna(inplace=True)

    # Convert 'Order Date' to datetime
    # Use errors='coerce' to turn unparseable dates into NaT (Not a Time)
    df_consolidated['Order Date'] = pd.to_datetime(df_consolidated['Order Date'], errors='coerce')
    df_consolidated.dropna(subset=['Order Date'], inplace=True) # Drop rows where date conversion failed

    # Clean and convert 'Price Each' and 'Quantity Ordered' to numeric
    # Remove non-numeric characters (e.g., commas, currency symbols if any)
    df_consolidated['Price Each'] = df_consolidated['Price Each'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df_consolidated['Quantity Ordered'] = df_consolidated['Quantity Ordered'].astype(str).str.replace(r'[^\d.]', '', regex=True)

    # Convert to numeric, coercing errors to NaN
    df_consolidated['Price Each'] = pd.to_numeric(df_consolidated['Price Each'], errors='coerce')
    df_consolidated['Quantity Ordered'] = pd.to_numeric(df_consolidated['Quantity Ordered'], errors='coerce')

    # Drop rows where numeric conversion failed
    df_consolidated.dropna(subset=['Price Each', 'Quantity Ordered'], inplace=True)

    # Ensure Quantity Ordered is integer (as it represents count)
    df_consolidated['Quantity Ordered'] = df_consolidated['Quantity Ordered'].astype(int)

    # 3. Feature Engineering y Agregación Temporal
    # Calculate Sales Revenue
    df_consolidated['Sales Revenue'] = df_consolidated['Quantity Ordered'] * df_consolidated['Price Each']

    # Aggregate daily sales revenue
    df_ts = df_consolidated.groupby('Order Date')['Sales Revenue'].sum().reset_index()
    df_ts.columns = ['ds', 'y']

    # Ensure continuity of the time series by filling missing dates with y=0
    # First, set 'ds' as index to use resample
    df_ts = df_ts.set_index('ds')
    # Resample to daily frequency and fill missing values with 0
    df_ts = df_ts.resample('D').sum().fillna(0).reset_index()

    return df_ts, df_consolidated

if __name__ == '__main__':
    # Example usage (assuming CSVs are in a 'CSV' folder relative to this script)
    current_dir = os.path.dirname(__file__)
    csv_data_path = os.path.join(current_dir, '..', 'CSV')
    
    try:
        processed_df, full_df = run_etl_pipeline(csv_data_path)
        print("ETL Pipeline completed successfully. Head of the processed DataFrame:")
        print(processed_df.head())
        print("\nTail of the processed DataFrame:")
        print(processed_df.tail())
        print(f"\nTotal rows in processed DataFrame: {len(processed_df)}")
        print("\nHead of the full (non-aggregated) DataFrame:")
        print(full_df.head())
    except ValueError as e:
        print(f"Error during ETL pipeline: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}") 