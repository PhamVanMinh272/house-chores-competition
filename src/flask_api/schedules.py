from flask import Blueprint, request

from src.api_logic import schedules

schedules_router = Blueprint("schedules", __name__)


@schedules_router.route("", methods=["GET"])
def get_schedules():
    group_id = request.args.get("groupId", type=int)
    return schedules.get_schedules(group_id=group_id) if group_id is not None else schedules.get_schedules()

@schedules_router.route("", methods=["POST"])
def create_schedule():
    return schedules.create_schedule(**request.json)
