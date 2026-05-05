import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed_district_data.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'district_risk_classifier.pkl')
VISUALS_DIR = os.path.join(BASE_DIR, 'outputs', 'visuals')

def generate_confusion_matrix():
    print("Loading model and data...")
    try:
        df = pd.read_csv(DATA_PATH)
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error: {e}")
        return

    features = ['POPULATION', 'BCG', 'IS_ASHA', 'dropout_gap_percent', 'asha_efficiency_ratio']
    X = df[features].fillna(0)
    y = df['IMR_TARGET_NUM']

    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    y_pred = model.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Low Risk (0)', 'High Risk (1)'], 
                yticklabels=['Low Risk (0)', 'High Risk (1)'])
    
    plt.title('Model Performance: Confusion Matrix', fontsize=14, pad=20)
    plt.ylabel('Actual Category', fontsize=12)
    plt.xlabel('Predicted Category', fontsize=12)

    output_path = os.path.join(VISUALS_DIR, 'confusion_matrix.png')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Confusion Matrix generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_confusion_matrix()