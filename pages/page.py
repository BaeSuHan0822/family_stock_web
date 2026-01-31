import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz,random
import FinanceDataReader as fdr
from summarize_news import summarize_ai

KST = pytz.timezone('Asia/Seoul')

# 1. 페이지 설정 
st.set_page_config(page_title="주식 상세 정보", layout="wide")

query_params = st.query_params

if "code" in query_params :
    ticker_symbol = query_params["code"]
else :
    ticker_symbol = "005930.KS"
    
stock_code = ticker_symbol.split('.')[0]
df = fdr.StockListing('KRX')
row = df[df['Code'] == stock_code]
stock_name = row.iloc[0]['Name']

@st.cache_data(ttl=10800,show_spinner = "AI가 뉴스를 분석 중입니다...")
def load_ai_news(code) :
    return summarize_ai("sub",code)

news_list = load_ai_news(stock_code)

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
        
st.divider()
st.subheader(f"오늘의 {stock_name} 주요뉴스")

col1, col2, col3, col4 = st.columns(4)
columns = [col1, col2, col3, col4]
for col, news in zip(columns, news_list):
    with col:
        title = news[0]
        link = news[1]
        reason = news[2]
        analysis = news[3]
        
        random_id = random.randint(1, 1000)
        img_url = f"https://picsum.photos/300/200?random={random_id}"
        
        st.markdown(
            f"""
            <a href="{link}" target="_blank">
                <img src="{img_url}" style="width:100%; border-radius: 10px; margin-bottom: 10px;">
            </a?
            """,
            unsafe_allow_html=True
        )
        
        # 기존 코드 지우고 이걸로 붙여넣으세요!
        st.markdown(
            f"""
            <a href="{link}" target="_blank" style="color: #007bff; text-decoration: underline; font-weight: bold;">
                {title}
            </a>
            """,
            unsafe_allow_html=True
        )
        with st.expander("🔍 AI 요약본 확인하기 (클릭)") :
            st.markdown(f"**💡 선정 이유**")
            st.info(reason) # 파란색 박스로 강조
            
            st.markdown(f"**📈 주식 시장 영향**")
            st.success(analysis) # 초록색 박스로 강조
            
            st.markdown(f"[👉 기사 원문 읽기]({link})")