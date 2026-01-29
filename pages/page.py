import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz

KST = pytz.timezone('Asia/Seoul')

# 1. 페이지 설정 
st.set_page_config(page_title="주식 상세 정보", layout="wide")

query_params = st.query_params

if "code" in query_params :
    ticker_symbol = query_params["code"]
else :
    ticker_symbol = "005930.KS"

# 메인으로 돌아가기 버튼
st.page_link("app.py", label="메인으로 돌아가기", icon="🏠")

@st.fragment(run_every=1)
def show_live_time() :
    now = datetime.now(KST)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    st.markdown(f"""
        <h3 style='text-align: left; margin-bottom: 0;'>
            오늘 날짜 : {date_str} &nbsp;&nbsp;&nbsp; 
            <span style='color: gray; font-size: 0.8em;'>현재 시각 : {time_str}</span>
        </h3>
    """, unsafe_allow_html=True)

show_live_time()
st.divider()

with st.spinner("주식 정보를 가져오는 중....") :
    try :
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.info
        
        stock_name = stock_info.get('longName',stock_info.get('shortName',ticker_symbol))
        st.title(f"{stock_name} ({ticker_symbol}) 상세정보")
        
        df = stock.history(period = '3mo')
        
        if not df.empty :
            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2]
            price_diff = current_price - prev_price
    
            # 통화 단위 설정 (한국 주식은 원, 미국 주식은 달러)
            currency = "KRW" if (".KS" in ticker_symbol or ".KQ" in ticker_symbol) else "USD"
    
            # 멋진 숫자 카드(Metric) 표시
            st.metric(
                label=f"{stock_name} 현재가",
                value=f"{current_price:,.0f} {currency}" if currency == "KRW" else f"{current_price:,.2f} {currency}",
                delta=f"{price_diff:,.0f} (전일대비)" if currency == "KRW" else f"{price_diff:,.2f} (전일대비)"
            )

            # 5. 차트 그리기
            fig,ax = plt.subplots(figsize=(8,4))
            ax.plot(df.index,df['Close'],color = 'red')
            
            ax.set_title("3 Month Price Trend")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.grid(True)
            
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            
            st.pyplot(fig,width="stretch")
    
            # 데이터 표 보여주기 (옵션)
            with st.expander("상세 데이터 보기"):
                st.dataframe(df.sort_index(ascending=False))

        else:
            st.error("데이터를 가져오는데 실패했습니다.")

    except Exception as e:
        # 에러 발생 시(네트워크 문제나 잘못된 티커 등)
        st.error(f"정보를 가져오는 중 오류가 발생했습니다: {e}")
        # 에러가 나도 제목은 보여주기 위해 티커로 표시
        st.title(f"{ticker_symbol} 상세 정보")