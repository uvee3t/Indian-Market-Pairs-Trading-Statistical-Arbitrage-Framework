import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Pairs Trading Dashboard", layout="wide")
st.title("📈 Pairs Trading Profit Simulator")

# --- 1. LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Load CSVs
        fundamentals = pd.read_csv("fundamentals.csv")
        trades = pd.read_csv("trade_df.csv")
        
        # Strip spaces from column names
        trades.columns = trades.columns.str.strip()
        
        # --- FIX: MAP EXIT DATE TO DATE ---
        if "Exit Date" in trades.columns:
            trades.rename(columns={"Exit Date": "Date"}, inplace=True)
        elif "Entry Date" in trades.columns:
            trades.rename(columns={"Entry Date": "Date"}, inplace=True)
        
        # Ensure 'Pair' exists (your CSV has 'pair_id')
        if "pair_id" in trades.columns:
            trades.rename(columns={"pair_id": "Pair"}, inplace=True)
            
        # Ensure Date column is datetime
        if "Date" in trades.columns:
            trades["Date"] = pd.to_datetime(trades["Date"])
        else:
            st.error(f"❌ No date column found. Available: {list(trades.columns)}")
            st.stop()
            
        return fundamentals, trades
    except FileNotFoundError:
        return None, None
fundamentals_df, trade_df = load_data()

if fundamentals_df is None or trade_df is None:
    st.error("❌ Data files (fundamentals.csv, trade_df.csv) not found. Please ensure they are in the same folder as this script.")
    st.stop()

# Create 'Pair' column if it doesn't exist
if "Pair" not in trade_df.columns:
    # Ensure Stock1 and Stock2 exist before concatenating
    if "Stock1" in trade_df.columns and "Stock2" in trade_df.columns:
        trade_df["Pair"] = trade_df["Stock1"] + " - " + trade_df["Stock2"]
    else:
        st.error("❌ 'Stock1' or 'Stock2' columns are missing from the CSV.")
        st.stop()

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("🛠 Strategy Controls")

# A. Investment Amount Input
initial_investment = st.sidebar.number_input(
    "Enter Investment Amount", 
    min_value=1000, 
    value=100000, 
    step=5000,
    help="Enter the amount you want to simulate investing in this pair."
)

# B. Stock Filter
all_stocks = pd.concat([trade_df["Stock1"], trade_df["Stock2"]]).unique()
selected_stock_filter = st.sidebar.selectbox("Filter by Stock (Optional)", ["All"] + list(all_stocks))

# C. Pair Selection
if selected_stock_filter != "All":
    filtered_pairs = trade_df[
        (trade_df["Stock1"] == selected_stock_filter) | 
        (trade_df["Stock2"] == selected_stock_filter)
    ]["Pair"].unique()
else:
    filtered_pairs = trade_df["Pair"].unique()

if len(filtered_pairs) == 0:
    st.warning("No pairs found for the selected filters.")
    st.stop()

selected_pair = st.sidebar.selectbox("Select Pair Strategy", filtered_pairs)

# --- 3. CALCULATIONS ---
pair_data = trade_df[trade_df["Pair"] == selected_pair].copy().reset_index(drop=True)

if pair_data.empty:
    st.warning("No trades found for this pair.")
    st.stop()

# Logic: Simple Return on Capital
pair_data["Cumulative Return"] = pair_data["Net Return"].cumsum()
pair_data["Equity"] = initial_investment + (initial_investment * pair_data["Cumulative Return"])
pair_data["Trade Profit"] = initial_investment * pair_data["Net Return"]

# Metrics
total_net_return_pct = pair_data["Net Return"].sum()
total_profit_value = initial_investment * total_net_return_pct
final_equity = initial_investment + total_profit_value
win_rate = (pair_data["Net Return"] > 0).mean()
total_trades = len(pair_data)

# --- 4. DASHBOARD DISPLAY ---

st.subheader(f"Results for {selected_pair}")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Net Profit", f"{total_profit_value:,.2f}", delta=f"{total_net_return_pct:.2%}")
col2.metric("Final Portfolio Value", f"{final_equity:,.2f}")
col3.metric("Win Rate", f"{win_rate:.2%}")
col4.metric("Total Trades", total_trades)

st.markdown("---")
col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    st.write(f"### 💰 Profit Growth (Equity Curve)")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Using the cleaned "Date" column
    ax.plot(pair_data["Date"], pair_data["Equity"], color="#00C805", linewidth=2, label="Portfolio Value")
    
    ax.fill_between(pair_data["Date"], pair_data["Equity"], initial_investment, 
                    where=(pair_data["Equity"] >= initial_investment), 
                    interpolate=True, color='green', alpha=0.1)
    ax.fill_between(pair_data["Date"], pair_data["Equity"], initial_investment, 
                    where=(pair_data["Equity"] < initial_investment), 
                    interpolate=True, color='red', alpha=0.1)
    
    ax.axhline(y=initial_investment, color='gray', linestyle='--', alpha=0.7, label="Initial Investment")
    
    ax.set_title(f"Growth of {initial_investment:,.0f} Investment")
    ax.set_ylabel("Value")
    ax.legend()
    ax.grid(True, alpha=0.2)
    
    st.pyplot(fig)

with col_chart2:
    st.write("### 📊 Trade Outcome Distribution")
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    sns.histplot(pair_data["Net Return"] * 100, bins=20, kde=True, ax=ax2, color="blue")
    ax2.set_xlabel("Return per Trade (%)")
    ax2.set_title("Distribution of Trade Returns")
    st.pyplot(fig2)

st.markdown("---")
st.write("### 📝 Detailed Trade Log")

display_df = pair_data[["Date", "Stock1", "Stock2", "Net Return", "Trade Profit", "Equity"]].copy()
display_df.index = display_df.index + 1
display_df.index.name = "Trade #"

st.dataframe(
    display_df.style.format({
        "Date": "{:%Y-%m-%d}",
        "Net Return": "{:.2%}",
        "Trade Profit": "{:,.2f}",
        "Equity": "{:,.2f}"
    })
)