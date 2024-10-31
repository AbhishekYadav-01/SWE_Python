import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

# Loading and preparing the option chain data
def load_and_prepare_data(file_path, selected_expiry):
    with open(file_path, 'r') as file:
        data = json.load(file)
    option_chain = data['records']['data']
    rows = []
    for item in option_chain:
        if 'CE' in item and 'PE' in item:
            rows.append({
                'strikePrice': item['strikePrice'],
                'expiryDate': item['expiryDate'],
                'call_open_interest': item['CE']['openInterest'],
                'put_open_interest': item['PE']['openInterest'],
                'call_iv': item['CE']['impliedVolatility'],
                'put_iv': item['PE']['impliedVolatility'],
                'call_change_in_oi': item['CE']['changeinOpenInterest'],
                'put_change_in_oi': item['PE']['changeinOpenInterest'],
            })
    # Creating a DataFrame and filtering by the selected expiry date
    df = pd.DataFrame(rows)
    return df[df['expiryDate'] == selected_expiry]

# Setting the Streamlit title
st.title("::::::: Option Chain Dashboard :::::::")

# Selecting a background color
bg_color = st.color_picker("Please pick your favorite background Color and click anywhere to apply changes", "#f0f8ff")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Choosing the symbol and loading the file path
symbol = st.selectbox("Please select Symbol", ["NIFTY", "HDFCBANK"])
file_path = "NIFTY_option_chain.json" if symbol == "NIFTY" else "HDFCBANK_option_chain.json"

# Reading the expiry dates from the data
with open(file_path, 'r') as file:
    data = json.load(file)
expiry_dates = data['records']['expiryDates']
selected_expiry = st.selectbox("Please select expiry Date", expiry_dates)

# Preparing the data
df = load_and_prepare_data(file_path, selected_expiry)

# Plotting the Open Interest for calls and puts
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['strikePrice'], y=df['call_open_interest'], mode='lines+markers', name='Call OI'))
fig1.add_trace(go.Scatter(x=df['strikePrice'], y=df['put_open_interest'], mode='lines+markers', name='Put OI'))
fig1.update_layout(
    title=f" For {symbol}  Strike Price vs Open Interest for {selected_expiry}",
    xaxis_title="Strike Price",
    yaxis_title="Open Interest"
)

# Plotting Implied Volatility and Open Interest Change
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['strikePrice'], y=df['call_iv'], mode='lines+markers', name='Call IV', yaxis='y1'))
fig2.add_trace(go.Scatter(x=df['strikePrice'], y=df['put_iv'], mode='lines+markers', name='Put IV', yaxis='y1'))
fig2.add_trace(go.Scatter(x=df['strikePrice'], y=df['call_change_in_oi'], mode='lines+markers', name='Call OI Change', yaxis='y2'))
fig2.add_trace(go.Scatter(x=df['strikePrice'], y=df['put_change_in_oi'], mode='lines+markers', name='Put OI Change', yaxis='y2'))
fig2.update_layout(
    title=f" For {symbol} - Implied Volatility and Open Interest Change for {selected_expiry}",
    xaxis_title="Strike Price",
    yaxis=dict(title="Implied Volatility", side='left'),
    yaxis2=dict(title="Open Interest Change", overlaying='y', side='right')
)

# Displaying the plots in the Streamlit app
st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
