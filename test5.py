import json
import configparser
import http.client
import streamlit as st

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/completions/LK-D2', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']['text']
        else:
            return 'Error'

config = configparser.ConfigParser()
config.sections()
config.read('./your_apikey5.ini')

completion_executor = CompletionExecutor(
    host=config['CLOVA']['host'],
    api_key=config['CLOVA']['api_key'],
    api_key_primary_val=config['CLOVA']['api_key_primary_val'],
    request_id=config['CLOVA']['request_id']
)

st.title('좋은 질문 생성기')
keyword = st.text_input(
    '키워드', 
    placeholder='키워드를 입력해 주세요'
)

if keyword:
    preset_text = f'다음 키워드를 포함하여 다음과 같이 질문형 문장을 생성합니다.\n\n키워드: 달팽이\n\n질문: 1. 이 책에 어떤 동물이 나왔나요?\n2. 이 동물의 이름은 무엇인가요?\n3. 이 동물은 무슨 색인가요?\n4. 달팽이는 어떤 음식을 좋아하나요?\n5. 달팽이의 수명은 얼마나 되나요?\n6. 달팽이처럼 느린 동물은 또 무엇이 있을까요?\n7. 달팽이는 동물일까요, 곤충일까요?\n8. 달팽이는 알을 낳을까요, 새끼를 낳을까요?\n9. 달팽이도 겨울잠을 잘까요?\n10. 달팽이를 키울 대 주의해야 할 점은 무엇인가요?\n11. 달팽이에게 먹이를 주면 어떤 색의 배설물이 나올까요?\n12. 달팽이가 상추를 좋아하는 이유는 무엇인가요?\n13. 달팽이와 거북이는 어떤 점이 비슷한가요? \n14. 만약 나에게도 달팽이처럼 등껍질이 있다면 어떻게 사용할 수 있을까요?\n15. 만약 달팽이를 애완동물로 키우면 어떨까요?###\n키워드:{keyword}'

    request_data = {
        'text': preset_text,
        'maxTokens': 303,
        'temperature': 0.1,
        'topK': 0,
        'topP': 0.8,
        'repeatPenalty': 5.0,
        'start': '\n###질문:',
        'stopBefore': ['###', '키워드:', '질문:', '###\n'],
        'includeTokens': True,
        'includeAiFilters': True,
        'includeProbs': True
    }

    response_text = completion_executor.execute(request_data)
    #print(response_text)
    st.markdown(response_text.split('###')[1])