
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, MethodNotAllowed, Unauthorized, Forbidden, Conflict, UnprocessableEntity
import logging
import traceback
import uuid

from src.common.exceptions import InvalidData
# from src.flask_api.sessions import session_router
from src.flask_api.members import members_router
from src.flask_api.reservations import reservations_router
from src.flask_api.attendances import attendances_router
from src.swagger.flask_main import swagger_bp
from src.flask_api.users import users_router
from src.flask_api.house_chores import chores_router
from src.flask_api.schedules import schedules_router

# -------- Logging config (optional) --------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger("api")

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})

# --------- Error model & helpers ----------
class AppError(Exception):
    """Base class for domain/app errors with an HTTP status."""
    def __init__(self, message: str, status_code: int = 400, code: str = "APP_ERROR", details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details

class ValidationError(AppError):
    def __init__(self, message: str, details=None):
        super().__init__(message=message, status_code=422, code="VALIDATION_ERROR", details=details)

class BusinessRuleError(AppError):
    def __init__(self, message: str, details=None):
        super().__init__(message=message, status_code=409, code="BUSINESS_RULE_ERROR", details=details)

def new_request_id() -> str:
    # Short, sortable request id
    return uuid.uuid4().hex[:12]

def error_response(message: str, status: int, code: str, details=None, exc: Exception | None = None):
    rid = getattr(request, "_rid", new_request_id())
    payload = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "status": status,
            "details": details,
            "requestId": rid
        }
    }
    # Log with traceback for server-side diagnostics
    if exc is not None:
        logger.error(f"[{rid}] {code} {status}: {message}")
        logger.debug("[%s] Traceback:\n%s", rid, traceback.format_exc())
    else:
        logger.warning(f"[{rid}] {code} {status}: {message}")
    return jsonify(payload), status

# --------- Centralized error handlers ----------
@app.before_request
def assign_request_id():
    # Assign a request id to each incoming request
    request._rid = new_request_id()

@app.errorhandler(AppError)
def handle_app_error(err: AppError):
    return error_response(
        message=err.message,
        status=err.status_code,
        code=err.code,
        details=err.details,
        exc=err
    )

@app.errorhandler(HTTPException)
def handle_http_exception(err: HTTPException):
    # Werkzeug HTTPException has code and description
    status = err.code or 500
    # Map standard status to short codes
    code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "UNPROCESSABLE_ENTITY",
        500: "INTERNAL_SERVER_ERROR",
    }
    return error_response(
        message=(err.description or "HTTP error"),
        status=status,
        code=code_map.get(status, "HTTP_ERROR"),
        details=None,
        exc=err
    )

@app.errorhandler(Exception)
def handle_unexpected_exception(err: Exception):
    # For security, do not leak internals; you can add err.__class__.__name__ in details for debugging

    # Always capture the full traceback here
    logger.error("Unhandled exception: %s", str(err))
    logger.error("Traceback:\n%s", traceback.format_exc())

    return error_response(
        message="An unexpected error occurred.",
        status=500,
        code="INTERNAL_SERVER_ERROR",
        details=None,
        exc=err
    )

# Optional: explicit handlers if you want custom messages per status
@app.errorhandler(InvalidData)
def handle_invalid_data(err: InvalidData):
    return error_response("Invalid data", 400, "INVALID_DATA", exc=err)

@app.errorhandler(NotFound)
def handle_not_found(err: NotFound):
    return error_response("Resource not found", 404, "NOT_FOUND", exc=err)

@app.errorhandler(MethodNotAllowed)
def handle_method_not_allowed(err: MethodNotAllowed):
    return error_response("Method not allowed", 405, "METHOD_NOT_ALLOWED", exc=err)

@app.errorhandler(BadRequest)
def handle_bad_request(err: BadRequest):
    return error_response("Bad request", 400, "BAD_REQUEST", details=err.description, exc=err)

@app.errorhandler(UnprocessableEntity)
def handle_unprocessable_entity(err: UnprocessableEntity):
    return error_response("Unprocessable entity", 422, "UNPROCESSABLE_ENTITY", details=err.description, exc=err)

# -------- Register blueprints --------
app.register_blueprint(swagger_bp, url_prefix="/api/swagger")
# app.register_blueprint(session_router, url_prefix="/api/sessions")
app.register_blueprint(members_router, url_prefix="/api/members")
app.register_blueprint(reservations_router, url_prefix="/api/reservations")
app.register_blueprint(attendances_router, url_prefix="/api/attendances")
app.register_blueprint(users_router, url_prefix="/api/users")
app.register_blueprint(chores_router, url_prefix="/api/chores")
app.register_blueprint(schedules_router, url_prefix="/api/schedules")

# -------- Teardown --------
@app.teardown_appcontext
def shutdown_session(exception=None):
    # Close DB session/connection here (e.g., SQLAlchemy session.remove())
    # If you use sessionmaker scoped_session, call scoped_session.remove()
    pass

if __name__ == "__main__":
    # In production, set debug=False. With debug=True, Flask may intercept exceptions
    app.run(debug=True)
