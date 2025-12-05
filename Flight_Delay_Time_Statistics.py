"""
Flight_Delay_Time_Statistics.py
Standalone script for batch analysis of flight delays.
Can be run directly without Jupyter or Streamlit.
"""

import pandas as pd
import data as data_module


def main():
    print("=" * 80)
    print("Flight Delay Time Statistics - Batch Analysis")
    print("=" * 80)
    
    # Load data
    print("\n📥 Loading airline data...")
    airline_data = data_module.load_airline_data("airline_data.csv")
    print(f"✅ Loaded {len(airline_data)} records")
    
    # Sample for faster processing (optional)
    print("\n📊 Sampling 500 records for analysis...")
    data_sample = data_module.sample_data(airline_data, n=500)
    
    # Clean data
    print("\n🧹 Cleaning data...")
    data_clean = data_module.clean_delay_data(data_sample)
    print(f"✅ Cleaned data: {len(data_clean)} records with valid arrival delays")
    
    # Compute on-time performance
    print("\n📈 Computing on-time performance metrics...")
    kpis = data_module.get_on_time_performance(data_clean)
    print(f"   On-Time: {kpis['on_time_pct']:.1f}%")
    print(f"   Delayed: {kpis['delayed_pct']:.1f}%")
    print(f"   Median Delay: {kpis['median_delay']:.1f} minutes")
    print(f"   90th Percentile: {kpis['p90_delay']:.1f} minutes")
    
    # Compute carrier KPIs
    print("\n✈️ Computing per-carrier KPIs...")
    carrier_kpis = data_module.compute_carrier_kpis(data_clean)
    print("\nTop Carriers by Number of Flights:")
    print(carrier_kpis[['Reporting_Airline', 'Total_Flights', 'Avg_Delay', 'Pct_Delayed_Over_15min']].head(10).to_string(index=False))
    
    # Export results
    print("\n💾 Exporting carrier KPIs to CSV...")
    carrier_kpis.to_csv("carrier_kpis.csv", index=False)
    print("✅ Saved to carrier_kpis.csv")
    
    # Time-of-day analysis
    print("\n🕐 Performing time-of-day analysis...")
    time_analysis = data_module.create_time_of_day_bins(data_clean)
    delay_by_time_distance = data_module.compute_delay_rates_by_time_distance(time_analysis)
    
    if len(delay_by_time_distance) > 0:
        pivot_table = delay_by_time_distance.pivot(index='DistanceGroup', columns='TimeOfDay', values='Pct_Delayed')
        print("\nDelay Rates (%) by Distance Group and Time of Day:")
        print(pivot_table.round(1).to_string())
        pivot_table.to_csv("delay_by_time_distance.csv")
        print("\n✅ Saved to delay_by_time_distance.csv")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("📊 Analysis Summary")
    print("=" * 80)
    print(f"Total Records Analyzed: {len(data_clean)}")
    print(f"Unique Airlines: {data_clean['Reporting_Airline'].nunique()}")
    print(f"Months Covered: {int(data_clean['Month'].max())}")
    print(f"Average Delay Across All Flights: {data_clean['ArrDelay'].mean():.1f} minutes")
    print(f"Flights On-Time (≤15 min late): {kpis['on_time_pct']:.1f}%")
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
