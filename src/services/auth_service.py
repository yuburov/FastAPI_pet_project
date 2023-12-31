from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from starlette.background import BackgroundTasks

from config import JWT_SECRET_KEY, ALGORITHM
from models.tokens import TokenTable
from models.users import User
from repositories.auth_repo import JWTRepo
from schemas.users import UserSchemaAdd, RequestDetails
from services.token_service import TokenService
from adapters.notifications import EmailNotifications
from adapters.unitofwork import IUnitOfWork

# Encrypt password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    async def register_service(uow: IUnitOfWork, background_tasks: BackgroundTasks, register: UserSchemaAdd):

        # Create uuid
        _users_id = str(uuid4())
        _users = User(id=_users_id, username=register.username, email=register.email,
                      password=pwd_context.hash(register.password))
        async with uow:
            _username = await uow.users.find_one(username=register.username)
            if _username:
                raise HTTPException(
                    status_code=400, detail="Username already exists!")

            _email = await uow.users.find_one(email=register.email)
            if _email:
                raise HTTPException(
                    status_code=400, detail="Email already exists!")

            data = await uow.users.add_one(_users.to_dict())
            email_notifier = EmailNotifications()
            send_welcome_email(register, email_notifier, background_tasks)
            await uow.commit()

            return data.to_read_model()

    @staticmethod
    async def logins_service(uow: IUnitOfWork, request: RequestDetails):
        async with uow:
            _user = await uow.users.find_one(email=request.email)

            if _user is not None:
                if not pwd_context.verify(request.password, _user.password):
                    raise HTTPException(
                        status_code=400, detail="Invalid Password !")
                access_token, refresh_token = TokenService.generate_tokens(_user.id)
                await TokenService.add_token_to_db(uow, _user.id, access_token, refresh_token)
                return {"token_type": "Bearer", "access_token": access_token, "refresh_token": refresh_token}
            raise HTTPException(status_code=404, detail="Username not found !")

    @staticmethod
    async def refresh_service(uow: IUnitOfWork, credentials, secret_key):
        user_info = JWTRepo.extract_token(credentials, secret_key)
        user_id = user_info['sub']
        access_token, refresh_token = TokenService.generate_tokens(user_id)
        await TokenService.update_tokens_in_db(uow, user_id, access_token, refresh_token)
        return {"token_type": "Bearer", "access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    async def logout(uow: IUnitOfWork, token):
        payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
        user_id = payload['sub']
        async with uow:
            token_record = await uow.tokens.find_all()
            info = []
            for record in token_record:
                if (datetime.utcnow() - record.created_date).days > 1:
                    info.append(record.user_id)
            if info:
                await uow.tokens.delete_by_ids(TokenTable.user_id, info)

            existing_token = await uow.tokens.find_one(user_id=user_id, access_token=token)
            if existing_token:
                await uow.tokens.edit_one(access_token=existing_token.access_token, data={'status': False})
                await uow.commit()
            return "Done"


def send_welcome_email(user, email_notifier, background_task):
    destination = user.email
    subject = "Сообщение о регистрации"
    welcome_message = f"Здравствуйте, {user.username}! Добро пожаловать на наш сайт! Спасибо за регистрацию."
    background_task.add_task(email_notifier.send, destination, subject, welcome_message)
