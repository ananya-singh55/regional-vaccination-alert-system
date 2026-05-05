import pandas as pd
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

RAW_DATA_PATH = os.path.join(DATA_DIR, 'child_immunization_dataset.xls')
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_district_data.csv')

def preprocess_data():
    print("Loading raw Excel data...")
    try:
        df = pd.read_excel(RAW_DATA_PATH, engine='xlrd')
    except Exception as e:
        print(f"Error loading data: {e}. Please ensure the file is named correctly and inside the 'data' folder.")
        return

    print("Data loaded successfully. Cleaning and engineering features...")
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)
    df['dropout_gap_percent'] = ((df['BCG'] - df['T_FI_9_11']) / df['BCG']).clip(lower=0) * 100
    df['dropout_gap_percent'] = df['dropout_gap_percent'].fillna(0)
    df['asha_efficiency_ratio'] = (df['IS_ASHA'] / df['POPULATION']) * 1000  # per 1000 people
    df['asha_efficiency_ratio'] = df['asha_efficiency_ratio'].fillna(0)

    if 'IMR' in df.columns:
        df['IMR_TARGET'] = df['IMR'].astype(str).str.strip().str.upper()
        df['IMR_TARGET_NUM'] = df['IMR_TARGET'].map({'HIGH': 1, 'LOW': 0})
        df['IMR_TARGET_NUM'] = df['IMR_TARGET_NUM'].fillna(0).astype(int)
    else:
        print("Warning: 'IMR' column not found in dataset. Target variable cannot be created.")
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Preprocessing complete! Cleaned data saved to: {PROCESSED_DATA_PATH}")
    print(f"Total Districts Processed: {len(df)}")

if __name__ == "__main__":
    preprocess_data()