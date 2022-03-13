from backend.model.users import User
import bcrypt
# https://github.com/scionoftech/FastAPI-Full-Stack-Samples/blob/master/FastAPISQLAlchamy/app/crud/crud_users.py
def create_user(session, body):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(body.password, salt)

    user = User(username=body.username, password=hashed_password, email=body.email)

    with session() as session_:
        session_.add(user)
        session_.commit()

    


def delete_user():
    pass


def update_user():
    pass
