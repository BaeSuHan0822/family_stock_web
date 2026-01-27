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
    options.add_argument("--no-sandbox") # [추가] 리눅스 환경 필수 옵션
    options.add_argument("--disable-dev-shm-usage") # [추가] 메모리 공유 문제 해결
    options.add_argument("User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    driver.get(URL)
    return driver


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
