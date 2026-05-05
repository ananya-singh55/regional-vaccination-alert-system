import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed_district_data.csv')
VISUALS_DIR = os.path.join(BASE_DIR, 'outputs', 'visuals')

os.makedirs(VISUALS_DIR, exist_ok=True)

def generate_visuals():
    print("Loading processed data for visualization...")
    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    if 'DISTRICT' in df.columns and 'STATE' in df.columns:
        df['Location'] = df['DISTRICT'] + " (" + df['STATE'] + ")"
    else:
        df['Location'] = "Unknown District"

    sns.set_theme(style="whitegrid")

    # Chart 1: Top 10 High-Risk Districts (By Dropout Gap)

    print("Generating Chart 1: Top 10 High-Risk Districts...")
    plt.figure(figsize=(12, 8))
    top_10 = df.sort_values(by='dropout_gap_percent', ascending=False).head(10)
    
    ax1 = sns.barplot(data=top_10, x='dropout_gap_percent', y='Location', palette='Reds_r')
    plt.title('Top 10 High-Risk Districts (Immunization Dropout Gap)', fontsize=16, pad=15)
    plt.xlabel('Dropout Gap (%) - Difference between BCG Starts and Full Immunization', fontsize=12)
    plt.ylabel('District (State)', fontsize=12)
    
    for i in ax1.containers:
        ax1.bar_label(i, fmt='%.1f%%', padding=5)

    chart1_path = os.path.join(VISUALS_DIR, 'top_10_risk_districts.png')
    plt.tight_layout()
    plt.savefig(chart1_path, dpi=300)  
    plt.close()

    # Chart 2: Infrastructure Impact (ASHA vs Dropout)

    print("Generating Chart 2: Infrastructure Efficiency Impact...")
    plt.figure(figsize=(10, 6))
    plot_df = df[df['asha_efficiency_ratio'] < df['asha_efficiency_ratio'].quantile(0.95)]
    
    sns.scatterplot(
        data=plot_df, 
        x='asha_efficiency_ratio', 
        y='dropout_gap_percent', 
        hue='IMR_TARGET_NUM',
        palette={0: 'blue', 1: 'red'},
        alpha=0.6
    )
    
    plt.title('Impact of ASHA Worker Efficiency on Dropout Rates', fontsize=14)
    plt.xlabel('ASHA Worker Sessions (Per 1000 Population)', fontsize=12)
    plt.ylabel('Dropout Gap (%)', fontsize=12)
    plt.legend(title='Infant Mortality Risk')
    
    chart2_path = os.path.join(VISUALS_DIR, 'infrastructure_impact_scatter.png')
    plt.tight_layout()
    plt.savefig(chart2_path, dpi=300)
    plt.close()

    print(f"Visuals generated successfully! Check the '{VISUALS_DIR}' folder.")

if __name__ == "__main__":
    generate_visuals()