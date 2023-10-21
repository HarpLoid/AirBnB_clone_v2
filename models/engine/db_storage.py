#!/usr/bin/python3
"""
Manages the Database Storage
"""
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """
    Manages storage of object to the Database
    """
    __engine = None
    __session = None
    __classes = {'BaseModel': BaseModel,
                 'User': User,
                 'Place': Place,
                 'State': State,
                 'City': City,
                 'Amenity': Amenity,
                 'Review': Review}

    def __init__(self):
        """
        Initailizes a DBStorage instance.
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """
        Creates all tables in the database
        Creates the current database session using
        sessionmaker
        """
        Base.metadata.create_all(self.__engine)
        db_session = sessionmaker(self.__engine,
                                  expire_on_commit=False)
        Session = scoped_session(db_session)
        self.__session = Session()

    def all(self, cls=None):
        """
        Query all objects on the current database
        """
        if cls is not None:
            if type(cls) == str:
                cls = self.__classes[cls]
            objects = self.__session.query(cls)
        else:
            objects = self.__session.query(User).all()
            objects.extend(self.__session.query(Place).all())
            objects.extend(self.__session.query(State).all())
            objects.extend(self.__session.query(City).all())
            objects.extend(self.__session.query(Amenity).all())
            objects.extend(self.__session.query(Review).all())

        return ({"{}.{}".format(type(obj).__name__, obj.id):
                obj for obj in objects})

    def new(self, obj):
        """
        Add obj to current Database Session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes  from the current database session obj
        """
        if obj:
            self.__session.delete(obj)

    def close(self):
        """
        Closes a session with the db
        """
        self.__session.close()
