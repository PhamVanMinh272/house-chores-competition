from flask import Blueprint

from src.api_logic import users

users_router = Blueprint("users", __name__)


@users_router.route("", methods=["GET"])
def get_users():
    return users.get_users()

@users_router.route("/<int:user_id>/groups", methods=["GET"])
def get_groups(user_id):
    return users.get_groups(user_id=user_id)
