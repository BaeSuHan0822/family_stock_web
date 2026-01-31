from google import genai
from dotenv import load_dotenv
from main_page_news_crawling import create_driver as main_driver,push_button,get_title_link as main_title_link
from pages.stock_news_crawling import create_driver as sub_driver,page_scroll,get_title_link as sub_title_link
import ast,os

def summarize_ai(from_where : str,code : str = None) :
    load_dotenv()

    if from_where == 'main' :
        # 메인 페이지 정리
        driver = main_driver()
        push_button(driver)
        title_link = main_title_link(driver)
    else :
        driver = sub_driver(code)
        page_scroll(driver)
        title_link = sub_title_link(driver)
    # 세부 페이지 정리
    

    api_key = os.getenv("GOOGLE_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    [너의 역할]
    너는 주식 공부를 20년간 한 주식 및 경제 전문가로서 주식을 잘 모르는 이들을 위해 주요 뉴스를 선택하는 셀렉터야.
    
    [데이터]
    다음은 오늘의 경제 뉴스 150여개의 헤드라인과 링크가 있는 데이터야
    {title_link.items()}
    
    
    [할 일]
    너의 역할과 같이 주식에 영향을 미칠 것 같은 헤드라인 4개를 선택해서 대답하면 돼
    
    [출력형식]
    1.출력형식은 반드시 **python의 List 형식**으로 출력해야돼
    2. **줄바꿈 문자(\\n)를 절대 사용하지 말고**, 처음부터 끝까지 **단 한 줄(Single line)**로 출력해.
    3. 리스트 안의 모든 문자열은 반드시 **큰따옴표(")**로 감싸줘. (작은따옴표 사용 금지)
    4. 코드 블록(```)이나 인사말, 설명은 제외하고 오직 순수한 리스트만 출력해.
    
    출력 형식 예시는 다음과 같다.
    [["제목1","링크1","선정이유","너가 생각하는 주식에 끼칠 영향 분석 결과"],
    ["제목2","링크2","선정이유","너가 생각하는 주식에 끼칠 영향 분석 결과"],...]
    선정이유와 영향 분석 결과에 대한 답변은 "~입니다"와 같은 **하십시오체**로 작성해
    
    [작성 예시]
    [["삼성전자, 3분기 실적 발표", "http://...", "반도체 업황 회복 확인", "반도체 관련주 상승 예상"], ["..."]]
    """

    response = client.models.generate_content(
        model = "gemini-flash-latest",
        contents = prompt
    )
    
    return ast.literal_eval(response.text.strip())