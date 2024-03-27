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
    
class UserManager(object):
    @staticmethod
    def resultRowToUser(res: tuple) -> User:
        return User(res[0], res[1], res[2], res[3]) # id, email, password

    @staticmethod
    def get(id: int | str) -> User | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return UserManager.resultRowToUser(res)

    @staticmethod
    def getByEmail(email: str) -> User | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = %s", (email, ))
        res = cur.fetchone()
        if res:
            return UserManager.resultRowToUser(res)

    @staticmethod
    def add(email: str, hashPassword: str) -> User:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        if UserManager.getByEmail(email):
            return None

        cur.execute("INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s)", (email, hashPassword, False))
        conn.commit()
        added_user = UserManager.getByEmail(email)
        assert added_user != None
        return added_user
    
class Operator(object):
    def __init__(self, id: int, name: str, surname: str, categories: list[str], events: dict[int, list[tuple]]) -> None:
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__categories = categories
        self.__events = events
        super.__init__()
        
    def getEventsByDay(self, day: int) -> list[tuple]:
        return self.__events[day]
    
    def getEventByUserId(self, user_id: int) -> list[tuple]:
        return [event for event in self.__events if event[3] == user_id]

    def getEventById(self, event_id: int) -> tuple | None:
        for event in self.__events:
            if event[0] == event_id:
                return event
        return None
    
    def dayIsFull(self, day: int) -> bool:
        events = self.__events[day]
        for i in range(len(events) - 1):
            if events[i][2] < events[i+1][1]:
                return False
        
        return True
    
    def getInformations(self) -> tuple:
        return (self.__name, self.__surname, self.__categories)
    
class OperatorManager(object):
    @staticmethod
    def resultRowToOperatorDay(res: tuple, events: list[tuple]) -> Operator:
        return Operator(res[0], res[1], res[2], res[3], events) # id, name, surname, categories, events
    
    @staticmethod
    def get(id: int) -> Operator | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM operators WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return OperatorManager.resultRowToOperatorDay(res)
    
    @staticmethod
    def getOperatorsByCategory(category: str) -> list[Operator]:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM operators WHERE categories = %s", (category, ))
        res = cur.fetchall()
        return [OperatorManager.resultRowToOperatorDay(row) for row in res]
    
    @staticmethod
    def add(id: int, name: str, surname: str, categories: list[str]) -> Operator | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        if OperatorManager.get(id):
            return None
        
        cur.execute("INSERT INTO operators (id, name, surname, categories) VALUES (%s, %s, %s, %s)", (id, name, surname, categories))
        conn.commit()
        added_operator = OperatorManager.get(cur.lastrowid)
        assert added_operator != None
        return added_operator
    
    # TODO : add function to add/remove event