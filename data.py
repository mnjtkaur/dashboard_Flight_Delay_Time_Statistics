"""
Data loading and preprocessing module for Flight Delay Time Statistics.
Handles data ingestion, cleaning, and transformation for analysis and visualization.
"""

import pandas as pd
import numpy as np
import requests
from typing import Tuple, Optional


def download_airline_data(url: str, output_path: str = "airline_data.csv") -> pd.DataFrame:
    """
    Download airline data from URL and save locally.
    
    Args:
        url (str): URL to download CSV from
        output_path (str): Path to save CSV locally
        
    Returns:
        pd.DataFrame: Loaded airline data
    """
    response = requests.get(url)
    with open(output_path, "wb") as file:
        file.write(response.content)
    
    # Load with proper dtype handling
    airline_data = pd.read_csv(
        output_path,
        encoding="ISO-8859-1",
        dtype={
            'Div1Airport': str,
            'Div1TailNum': str,
            'Div2Airport': str,
            'Div2TailNum': str
        }
    )
    print(f"Data downloaded and saved to {output_path}")
    return airline_data


def load_airline_data(file_path: str = "airline_data.csv") -> pd.DataFrame:
    """
    Load airline data from local CSV file.
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        pd.DataFrame: Loaded airline data
    """
    airline_data = pd.read_csv(
        file_path,
        encoding="ISO-8859-1",
        dtype={
            'Div1Airport': str,
            'Div1TailNum': str,
            'Div2Airport': str,
            'Div2TailNum': str
        }
    )
    return airline_data


def clean_delay_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare delay data for analysis.
    Properly handles missing values and creates useful features.
    
    Args:
        data (pd.DataFrame): Raw airline data
        
    Returns:
        pd.DataFrame: Cleaned data with additional features
    """
    data_clean = data.copy()
    
    # Add missing value indicators
    data_clean['ArrDelay_missing'] = data_clean['ArrDelay'].isna()
    data_clean['DepTime_missing'] = data_clean['DepTime'].isna()
    
    # Drop rows with missing ArrDelay for delay analysis
    data_clean = data_clean.dropna(subset=['ArrDelay'])
    
    return data_clean


def convert_deptime_to_minutes(dep_time: float) -> Optional[int]:
    """
    Convert departure time in HHMM format to minutes since midnight.
    
    Args:
        dep_time (float): Departure time in HHMM format (e.g., 1430 for 2:30 PM)
        
    Returns:
        Optional[int]: Minutes since midnight, or None if invalid
    """
    if pd.isna(dep_time):
        return np.nan
    dep_int = int(dep_time)
    hours = dep_int // 100
    minutes = dep_int % 100
    return hours * 60 + minutes


def create_time_of_day_bins(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create time-of-day categorical bins from DepTime.
    
    Args:
        data (pd.DataFrame): Data with DepTime column
        
    Returns:
        pd.DataFrame: Data with new TimeOfDay column
    """
    data_time = data.copy()
    data_time['DepMinutes'] = data_time['DepTime'].apply(convert_deptime_to_minutes)
    
    bins = [0, 360, 720, 1020, 1440]  # Midnight, 6am, 12pm, 5pm, midnight
    labels = ['Night (0-6)', 'Morning (6-12)', 'Afternoon (12-17)', 'Evening (17-24)']
    data_time['TimeOfDay'] = pd.cut(data_time['DepMinutes'], bins=bins, labels=labels, right=False)
    
    return data_time


def compute_carrier_kpis(data: pd.DataFrame, delay_threshold: int = 15) -> pd.DataFrame:
    """
    Compute Key Performance Indicators (KPIs) for each reporting airline.
    
    Args:
        data (pd.DataFrame): Cleaned airline data with ArrDelay
        delay_threshold (int): Minutes threshold for "delayed" classification
        
    Returns:
        pd.DataFrame: KPI table with per-carrier metrics
    """
    carrier_kpis = data.groupby('Reporting_Airline').agg({
        'Flights': 'sum',
        'ArrDelay': ['mean', 'median', 'std', 'count']
    }).reset_index()
    
    # Flatten column names
    carrier_kpis.columns = ['Reporting_Airline', 'Total_Flights', 'Avg_Delay', 
                            'Median_Delay', 'Std_Delay', 'Valid_Delays']
    
    # Calculate percentage delayed
    delayed_counts = data.groupby('Reporting_Airline').apply(
        lambda x: (x['ArrDelay'] > delay_threshold).sum()
    ).reset_index(name='Flights_Delayed_Over_15min')
    
    carrier_kpis = carrier_kpis.merge(delayed_counts, on='Reporting_Airline')
    carrier_kpis['Pct_Delayed_Over_15min'] = (
        carrier_kpis['Flights_Delayed_Over_15min'] / carrier_kpis['Valid_Delays'] * 100
    ).round(1)
    
    # Sort by total flights descending
    carrier_kpis = carrier_kpis.sort_values('Total_Flights', ascending=False)
    
    return carrier_kpis


