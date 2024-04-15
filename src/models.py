from flask_login import UserMixin
from flask import current_app
import db, utils

##################### USER CLASS #####################
class User(UserMixin):
    """
    Represents a user in the system.

    Attributes:
        __id (int): The user's ID.
        __email (str): The user's email address.
        __hashPassword (str): The hashed password of the user.
        __isadmin (bool): Indicates whether the user has admin privileges.
    """

    def __init__(self, id: int, email: str, hashPassword: str, privilege: bool) -> None:
        """
        Initializes a new instance of the User class.

        Args:
            id (int): The user's ID.
            email (str): The user's email address.
            hashPassword (str): The hashed password of the user.
            privilege (bool): Indicates whether the user has admin privileges.
        """
        self.__id = id
        self.__email = email
        self.__hashPassword = hashPassword
        self.__isadmin = privilege
        super().__init__()

    def get_id(self) -> int:
        """
        Gets the user's ID.

        Returns:
            int: The user's ID.
        """
        return self.__id
    
    def get_password(self) -> str:
        """
        Gets the hashed password of the user.

        Returns:
            str: The hashed password of the user.
        """
        return self.__hashPassword
    
    def get_email(self) -> str:
        """
        Gets the email of the user.

        Returns:
            str: The email of the user.
        """

        return self.__email
    
    def get_privilege(self) -> bool:
        """
        Checks if the user has admin privileges.

        Returns:
            bool: True if the user has admin privileges, False otherwise.
        """
        return self.__isadmin
    
################## END OF USER CLASS ##################

