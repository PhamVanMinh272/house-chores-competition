from flask import Blueprint, request

from src.api_logic import house_chores

chores_router = Blueprint("chores", __name__)


@chores_router.route("", methods=["GET"])
def get_users():
    group_id = request.args.get("groupId", type=int)
    return house_chores.get_house_chores(group_id=group_id) if group_id is not None else house_chores.get_house_chores()

@chores_router.route("", methods=["POST"])
def create_chore():
    return house_chores.create_house_chore(**request.json)
