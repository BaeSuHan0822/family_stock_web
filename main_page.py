import streamlit as st
import yfinance as yf
import pandas as pd
import base64
from datetime import datetime

# 메인 페이지로 돌아가기
st.page_link("main_page.py", label="메인으로 돌아가기", icon="🏠")

# 1. 페이지 설정
st.set_page_config(page_title="주식 포트폴리오", layout="wide")

# --- 1. 상단: 날짜와 시간 ---
# 현재 시간 가져오기
@st.fragment(run_every=1)
def show_live_time() :
    now = datetime.now()
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

# 가짜 뉴스 데이터 (나중에 크롤링한 데이터로 교체하세요)
news_list = [
    {"title": "반도체 경기 회복 신호...", "img": "https://picsum.photos/300/200?random=1"},
    {"title": "전기차 시장의 미래는?", "img": "https://picsum.photos/300/200?random=2"},
    {"title": "글로벌 금리 인하 기대감", "img": "https://picsum.photos/300/200?random=3"},
    {"title": "K-콘텐츠 수출 역대 최고", "img": "https://picsum.photos/300/200?random=4"},
]

# 반복문으로 뉴스 카드 배치
columns = [col1, col2, col3, col4]
for col, news in zip(columns, news_list):
    with col:
        # 뉴스 썸네일 (가짜 이미지)
        st.image(news["img"], width="stretch")
        # 뉴스 제목
        st.write(f"**{news['title']}**")
        st.caption("2024.05.20 | 경제신문")
        with st.expander(f"AI 요약본 확인하기 (클릭)",expanded=False) :
            st.markdown("""
                        """)

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