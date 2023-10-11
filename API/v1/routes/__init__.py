from flask_jwt_extended import get_jwt_identity, jwt_required
from v1.data_store.db import StackOverflowLiteDB

db = StackOverflowLiteDB()


@jwt_required
def get_curent_user():
    return db.users.query_by_field("email", get_jwt_identity())
