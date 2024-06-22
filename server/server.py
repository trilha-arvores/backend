from services import FlaskService, ObjectStorageService
from controllers import trails_controller, admin_controller
from flask_cors import CORS

FlaskService.setup_app()
app = FlaskService.app
CORS(app)

ObjectStorageService.setup()


app.register_blueprint(trails_controller, url_prefix="/trails")
app.register_blueprint(admin_controller, url_prefix="/admin")


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {}, 200


if __name__ == "__main__":
    FlaskService.run_app()
