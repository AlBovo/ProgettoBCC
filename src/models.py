from flask_login import UserMixin, current_user
from flask import current_app
import db

class User(UserMixin):
    def __init__(self, id: int, email: str, hashPassword: str) -> None:
        self.id = id
        self.email = email
        self.hashPassword = hashPassword
        super().__init__()

    def get_id(self):
        return str(self.id)
    
class Users(object):
    @staticmethod
    def resultRowToUser(res: dict):
        return User(res['id'], res['email'], res['hashPassword'])

    @staticmethod
    def get(id: int | str) -> User | None:
        cur = db.getDatabaseCursor(current_app)
        cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return Users.resultRowToUser(res)

    @staticmethod
    def getByEmail(email: str):
        cur = db.getDatabaseCursor(current_app)
        cur.execute("SELECT * FROM users WHERE email = %s", (email, ))
        res = cur.fetchone()
        if res:
            return Users.resultRowToUser(res)
        else:
            return None

    @staticmethod
    def add(email: str, hashPassword: str) -> User | None:
        cur = db.getDatabaseCursor(current_app)
        # try:
        cur.execute("INSERT INTO users VALUES (?, ?, ? )", (email, hashPassword, False))
        cur.commit() # TODO : test
        added_user = User(email, hashPassword, False)
        return added_user
        # except Exception as error:
        #     current_app.logger.error(error)
        #     con.rollback()