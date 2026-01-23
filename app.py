import streamlit as st
import yfinance as yf
import pandas as pd
import datetime,base64

# 1. 페이지 설정
st.set_page_config(page_title="우리 가족 주식 포트폴리오", layout="wide")

st.title(f"오늘 날짜 : {datetime.date.today()} 현재 시각 : {datetime.datetime.now().strftime("%H:%M:%S")}")
st.markdown("오늘의 주요 뉴스들입니다.")

# 2. 사이드바: 종목 선택 기능
st.sidebar.header("종목 선택")
# 딕셔너리로 종목 이름과 티커(Ticker) 매핑
portfolio = {
    "삼성전자": "005930.KS",
    "현대차": "005380.KS",
    "YG": "122870.KQ",
}

# 선택 박스 만들기
selected_stock_name = st.sidebar.selectbox("보고 싶은 종목을 선택하세요", list(portfolio.keys()))
ticker_symbol = portfolio[selected_stock_name]

# 3. 데이터 가져오기 (yfinance 이용)
with st.spinner('데이터를 불러오는 중...'):
    stock_data = yf.Ticker(ticker_symbol)
    # 최근 1년치 데이터 가져오기
    df = stock_data.history(period="1y")

# 4. 메인 화면 구성
if not df.empty:
    # 현재가 정보 표시
    current_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    price_diff = current_price - prev_price
    
    # 통화 단위 설정 (한국 주식은 원, 미국 주식은 달러)
    currency = "KRW" if (".KS" in ticker_symbol or ".KQ" in ticker_symbol) else "USD"
    
    # 멋진 숫자 카드(Metric) 표시
    st.metric(
        label=f"{selected_stock_name} 현재가",
        value=f"{current_price:,.0f} {currency}" if currency == "KRW" else f"{current_price:,.2f} {currency}",
        delta=f"{price_diff:,.0f} (전일대비)" if currency == "KRW" else f"{price_diff:,.2f} (전일대비)"
    )

    # 5. 차트 그리기 (Streamlit 내장 차트)
    st.subheader("지난 1년 주가 흐름")
    st.line_chart(df['Close'])
    
    # 데이터 표 보여주기 (옵션)
    with st.expander("상세 데이터 보기"):
        st.dataframe(df.sort_index(ascending=False))

else:
    st.error("데이터를 가져오는데 실패했습니다.")
    
# 6. page 이동하기
def get_image_base64(image_path) :
    with open(image_path,"rb") as img_file :
        return base64.b64encode(img_file.read()).decode()
    
img_base64 = get_image_base64("pages/samsung.JPG")

st.markdown(
    f"""
    <a href="https://www.samsung.com" target="_blank" style="display: inline-block;">
        <img src="data:image/jpeg;base64,{img_base64}" 
             style="width: 100px; height: 100px; object-fit: cover; border-radius: 10px;">
    </a>
    """,
    unsafe_allow_html=True
)