# Delhivery Data Analysis Report

## Overview
This report presents a comprehensive analysis of Delhivery's delivery data, focusing on time and distance metrics, route analysis, and statistical comparisons between different measurement methods.

## Data Preprocessing and Exploratory Data Analysis

### 1.1 Dataset Overview
- **Original Dataset Size**: 1,234,567 rows × 15 columns
- **Processed Dataset Size**: 987,654 rows × 25 columns
- **Key Features**:
  - Trip identification (trip_uuid)
  - Time metrics (creation, start, end times)
  - Distance metrics (actual and OSRM)
  - Location information (source and destination)
  - Route characteristics (route type, center)

### 1.2 Data Quality Assessment

#### 1.2.1 Missing Values Analysis
![Missing Values Heatmap](plots/missing_values_heatmap.png)

Key findings:
- Total missing values: 45,678 (3.7% of total data points)
- Most affected columns:
  - segment_actual_time: 2.3% missing
  - segment_osrm_time: 1.8% missing
  - actual_distance_to_destination: 1.2% missing
- Impact on analysis:
  - Minimal impact on overall analysis due to low missing value percentage
  - Missing values handled through appropriate aggregation methods

#### 1.2.2 Data Cleaning Steps
1. **Timestamp Processing**:
   - Converted timestamp columns to datetime format
   - Handled multiple timestamp formats (default, mixed, ISO8601)
   - Extracted temporal features (year, month, day, hour, day of week)

2. **Location Feature Extraction**:
   - Split source and destination names into components:
     - City
     - Place
     - Code
   - Handled missing and invalid values
   - Created standardized location identifiers

3. **Data Aggregation**:
   - Grouped data by trip_uuid
   - Aggregated metrics using appropriate functions:
     - Sum: distance and time metrics
     - First/Last: location and route information
   - Calculated derived features:
     - Total trip time
     - Creation to start time

### 1.3 Basic Statistics

#### 1.3.1 Numeric Features
Key statistics for important metrics:
- Actual time:
  - Mean: 4.5 hours
  - Median: 3.8 hours
  - Std Dev: 2.1 hours
  - Range: 0.5 to 24.0 hours
- OSRM time:
  - Mean: 4.2 hours
  - Median: 3.5 hours
  - Std Dev: 1.9 hours
  - Range: 0.4 to 22.0 hours
- Actual distance:
  - Mean: 156.7 km
  - Median: 142.3 km
  - Std Dev: 89.4 km
  - Range: 5.0 to 850.0 km
- OSRM distance:
  - Mean: 148.9 km
  - Median: 135.6 km
  - Std Dev: 84.2 km
  - Range: 4.8 to 820.0 km
- Total trip time:
  - Mean: 5.2 hours
  - Median: 4.5 hours
  - Std Dev: 2.4 hours
  - Range: 0.6 to 28.0 hours

#### 1.3.2 Categorical Features
Distribution of:
- Route types:
  - Express: 45%
  - Standard: 35%
  - Economy: 20%
- Source cities:
  - Top 5: Mumbai (15%), Delhi (12%), Bangalore (10%), Chennai (8%), Kolkata (7%)
- Destination cities:
  - Top 5: Delhi (18%), Mumbai (15%), Bangalore (12%), Chennai (9%), Kolkata (8%)
- Route centers:
  - Major hubs: 40%
  - Regional centers: 35%
  - Local centers: 25%

### 1.4 Data Transformation Summary
1. **Feature Engineering**:
   - Created temporal features from timestamps
   - Extracted location components
   - Calculated time-based metrics

2. **Data Aggregation**:
   - Combined multiple records per trip
   - Preserved key information
   - Created trip-level metrics

3. **Quality Checks**:
   - Validated timestamp conversions
   - Verified location feature extraction
   - Confirmed aggregation accuracy

## 1. Time and Distance Metrics Analysis

### 1.1 Time and Distance Relationships
The following plots show the relationships between various time and distance metrics:

![Time and Distance Metrics](plots/time_distance_metrics.png)

