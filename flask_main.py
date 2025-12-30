from flask import Flask
from flask_cors import CORS

# from src.flask_api.sessions import session_router
from src.flask_api.members import members_router
from src.flask_api.reservations import reservations_router
from src.flask_api.attendances import attendances_router
from src.swagger.flask_main import swagger_bp
from src.flask_api.users import users_router
from src.flask_api.house_chores import chores_router
from src.flask_api.schedules import schedules_router


app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://localhost:*"}})

app.register_blueprint(swagger_bp, url_prefix="/api/swagger")
# app.register_blueprint(session_router, url_prefix="/api/sessions")
app.register_blueprint(members_router, url_prefix="/api/members")
app.register_blueprint(reservations_router, url_prefix="/api/reservations")
app.register_blueprint(attendances_router, url_prefix="/api/attendances")
app.register_blueprint(users_router, url_prefix="/api/users")
app.register_blueprint(chores_router, url_prefix="/api/chores")
app.register_blueprint(schedules_router, url_prefix="/api/schedules")


# app exit handler
@app.teardown_appcontext
def shutdown_session(exception=None):
    # should close db session here
    pass


if __name__ == "__main__":
    app.run(debug=True)
