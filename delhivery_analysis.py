# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import warnings
import os
import json
warnings.filterwarnings('ignore')

# Create directories for outputs
os.makedirs('plots', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Set style for better visualizations
plt.style.use('default')  # Using default style instead of seaborn
sns.set_theme()  # This will apply seaborn's styling

# Load the data
df = pd.read_csv('delhivery_data.csv')

# Store basic information
basic_info = {
    'original_shape': df.shape,
    'columns': df.columns.tolist(),
    'dtypes': df.dtypes.astype(str).to_dict()
}

# Display and save basic information
print("Dataset Shape:", df.shape)
print("\nDataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nBasic Statistics:")
print(df.describe())

# Function to analyze missing values
def analyze_missing_values(df):
    missing_df = pd.DataFrame({
        'missing_count': df.isnull().sum(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2)
    })
    return missing_df[missing_df['missing_count'] > 0].sort_values('missing_percentage', ascending=False)

# Analyze missing values
missing_analysis = analyze_missing_values(df)
print("\nMissing Value Analysis:")
print(missing_analysis)

# Save missing value analysis
missing_analysis.to_csv('results/missing_values_analysis.csv')

# Visualize missing values
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), yticklabels=False, cbar=False, cmap='viridis')
plt.title('Missing Values Heatmap')
plt.tight_layout()
plt.savefig('plots/missing_values_heatmap.png')
plt.close()

# Convert timestamp columns to datetime with proper format
timestamp_columns = ['trip_creation_time', 'od_start_time', 'od_end_time', 'cutoff_timestamp']
for col in timestamp_columns:
    try:
        # First try with the default format
        df[col] = pd.to_datetime(df[col])
    except ValueError:
        try:
            # If that fails, try with mixed format
            df[col] = pd.to_datetime(df[col], format='mixed')
        except ValueError:
            # If that also fails, try with ISO8601 format
            df[col] = pd.to_datetime(df[col], format='ISO8601')

# Extract features from trip_creation_time
df['creation_year'] = df['trip_creation_time'].dt.year
df['creation_month'] = df['trip_creation_time'].dt.month
df['creation_day'] = df['trip_creation_time'].dt.day
df['creation_hour'] = df['trip_creation_time'].dt.hour
df['creation_dayofweek'] = df['trip_creation_time'].dt.dayofweek

# Extract location features from source and destination names
def extract_location_features(name):
    if pd.isna(name):  # Handle NaN values
        return pd.Series({'city': np.nan, 'place': np.nan, 'code': np.nan})
    
    if not isinstance(name, str):  # Handle non-string values
        return pd.Series({'city': str(name), 'place': '', 'code': ''})
    
    parts = name.split('-')
    if len(parts) >= 3:
        return pd.Series({
            'city': parts[0].strip(),
            'place': parts[1].strip(),
            'code': parts[2].strip()
        })
    return pd.Series({'city': name, 'place': '', 'code': ''})

# Apply to source and destination names
source_features = df['source_name'].apply(extract_location_features)
destination_features = df['destination_name'].apply(extract_location_features)

# Add new columns
df['source_city'] = source_features['city']
df['source_place'] = source_features['place']
df['source_code'] = source_features['code']

df['destination_city'] = destination_features['city']
df['destination_place'] = destination_features['place']
df['destination_code'] = destination_features['code']

# Save sample of extracted features
df[['source_name', 'source_city', 'source_place', 'source_code',
    'destination_name', 'destination_city', 'destination_place', 'destination_code']].head().to_csv('results/extracted_features_sample.csv')

# Define aggregation functions for different columns
agg_dict = {
    'actual_distance_to_destination': 'sum',
    'actual_time': 'sum',
    'osrm_time': 'sum',
    'osrm_distance': 'sum',
    'segment_actual_time': 'sum',
    'segment_osrm_time': 'sum',
    'segment_osrm_distance': 'sum',
    'route_type': 'first',
    'source_center': 'first',
    'source_name': 'first',
    'source_city': 'first',
    'source_place': 'first',
    'source_code': 'first',
    'destination_center': 'last',
    'destination_name': 'last',
    'destination_city': 'last',
    'destination_place': 'last',
    'destination_code': 'last',
    'od_start_time': 'first',
    'od_end_time': 'last',
    'trip_creation_time': 'first'
}

# Group by trip_uuid and aggregate
df_aggregated = df.groupby('trip_uuid').agg(agg_dict).reset_index()

# Calculate additional time-based features
df_aggregated['total_trip_time'] = (df_aggregated['od_end_time'] - df_aggregated['od_start_time']).dt.total_seconds() / 3600
df_aggregated['creation_to_start_time'] = (df_aggregated['od_start_time'] - df_aggregated['trip_creation_time']).dt.total_seconds() / 3600

# Save sample of aggregated data
df_aggregated.head().to_csv('results/aggregated_data_sample.csv')

# Update basic info with processed data shape
basic_info['processed_shape'] = df_aggregated.shape

# Save basic information
with open('results/basic_info.json', 'w') as f:
    json.dump(basic_info, f, indent=4)

# Save processed data
df_aggregated.to_csv('processed_delhivery_data.csv', index=False)

print("\nPreprocessing complete! Results have been saved to the 'results' directory.") 