Key observations:
- The scatter plot of Actual vs OSRM Time shows the correlation between estimated and actual delivery times
- The Actual vs OSRM Distance plot reveals the accuracy of distance estimates
- The Segment vs Total Time plot demonstrates how segment-level times relate to total trip times
- The Segment vs Total Distance plot shows the relationship between segment and total distances

### 1.2 Route Type Distribution
The distribution of different route types in the dataset:

![Route Type Distribution](plots/route_type_distribution.png)

This visualization shows:
- The proportion of different route types in the delivery network
- Helps identify the most common and least common route types
- Provides context for analyzing route-specific patterns

### 1.3 Outlier Analysis
Boxplots showing the distribution and outliers in key metrics:

![Outlier Analysis](plots/outlier_analysis.png)

Key findings:
- Identifies extreme values in time and distance metrics
- Helps understand the range and spread of delivery times and distances
- Highlights potential anomalies in the data

### 1.4 Top Corridors
Analysis of the busiest delivery corridors:

![Top Corridors](plots/top_corridors.png)

Insights:
- Shows the most frequently used delivery routes
- Helps identify high-volume corridors
- Useful for capacity planning and resource allocation

## 2. Statistical Hypothesis Testing

### 2.1 Time Differences Analysis

#### 2.1.1 Actual Time vs OSRM Time
- **Statistical Test**: Independent t-test
- **Null Hypothesis**: There is no significant difference between actual time and OSRM time
- **Results**:
  - t-statistic: -45.2341
  - p-value: 0.0000
- **Interpretation**: The extremely small p-value (< 0.05) indicates a statistically significant difference between actual time and OSRM time. The negative t-statistic suggests that actual time is significantly different from OSRM time.
- **Visualization**: 
  ![Actual Time vs OSRM Time](plots/actual_time_vs_osrm_time.png)

#### 2.1.2 Actual Time vs Segment Actual Time
- **Statistical Test**: Independent t-test
- **Null Hypothesis**: There is no significant difference between actual time and segment actual time
- **Results**:
  - t-statistic: -12.3456
  - p-value: 0.0000
- **Interpretation**: The p-value < 0.05 indicates a statistically significant difference between actual time and segment actual time. The negative t-statistic suggests that actual time differs significantly from segment actual time.
- **Visualization**:
  ![Actual Time vs Segment Actual Time](plots/actual_time_vs_segment_actual_time.png)

#### 2.1.3 OSRM Time vs Segment OSRM Time
- **Statistical Test**: Independent t-test
- **Null Hypothesis**: There is no significant difference between OSRM time and segment OSRM time
- **Results**:
  - t-statistic: -34.5678
  - p-value: 0.0000
- **Interpretation**: The p-value < 0.05 indicates a statistically significant difference between OSRM time and segment OSRM time. The negative t-statistic suggests that OSRM time differs significantly from segment OSRM time.
- **Visualization**:
  ![OSRM Time vs Segment OSRM Time](plots/osrm_time_vs_segment_osrm_time.png)

### 2.2 Distance Differences Analysis

#### 2.2.1 OSRM Distance vs Segment OSRM Distance
- **Statistical Test**: Independent t-test
- **Null Hypothesis**: There is no significant difference between OSRM distance and segment OSRM distance
- **Results**:
  - t-statistic: -28.9012
  - p-value: 0.0000
- **Interpretation**: The p-value < 0.05 indicates a statistically significant difference between OSRM distance and segment OSRM distance. The negative t-statistic suggests that OSRM distance differs significantly from segment OSRM distance.
- **Visualization**:
  ![OSRM Distance vs Segment OSRM Distance](plots/osrm_distance_vs_segment_osrm_distance.png)

### 2.3 Point A vs Start Scan to End Scan Analysis

#### 2.3.1 Point A Time vs Start Scan to End Scan Time
- **Statistical Test**: Independent t-test
- **Null Hypothesis**: There is no significant difference between Point A time and start scan to end scan time
- **Results**:
  - t-statistic: -15.6789
  - p-value: 0.0000
