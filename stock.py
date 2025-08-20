import streamlit as st 
import pandas as pd 
import numpy as np 
import yfinance as yf
import plotly.express as px
import datetime
from stocknews import StockNews

# ------------------- HEADER -------------------
col1, col2 = st.columns([1,5])
with col1:
    st.image("stock-market.png", width=90)

with col2:
    st.markdown("<h1 style='text-align: center;'>STOCK DASHBOARD</h1>", unsafe_allow_html=True)

# ------------------- SIDEBAR -------------------
st.sidebar.title("Stock Options")
ticker = st.sidebar.text_input('Ticker', 'AAPL')   # Default Apple
start_date = st.sidebar.date_input('Start_Date')
end_date = st.sidebar.date_input('End_Date')

# ------------------- DOWNLOAD DATA -------------------
if ticker:
    data = yf.download(ticker, start=start_date, end=end_date)

    if not data.empty:
        st.write(data)

        # Plot Closing Price
        fig = px.line(data, x=data.index, y=data['Close'].squeeze(), title=f"{ticker} Closing Price")
        st.plotly_chart(fig)

        # Tabs
        pricing_data, fundamental_data, news = st.tabs(["Pricing Data", "Fundamental Data", "Top 10 News"])

        # ------------------- PRICING DATA -------------------
        with pricing_data:
            st.header('Price Movements')
            data2 = data.copy()
            data2['% Change'] = data['Close'] / data['Close'].shift(1) - 1
            data2.dropna(inplace=True)
            st.write(data2)

            # Annual Return
            annual_return = data2['% Change'].mean() * 252 * 100
            st.write('Annual Return is:', round(annual_return, 2), '%')

            # Standard Deviation
            stdev = np.std(data2['% Change']) * np.sqrt(252)
            st.write('Standard Deviation is:', round(stdev*100, 2), '%')

            # Risk Adjusted Return
            st.write('Risk Adj. Return is:', round(annual_return/(stdev*100), 2))

        # ------------------- FUNDAMENTAL DATA (via yfinance) -------------------
        with fundamental_data:
            stock = yf.Ticker(ticker)

            st.subheader("Balance Sheet")
            st.write(stock.balance_sheet)

            st.subheader("Income Statement")
            st.write(stock.financials)

            st.subheader("Cash Flow Statement")
            st.write(stock.cashflow)

        # ------------------- STOCK NEWS -------------------
        with news:
            st.header(f'News of {ticker}')
            sn = StockNews(ticker, save_news=False)
            df_news = sn.read_rss()
            
            for i in range(min(10, len(df_news))):
                st.subheader(f'News {i+1}')
                st.write(df_news['published'][i])
                st.write(df_news['title'][i])
                st.write(df_news['summary'][i])
                title_sentiment = df_news['sentiment_title'][i]
                st.write(f'Title Sentiment: {title_sentiment}')
                news_sentiment = df_news['sentiment_summary'][i]
                st.write(f'Summary Sentiment: {news_sentiment}')

    else:
        st.error("No data found for this ticker. Please try another symbol.")


          



