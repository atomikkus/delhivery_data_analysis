# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import json
import os
warnings.filterwarnings('ignore')

# Create directories for outputs if they don't exist
os.makedirs('plots', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

def preprocess_data(df):
    """
    Preprocess the data by converting timestamps and handling missing values
    """
    # Convert timestamp columns to datetime
    timestamp_columns = ['trip_creation_time', 'od_start_time', 'od_end_time', 'cutoff_timestamp']
    for col in timestamp_columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except ValueError:
            try:
                df[col] = pd.to_datetime(df[col], format='mixed')
            except ValueError:
                df[col] = pd.to_datetime(df[col], format='ISO8601')
    
    # Convert numeric columns to float
    numeric_columns = ['actual_time', 'osrm_time', 'segment_actual_time', 
                      'segment_osrm_time', 'actual_distance_to_destination',
                      'osrm_distance', 'segment_osrm_distance']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df

def perform_hypothesis_test(group1, group2, test_name, save_plot=True):
    """
    Perform t-test and create visualization for two groups of data
    """
    # Remove any NaN values
    mask = ~(np.isnan(group1) | np.isnan(group2))
    group1 = group1[mask]
    group2 = group2[mask]
    
    # Perform t-test
    t_stat, p_value = stats.ttest_ind(group1, group2, nan_policy='omit')
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    data = pd.DataFrame({
        'Group 1': group1,
        'Group 2': group2
    })
    sns.boxplot(data=data)
    plt.title(f'{test_name}\np-value: {p_value:.4f}')
    
    if save_plot:
        # Save plot
        plt.savefig(f'plots/{test_name.lower().replace(" ", "_")}.png')
    
    # Show plot
    plt.show()
    plt.close()
    
    return t_stat, p_value

def analyze_time_differences(df):
    """
    Analyze differences between various time metrics
    """
    print("\n=== Time Differences Analysis ===")
    results = {}
    
    # 1. Compare actual_time vs OSRM time
    print("\n1. Actual Time vs OSRM Time")
    t_stat, p_value = perform_hypothesis_test(
        df['actual_time'], 
        df['osrm_time'],
        'Actual Time vs OSRM Time'
    )
    results['actual_vs_osrm'] = {
        't_statistic': t_stat,
        'p_value': p_value
    }
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    # 2. Compare actual_time vs segment_actual_time
    print("\n2. Actual Time vs Segment Actual Time")
    t_stat, p_value = perform_hypothesis_test(
        df['actual_time'], 
        df['segment_actual_time'],
        'Actual Time vs Segment Actual Time'
    )
    results['actual_vs_segment'] = {
        't_statistic': t_stat,
        'p_value': p_value
    }
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    # 3. Compare osrm_time vs segment_osrm_time
    print("\n3. OSRM Time vs Segment OSRM Time")
    t_stat, p_value = perform_hypothesis_test(
        df['osrm_time'], 
        df['segment_osrm_time'],
        'OSRM Time vs Segment OSRM Time'
    )
    results['osrm_vs_segment'] = {
        't_statistic': t_stat,
        'p_value': p_value
    }
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    return results

def analyze_distance_differences(df):
    """
    Analyze differences between various distance metrics
    """
    print("\n=== Distance Differences Analysis ===")
    results = {}
    
    # Compare osrm_distance vs segment_osrm_distance
    print("\n1. OSRM Distance vs Segment OSRM Distance")
    t_stat, p_value = perform_hypothesis_test(
        df['osrm_distance'], 
        df['segment_osrm_distance'],
        'OSRM Distance vs Segment OSRM Distance'
    )
    results['osrm_vs_segment_distance'] = {
        't_statistic': t_stat,
        'p_value': p_value
    }
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    return results

def analyze_point_a_to_scan_differences(df):
    """
    Analyze differences between Point A and start_scan_to_end_scan
    """
    print("\n=== Point A vs Start Scan to End Scan Analysis ===")
    results = {}
    
    # Calculate start_scan_to_end_scan
    df['start_scan_to_end_scan'] = (df['od_end_time'] - df['od_start_time']).dt.total_seconds() / 3600
    
    # Compare Point A time vs start_scan_to_end_scan
    print("\n1. Point A Time vs Start Scan to End Scan Time")
    t_stat, p_value = perform_hypothesis_test(
        df['actual_time'], 
        df['start_scan_to_end_scan'],
        'Point A Time vs Start Scan to End Scan Time'
    )
    results['point_a_vs_scan'] = {
        't_statistic': t_stat,
        'p_value': p_value
    }
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    return results

def create_correlation_heatmap(df):
    """
    Create correlation heatmap for all numeric columns
    """
    # Define numeric columns that exist in the data
    numeric_cols = ['actual_time', 'osrm_time', 'segment_actual_time', 
                   'segment_osrm_time', 'actual_distance_to_destination',
                   'osrm_distance', 'segment_osrm_distance']
    
    # Filter to only include columns that exist in the dataframe
    existing_cols = [col for col in numeric_cols if col in df.columns]
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(df[existing_cols].corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap of Time and Distance Metrics')
    plt.tight_layout()
    
    # Save plot
    plt.savefig('plots/correlation_heatmap.png')
    
    # Show plot
    plt.show()
    plt.close()
    
    # Save correlation matrix
    correlation_matrix = df[existing_cols].corr()
    correlation_matrix.to_csv('results/correlation_matrix.csv')

def main():
    # Load the data
    print("Loading data...")
    df = pd.read_csv('delhivery_data.csv')
    
    # Preprocess the data
    print("Preprocessing data...")
    df = preprocess_data(df)
    
    # Run all analyses
    print("\nStarting analyses...")
    time_results = analyze_time_differences(df)
    distance_results = analyze_distance_differences(df)
    scan_results = analyze_point_a_to_scan_differences(df)
    create_correlation_heatmap(df)
    
    # Save all results
    all_results = {
        'time_analysis': time_results,
        'distance_analysis': distance_results,
        'scan_analysis': scan_results
    }
    
    with open('results/analysis_results.json', 'w') as f:
        json.dump(all_results, f, indent=4)
    
    print("\nAnalysis complete! Results and plots have been saved.")

if __name__ == "__main__":
    main() 