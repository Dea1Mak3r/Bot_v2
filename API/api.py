from fastapi import FastAPI, Depends
from datetime import datetime
import httpx
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Status, Version
from config import settings


app = FastAPI()

login = settings.login
password = settings.password

STANDS = {
    "lenta": {"login_url": settings.LENTA_LOGIN_URL, "info_url": settings.LENTA_INFO_URL, "name": "LENTA"},
    "mars": {"login_url": settings.MARS_LOGIN_URL, "info_url": settings.MARS_INFO_URL, "name": "MARS"}
}



@app.get("/")
def get_home():
    return {"Hello": "World"}



@app.get("/status/{stand_name}")
async def get_status(stand_name: str, db: Session = Depends(get_db)):
    # Проверяем, знаем ли мы такой стенд
    stand_name = stand_name.lower()
    if stand_name not in STANDS:
        raise HTTPException(status_code=404, detail="Стенд не найден")

    config = STANDS[stand_name]

    testData = {"stand": config["name"],
                "status": 0,
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "date": datetime.now().strftime("%d-%m-%Y"),
                "description": ''}

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(
                config["login_url"],
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
                testData["description"] = f"Ошибка! Код: {response.status_code}"
                # return testData


        except httpx.RequestError as exc:
            testData["status"] = 500
            testData["description"] = f"Ошибка сети при запросе к {exc.request.url!r}"

        except Exception as e:
            testData["status"] = 0
            testData["description"] = f"Критическая ошибка: {str(e)}"

        finally:
            db_item = Status(
                status_code=testData["status"],
                status_desc=testData["description"],
                timestamp=datetime.now(),
                stand=config["name"],
            )
            db.add(db_item)
            db.commit()
            db.refresh(db_item)

            return testData


@app.get("/version/{stand_name}")
async def get_version(stand_name: str, db: Session = Depends(get_db)):
    stand_name = stand_name.lower()
    if stand_name not in STANDS:
        raise HTTPException(status_code=404, detail="Стенд не найден")

    config = STANDS[stand_name]

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(
                url=config["info_url"],
                timeout=10
            )
            response.raise_for_status()
            stand_version = response.json().get('version', 'unknown')
        except Exception as e:
            stand_version = "Error"

    db_item = Version(
        stand = config["name"],  # Тут можно динамически взять из URL
        version = stand_version
                       )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return {"stand": config["name"], "version": stand_version}


# История статусов для вывода на фронте
@app.get("/history/status")
async def get_status_history(limit: int = 1000, db: Session = Depends(get_db)):
    # Забираем последние N записей, сортируя по ID или времени
    history = db.query(Status).order_by(Status.id.asc()).limit(limit).all()
    return history

# Аккумулируем историю запросов версий
@app.get("/history/version")
async def get_version_history(limit: int = 1000, db: Session = Depends(get_db)):
    history = db.query(Version).order_by(Version.id.desc()).limit(limit).all()
    return history

# Отправка результатов тестирования Newman в бота
async def send_telegram_report(message: str):
    """Отправка сообщения в телеграм через API бота"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.ADMIN_CHAT_ID, # ID чата, куда слать отчет
        "text": message,
        "parse_mode": "Markdown"
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)