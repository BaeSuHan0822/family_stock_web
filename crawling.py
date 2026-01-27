from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

URL = "https://news.naver.com/section/101"

def create_driver() :
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

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(URL)
        return driver
        
    except Exception as e:
        print(f"❌ 크롬 드라이버 실행 에러: {e}")
        raise e


def push_button(driver) :
    target_count = 150
    current_count = 0
    while True :
        try :
            btn = driver.find_element(By.CSS_SELECTOR
                                  ,"a.section_more_inner._CONTENT_LIST_LOAD_MORE_BUTTON")
            btn.click()
        
            time.sleep(2)
        
            articles = driver.find_elements(By.CLASS_NAME,"sa_text_title")
            current_count = len(articles)
        
            if current_count >= target_count :
                break
    
        except Exception as e:
            print(f"에러 발생 : {e}")
            break

def get_title_link(driver) :
    title_link_dict = {}
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    tags = soup.select("a.sa_text_title")

    for idx,tag in enumerate(tags,1) :
        title = tag.get_text(strip=True)
        link = tag["href"]
        title_link_dict[title] = link
        
    return title_link_dict
