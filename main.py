from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


from studturism_database import StudturismDatabase
from studturism_database.exc import BaseStudturismDatabaseError, EntityAlreadyExistsError

from models.user import User, UserCreate

from send_models.dormitory import DormitoryTitleInfo

from config.config import PostgreSQLConfig


postgres_config = PostgreSQLConfig.from_json_config('config/postgresql.json')
studturism_database = StudturismDatabase(async_engine=postgres_config.async_engine, sync_engine=postgres_config.sync_engine)






SECRET_KEY = "d73283a96f7413d600c8b8782d2f433e6b15f3d21939c772e0fb5790a8718024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

@app.get('/')
async def root():
    return {'hello': 'world'}

# region Auth
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str):
    user = await studturism_database.get_user(email=email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def register_user(email: str, password: str):
    return await studturism_database.create_user(email=email, password_hash=hash_password(password))


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception
    else:
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)

    user = await studturism_database.get_user(username=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_public:
        raise HTTPException(status_code=400, detail="Not public user")
    return current_user
# endregion


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/users/register', response_model=User)
async def create_user(user_create: UserCreate):
    try:
        return await register_user(user_create.email, user_create.password)
    except EntityAlreadyExistsError:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email is already registered',
        )

# endregion


# region Universities

@app.get('/universities/all')
async def get_all_universities():
    u = [m.dict() for m in await studturism_database.get_universities()]
    return {'total_count': len(u), 'universities': u}

# endregion

# region Dormitories

@app.get('/dormitories/all')
async def get_all_dormitories():
    d = [d.dict() for d in await studturism_database.get_dormitories()]
    return {'total_count': len(d), 'dormitories': d}

@app.get('/dormitories/title/all', response_model=DormitoryTitleInfo)
async def get_all_dormitories_titles():
    dormitories = studturism_database.get_dormitories()

# endregion

# region Cities
@app.get('/cities/all')
async def get_all_cities():
    return await studturism_database.get_cities()

# endregion


@app.get('/reflect')
async def reflect_site():
    from studturism_site_reflector import StudturismSiteReflector
    reflector = StudturismSiteReflector(studturism_database)
    await reflector.reflect()
    return {'message': 'reflect completed'}

