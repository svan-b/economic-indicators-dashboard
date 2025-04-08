import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Page configuration
st.set_page_config(
    page_title="Economic Indicators Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header section
st.title("Economic Indicators Dashboard")
st.caption("Data source: Bloomberg Terminal & BLS")
st.write(f"Last updated: {datetime.date.today().strftime('%B %d, %Y')}")

# Sidebar with data upload option
st.sidebar.header("Data Options")

# File uploader for future real data
uploaded_file = st.sidebar.file_uploader("Upload Excel data", type=["xlsx", "xls"])

# Filters
st.sidebar.header("Filters")
time_period = st.sidebar.selectbox(
    "Time Period", 
    ["Last 6 Months", "Last 12 Months", "Year to Date", "Custom"]
)

if time_period == "Custom":
    start_date = st.sidebar.date_input("Start Date", datetime.date(2024, 10, 1))
    end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Function to create dummy data (to be replaced with real data later)
def create_dummy_data():
    # Key metrics
    key_metrics = {
        "Steel Price": {"value": 342.17, "change": 0.93, "period": "vs Q4 2024"},
        "Oil Price (WTI)": {"value": 78.45, "change": -1.2, "period": "vs Q4 2024"},
        "Freight Rate Index": {"value": 112.47, "change": -5.0, "period": "Semi-Annual"},
        "Grinding Media Index": {"value": 121.33, "change": 0.40, "period": "vs 2024"},
        "Equipment Index": {"value": 146.52, "change": 9.01, "period": "vs 2024"},
        "Supply Chain Pressure": {"value": 98.72, "change": -0.81, "period": "vs Q4 2024"}
    }
    
    # Time series data
    dates = pd.date_range(start='2024-10-01', periods=6, freq='M')
    time_series = pd.DataFrame({
        'Date': dates,
        'Steel Price': [330, 335, 338, 340, 342, 345],
        'Oil Price': [80, 78, 77, 76, 78, 79],
        'Supply Chain Index': [100, 99.5, 99, 98.8, 98.7, 98.5],
        'Freight Rate': [115, 114, 113, 112.5, 112.4, 112.3],
        'Grinding Media': [120, 120.5, 120.8, 121, 121.2, 121.4]
    })
    
    # PMI data
    pmi_data = pd.DataFrame({
        'Country': ['Canada', 'US', 'Peru', 'Chile', 'China'],
        'Manufacturing PMI': [51.2, 52.7, 49.8, 50.3, 51.8],
        'Input Prices Sub-index': [58.3, 57.1, 55.9, 56.2, 54.7]
    })
    
    # Forecast data
    forecast_data = pd.DataFrame({
        'Indicator': ['Steel Price', 'Oil Price (WTI)', 'Freight Rate Index', 
                     'Grinding Media Index', 'Equipment Index', 'Supply Chain Pressure'],
        'Current': [0.93, -1.2, -5.0, 0.40, 9.01, -0.81],
        'Q2 2025 (Forecast)': [0.97, -0.8, -4.5, 0.45, 9.2, -0.79],
        'Q3 2025 (Forecast)': [1.02, -0.5, -3.8, 0.52, 9.3, -0.75],
        'Trend': ['Increasing', 'Improving', 'Improving', 'Slight Increase', 'Increasing', 'Improving']
    })
    
    return key_metrics, time_series, pmi_data, forecast_data

# Check if we have uploaded data, otherwise use dummy data
if uploaded_file is not None:
    st.sidebar.success("Data file uploaded successfully!")
    # This is where you would process the real data
    # For now, we'll still use dummy data
    key_metrics, time_series, pmi_data, forecast_data = create_dummy_data()
else:
    # Use dummy data
    key_metrics, time_series, pmi_data, forecast_data = create_dummy_data()

# Main Dashboard Content
# =====================

# 1. Key Metrics Section
st.header("Key Metrics Summary")
cols = st.columns(3)
metric_list = list(key_metrics.items())

for i, (metric_name, metric_data) in enumerate(metric_list):
    col_index = i % 3
    with cols[col_index]:
        change = metric_data["change"]
        st.metric(
            label=f"{metric_name} ({metric_data['period']})",
            value=f"{metric_data['value']:.2f}",
            delta=f"{change:.2f}%"
        )

# 2. Commodity Price Trends
st.header("Commodity Price Trends (6-month)")

# Allow user to select which commodities to display
commodities = st.multiselect(
    "Select commodities to display",
    options=["Steel Price", "Oil Price", "Supply Chain Index", "Freight Rate", "Grinding Media"],
    default=["Steel Price", "Oil Price", "Supply Chain Index"]
)

# Plot the selected commodities
if commodities:
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    for commodity in commodities:
        ax1.plot(time_series['Date'], time_series[commodity], marker='o', label=commodity)
    
    ax1.set_title('6-Month Commodity Price Trends')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    st.pyplot(fig1)
else:
    st.warning("Please select at least one commodity to display")

# 3. Equipment Index Comparison (Colin's requirement)
st.header("Equipment Index Comparison")
equipment_data = pd.DataFrame({
    'Index': ['CAT Equipment', 'Komatsu Equipment', 'John Deere Equipment'],
    'Current Value': [146.52, 139.8, 142.3],
    'YoY Change': [9.01, 7.2, 8.5]
})

fig2, ax2 = plt.subplots(figsize=(10, 5))
bars = ax2.bar(equipment_data['Index'], equipment_data['YoY Change'])

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'+{height:.1f}%', ha='center', va='bottom')

ax2.set_title('Equipment Indices Year-over-Year Changes')
ax2.set_ylabel('YoY Change (%)')
ax2.grid(axis='y', alpha=0.3)
st.pyplot(fig2)

# 4. PMI Data Section
st.header("Manufacturing PMI - Input Prices Sub-index")
fig3, ax3 = plt.subplots(figsize=(10, 5))
bars = ax3.bar(pmi_data['Country'], pmi_data['Input Prices Sub-index'])

# Add data labels
for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{height:.1f}', ha='center', va='bottom')

ax3.set_title('Input Prices Sub-index by Country')
ax3.set_ylabel('Index Value')
ax3.axhline(y=50, color='r', linestyle='-', alpha=0.3)  # Add reference line at 50
ax3.grid(axis='y', alpha=0.3)
st.pyplot(fig3)

# 5. Table view of PMI data
st.subheader("PMI Data Table")
st.dataframe(pmi_data, use_container_width=True)

# 6. Forecast summary
st.header("Forecast Summary (Next 2 Quarters)")
st.dataframe(forecast_data, use_container_width=True)

# 7. Data Download Section
st.header("Export Data")
time_series_csv = time_series.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Time Series Data as CSV",
    data=time_series_csv,
    file_name='economic_indicators_timeseries.csv',
    mime='text/csv',
)

# Display data source and notes
st.sidebar.markdown("---")
st.sidebar.caption("""
**Data Sources:**
- Bloomberg Terminal
- Bureau of Labor Statistics (BLS)
- Manufacturing PMIs
- New York Fed Supply Chain Pressure Index
""")

st.sidebar.caption("Dashboard created with Streamlit")