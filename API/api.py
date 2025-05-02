from fastapi import FastAPI
from datetime import datetime
import httpx

app = FastAPI()

api_versions = dict()

api_dict = {'DEV': 'https://ao-gpn-dev.platform.gf/api/autoorder/version', 'TEST': 'https://ao-gpn-test.platform.gf/api/autoorder/version', 'CALC': 'https://autoorder-calculate.platform.gf/api/autoorder/version'}

json_data = {
    'userName': 'kodintsev_roman',
    'password': '5kwSbxpygiM#',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://ao-gpn-dev.platform.gf',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://ao-gpn-dev.platform.gf/authentication/login',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Opera";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition Yx 05)',
}

# headers = {
#     'accept': 'application/json, text/plain, */*',
#     'accept-encoding': 'gzip, deflate, br, zstd',
#     'accept-language': 'ru-RU,ru;q=0.9',
#     'cache-control': 'no-cache',
#     'content-length': '639',
#     'content-type': 'application/x-www-form-urlencoded',
#     'origin': 'https://gfc.dev.platform.lenta.tech',
#     'pragma': 'no-cache',
#     'priority': 'u=1, i',
#     'referer': 'https://gfc.dev.platform.lenta.tech/authentication/login-callback',
#     'sec-ch-ua': '"Not(A:Brand";v="99", "Opera";v="118", "Chromium";v="133"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': "Windows",
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0 (Edition Yx 05)'
# }

@app.get("/")
def get_home():
    return {"Hello": "World"}

# @app.get("/status")
# def get_status():
#
#     with httpx.Client(verify=False) as client:
#         response = client.get(
#             'https://autoorder-calculate.platform.gf/authentication/login',
#             headers=headers,
#             auth=('kodintsev_roman', '5kwSbxpygiM#'),
#             follow_redirects=True
#         )
#
#         calcData = {"stand": "CALC-стенд", "status": response.status_code,
#                    "timestamp": datetime.now().strftime("%H:%M:%S"), "date": datetime.now().strftime("%d-%m-%Y"),
#                    "description": {True: "Сервис доступен!", False: "Ошибка! Сервис не доступен!"}[
#                        response.status_code == 200]}
#
#         response = client.get(
#             'https://ao-gpn-dev.platform.gf/authentication/login',
#             headers=headers,
#             auth=('kodintsev_roman', '5kwSbxpygiM#'),
#             follow_redirects=True
#         )
#
#         devData = {"stand": "DEV-стенд", "status": response.status_code,
#                    "timestamp": datetime.now().strftime("%H:%M:%S"), "date": datetime.now().strftime("%d-%m-%Y"),
#                    "description":{True: "Сервис доступен!", False: "Ошибка! Сервис не доступен!"} [response.status_code==200]}
#
#         response = client.get(
#                     'https://ao-gpn-test.platform.gf/authentication/login',
#                     headers=headers,
#                     auth=('kodintsev_roman', '5kwSbxpygiM#'),
#                     follow_redirects=True
#                 )
#
#         testData = {"stand": "TEST-стенд", "status": response.status_code,
#                    "timestamp": datetime.now().strftime("%H:%M:%S"), "date": datetime.now().strftime("%d-%m-%Y"),
#                    "description":{True: "Сервис доступен!", False: "Ошибка! Сервис не доступен!"} [response.status_code==200]}
#
#     return calcData, devData, testData

@app.get("/status")
def get_status():

    with httpx.Client(verify=False) as client:
        response = client.get(
            'http://promo-lenta-test.k8s.gf/authentication/login',
            headers=headers,
            auth=('kodintsev_roman', '5kwSbxpygiM#12'),
            follow_redirects=True
        )

        testData = {"stand": "TEST-стенд", "status": response.status_code,
                   "timestamp": datetime.now().strftime("%H:%M:%S"), "date": datetime.now().strftime("%d-%m-%Y"),
                   "description": {True: "Сервис доступен!", False: "Ошибка! Сервис не доступен!"}[
                       response.status_code == 200]}

    return testData

"""Для трёх стендов"""
# @app.get("/version")
# def get_version():
#
#     for stand_name, stand_link in api_dict.items():
#
#         with httpx.Client(verify=False) as client:
#             response = client.get(
#                 url=stand_link,
#                 headers=headers,
#                 follow_redirects=True
#             )
#
#         val = response.text.split(': ')[1]
#         date, time = val.split(' ')
#         api_versions[stand_name] = [date, time]
#         print(api_versions)
#
#     return api_versions

"""Для одного стенда"""
@app.get("/version")
def get_version():

    with httpx.Client(verify=False) as client:
        response = client.get(
            url="http://promo-lenta-test.k8s.gf/api/v1.0/version",
            headers=headers,
            follow_redirects=True
        )
    stand_version = response.json()['version']
    return stand_version

    """Для трёх стендов"""
    # val = response.text.split(': ')[1]
    # date, time = val.split(' ')
    # api_versions[stand_name] = [date, time]
    # print(api_versions)

    # return api_versions
