# Delhivery Data Analysis

This repository contains scripts for analyzing Delhivery's delivery data, focusing on delivery patterns, route optimization, and business insights.

## Project Structure

- `delhivery_analysis.py`: Main script for data preprocessing and feature engineering
- `delhivery_analysis_viz.py`: Script for analysis and visualization
- `requirements.txt`: Required Python packages
- `README.md`: This file

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Place your Delhivery dataset as `delhivery_data.csv` in the project directory.

## Usage

1. First, run the preprocessing script:
```bash
python delhivery_analysis.py
```
This will:
- Load and clean the data
- Handle missing values
- Extract features from timestamps and location names
- Aggregate data based on trip_uuid
- Save processed data as `processed_delhivery_data.csv`

2. Then, run the analysis and visualization script:
```bash
python delhivery_analysis_viz.py
```
This will:
- Generate various visualizations saved as PNG files
- Perform statistical analysis
- Output insights about:
  - Time and distance metrics
  - Route type distribution
  - Outlier analysis
  - Corridor analysis

## Output Files

The analysis generates several visualization files:
- `missing_values_heatmap.png`: Visualization of missing values in the dataset
- `time_distance_analysis.png`: Comparison of actual vs. OSRM metrics
- `route_type_distribution.png`: Distribution of different route types
- `outlier_analysis.png`: Boxplots showing outliers in numeric variables
- `top_corridors.png`: Visualization of busiest delivery corridors

## Analysis Components

1. **Data Preprocessing**
   - Missing value handling
   - Feature extraction from timestamps
   - Location feature extraction
   - Data aggregation

2. **Time and Distance Analysis**
   - Comparison of actual vs. OSRM metrics
   - Segment vs. total time/distance analysis
   - Correlation analysis

3. **Route Type Analysis**
   - Distribution of route types
   - Performance metrics by route type
   - Route type efficiency analysis

4. **Outlier Analysis**
   - Identification of outliers using IQR method
   - Visualization of outliers
   - Impact assessment

5. **Corridor Analysis**
   - Identification of busiest corridors
   - Performance metrics by corridor
   - Optimization opportunities

## Business Insights

The analysis provides insights into:
- Most efficient route types
- Busiest delivery corridors
- Time and distance patterns
- Potential optimization areas
- Outlier identification for quality improvement

## Recommendations

Based on the analysis, recommendations are provided for:
- Route optimization
- Resource allocation
- Service quality improvement
- Operational efficiency enhancement 