from fastapi import FastAPI, Depends
from datetime import datetime
import httpx
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Status, Version

app = FastAPI()

login = 'kodintsev_roman'
password = '5kwSbxpygiM#12'

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



@app.get("/")
def get_home():
    return {"Hello": "World"}



@app.get("/status")
def get_status(db: Session = Depends(get_db)):
    testData = {"stand": "TEST",
                "status": '',
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "date": datetime.now().strftime("%d-%m-%Y"),
                "description": ''}

    with httpx.Client(verify=False) as client:
        try:
            response = client.get(
                'http://promo-lenta-test.k8s.gf/authentication/login',
                headers=headers,
                auth=(login, password),
                follow_redirects=True,
                timeout=10
            )
            response.raise_for_status()

            if response.status_code == 200:
                testData["status"] = 200
                testData["description"] = "Сервис доступен!"
                # return testData
            else:
                testData["status"] = response.status_code
                testData["description"] = "Ошибка! Сервис недоступен!"
                # return testData


        except Exception as e:
            testData["status"] = 0
            testData["description"] = f"При попытке установить статус была выявлена критическая ошибка!"

        finally:
            db_item = Status(
                status_code=testData["status"],
                status_desc=testData["description"],
                timestamp=datetime.now(),
                stand=testData["stand"],
            )
            db.add(db_item)
            db.commit()
            db.refresh(db_item)

            return testData



"""Для одного стенда"""
@app.get("/version")
def get_version(db: Session = Depends(get_db)):

    with httpx.Client(verify=False) as client:
        response = client.get(
            url="http://promo-lenta-test.k8s.gf/api/v1.0/version",
            headers=headers,
            follow_redirects=True
        )
    stand_version = response.json()['version']

    db_item = Version(
        stand = "TEST",  # Тут можно динамически взять из URL
        version = stand_version
                       )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {"version": stand_version}