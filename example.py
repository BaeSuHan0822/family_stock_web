import streamlit as st
from datetime import datetime

# 화면을 넓게 써서 4개 뉴스를 배치하기 위해 설정
st.set_page_config(layout="wide", page_title="My Stock Dashboard")

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
st.subheader("오늘의 주요뉴스")

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
        st.image(news["img"], use_container_width=True)
        # 뉴스 제목
        st.write(f"**{news['title']}**")
        st.caption("2024.05.20 | 경제신문")

st.write("") # 여백
st.write("") # 여백

# --- 3. 하단: 환율 및 기업 로고 ---
st.subheader("환율 / 관심 기업")

# 3개의 컬럼 생성 (삼성, 현대, YG)
img_col1, img_col2, img_col3 = st.columns(3)

# 로고 이미지 주소 (임시로 위키미디어 주소 사용)
# 나중에 get_image_base64("pages/samsung.JPG") 코드로 바꾸세요!
logos = {
    "Samsung": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Samsung_Logo.svg/2560px-Samsung_Logo.svg.png",
    "Hyundai": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Hyundai_Motor_Company_logo.svg/2560px-Hyundai_Motor_Company_logo.svg.png",
    "YG": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/YG_Entertainment_logo.svg/1200px-YG_Entertainment_logo.svg.png"
}

with img_col1:
    st.image(logos["Samsung"], width=150)
    st.metric(label="삼성전자", value="78,000 원", delta="▲ 500 원")

with img_col2:
    st.image(logos["Hyundai"], width=150)
    st.metric(label="현대차", value="250,000 원", delta="▼ 1,000 원")

with img_col3:
    st.image(logos["YG"], width=120)
    st.metric(label="와이지엔터", value="43,000 원", delta="▲ 1,200 원")