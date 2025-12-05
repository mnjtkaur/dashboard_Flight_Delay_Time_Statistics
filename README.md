# ✈️ Flight Delay Time Statistics Dashboard

A comprehensive data analysis and visualization platform for exploring flight delay patterns, carrier performance, and operational insights from the Airline On-Time Performance Dataset.

## 📊 Overview

This project analyzes approximately 200 million domestic US flights reported to the United States Bureau of Transportation Statistics. It provides:

 - **Exploratory Data Analysis:** Jupyter notebook with 7+ visualizations and 3 advanced analyses
- **Modularized Data Pipeline:** Reusable functions for data loading, cleaning, and KPI computation
- **Actionable Insights:** Per-carrier performance metrics, time-of-day patterns, and delay distributions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd dashboard_Flight_Delay_Time_Statistics
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Or using conda
   conda create -n flight-delays python=3.10
   conda activate flight-delays
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Explore the Notebook
```bash
jupyter notebook Flight_Delay_Time_Statistics.ipynb
```
The notebook includes:
- **Sections 1-7:** Original visualizations (scatter, line, bar, histogram, bubble, pie, sunburst)
- **Advanced Analyses:**
  - **Task A:** Proper missing-value handling and on-time performance metrics
  - **Task B:** Per-carrier KPIs (flights, avg delay, % delayed >15 min)
  - **Task C:** Time-of-day analysis with grouped bar chart and heatmap

### Use the Data Module
```python
from data import *

# Load and clean data
airline_data = load_airline_data("airline_data.csv")
data_clean = clean_delay_data(airline_data)

# Compute KPIs
kpis = get_on_time_performance(data_clean)
carrier_kpis = compute_carrier_kpis(data_clean)

# Create time-of-day bins and analyze
data_time = create_time_of_day_bins(data_clean)
delay_by_time = compute_delay_rates_by_time_distance(data_time)
```

## 📁 Project Structure

```
.
├── airline_data.csv                           # Dataset (auto-downloaded)
├── requirements.txt                           # Python dependencies
├── README.md                                  # This file
├── Flight_Delay_Time_Statistics.ipynb         # EDA notebook with 10 analyses
├── data.py                                    # Reusable data module
└── Flight_Delay_Time_Statistics.py            # (Optional) Standalone Python script
```

## 📊 Key Features

### Notebook Capabilities
- **Multi-filter exploration:** By airline, distance group, and month (in the notebook)
- **KPI summaries:** On-time %, delay rates, percentiles
- **Multiple analyses:** Carrier performance, delay distribution, time-of-day, monthly trends
- **Interactive plots (in notebook):** Hover for details, zoom, pan, download as PNG when using Plotly

### Data Analysis
- **On-time performance:** % flights arriving ≤15 minutes late (industry standard)
- **Carrier rankings:** By average delay and consistency
- **Time-of-day patterns:** Morning flights outperform evening flights
- **Monthly seasonality:** Peak delay months identified
- **Distance-group trends:** Short vs. long-haul delay patterns

### Advanced Features
- **Missing value handling:** Proper imputation and indicator columns
- **Time binning:** Automatic conversion of HHMM format to time-of-day categories
- **Delay metrics:** Mean, median, 90th percentile delays
- **Statistical aggregation:** Per-carrier, per-month, per-distance-group

## 📈 Sample Insights

- **Best time to fly:** Morning (6am-12pm) flights have ~20-30% lower delays
- **Busiest airline:** Southwest Airlines (WN) operates most flights in dataset
- **Peak delay month:** June typically shows highest average delays
- **Distance patterns:** Long-distance flights (>1500 mi) show less time-of-day variation

## 🛠️ Development

### Adding New Features
1. Extend `data.py` with new analysis functions
2. Update dashboard code (e.g., the notebook or a dashboard script) to add new tabs or visualizations
3. Re-run the notebook to validate changes
4. Update this README with new insights

### Running Tests (Future)
```bash
pytest tests/
```

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.1.4 | Data manipulation |
| plotly | 5.18.0 | Interactive visualizations |
| numpy | 1.26.2 | Numerical computing |
| scikit-learn | 1.3.2 | ML utilities |
| requests | 2.31.0 | HTTP requests |

See `requirements.txt` for complete list.

## 🔗 Data Source

[Reporting Carrier On-Time Performance Dataset](https://dax-cdn.cdn.appdomain.cloud/dax-airline/1.0.1/data-preview/index.html)
- **Records:** ~200 million domestic US flights
- **Coverage:** Multiple years of flight data
- **Features:** Departure/arrival times, delays, cancellations, delay reasons

## 📝 License

This project is provided as-is for educational and analytical purposes.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues or bugs
- Suggest new analyses or visualizations
- Improve documentation
- Add test coverage

## 📧 Support

For questions or issues, please open a GitHub issue or contact the maintainers.

---

**Last Updated:** December 2024  
**Status:** Active Development
