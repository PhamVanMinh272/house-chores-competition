from flask import Blueprint, request

from src.api_logic import members

members_router = Blueprint("member", __name__)


@members_router.route("", methods=["GET"])
def get_members():
    group_id = request.args.get("groupId", type=int)
    return members.get_members(groupId=group_id)
