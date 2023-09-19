#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime


Base = declarative_base()

class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

        for key, value in kwargs.items():
            if key != '__class__':
                setattr(self, key, value)

        date_format = '%Y-%m-%d %H:%M:%S.%f'
        if isinstance(self.created_at, str):
            self.created_at = datetime.strptime(self.created_at,
                                                date_format)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.strptime(self.updated_at,
                                                date_format)

        self.save()
        # if not kwargs:
        #     from models import storage
        #     self.id = str(uuid.uuid4())
        #     self.created_at = datetime.now()
        #     self.updated_at = datetime.now()
        # else:
        #     date_format = "%Y-%m-%dT%H:%M:%S.%f"
        #     kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
        #                                              date_format)
        #     kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
        #                                              date_format)
        #     del kwargs['__class__']
        #     self.__dict__.update(kwargs)
            # for k, v in kwargs.items():
            #     if k == "__class__":
            #         pass
            #     elif k == "created_at":
            #         self.created_at = datetime.strptime(v, date_format)
            #     elif k == "updated_at":
            #         self.updated_at = datetime.strptime(v, date_format)
            #     else:
            #         setattr(self, k, v)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        from models import storage
        storage.delete()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        del dictionary['_sa_instance_state']
        return dictionary
