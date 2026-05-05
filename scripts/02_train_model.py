import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODEL_DIR = os.path.join(BASE_DIR, 'models')

PROCESSED_DATA_PATH = os.path.join(DATA_DIR, 'processed_district_data.csv')
MODEL_PATH = os.path.join(MODEL_DIR, 'district_risk_classifier.pkl')

def train_model():
    print("Loading processed data...")
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH)
    except Exception as e:
        print(f"Error loading data: {e}. Please ensure step 1 was completed.")
        return
    features = [
        'POPULATION',
        'BCG',
        'IS_ASHA',
        'dropout_gap_percent',
        'asha_efficiency_ratio'
    ]
    target = 'IMR_TARGET_NUM'

    if target not in df.columns:
        print(f"Target column '{target}' not found. Cannot train model.")
        return

    print("Preparing training data...")
    X = df[features]
    y = df[target]
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_train, y_train)
    print("Evaluating model performance...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"\n" + "="*30)
    print(f"Accuracy: {acc * 100:.2f}%")
    print("="*30)
    print("Classification Report:")
    unique_labels = sorted(y_test.unique())
    target_names = ['LOW Risk (0)', 'HIGH Risk (1)'] if len(unique_labels) == 2 else [str(l) for l in unique_labels]
    print(classification_report(y_test, y_pred, target_names=target_names))
    print("Saving the trained model...")
    joblib.dump(model, MODEL_PATH)

    feature_names_path = os.path.join(MODEL_DIR, 'model_features.pkl')
    joblib.dump(features, feature_names_path)

    print(f"Model saved successfully to: {MODEL_PATH}")

if __name__ == "__main__":
    train_model()