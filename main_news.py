from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

question = "네이버에서 국내 증시에 대한 경제 주요 뉴스 4개의 헤드라인, url 주소를 알려줘"

response = client.models.generate_content(
    model = "gemini-flash-latest",
    contents = question
)

print(f"답변 : {response.text}")