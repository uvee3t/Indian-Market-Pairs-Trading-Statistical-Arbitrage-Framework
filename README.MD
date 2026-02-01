App link - https://indian-market-pairs-trading-statistical-arbitrage-framework-9r.streamlit.app

# Indian-Market-Pairs-Trading-Statistical-Arbitrage-Framework
Pairs Trading is a statistical arbitrage strategy that exploits temporary mispricing between two historically related financial instruments. Instead of predicting market direction, the strategy focuses on mean reversion of price relationships, making it largely market-neutral.


📈 Statistical Arbitrage: Indian Market Pairs Trading Framework An End-to-End Quantitative Pipeline utilizing Machine Learning and Time-Series Econometrics.

Project Overview This project develops a robust framework for Pairs Trading (a market-neutral investment strategy) specifically tailored for the National Stock Exchange (NSE). It systematically identifies cointegrated stock pairs using clustering techniques and simulates strategy performance through a custom backtesting engine and an interactive dashboard.

Universe & Data Scope The strategy is applied to a universe of 90+ high-liquidity Indian tickers organized into 10 key sectors:

Banking: HDFC, ICICI, SBI, Axis, Kotak, etc.

IT: TCS, Infosys, Wipro, HCL Tech, Tech Mahindra, etc.

Auto: Maruti, Tata Motors, M&M, Bajaj Auto, Eicher, etc.

Energy & Metal: Reliance, ONGC, Tata Steel, JSW Steel, etc.

Pharma, FMCG, Chemicals, Infra, and Financials.

Technical Architecture Phase I: Feature Engineering & Fundamental Analysis Data Ingestion: Real-time and historical data fetching via yfinance.
Metric Extraction: Analysis of Market Cap, PE Ratio, ROE, ROI, and Net Profit Margins to understand business fundamentals.

Beta Analysis: Calculating historical sensitivity to market movements.

Phase II: Unsupervised Learning (Clustering) To minimize the search space for pairs and ensure business similarity, we utilize:

Principal Component Analysis (PCA): For dimensionality reduction of fundamental features.

K-Means Clustering: To segment stocks into "statistical neighborhoods" where they are more likely to exhibit long-term cointegration.

Phase III: Statistical Modeling Stationarity Testing: Augmented Dickey-Fuller (ADF) test to ensure mean-reverting properties.

Cointegration: Engle-Granger Cointegration Test to find pairs with a stable long-term equilibrium.

Z-Score Calculation: Real-time monitoring of spread deviations from the mean to generate trade signals.

Phase IV: Strategy Backtesting & Visualization Risk Metrics: Calculation of Total Net Return, Max Drawdown, and Sharpe Ratio.

Equity Curve Simulation: Visualizing the growth of initial capital (e.g., ₹1,00,000) over time.

Interactive Dashboard: A Streamlit-based UI allowing for pair selection and real-time trade log analysis.

Tech Stack Language: Python
Analytical Core: pandas, numpy, statsmodels, scikit-learn

Visualization: matplotlib, seaborn, streamlit
