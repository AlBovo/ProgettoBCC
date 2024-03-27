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
    
    def dayIsFull(self, day: int) -> bool: # TODO: fix -> find at least one gap between 2 events as big as the argument
        events = self.__events[day]
        for i in range(len(events) - 1):
            if events[i][2] < events[i+1][1]:
                return False
        
        return True
    
    def getInformations(self) -> tuple:
        return (self.__name, self.__surname, self.__categories)
    
class OperatorManager(object):
    @staticmethod
    def resultRowToOperator(res: tuple, events: list[tuple]) -> Operator:
        return Operator(res[0], res[1], res[2], res[3], events) # id, name, surname, categories, events
    
    @staticmethod
    def get(id: int) -> Operator | None:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM operators WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return OperatorManager.resultRowToOperator(res)
    
    @staticmethod
    def getOperatorsByCategory(category: str) -> list[Operator]:
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM operators WHERE categories = %s", (category, ))
        res = cur.fetchall()
        return [OperatorManager.resultRowToOperator(row) for row in res]
    
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

class Event(object):
    def __init__(self, id: int, start_hour:int, end_hour:int, user_id: int, operator_id: int) -> None:
        self.__id = id # TODO: Add date (already stored in db)
        self.__start_hour = start_hour
        self.__end_hour = end_hour
        self.__user_id = user_id
        self.__operator_id = operator_id
        super.__init__()

    def getTimeSpan(self) -> tuple : 
        return (self.__start_hour, self.__end_hour)
    
    def getOperator(self) -> Operator :
        return OperatorManager.get(self.__operator_id)
    
    def getUser(self) -> User :
        return UserManager.get(self.__user_id)

class EventManager(object):
    @staticmethod
    def resultRowToEvent(res: tuple) -> Event:
        return Event(res[0], res[2], res[3], res[4], res[5])
    
    @staticmethod
    def get(id: int) -> Event | None :
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("SELECT * FROM events WHERE id = %s", (id,))
        if event := cur.fetchone():
            return EventManager.resultRowToEvent(event)
        
    @staticmethod #TODO: add check to not override existing event
    def addEvent(start_hour:int, end_hour:int, user_id: int, operator_id: int) -> Event: # TODO: add Date
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("INSERT INTO events VALUES ('2006-05-18', %s, %s, %s, %s)", (start_hour, end_hour, user_id, operator_id,))
        conn.commit()

    # TODO : add function to add/remove event