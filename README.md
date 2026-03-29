📊 Crypto Asset Risk & Return Analysis
🔹 Overview

This project analyzes cryptocurrency price data using Python and evaluates key financial metrics such as returns, volatility, and cumulative performance.

The application retrieves historical market data from a public API, processes time-series data, and generates analytical outputs including visualizations and statistical summaries.

🔹 Features
📡 Fetch cryptocurrency data via API
📏 Detect and normalize sampling rate
🔁 Resample irregular time-series data
📈 Compute daily returns
📊 Calculate cumulative returns
📉 Generate price and return visualizations
💾 Export results to CSV and JSON
🔹 Methodology
Data Processing

Raw price data is obtained from an external API and converted into a structured time-series format.

Irregular sampling intervals are normalized using resampling and interpolation.

Returns Calculation

Daily returns are computed as:

[
r_t = \frac{P_t}{P_{t-1}} - 1
]

Cumulative Return

Cumulative return is calculated using:

[
R_t = \prod_{i=1}^{t}(1 + r_i)
]

Metrics

The following statistical metrics are computed:

Mean price
Standard deviation
Maximum price
Minimum price
🔹 Example Output

The program generates:

📈 Price chart
📉 Daily returns chart
📊 Cumulative return chart
📄 CSV file with processed data
📁 JSON file with summary statistics
🔹 Usage

Run the script from the command line:

python crypto_analyzer.py <coin> <days> <currency>
Example:
python crypto_analyzer.py ethereum 30 usd
Parameters:
coin — cryptocurrency name (e.g. bitcoin, ethereum)
days — number of days to analyze
currency — fiat currency (usd, eur, etc.)
🔹 Tech Stack
Python
Pandas
NumPy
Matplotlib
Requests
🔹 Project Structure
crypto-analyzer/
│
├── crypto_analyzer.py
├── README.md
├── requirements.txt
🔹 Key Concepts Demonstrated
Time-series data processing
Handling irregular sampling
Data normalization and interpolation
Financial return calculations
Basic risk analysis
API integration
🔹 Future Improvements
Add volatility and Sharpe ratio
Support multiple assets comparison
Implement rolling statistics
Build a simple web interface
🔹 Author

Andrey
