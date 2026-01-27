import streamlit as st
import yfinance as yf
import pandas as pd
import pytz,ast,base64,random
from datetime import datetime
from summarize_news import summarize_ai

KST = pytz.timezone('Asia/Seoul')

# 1. 페이지 설정
st.set_page_config(page_title="주식 포트폴리오", layout="wide")

# --- 1. 상단: 날짜와 시간 ---
# 현재 시간 가져오기
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
st.divider() # 구분선

# --- 2. 중단: 오늘의 주요 뉴스 (네모 박스 4개) ---
st.subheader("오늘의 경제 주요뉴스")

# 4개의 컬럼 생성
col1, col2, col3, col4 = st.columns(4)
@st.cache_data(ttl=10800,show_spinner = "AI가 뉴스를 분석 중입니다...")
def load_ai_news() :
    return summarize_ai()

news_list = load_ai_news()

# 반복문으로 뉴스 카드 배치
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
        
        st.markdown(f"**[{title}]({link})**")
        with st.expander("🔍 AI 요약본 확인하기 (클릭)") :
            st.markdown(f"**💡 선정 이유**")
            st.info(reason) # 파란색 박스로 강조
            
            st.markdown(f"**📈 주식 시장 영향**")
            st.success(analysis) # 초록색 박스로 강조
            
            st.markdown(f"[👉 기사 원문 읽기]({link})")
        
        

st.write("") # 여백
st.write("") # 여백

# --- 3. 하단: 환율 및 기업 로고 ---
st.subheader("환율 / 관심 기업")

with st.spinner('데이터를 불러오는 중...'):
    exchange_rate_data = yf.Ticker("KRW=X")
    # 최근 1년치 데이터 가져오기
    df = exchange_rate_data.history(period="1y")
    
if not df.empty:
    current_rate = df['Close'].iloc[-1]
    prev_rate = df['Open'].iloc[-1]
    
    diff = current_rate - prev_rate
    
    # 멋진 숫자 카드(Metric) 표시
    st.metric(
        label = "USD/KRW 환율",
        value = f"{current_rate:.2f}원",
        delta = f"{diff:.2f}원"
    )
    st.caption(f"전일 종가 : {prev_rate:.2f}원")
    # 5. 차트 그리기 (Streamlit 내장 차트)
    st.subheader("지난 1달간 환율 차트")
    st.line_chart(df['Close'])
else:
    st.error("데이터를 가져오는데 실패했습니다.")

# 3개의 컬럼 생성 (삼성, 현대, YG)
img_col1, img_col2, img_col3 = st.columns(3)

# 6. 이동할 페이지 로고 설정
samsung_img = "https://cdn.vectorstock.com/i/500p/18/66/samsung-brand-logo-phone-symbol-blue-and-white-vector-46231866.jpg"
hyundai_img = "https://static.vecteezy.com/system/resources/previews/020/500/443/non_2x/hyundai-logo-brand-symbol-with-name-white-design-south-korean-car-automobile-illustration-with-blue-background-free-vector.jpg"
yg_img = "https://static.wikia.nocookie.net/kpop/images/3/31/YG_Entertainment_logo.png/revision/latest?cb=20211222013131"

# 화면을 3개의 컬럼으로 나눕니다 (비율 조절 가능)
col1, col2, col3 = st.columns(3)

### 삼성 화면 이동
with col1:
    # [삼성] 화면 이동
    st.markdown(
        f"""
        <a href="pages?code=005930.KS" target="_blank">
            <img src="{samsung_img}" 
                 style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px;">
        </a>
        """, unsafe_allow_html=True
    )

### 현대 화면 이동
with col2:
    st.markdown(
        f"""
        <a href="pages?code=005380.KS" target="_blank">
            <img src="{hyundai_img}" 
                 style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px;">
        </a>
        """, unsafe_allow_html=True
    )

### 와이지 화면 이동
with col3:
    st.markdown(
        f"""
        <a href="pages?code=122870.KQ" target="_blank">
            <img src="{yg_img}" 
                 style="width: 200px; height: 200px; object-fit: cover; border-radius: 10px;">
        </a>
        """, unsafe_allow_html=True
    )