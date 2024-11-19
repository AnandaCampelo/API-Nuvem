import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
from datetime import datetime, timedelta
import bcrypt
import requests
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("DATABASE_URL")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    nome: str
    email: str
    senha: str

class Login(BaseModel):
    email: str
    senha: str

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    nome = Column(String(50))
    email = Column(String(50), unique=True)
    hashed_password = Column(String(100))

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token inválido")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/registrar")
def registrar(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email já registrado")

    hashed_password = bcrypt.hashpw(user.senha.encode('utf-8'), bcrypt.gensalt())
    new_user = UserDB(nome=user.nome, email=user.email, hashed_password=hashed_password.decode('utf-8'))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"jwt": create_token({"email": login.email, "nome": db_user.nome})}

@app.post("/login")
def login(login: Login, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == login.email).first()
    if not db_user or not bcrypt.checkpw(login.senha.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Dados incorretos")

    return {"jwt": create_token({"email": login.email, "nome": db_user.nome})}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/consultar")
def consultar(request: Request, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat=44.34&lon=10.99&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao consultar a API de dados")

    try:
        data = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Erro ao decodificar a resposta JSON")

    forecast_list = data.get("list", [])
    if not forecast_list:
        raise HTTPException(status_code=404, detail="Nenhuma previsão encontrada")

    last_forecast = forecast_list[-1]
    formatted_data = {
        "city": data.get("city", {}).get("name"),
        "country": data.get("city", {}).get("country"),
        "forecast": {
            "time": datetime.utcfromtimestamp(last_forecast.get("dt")).isoformat(),
            "temperature": last_forecast.get("main", {}).get("temp"),
            "feels_like": last_forecast.get("main", {}).get("feels_like"),
            "temp_min": last_forecast.get("main", {}).get("temp_min"),
            "temp_max": last_forecast.get("main", {}).get("temp_max"),
            "pressure": last_forecast.get("main", {}).get("pressure"),
            "humidity": last_forecast.get("main", {}).get("humidity"),
            "weather": last_forecast.get("weather", [{}])[0].get("description"),
            "weather_icon": last_forecast.get("weather", [{}])[0].get("icon"),
            "clouds": last_forecast.get("clouds", {}).get("all"),
            "wind_speed": last_forecast.get("wind", {}).get("speed"),
            "wind_deg": last_forecast.get("wind", {}).get("deg"),
            "visibility": last_forecast.get("visibility"),
            "pop": last_forecast.get("pop"),
            "rain": last_forecast.get("rain", {}).get("3h"),
            "snow": last_forecast.get("snow", {}).get("3h"),
        }
    }

    return formatted_data