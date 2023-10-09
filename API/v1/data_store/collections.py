from v1.models import BaseModel, User
from datetime import date
from passlib.handlers.bcrypt import bcrypt
import re
"""The data structure for storing non persistent data in models"""


class NonPersistentCollection:
    """base data structure, with functions to transact models"""

    def __init__(self):
        """Creates data structure index of items"""
        self.data = {}
        self.index = 1

    def query_all(self):
        """Get all items in collection"""
        return self.data

    def query_all_where_field_eq(self, field, value):
        """query all items by a specific field"""
        result = []
        for item in self.data.values():
            if item[field] == value:
                result.append(item)
        return result

    def insert(self, item):
        """Inserts an item into the collection"""
        assert isinstance(item, BaseModel)
        item.created_at = date.today().strftime('%m/%d/%y')
        self.data[self.index] = item
        self.index += 1

    def set(self, item, item_id):
        """Updates an item fields"""
        assert isinstance(item, BaseModel)
        item.updated_at = date.today().strftime('%m/%d/%y')
        self.data[item_id] = item

    def query(self, item_id):
        """Query an item by id"""
        return self.data.get(item_id)

    def query_by_field(self, field, value):
        """Query an item by a specific field"""
        for item in self.data.values():
            if item.to_json_object()[field] == value:
                return item

    def delete(self, item_index):
        """Delete an item from the collection"""
        del self.data[item_index]

    def is_valid(self, item):
        """Overried this method to check if an item is valid or not"""
        return True, {}

    def clear(self):
        """Clear the items in this collection"""
        self.data = {}


class UserCollection(NonPersistentCollection):
    def insert(self, item):
        """Encypt password before adding user into the collection"""
        assert isinstance(item, User)
        item.password = bcrypt.encrypt(item.password)
        #now insert item
        super().insert(item)

    def is_valid(self, item):
        """Check if the response has valid user details"""
        errors = {}
        if not item.get("first_name"):
            errors["first_name"] = "First name is required"
        if not item.get("last_name"):
            errors["last_name"] = "Lar name is required"
        if not item.get("email"):
            errors["email"] = "Email is required"
        elif self.query_by_field(field="email", value=item.get("email")) is not None:
            errors["email"] = "email address is already in use"
        elif re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', item.get("email")) is None:
            errors["email"] = "Not a valid email address"
        if not item.get("password"):
            errors["password"] = "password is required"
        elif len(item.get("password")) < 8:
            errors["password"] = "lenght of password must be 8 characters or more"
        return len(errors) == 0, errors


class QuestionCollection(NonPersistentCollection):
    def is_valid(self, item):
        """Check whether question object has valid fields"""
        errors = {}
        if not item.get("subject"):
            errors["subject"] = "Subject must be provided"
        if not item.get("user"):
            errors["user"] = "user must be provided"
        if not item.get("question"):
            errors["question"] = "The question must be provided"
        return len(errors) == 0, errors


class AnswerCollection(NonPersistentCollection):
    def is_valid(self, item):
        """Checks whether an answer to a question has valid fields"""
        errors = {}
        if not item.get("user"):
            errors["user"] = "User must be provided"
        # if not item.get("question"):
        #     errors["question"] = "question being answered must be provided"
        if not item.get("answer"):
            errors["answer"] = "Answer must be provided"
        return len(errors) == 0, errors
