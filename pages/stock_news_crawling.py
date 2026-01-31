from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os,time
import FinanceDataReader as fdr

URL = "https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query="

def create_driver(stock_code : str) :
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36")
    options.add_argument("--window-size=1920,1080")

    try:
        # [핵심 수정] 서버에 이미 설치된 드라이버가 있는지 확인
        if os.path.exists("/usr/bin/chromedriver"):
            # Streamlit Cloud 서버용 경로 (다운로드 안 하고 이거 씀)
            service = Service("/usr/bin/chromedriver")
            print("🖥️ 서버 환경 감지: 시스템 드라이버를 사용합니다.")
        else:
            # 내 컴퓨터용 (자동 다운로드)
            service = Service(ChromeDriverManager().install())
            print("💻 로컬 환경 감지: 드라이버를 다운로드합니다.")

        df = fdr.StockListing('KRX')
        row = df[df['Code'] == stock_code]
        stock_name = row.iloc[0]['Name']
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(URL + stock_name)
        return driver
        
    except Exception as e:
        print(f"❌ 크롬 드라이버 실행 에러: {e}")
        raise e


def page_scroll(driver) :
    target_count = 150
    prev_height = driver.execute_script("return document.body.scrollHeight")
    
    while True :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        articles = driver.find_elements(By.CSS_SELECTOR, 'a[data-heatmap-target=".tit"]')
        current_count = len(articles)
        
        if current_count >= target_count :
            break
        
        curr_height = driver.execute_script("return document.body.scrollHeight")
        if curr_height == prev_height :
            break
        
        prev_height = curr_height

def get_title_link(driver) :
    title_link_dict = {}
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    tags = soup.select('a[data-heatmap-target=".tit"]')

    if not tags:
        print("속성 검색 실패, span 태그 기반으로 재검색합니다.")
        # span 태그를 먼저 찾고, 그 부모인 a 태그를 가져옴
        spans = soup.select("span.sds-comps-text-type-headline1")
        tags = [span.find_parent("a") for span in spans if span.find_parent("a")]

    for tag in tags:
        # 제목 가져오기 (태그 안의 텍스트)
        title = tag.get_text(strip=True)
        # 링크 가져오기
        link = tag.get("href")
        
        if link:
            title_link_dict[title] = link
        
    return title_link_dict