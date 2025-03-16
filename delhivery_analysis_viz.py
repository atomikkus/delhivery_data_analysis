# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import warnings
import os
warnings.filterwarnings('ignore')

# Create plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)

# Set style for better visualizations
plt.style.use('default')  # Using default style instead of seaborn
sns.set_theme()  # This will apply seaborn's styling

# Load the processed data
df = pd.read_csv('processed_delhivery_data.csv')

# 1. Time and Distance Analysis
def analyze_time_distance_metrics(df):
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Actual vs OSRM Time
    sns.scatterplot(data=df, x='osrm_time', y='actual_time', ax=axes[0,0])
    axes[0,0].set_title('Actual vs OSRM Time')
    axes[0,0].set_xlabel('OSRM Time (hours)')
    axes[0,0].set_ylabel('Actual Time (hours)')
    
    # Plot 2: Actual vs OSRM Distance
    sns.scatterplot(data=df, x='osrm_distance', y='actual_distance_to_destination', ax=axes[0,1])
    axes[0,1].set_title('Actual vs OSRM Distance')
    axes[0,1].set_xlabel('OSRM Distance (km)')
    axes[0,1].set_ylabel('Actual Distance (km)')
    
    # Plot 3: Segment vs Total Time
    sns.scatterplot(data=df, x='segment_actual_time', y='actual_time', ax=axes[1,0])
    axes[1,0].set_title('Segment vs Total Time')
    axes[1,0].set_xlabel('Segment Time (hours)')
    axes[1,0].set_ylabel('Total Time (hours)')
    
    # Plot 4: Segment vs Total Distance
    sns.scatterplot(data=df, x='segment_osrm_distance', y='osrm_distance', ax=axes[1,1])
    axes[1,1].set_title('Segment vs Total Distance')
    axes[1,1].set_xlabel('Segment Distance (km)')
    axes[1,1].set_ylabel('Total Distance (km)')
    
    plt.tight_layout()
    
    # Save plot
    plt.savefig('plots/time_distance_metrics.png')
    
    # Show plot
    plt.show()
    plt.close()

# 2. Route Type Analysis
def analyze_route_types(df):
    # Count route types
    route_counts = df['route_type'].value_counts()
    
    # Create pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(route_counts, labels=route_counts.index, autopct='%1.1f%%')
    plt.title('Distribution of Route Types')
    
    # Save plot
    plt.savefig('plots/route_type_distribution.png')
    
    # Show plot
    plt.show()
    plt.close()
    
    # Calculate average metrics by route type
    route_metrics = df.groupby('route_type').agg({
        'actual_time': 'mean',
        'actual_distance_to_destination': 'mean',
        'total_trip_time': 'mean'
    }).round(2)
    
    print("\nAverage Metrics by Route Type:")
    print(route_metrics)

# 3. Outlier Analysis
def analyze_outliers(df):
    # Select numeric columns for outlier analysis
    numeric_cols = ['actual_time', 'actual_distance_to_destination', 
                   'osrm_time', 'osrm_distance', 'total_trip_time']
    
    # Create boxplots
    plt.figure(figsize=(15, 6))
    df[numeric_cols].boxplot()
    plt.title('Boxplots of Numeric Variables')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plt.savefig('plots/outlier_analysis.png')
    
    # Show plot
    plt.show()
    plt.close()
    
    # Calculate IQR and identify outliers
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
        print(f"\nOutliers in {col}:")
        print(f"Number of outliers: {len(outliers)}")
        print(f"Percentage of outliers: {(len(outliers)/len(df)*100):.2f}%")

# 4. Corridor Analysis
def analyze_corridors(df):
    # Create corridor identifier
    df['corridor'] = df['source_city'] + ' - ' + df['destination_city']
    
    # Analyze top corridors
    corridor_metrics = df.groupby('corridor').agg({
        'trip_uuid': 'count',
        'actual_time': 'mean',
        'actual_distance_to_destination': 'mean',
        'total_trip_time': 'mean'
    }).round(2)
    
    corridor_metrics.columns = ['number_of_trips', 'avg_time', 'avg_distance', 'avg_total_time']
    corridor_metrics = corridor_metrics.sort_values('number_of_trips', ascending=False)
    
    print("\nTop 10 Busiest Corridors:")
    print(corridor_metrics.head(10))
    
    # Visualize top corridors
    plt.figure(figsize=(12, 6))
    corridor_metrics.head(10)['number_of_trips'].plot(kind='bar')
    plt.title('Top 10 Busiest Corridors')
    plt.xlabel('Corridor')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot
    plt.savefig('plots/top_corridors.png')
    
    # Show plot
    plt.show()
    plt.close()

# Run all analyses
print("Starting analysis...")

print("\n1. Analyzing time and distance metrics...")
analyze_time_distance_metrics(df)

print("\n2. Analyzing route types...")
analyze_route_types(df)

print("\n3. Analyzing outliers...")
analyze_outliers(df)

print("\n4. Analyzing corridors...")
analyze_corridors(df)

print("\nAnalysis complete! All plots have been saved and displayed.") 