def compute_delay_rates_by_time_distance(data: pd.DataFrame, delay_threshold: int = 15) -> pd.DataFrame:
    """
    Compute delay rates (%) by distance group and time of day.
    
    Args:
        data (pd.DataFrame): Data with TimeOfDay column
        delay_threshold (int): Minutes threshold for "delayed" classification
        
    Returns:
        pd.DataFrame: Delay rates by distance group and time of day
    """
    delay_by_time_distance = data.groupby(
        ['DistanceGroup', 'TimeOfDay'], observed=True
    ).apply(
        lambda x: ((x['ArrDelay'] > delay_threshold).sum() / len(x) * 100) if len(x) > 0 else 0
    ).reset_index(name='Pct_Delayed')
    
    return delay_by_time_distance


def get_on_time_performance(data: pd.DataFrame, delay_threshold: int = 15) -> dict:
    """
    Compute overall on-time performance metrics.
    
    Args:
        data (pd.DataFrame): Cleaned airline data with ArrDelay
        delay_threshold (int): Minutes threshold for "on-time" classification
        
    Returns:
        dict: Dictionary with on-time performance metrics
    """
    pct_on_time = (data['ArrDelay'] <= delay_threshold).mean() * 100
    pct_delayed = (data['ArrDelay'] > delay_threshold).mean() * 100
    median_delay = data['ArrDelay'].median()
    p90_delay = data['ArrDelay'].quantile(0.90)
    
    return {
        'on_time_pct': round(pct_on_time, 1),
        'delayed_pct': round(pct_delayed, 1),
        'median_delay': round(median_delay, 1),
        'p90_delay': round(p90_delay, 1)
    }


def sample_data(data: pd.DataFrame, n: int = 500, random_state: int = 42) -> pd.DataFrame:
    """
    Sample data for faster exploration and testing.
    
    Args:
        data (pd.DataFrame): Input data
        n (int): Number of samples
        random_state (int): Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Sampled data
    """
    return data.sample(n=min(n, len(data)), random_state=random_state)


def analyze_delay_reasons(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze delay reasons: CarrierDelay, WeatherDelay, NASDelay, SecurityDelay, LateAircraftDelay.
    
    Args:
        data (pd.DataFrame): Cleaned airline data
        
    Returns:
        pd.DataFrame: Aggregated delay reasons by month
    """
    delay_reason_cols = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    
    # Fill NaN with 0 for delay reasons
    for col in delay_reason_cols:
        if col in data.columns:
            data[col] = data[col].fillna(0)
    
    # Group by month and sum delay reasons
    delay_reasons = data.groupby('Month')[delay_reason_cols].sum().reset_index()
    
    return delay_reasons


def get_top_routes(data: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Get top origin-destination pairs by number of flights.
    
    Args:
        data (pd.DataFrame): Cleaned airline data
        top_n (int): Number of top routes to return
        
    Returns:
        pd.DataFrame: Top routes with flight counts and average delay
    """
    route_analysis = data.groupby(['Origin', 'Dest']).agg({
        'Flights': 'sum',
        'ArrDelay': ['mean', 'count']
    }).reset_index()
    
    route_analysis.columns = ['Origin', 'Dest', 'Total_Flights', 'Avg_Delay', 'Valid_Delays']
    route_analysis['Route'] = route_analysis['Origin'] + ' → ' + route_analysis['Dest']
    route_analysis = route_analysis.sort_values('Total_Flights', ascending=False).head(top_n)
    
    return route_analysis


def analyze_day_of_week(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze delays by day of week.
    
    Args:
        data (pd.DataFrame): Cleaned airline data with DayOfWeek column
        
    Returns:
        pd.DataFrame: Delay metrics by day of week
    """
    if 'DayOfWeek' not in data.columns:
        return pd.DataFrame()
    
    day_names = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 
                 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    
    day_analysis = data.groupby('DayOfWeek').agg({
        'ArrDelay': ['mean', 'median', 'count'],
        'Flights': 'sum',
        'Cancelled': 'sum'
    }).reset_index()
    
    day_analysis.columns = ['DayOfWeek', 'Avg_Delay', 'Median_Delay', 'Flight_Count', 'Total_Flights', 'Cancelled']
    day_analysis['DayName'] = day_analysis['DayOfWeek'].map(day_names)
    day_analysis['Cancellation_Rate'] = (day_analysis['Cancelled'] / day_analysis['Flight_Count'] * 100).round(2)
    
    return day_analysis


def analyze_carrier_delay_reasons(data: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze delay reasons breakdown by carrier.
    
    Args:
        data (pd.DataFrame): Cleaned airline data
        
    Returns:
        pd.DataFrame: Delay reasons aggregated by carrier
    """
    delay_reason_cols = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    
    # Fill NaN with 0
    for col in delay_reason_cols:
        if col in data.columns:
            data[col] = data[col].fillna(0)
    
    carrier_reasons = data.groupby('Reporting_Airline')[delay_reason_cols].sum().reset_index()
    
    # Calculate total delays and percentages
    carrier_reasons['Total_Delays'] = carrier_reasons[delay_reason_cols].sum(axis=1)
    
    for col in delay_reason_cols:
        carrier_reasons[f'{col}_Pct'] = (carrier_reasons[col] / carrier_reasons['Total_Delays'] * 100).round(1)
    
    carrier_reasons = carrier_reasons.sort_values('Total_Delays', ascending=False)
    
    return carrier_reasons
