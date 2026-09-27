import json
import os

from http.server import BaseHTTPRequestHandler
from openai import OpenAI


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            # 1. 브라우저에서 보낸 데이터 읽기
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            data = json.loads(body.decode("utf-8"))

            grade = data.get("grade", "").strip()
            interest = data.get("interest", "").strip()
            topic = data.get("topic", "").strip()


            # 2. 빈 입력 검사
            if not grade or not interest or not topic:
                self.send_json(
                    400,
                    {"error": "학년, 관심사, 주제를 모두 입력해주세요."}
                )
                return


            # 3. 환경 변수에서 OpenAI API 키 가져오기
            api_key = os.environ.get("OPENAI_API_KEY")

            if not api_key:
                self.send_json(
                    500,
                    {"error": "OPENAI_API_KEY가 설정되지 않았습니다."}
                )
                return


            # 4. OpenAI 연결
            client = OpenAI(api_key=api_key)


            # 5. AI에게 보낼 프롬프트
            prompt = f"""
너는 초등학생의 창의적인 프로젝트 활동을 도와주는
친절한 교육 아이디어 코치야.

학생 정보:
- 학년: {grade}
- 관심사: {interest}
- 만들고 싶은 주제: {topic}

이 학생이 실제로 도전해볼 수 있는
재미있고 창의적인 프로젝트 아이디어 하나를 제안해줘.

반드시 다음 형식으로 한국어로 작성해줘.

🌟 프로젝트 이름
재미있는 프로젝트 이름

💡 어떤 프로젝트인가요?
학생이 이해하기 쉬운 설명

🎯 도전 미션
1. 첫 번째 미션
2. 두 번째 미션
3. 세 번째 미션

🚀 한 단계 더!
프로젝트를 더 발전시킬 수 있는 추가 아이디어

초등학생이 이해하기 쉬운 표현을 사용하고,
너무 어렵거나 거창한 프로젝트는 제안하지 마.
직접 만들고 완성할 수 있는 아이디어를 제안해줘.
"""


            # 6. OpenAI API 호출
            response = client.responses.create(
                model="gpt-5.6-luna",
                input=prompt
            )


            # 7. AI 결과 가져오기
            result = response.output_text


            # 8. 브라우저에 결과 반환
            self.send_json(
                200,
                {"result": result}
            )


        except Exception as error:

            print("SparkIdea AI Error:", str(error))

            self.send_json(
                500,
                {"error": "AI 아이디어 생성 중 오류가 발생했습니다."}
            )


    def send_json(self, status_code, data):

        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status_code)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.end_headers()

        self.wfile.write(response)