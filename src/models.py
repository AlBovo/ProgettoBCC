from flask_login import UserMixin
from flask import current_app
import db

class User(UserMixin):
    def __init__(self, id: int, email: str, hashPassword: str, privilege: bool) -> None:
        self.__id = id
        self.__email = email
        self.__hashPassword = hashPassword
        self.__isadmin = privilege
        super().__init__()

    def get_id(self) -> int:
        return str(self.__id)
    
    def get_password(self) -> str:
        return str(self.__hashPassword)
    
    def get_privilege(self) -> bool:
        return self.__isadmin
    
class Users(object):
    @staticmethod
    def resultRowToUser(res: tuple):
        return User(res[0], res[1], res[2], res[3]) # id, email, password

    @staticmethod
    def get(id: int | str) -> User | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return Users.resultRowToUser(res)

    @staticmethod
    def getByEmail(email: str):
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = %s", (email, ))
        res = cur.fetchone()
        if res:
            return Users.resultRowToUser(res)

    @staticmethod
    def add(email: str, hashPassword: str) -> User | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = %s", (email, ))
        if cur.fetchone():
            return None 

        cur.execute("INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s)", (email, hashPassword, False))
        conn.commit()
        added_user = Users.getByEmail(email)
        assert added_user != None
        return added_user