#################### USER MANAGER #####################    
class UserManager(object):
    """
    A class that manages user operations in the application.
    """

    @staticmethod
    def resultRowToUser(res: tuple) -> User:
        """
        Converts a result row tuple to a User object.

        Args:
            res (tuple): The result row tuple.

        Returns:
            User: The User object created from the result row.
        """
        return User(res[0], res[1], res[2], res[3]) # id, email, password

    @staticmethod
    def get(id: int | str) -> User | None:
        """
        Retrieves a user by their ID.

        Args:
            id (int | str): The ID of the user.

        Returns:
            User | None: The User object if found, None otherwise.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return UserManager.resultRowToUser(res)

    @staticmethod
    def getByEmail(email: str) -> User | None:
        """
        Retrieves a user by their email.

        Args:
            email (str): The email of the user.

        Returns:
            User | None: The User object if found, None otherwise.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE email = %s", (email, ))
        res = cur.fetchone()
        if res:
            return UserManager.resultRowToUser(res)

    @staticmethod
    def add(email: str, hashPassword: str) -> User:
        """
        Adds a new user to the database.

        Args:
            email (str): The email of the user.
            hashPassword (str): The hashed password of the user.

        Returns:
            User: The User object of the added user.

        Raises:
            AssertionError: If the user with the given email already exists.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        if UserManager.getByEmail(email):
            return None

        cur.execute("INSERT INTO users (email, password, is_admin) VALUES (%s, %s, %s)", (email, hashPassword, False, ))
        conn.commit()
        added_user = UserManager.getByEmail(email)
        assert added_user != None
        return added_user
    
################## END OF USER MANAGER ##################

######################## EVENT CLASS ########################
class Event(object):
    def __init__(self, id: int, date: str, start_hour: int, end_hour: int, category:str, user_id: int, operator_id: int) -> None:
        """
        Initialize an Event object.

        Args:
            id (int): The ID of the event.
            date (str): The date of the event.
            start_hour (int): The starting hour of the event.
            end_hour (int): The ending hour of the event.
            user_id (int): The ID of the user associated with the event.
            operator_id (int): The ID of the operator associated with the event.
        """
        self.__id = id
        self.__date = date
        self.__start_hour = start_hour
        self.__end_hour = end_hour
        self.__category = category
        self.__user_id = user_id
        self.operator_id = operator_id
        super().__init__()

    def getTimeSpan(self) -> tuple:
        """
        Get the time span of the event.

        Returns:
            tuple: A tuple containing the start hour and end hour of the event.
        """
        return (self.__date, self.__start_hour, self.__end_hour)
    
    def getUser(self) -> User:
        """
        Get the user associated with the event.

        Returns:
            User: The user object associated with the event.
        """
        return UserManager.get(self.__user_id)
    
    def getId(self) -> int:
        """
        Get the ID of the event.

        Returns:
            int: The ID of the event.
        """
        return self.__id
    
    def getCategory(self) -> str:
        """
        Get the category of the event as unique code for each category.

        Returns:
            str: The category code.
        """

        return self.__category
    
################## END OF EVENT CLASS ##################

#################### EVENT MANAGER #####################
class EventManager(object):
    """
    A class that manages events in the system.
    """

    @staticmethod
    def resultRowToEvent(res: tuple) -> Event:
        """
        Converts a result row tuple to an Event object.

        Args:
            res (tuple): The result row tuple.

        Returns:
            Event: The converted Event object.
        """
        return Event(res[0], res[1], res[2], res[3], res[4], res[5], res[6])
    
    @staticmethod
    def get(id: int) -> Event | None :
        """
        Retrieves an event by its ID.

        Args:
            id (int): The ID of the event.

        Returns:
            Event | None: The Event object if found, None otherwise.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("SELECT * FROM events WHERE id = %s", (id,))
        if event := cur.fetchone():
            return EventManager.resultRowToEvent(event)
        
    @staticmethod
    def getEventsByTimeRange(date: str, start: int, end: int, operator_id: int):
        """
        Retrieves events within a specified time range.

        Args:
            date (str): The date of the events.
            start (int): The start hour of the time range.
            end (int): The end hour of the time range.
            operator_id (int): The ID of the operator associated with the event.

        Returns:
            list[Event]: A list of Event objects within the specified time range.
        """
        assert utils.is_valid_date(date)
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("SELECT * FROM events WHERE date = %s AND start_hour >= %s AND end_hour <= %s AND operator_id = %s", (date, start, end, operator_id, ))  # TODO check if this is correct
        return [EventManager.resultRowToEvent(event) for event in cur.fetchall()]
        
    @staticmethod
    def addEvent(date: str, start_hour:int, end_hour:int, category: str, user_id: int, operator_id: int) -> Event | None:
        """
        Adds a new event to the system.

        Args:
            date (str): The date of the event.
            start_hour (int): The start hour of the event.
            end_hour (int): The end hour of the event.
            user_id (int): The ID of the user associated with the event.
            operator_id (int): The ID of the operator associated with the event.

        Returns:
            Event | None: The added Event object if successful, None otherwise.
        """
        if EventManager.getEventsByTimeRange(date, start_hour, end_hour, operator_id):
            return None

        if OperatorManager.get(operator_id) is None:
            return None
        
        conn = db.getConnection(current_app)
        cur = conn.cursor() 
        
        cur.execute("INSERT INTO events (date, start_hour, end_hour, category, user_id, operator_id) VALUES (%s, %s, %s, %s, %s)", 
                    (date, start_hour, end_hour, category, user_id, operator_id,))
        conn.commit()
        added_event = EventManager.get(cur.lastrowid)
        assert added_event != None
        return added_event
    
    @staticmethod
    def deleteEvent(id: int, user_id: int) -> bool:
        """
        Deletes an event with the given ID for the specified user.

        Args:
            id (int): The ID of the event to delete.
            user_id (int): The ID of the user who owns the event.

        Returns:
            bool: True if the event was successfully deleted, False otherwise.
        """
        assert UserManager.get(user_id) != None # user must exist
        
        if not EventManager.get(id):
            return False
        
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("DELETE FROM events WHERE id = %s AND user_id = %s", (id, user_id, ))
        conn.commit()
        return True
    
    @staticmethod
    def getEventsByMonth(month: int) -> list[Event]:
        """
        Retrieves events within a specified month.

        Args:
            month (int): The month of the events.

        Returns:
            list[Event]: A list of Event objects within the specified month.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("SELECT * FROM events WHERE MONTH(date) = %s", (month,))
        return [EventManager.resultRowToEvent(event) for event in cur.fetchall()]
    
    @staticmethod
    def getEventsByDate(date: str) -> list[Event]:
        """
        Retrieves events within a specified day.

        Args:
            date (string): The date of the events. format = YYYY-MM-GG

        Returns:
            list[Event]: A list of Event objects within the specified day.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("SELECT * FROM events WHERE date = %s", (date,))
        return [EventManager.resultRowToEvent(event) for event in cur.fetchall()]
    
    @staticmethod
    def getEventsByoperator(operatorId: int) -> list[Event]:
        """
        Retrieves events associated with the operator.

        Returns:
            list[Event]: A list of events associated with the operator.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()

        cur.execute("SELECT * FROM events WHERE operator_id = %s", (operatorId,))
        return [EventManager.resultRowToEvent(event) for event in cur.fetchall()]
    
#################### END OF EVENT MANAGER #####################

##################### OPERATOR CLASS ####################
class Operator(object):
    def __init__(self, id: int, name: str, surname: str, categories: str) -> None: # TODO list should be list[str]
        """
        Initializes an Operator object.

        Args:
            id (int): The ID of the operator.
            name (str): The name of the operator.
            surname (str): The surname of the operator.
            categories (list[str]): The categories the operator belongs to.
            events (dict[int, list[tuple]]): The events associated with the operator, organized by day.

        Returns:
            None
        """
        self.__id = id
        self.__name = name
        self.__surname = surname
        self.__categories = categories
        super().__init__()

    def getEventsByDate(self, date: str) -> list[Event]:
        """
        Retrieves events associated with the operator for a specific day.

        Args:
            date (str): The date to retrieve events for. format = YYYY-MM-GG

        Returns:
            list[Event]: A list of events associated with the operator for the specified day.
        """
        return [event for event in EventManager.getEventsByDate(date) if event.operator_id == self.__id]

    def getAllEvents(self) -> list[Event]:
        """
        Retrieves events associated with the operator.

        Returns:
            list[Event]: A list of events associated with the operator.
        """

        return EventManager.getEventsByoperator(self.__id)
    
    def getInformations(self) -> tuple:
        """
        Returns the operator's information.

        Returns:
            tuple: A tuple containing the operator's name, surname, and categories.
        """
        return (self.__name, self.__surname, self.__categories)
    
################ END OF OPERATOR CLASS ###############

################## OPERATOR MANAGER ##################
class OperatorManager(object):
    """
    A class that manages operators in the system.
    """

    @staticmethod
    def resultRowToOperator(res: tuple) -> Operator:
        """
        Converts a result row from the database to an Operator object.

        Args:
            res (tuple): The result row from the database.
            events (list[tuple]): The events associated with the operator.

        Returns:
            Operator: The Operator object.
        """
        return Operator(res[0], res[1], res[2], res[3]) # id, name, surname, categories, events
    
    @staticmethod
    def get(id: int) -> Operator | None:
        """
        Retrieves an operator by its ID.

        Args:
            id (int): The ID of the operator.

        Returns:
            Operator | None: The Operator object if found, None otherwise.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM operators WHERE id = %s", (id, ))
        res = cur.fetchone()
        if res:
            return OperatorManager.resultRowToOperator(res)
    
    @staticmethod
    def getOperatorsByCategory(category: str) -> list[Operator]:
        """
        Retrieves operators by category.

        Args:
            category (str): The category of the operators.

        Returns:
            list[Operator]: A list of Operator objects.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM operators WHERE categories = %s", (category, ))
        res = cur.fetchall()
        return [OperatorManager.resultRowToOperator(row) for row in res]
    
    @staticmethod
    def add(id: int, name: str, surname: str, categories: list[str]) -> Operator | None:
        """
        Adds a new operator to the system.

        Args:
            id (int): The ID of the operator.
            name (str): The name of the operator.
            surname (str): The surname of the operator.
            categories (list[str]): The categories of the operator.

        Returns:
            Operator | None: The added Operator object if successful, None if the operator already exists.
        """
        conn = db.getConnection(current_app)
        cur = conn.cursor()
        
        if OperatorManager.get(id):
            return None
        
        cur.execute("INSERT INTO operators (id, name, surname, categories) VALUES (%s, %s, %s, %s)", (id, name, surname, categories))
        conn.commit()
        added_operator = OperatorManager.get(cur.lastrowid)
        assert added_operator != None
        return added_operator
    
################## END OF OPERATOR MANAGER ##################