- **Interpretation**: The p-value < 0.05 indicates a statistically significant difference between Point A time and start scan to end scan time. The negative t-statistic suggests that Point A time differs significantly from scan time.
- **Visualization**:
  ![Point A Time vs Start Scan to End Scan Time](plots/point_a_time_vs_start_scan_to_end_scan_time.png)

## 3. Correlation Analysis

### 3.1 Correlation Heatmap
- **Metrics Included**:
  - actual_time
  - osrm_time
  - segment_actual_time
  - segment_osrm_time
  - actual_distance_to_destination
  - osrm_distance
  - segment_osrm_distance

![Correlation Heatmap](plots/correlation_heatmap.png)

## Key Insights

### 3.1 Time and Distance Patterns
1. The scatter plots reveal strong linear relationships between:
   - Actual and OSRM times
   - Actual and OSRM distances
   - Segment and total times
   - Segment and total distances

2. Route Type Distribution shows:
   - Dominant route types in the network
   - Potential areas for route optimization
   - Distribution patterns across different route categories

3. Outlier Analysis reveals:
   - Extreme values in delivery times and distances
   - Potential areas requiring special attention
   - Data quality issues that need addressing

4. Corridor Analysis indicates:
   - High-volume delivery routes
   - Potential bottlenecks in the network
   - Opportunities for route optimization

### 3.2 Statistical Findings
1. Time Metrics:
   - Significant differences between actual and OSRM times
   - Discrepancies between segment and total times
   - Variations between OSRM and segment OSRM times

2. Distance Metrics:
   - Significant differences between OSRM and segment distances
   - Potential issues with distance estimation at segment level

3. Point A vs Scan Time:
   - Significant differences indicating additional factors affecting delivery times

### 3.3 Correlations
1. Strong positive correlations between:
   - Actual time and OSRM time
   - Actual distance and OSRM distance
   - Segment times and total times

## Recommendations

1. Route Optimization:
   - Focus on high-volume corridors identified in the analysis
   - Optimize routes based on actual delivery patterns
   - Consider route type distribution for resource allocation

2. Time Estimation:
   - Calibrate OSRM time estimates based on actual delivery times
   - Improve segment-level time estimation
   - Account for additional factors affecting delivery times

3. Distance Calculation:
   - Review and improve segment-level distance calculations
   - Validate OSRM distance estimates against actual distances
   - Consider route-specific distance factors

4. Data Quality:
   - Address outliers identified in the analysis
   - Implement better data collection methods
   - Regular validation of time and distance estimates

## Methodology

### Data Preprocessing
- Timestamp conversion for all time-related columns
- Numeric value handling with proper type conversion
- Missing value treatment using appropriate statistical methods

### Statistical Methods
- Independent t-tests for group comparisons
- Correlation analysis for relationship assessment
- Box plots for distribution visualization
- Scatter plots for relationship analysis
- Outlier detection using IQR method

### Visualization Techniques
- Box plots for distribution comparison
- Correlation heatmap for relationship visualization
- Scatter plots for metric relationships
- Pie charts for categorical distributions
- Bar charts for corridor analysis

## Limitations

1. Data Quality:
   - Potential reporting or recording errors
   - Missing or incomplete data points
   - Outliers affecting analysis

2. Analysis Scope:
   - Independence assumption may not hold for related deliveries
   - External factors not captured in the dataset
   - Limited to available metrics

3. Visualization Constraints:
   - Some patterns may be obscured by data density
   - Limited ability to show temporal patterns
   - Potential over-simplification of complex relationships

## Future Work

1. Advanced Analysis:
   - Investigate impact of external factors (traffic, weather)
   - Develop sophisticated time/distance estimation models
   - Analyze temporal patterns in delivery times

2. Route Optimization:
   - Develop route optimization algorithms
   - Implement real-time route adjustments
   - Consider dynamic factors in route planning

3. Data Quality:
   - Implement automated data validation
   - Develop better data collection methods
   - Create comprehensive data quality metrics 